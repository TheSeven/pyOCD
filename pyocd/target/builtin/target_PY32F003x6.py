# pyOCD debugger
# Copyright (c) 2006-2013 Arm Limited
# Copyright (c) 2021 Chris Reed
# Copyright (c) 2023 Michael Sparmann
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

from ...coresight.coresight_target import CoreSightTarget
from ...core.memory_map import (FlashRegion, RamRegion, MemoryMap)
from ...debug.svd.loader import SVDFile

RCC_APBENR1 = 0x4002103c
RCC_APBENR1_DBGMCU = 0x08000000

DBGMCU_CR = 0x40015804
DBG_APB_FZ1 = 0x40015808
DBG_APB_FZ2 = 0x4001580c

DBGMCU_CR_VAL = 0x00000002
DBG_APB_FZ1_VAL = 0xffffffff
DBG_APB_FZ2_VAL = 0xffffffff


FLASH_ALGO = {
    'load_address': 0x20000000,
    'instructions': [
        0xe7fdbe00,
        0xcf03a721, 0x0c13c814, 0x0a160c25, 0xc81cc17c, 0x0c2546c0, 0xcffcc13c, 0x68003870, 0x6a396050,
        0xd2040b49, 0x2406601c, 0x0c44605c, 0x60bd609c, 0x250160be, 0x432e04ee, 0x2001e01f, 0x617807c0,
        0x317fe01b, 0xd01809c9, 0x617d231f, 0xc010ca10, 0xd1fa3b01, 0xca10617e, 0x3901c010, 0x2100e7f3,
        0x23802202, 0xd1030504, 0xd0010b0c, 0x015b0292, 0x1ac9617a, 0x44186000, 0x2000d8f2, 0x47706178,
        0x22042100, 0xe7f30650, 0x1fff0f6c, 0x40022100, 0x40021000, 0x40003000, 0x00005555, 0x45670123,
        0xcdef89ab, 0x40022000,
    ],
    'pc_init': 0x20000005,
    'pc_unInit': 0x2000003f,
    'pc_program_page': 0x20000047,
    'pc_erase_sector': 0x20000063,
    'pc_erase_multi': 0x20000065,
    'pc_eraseAll': 0x20000085,
    'static_base': 0x200000ac,
    'begin_stack': 0x20000200,
    'end_stack': 0x20000100,
    'page_size': 0x80,
    'analyzer_supported': True,
    'analyzer_address': 0x20000300,
    'begin_data': 0x20000200,
    'page_buffers': [
        0x20000200,
        0x20000280,
    ],
    'min_program_length': 0x80,
    'flash_start': 0x8000000,
    'flash_size': 0x8000,
    'sector_sizes': (
        (0x0, 0x80),
    ),
}

OPT_ALGO = {
    'load_address': 0x20000000,
    'instructions': [
        0xe7fdbe00,
        0xcf03a717, 0x0c13c814, 0x0a160c25, 0xc81cc17c, 0x0c2546c0, 0xcffec13c, 0x68003870, 0x69f86050,
        0xd2040b40, 0x2406601c, 0x0c44605c, 0x186b609c, 0x18740849, 0x607b607d, 0x60bc60be, 0x20c0e00d,
        0x61380600, 0x8810e009, 0x89928891, 0x045b2301, 0x623961f8, 0x613b62ba, 0x200067fb, 0x47706138,
        0x1fff0f6c, 0x40022100, 0x88888888, 0x40021000, 0x40003000, 0x00005555, 0x45670123, 0x08192a3b,
        0x40022004,
    ],
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000043,
    'pc_program_page': 0x2000004b,
    'pc_erase_sector': 0x2000005f,
    'pc_eraseAll': 0x2000005f,
    'static_base': 0x20000088,
    'begin_stack': 0x20000200,
    'end_stack': 0x20000100,
    'page_size': 0x10,
    'analyzer_supported': False,
    'analyzer_address': 0x20000300,
    'begin_data': 0x20000200,
    'page_buffers': [
        0x20000200,
    ],
    'min_program_length': 0x10,
    'flash_start': 0x1fff0e80,
    'flash_size': 0x10,
    'sector_sizes': (
        (0x0, 0x10),
    ),
}


class PY32F003x6(CoreSightTarget):
    VENDOR = "Puya"

    MEMORY_MAP = MemoryMap(
        FlashRegion(    start=0x1fff0e80,  length=0x10,        blocksize=0x10,                      algo=OPT_ALGO),
        FlashRegion(    start=0x08000000,  length=0x8000,      blocksize=0x80, is_boot_memory=True, algo=FLASH_ALGO, erase_all_weight=3, erase_sector_weight=3, program_page_weight=2),
        RamRegion(      start=0x20000000,  length=0x1000),
    )

    def __init__(self, session):
        super(PY32F003x6, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("py32f003xx.svd")

    def post_connect_hook(self):
        self.write_memory(RCC_APBENR1, self.read_memory(RCC_APBENR1) | RCC_APBENR1_DBGMCU)
        self.write_memory(DBGMCU_CR, DBGMCU_CR_VAL)
        self.write_memory(DBG_APB_FZ1, DBG_APB_FZ1_VAL)
        self.write_memory(DBG_APB_FZ2, DBG_APB_FZ2_VAL)
