# pyOCD debugger
# Copyright (c) 2013-2019 Arm Limited
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
from time import sleep

from pyocd.coresight.generic_mem_ap import GenericMemAPTarget
from ...core import exceptions
from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (MemoryMap, RamRegion)
from ...core.target import Target
from ...coresight.cortex_m import CortexM
from ...utility.timeout import Timeout

LOG = logging.getLogger(__name__)


class CortexM_PSoC4(CortexM):
    def reset(self, reset_type=None):
        if reset_type is not Target.ResetType.HW:
            self.session.notify(Target.Event.PRE_RESET, self)
        self._run_token += 1
        if reset_type is Target.ResetType.HW:
            self._ap.dp.reset()
            sleep(0.5)
            self._ap.dp.connect()
            self.fpb.enable()
        else:
            if reset_type is Target.ResetType.SW_VECTRESET:
                mask = CortexM.NVIC_AIRCR_VECTRESET
            else:
                mask = CortexM.NVIC_AIRCR_SYSRESETREQ

            try:
                self.write_memory(CortexM.NVIC_AIRCR, CortexM.NVIC_AIRCR_VECTKEY | mask)
                self.flush()
            except exceptions.TransferError:
                self.flush()

        with Timeout(5.0) as t_o:
            while t_o.check():
                try:
                    dhcsr_reg = self.read32(CortexM.DHCSR)
                    if (dhcsr_reg & CortexM.S_RESET_ST) == 0:
                        break
                except exceptions.TransferError:
                    self.flush()
                    try:
                        self._ap.dp.connect()
                    except exceptions.TransferError:
                        self.flush()

                    sleep(0.01)

        if reset_type is not Target.ResetType.HW:
            self.session.notify(Target.Event.POST_RESET, self)

    def wait_halted(self):
        with Timeout(5.0) as t_o:
            while t_o.check():
                try:
                    if not self.is_running():
                        break
                except exceptions.TransferError:
                    self.flush()
                    sleep(0.01)
            else:
                raise exceptions.TimeoutError("Timeout waiting for target halt")

    def reset_and_halt(self, reset_type=None):
        self.halt()
        self.reset(reset_type)
        self.halt()
        self.wait_halted()


class PSoC4(CoreSightTarget):
    VENDOR = "Cypress"
    cortex_m_core_class = None

    def __init__(self, session, cortex_m_core_class, memory_map):
        self.cortex_m_core_class = cortex_m_core_class
        super(PSoC4, self).__init__(session, memory_map)

    def create_init_sequence(self):
        seq = super(PSoC4, self).create_init_sequence()
        seq.wrap_task('discovery',
            lambda seq: seq.replace_task('create_cores', self.create_psoc_cores)
        )
        return seq

    def create_psoc_cores(self):
        core0 = self.cortex_m_core_class(self.session, self.aps[0], self.memory_map, 0)
        core0.default_reset_type = self.ResetType.SW_SYSRESETREQ
        self.aps[0].core = core0
        core0.init()
        self.add_core(core0)
