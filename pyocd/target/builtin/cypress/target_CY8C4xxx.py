# pyOCD debugger
# Copyright (c) 2020 Cypress Semiconductor Corporation
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

from ...family.target_psoc4 import PSoC4, CortexM_PSoC4
from ....core.memory_map import (RamRegion, FlashRegion, MemoryMap)

LOG = logging.getLogger(__name__)


class CY8C4xxx(PSoC4):
    from .flash_algos.flash_algo_CY8C4xxx import FLASH_ALGO as flash_algo_main

    MEMORY_MAP = MemoryMap(
        RamRegion(start=0x08000000, length=0x2000),
        FlashRegion(start=0x00000000, length=0x10000, blocksize=0x100,
                    is_boot_memory=True,
                    erased_byte_value=0,
                    algo=flash_algo_main,
                    erase_all_weight=0.5,
                    erase_sector_weight=0.05,
                    program_page_weight=0.07),
    )

    def __init__(self, session):
        super(CY8C4xxx, self).__init__(session, CortexM_PSoC4, self.MEMORY_MAP)
