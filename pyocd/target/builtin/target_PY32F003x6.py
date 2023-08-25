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

#DBGMCU clock
RCC_APB2ENR_CR = 0x40021018
RCC_APB2ENR_DBGMCU = 0x00400000

DBGMCU_CR = 0x40015804
DBGMCU_APB1_CR = 0x40015808
DBGMCU_APB2_CR = 0x4001580C

#0000 0000 0000 0000 0000 0000 0000 0100
#BGMCU_CR_VAL = 0x00000000

#0000 0010 0010 0000 0001 1101 0011 0011
DBGMCU_APB1_VAL = 0x02201D33

#0000 0000 0000 0111 0000 1000 0000 0000
DBGMCU_APB2_VAL = 0x00070800


FLASH_ALGO = {
    'load_address': 0x20000000,
    'instructions': [
        0xe7fdbe00,
        0xcf03a71f, 0x0c13c814, 0x0a160c25, 0xc81cc17c, 0xc13c0c25, 0x3870cffc, 0x60506800, 0x0b496a39,
        0x601cd204, 0x605c2406, 0x609c0c44, 0x60be60bd, 0x2001e01f, 0x617807c0, 0x317fe01b, 0x014909c9,
        0xd3163901, 0x06cc2301, 0x04dbd101, 0x617b3301, 0xc008ca08, 0x2100e7f4, 0x23802202, 0xd1030504,
        0xd0010b0c, 0x015b0292, 0x1ac9617a, 0x44186000, 0x2000d8f2, 0x47706178, 0x22042100, 0xe7f30650,
        0x1fff0f6c, 0x40022100, 0x40021000, 0x40003000, 0x00005555, 0x45670123, 0xcdef89ab, 0x40022000,
    ],
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000037,
    'pc_program_page': 0x2000003f,
    'pc_erase_sector': 0x2000005b,
    'pc_erase_multi': 0x2000005d,
    'pc_eraseAll': 0x2000007d,
    'static_base': 0x200000a8,
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
        0xcf03a717, 0x0c13c814, 0x0a160c25, 0xc81cc17c, 0xc13c0c25, 0x3870cffe, 0x60506800, 0x0b4069f8,
        0x601cd204, 0x605c2406, 0x609c0c44, 0x0849186b, 0x607d1874, 0x60be607b, 0xe00d60bc, 0x060020c0,
        0xe0096138, 0x88918810, 0x23018992, 0x61f8045b, 0x62ba6239, 0x67fb613b, 0x61382000, 0x46c04770,
        0x1fff0f6c, 0x40022100, 0x88888888, 0x40021000, 0x40003000, 0x00005555, 0x45670123, 0x08192a3b,
        0x40022004,
    ],
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000041,
    'pc_program_page': 0x20000049,
    'pc_erase_sector': 0x2000005d,
    'pc_eraseAll': 0x2000005d,
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
        enclock = self.read_memory(RCC_APB2ENR_CR)
        enclock |= RCC_APB2ENR_DBGMCU
        self.write_memory(RCC_APB2ENR_CR, enclock)
        self.write_memory(DBGMCU_APB1_CR, DBGMCU_APB1_VAL)
        self.write_memory(DBGMCU_APB2_CR, DBGMCU_APB2_VAL)
