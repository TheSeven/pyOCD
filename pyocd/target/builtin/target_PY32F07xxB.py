# pyOCD debugger
# Copyright (c) 2006-2013 Arm Limited
# Copyright (c) 2021 Chris Reed
# Copyright (c) 2025 Michael Sparmann
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

RCC_APBENR2 = 0x40021040
RCC_APBENR2_MCUDBGEN = 0x00000400

DBGMCU_CR = 0x40015804
DBG_APB_FZ1 = 0x40015808
DBG_APB_FZ2 = 0x4001580c

DBGMCU_CR_VAL = 0x00000003
DBG_APB_FZ1_VAL = 0xffffffff
DBG_APB_FZ2_VAL = 0xffffffff


FLASH_ALGO = {
    'load_address' : 0x20000000,
    'instructions': [
        0xe7fdbe00,
        0xcf03a720, 0x0c13c81c, 0x0a160c25, 0xc87cc17c, 0x0c360035, 0xcffcc1f4, 0x680038dc, 0x6a396050,
        0xd2040b49, 0x2406601c, 0x0c44605c, 0x60bd609c, 0xe01f60be, 0x07c02001, 0xe01b6178, 0x0a0931ff,
        0x39010189, 0x2301d316, 0xd10106cc, 0x330104db, 0xca08617b, 0xe7f4c008, 0x22022100, 0x050401d3,
        0x0b0cd103, 0x0292d001, 0x617a015b, 0x60001ac9, 0xd8f24418, 0x61782000, 0x21004770, 0x06502204,
        0x46c0e7f3, 0x1fff32d8, 0x40022100, 0x40021000, 0x40003000, 0x00005555, 0x45670123, 0xcdef89ab,
        0x40022000,
    ],
    'pc_init': 0x20000005,
    'pc_unInit': 0x20000039,
    'pc_program_page': 0x20000041,
    'pc_erase_sector': 0x2000005d,
    'pc_erase_multi': 0x2000005f,
    'pc_eraseAll': 0x2000007f,
    'static_base': 0x200000a8,
    'begin_stack': 0x20000200,
    'end_stack': 0x20000100,
    'page_size': 0x100,
    'analyzer_supported': True,
    'analyzer_address': 0x20000400,
    'begin_data': 0x20000200,
    'page_buffers': [
        0x20000200,
        0x20000300,
    ],
    'min_program_length': 0x100,
    'flash_start': 0x8000000,
    'flash_size': 0x20000,
    'sector_sizes': (
        (0x0, 0x100),
    ),
}

OPT_ALGO = {
    'load_address' : 0x20000000,
    'instructions': [
        0xe7fdbe00,
        0xcf03a717, 0x0c13c81c, 0x0a160c25, 0xc87cc17c, 0x0c360035, 0xcffec1f4, 0x680038dc, 0x69f86050,
        0xd2040b40, 0x2406601c, 0x0c44605c, 0x186b609c, 0x18740849, 0x607b607d, 0x60bc60be, 0x20c0e00d,
        0x61380600, 0x8810e009, 0x8a128911, 0x045b2301, 0x623961f8, 0x613b62ba, 0x200067fb, 0x47706138,
        0x1fff32d8, 0x40022100, 0x88888888, 0x40021000, 0x40003000, 0x00005555, 0x45670123, 0x08192a3b,
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
    'page_size': 0x20,
    'analyzer_supported': False,
    'begin_data': 0x20000200,
    'page_buffers': [
        0x20000200,
    ],
    'min_program_length': 0x20,
    'flash_start': 0x1fff3100,
    'flash_size': 0x20,
    'sector_sizes': (
        (0x0, 0x20),
    ),
}


class PY32F07xxB(CoreSightTarget):
    VENDOR = "Puya"

    MEMORY_MAP = MemoryMap(
        FlashRegion(    start=0x1fff3100,  length=0x20,        blocksize=0x20,                       algo=OPT_ALGO),
        FlashRegion(    start=0x08000000,  length=0x20000,     blocksize=0x100, is_boot_memory=True, algo=FLASH_ALGO, erase_all_weight=3, erase_sector_weight=3, program_page_weight=2),
        RamRegion(      start=0x20000000,  length=0x8000),
    )

    def __init__(self, session):
        super(PY32F07xxB, self).__init__(session, self.MEMORY_MAP)
        self._svd_location = SVDFile.from_builtin("py32f072xx.svd")

    def post_connect_hook(self):
        self.write_memory(RCC_APBENR2, self.read_memory(RCC_APBENR2) | RCC_APBENR2_MCUDBGEN)
        self.write_memory(DBGMCU_CR, DBGMCU_CR_VAL)
        self.write_memory(DBG_APB_FZ1, DBG_APB_FZ1_VAL)
        self.write_memory(DBG_APB_FZ2, DBG_APB_FZ2_VAL)
