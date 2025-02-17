# pyOCD debugger
# Copyright (c) 2024 PyOCD Authors
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

FLASH_ALGO = {
    'load_address' : 0x20000000,

    # Flash algorithm as a hex string
    'instructions': [
    0xe7fdbe00,
    0xe0052200, 0x2b005c83, 0x2001d001, 0x1c524770, 0xd3f7428a, 0x47702000, 0x20006001, 0x68004770,
    0x20006008, 0x22004770, 0xe0044bc4, 0x1c492100, 0xdbfc4299, 0x42821c52, 0x4770dbf8, 0x4684b5f0,
    0x460f48bf, 0x69064448, 0x20092400, 0x07006835, 0x20014005, 0xffe7f7ff, 0x45641c64, 0x2d00da0c,
    0x48b7d1f3, 0x44482f00, 0x68006940, 0x6038d001, 0x0f00e004, 0xd001280a, 0xbdf02001, 0xbdf02000,
    0x4cafb470, 0x444c4daf, 0x341c0600, 0x23001946, 0x60261e50, 0xe00d6060, 0x784618c8, 0x02365ccd,
    0x788619ad, 0x043678c0, 0x18300600, 0x18e0182d, 0x60851d1b, 0xdbef4293, 0x444949a1, 0x60046948,
    0x49a16908, 0xbc706001, 0x20c82100, 0x489fe7b6, 0x79007801, 0x0d000700, 0x47704308, 0x39f91fc1,
    0x489bd004, 0x02406800, 0x47700f40, 0xe7f94899, 0x39924601, 0xd9072904, 0xd0052898, 0xd0032899,
    0xd001289c, 0x47702000, 0x47702001, 0xf7ffb570, 0x4602ffde, 0xffecf7ff, 0x28004c89, 0xd005444c,
    0x6120488d, 0x61601d00, 0xe004488c, 0x6120488c, 0x61601d00, 0x61a0488b, 0x04816800, 0x60210c89,
    0x0f890201, 0x0f800280, 0x60e06061, 0xf7ff4610, 0x2800ffcf, 0xd0056820, 0x60200200, 0x01c06860,
    0xe00a6060, 0x30ff0200, 0x60203001, 0x01806860, 0x60603040, 0x1c4068e0, 0xcc2160e0, 0x46293c08,
    0xf920f000, 0x462860a0, 0xffa8f7ff, 0x41016821, 0x60212000, 0x496abd70, 0x4449b508, 0x4a726948,
    0x69086002, 0x31114968, 0x46696001, 0xf7ff20c8, 0x0002ff45, 0x2001d001, 0x9800bd08, 0x290a0f01,
    0x496ad00e, 0x42882201, 0x4968d009, 0x42883908, 0xf7ffd106, 0xf7ffff7c, 0x2800ff8b, 0x2200d000,
    0xbd084610, 0x4604b510, 0xff90f7ff, 0xd0032801, 0xd0012c00, 0xffcff7ff, 0xb5ffbd10, 0x46171844,
    0xb083484f, 0x4e4e2200, 0x92004448, 0x68c1444e, 0x6880361c, 0xf8d6f000, 0x90022500, 0x900119e0,
    0x4847e02e, 0x68404448, 0x46019000, 0xf0004620, 0x4607f8c9, 0xf0009902, 0x9906f8c5, 0x1949b2c0,
    0xf7ff9a00, 0x2801ff1d, 0x0a39d01d, 0x0209b2f8, 0x49471840, 0x4f3a0400, 0x444f1840, 0x69786030,
    0x60064939, 0x1c496938, 0x21006001, 0xf7ff20c8, 0x9000fee5, 0xd0062801, 0x19046878, 0x98011945,
    0xd8ce42a0, 0xb0079800, 0xb5f8bdf0, 0x22004d2c, 0x444d4e2b, 0x444e3524, 0xe0014613, 0x1c5254ab,
    0x42946874, 0x4604dcfa, 0xe0141847, 0x42a06830, 0x4620dd13, 0xf7ff6871, 0x2801fea3, 0x462bd109,
    0x46202100, 0xf7ff6872, 0x2800ff98, 0x2001d001, 0x6870bdf8, 0x42a71904, 0x2000d8e8, 0xb5f0bdf8,
    0x27014d17, 0x444d06ff, 0xd1032800, 0x681c692b, 0x601c433c, 0xe0042300, 0x5cc45cd6, 0xd10242a6,
    0x428b1c5b, 0x2800d3f8, 0x6929d103, 0x43ba680a, 0x18c0600a, 0xb530bdf0, 0x46044b09, 0x681b444b,
    0xe0071841, 0xd9074283, 0x42955c25, 0x2001d001, 0x1c40bd30, 0xd8f54281, 0xbd302000, 0x00000d05,
    0x00000004, 0x0000d7b6, 0x80000004, 0xf0000fe0, 0x0ffff140, 0x0ffff240, 0x40000004, 0x400e0000,
    0x40100004, 0x40110000, 0x0000e8b6, 0xf0000013, 0x0000d8b6, 0x2a01b510, 0x2a02d005, 0x2000d003,
    0xff30f7ff, 0x2001bd10, 0x2000e7fa, 0x490c4770, 0x4449b510, 0xf7ff6809, 0xbd10ff78, 0xe7f62000,
    0xb5104613, 0x2100460a, 0xff27f7ff, 0xb510bd10, 0xff95f7ff, 0xb510bd10, 0xffadf7ff, 0x0000bd10,
    0x00000004, 0x2400b570, 0x28004625, 0x2401da01, 0x29004240, 0x2501da01, 0xf0004249, 0x42acf807,
    0x4240d000, 0xd0002c00, 0xbd704249, 0x460bb530, 0x20004601, 0x24012220, 0x460de009, 0x429d40d5,
    0x461dd305, 0x1b494095, 0x40954625, 0x46151940, 0x2d001e52, 0xbd30dcf1,
    ],

    # Relative function addresses
    'pc_init': 0x20000379,
    'pc_unInit': 0x2000038f,
    'pc_program_page': 0x200003a5,
    'pc_erase_sector': 0x20000393,
    'pc_eraseAll': 0x200003a1,

    'static_base' : 0x2000041c,
    'begin_stack' : 0x20000b38,
    'end_stack' : 0x20000550,
    'begin_data' : 0x20001000,
    'page_size' : 0x100,
    'analyzer_supported' : False,
    'analyzer_address' : 0x20000b38,
    # Enable double buffering
    'page_buffers' : [
        0x20001000,
        #0x20001100,
    ],
    'min_program_length' : 0x100,

    # Relative region addresses and sizes
    'ro_start': 0x4,
    'ro_size': 0x418,
    'rw_start': 0x41c,
    'rw_size': 0x4,
    'zi_start': 0x420,
    'zi_size': 0x124,

    # Flash information
    'flash_start': 0x0,
    'flash_size': 0x10000,
    'sector_sizes': (
        (0x0, 0x10000),
    )
}
