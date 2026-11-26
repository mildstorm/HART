# -*- coding: utf-8 -*-
"""Linear 6502 disassembler for the HART ROM listings in disasm/.

    python tools/disasm6502.py            regenerate disasm/U45_CD8.asm, U46_EF5.asm, U65_VD5.asm

Each ROM is listed at the address its own code says it runs at (JSR/JMP targets
and vectors, docs/13 3.2.1):
  U45 C/D8  main 6502  $C000-$DFFF
  U46 EF5   main 6502  $E000-$FFFF
  U65 VD5   U64 6502   $C000-$DFFF (reset vector $C000; also mirrored at $E000)

Operand comments come from the symbol table of the CPU that runs the ROM, so
U65 gets U64's I/O map, not the Apple II one. Address labels ([NAME]) are put
only on addresses the ROM really occupies. Undocumented opcodes and data are
listed as .BYTE; the listing is linear, so data may show as code.
"""
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')

# ---------- NMOS 6502 documented opcodes ----------
MODES = {
    'imp': 1, 'acc': 1, 'imm': 2, 'zp': 2, 'zpx': 2, 'zpy': 2, 'izx': 2, 'izy': 2,
    'rel': 2, 'abs': 3, 'abx': 3, 'aby': 3, 'ind': 3,
}
OPS = {}


def _op(name, *pairs):
    for code, mode in pairs:
        OPS[code] = (name, mode)


_op('ADC', (0x69, 'imm'), (0x65, 'zp'), (0x75, 'zpx'), (0x6D, 'abs'), (0x7D, 'abx'), (0x79, 'aby'), (0x61, 'izx'), (0x71, 'izy'))
_op('AND', (0x29, 'imm'), (0x25, 'zp'), (0x35, 'zpx'), (0x2D, 'abs'), (0x3D, 'abx'), (0x39, 'aby'), (0x21, 'izx'), (0x31, 'izy'))
_op('ASL', (0x0A, 'acc'), (0x06, 'zp'), (0x16, 'zpx'), (0x0E, 'abs'), (0x1E, 'abx'))
_op('BCC', (0x90, 'rel')); _op('BCS', (0xB0, 'rel')); _op('BEQ', (0xF0, 'rel')); _op('BMI', (0x30, 'rel'))
_op('BNE', (0xD0, 'rel')); _op('BPL', (0x10, 'rel')); _op('BVC', (0x50, 'rel')); _op('BVS', (0x70, 'rel'))
_op('BIT', (0x24, 'zp'), (0x2C, 'abs'))
_op('BRK', (0x00, 'imp')); _op('CLC', (0x18, 'imp')); _op('CLD', (0xD8, 'imp')); _op('CLI', (0x58, 'imp'))
_op('CLV', (0xB8, 'imp'))
_op('CMP', (0xC9, 'imm'), (0xC5, 'zp'), (0xD5, 'zpx'), (0xCD, 'abs'), (0xDD, 'abx'), (0xD9, 'aby'), (0xC1, 'izx'), (0xD1, 'izy'))
_op('CPX', (0xE0, 'imm'), (0xE4, 'zp'), (0xEC, 'abs'))
_op('CPY', (0xC0, 'imm'), (0xC4, 'zp'), (0xCC, 'abs'))
_op('DEC', (0xC6, 'zp'), (0xD6, 'zpx'), (0xCE, 'abs'), (0xDE, 'abx'))
_op('DEX', (0xCA, 'imp')); _op('DEY', (0x88, 'imp'))
_op('EOR', (0x49, 'imm'), (0x45, 'zp'), (0x55, 'zpx'), (0x4D, 'abs'), (0x5D, 'abx'), (0x59, 'aby'), (0x41, 'izx'), (0x51, 'izy'))
_op('INC', (0xE6, 'zp'), (0xF6, 'zpx'), (0xEE, 'abs'), (0xFE, 'abx'))
_op('INX', (0xE8, 'imp')); _op('INY', (0xC8, 'imp'))
_op('JMP', (0x4C, 'abs'), (0x6C, 'ind')); _op('JSR', (0x20, 'abs'))
_op('LDA', (0xA9, 'imm'), (0xA5, 'zp'), (0xB5, 'zpx'), (0xAD, 'abs'), (0xBD, 'abx'), (0xB9, 'aby'), (0xA1, 'izx'), (0xB1, 'izy'))
_op('LDX', (0xA2, 'imm'), (0xA6, 'zp'), (0xB6, 'zpy'), (0xAE, 'abs'), (0xBE, 'aby'))
_op('LDY', (0xA0, 'imm'), (0xA4, 'zp'), (0xB4, 'zpx'), (0xAC, 'abs'), (0xBC, 'abx'))
_op('LSR', (0x4A, 'acc'), (0x46, 'zp'), (0x56, 'zpx'), (0x4E, 'abs'), (0x5E, 'abx'))
_op('NOP', (0xEA, 'imp'))
_op('ORA', (0x09, 'imm'), (0x05, 'zp'), (0x15, 'zpx'), (0x0D, 'abs'), (0x1D, 'abx'), (0x19, 'aby'), (0x01, 'izx'), (0x11, 'izy'))
_op('PHA', (0x48, 'imp')); _op('PHP', (0x08, 'imp')); _op('PLA', (0x68, 'imp')); _op('PLP', (0x28, 'imp'))
_op('ROL', (0x2A, 'acc'), (0x26, 'zp'), (0x36, 'zpx'), (0x2E, 'abs'), (0x3E, 'abx'))
_op('ROR', (0x6A, 'acc'), (0x66, 'zp'), (0x76, 'zpx'), (0x6E, 'abs'), (0x7E, 'abx'))
_op('RTI', (0x40, 'imp')); _op('RTS', (0x60, 'imp'))
_op('SBC', (0xE9, 'imm'), (0xE5, 'zp'), (0xF5, 'zpx'), (0xED, 'abs'), (0xFD, 'abx'), (0xF9, 'aby'), (0xE1, 'izx'), (0xF1, 'izy'))
_op('SEC', (0x38, 'imp')); _op('SED', (0xF8, 'imp')); _op('SEI', (0x78, 'imp'))
_op('STA', (0x85, 'zp'), (0x95, 'zpx'), (0x8D, 'abs'), (0x9D, 'abx'), (0x99, 'aby'), (0x81, 'izx'), (0x91, 'izy'))
_op('STX', (0x86, 'zp'), (0x96, 'zpy'), (0x8E, 'abs'))
_op('STY', (0x84, 'zp'), (0x94, 'zpx'), (0x8C, 'abs'))
_op('TAX', (0xAA, 'imp')); _op('TAY', (0xA8, 'imp')); _op('TSX', (0xBA, 'imp')); _op('TXA', (0x8A, 'imp'))
_op('TXS', (0x9A, 'imp')); _op('TYA', (0x98, 'imp'))

# ---------- symbols ----------
# Main 6502 (Apple II+ compatible): soft switches and Monitor entry points.
APPLE_IO = {
    0xC000: 'KBD', 0xC010: 'KBDSTRB', 0xC020: 'TAPEOUT', 0xC030: 'SPKR', 0xC040: 'STROBE',
    0xC050: 'TEXTOFF', 0xC051: 'TEXTON', 0xC052: 'MIXEDOFF', 0xC053: 'MIXEDON',
    0xC054: 'PAGE2OFF', 0xC055: 'PAGE2ON', 0xC056: 'HIRESOFF', 0xC057: 'HIRESON',
    0xC058: 'AN0OFF', 0xC059: 'AN0ON', 0xC05A: 'AN1OFF', 0xC05B: 'AN1ON',
    0xC05C: 'AN2OFF', 0xC05D: 'AN2ON', 0xC05E: 'AN3OFF', 0xC05F: 'AN3ON',
    0xC060: 'CASSETTE_IN', 0xC061: 'PB0', 0xC062: 'PB1', 0xC063: 'PB2',
    0xC064: 'PADDL0', 0xC065: 'PADDL1', 0xC066: 'PADDL2', 0xC067: 'PADDL3', 0xC070: 'PTRIG',
    # $C080-$C08F: slot 0 device select -> U49 bank latch (language card style, docs/13 3.2.1)
    0xC080: 'LC_BANK2_RAM', 0xC081: 'LC_BANK2_ROM_W', 0xC082: 'LC_BANK2_ROM', 0xC083: 'LC_BANK2_RAM_W',
    0xC088: 'LC_BANK1_RAM', 0xC089: 'LC_BANK1_ROM_W', 0xC08A: 'LC_BANK1_ROM', 0xC08B: 'LC_BANK1_RAM_W',
    # built-in Disk II, slot 6 ($C080 + $60, used as $C08x,X with X = $60)
    0xC0E0: 'PHASE0OFF', 0xC0E1: 'PHASE0ON', 0xC0E2: 'PHASE1OFF', 0xC0E3: 'PHASE1ON',
    0xC0E4: 'PHASE2OFF', 0xC0E5: 'PHASE2ON', 0xC0E6: 'PHASE3OFF', 0xC0E7: 'PHASE3ON',
    0xC0E8: 'MOTOROFF', 0xC0E9: 'MOTORON', 0xC0EA: 'DRV0EN', 0xC0EB: 'DRV1EN',
    0xC0EC: 'Q6L', 0xC0ED: 'Q6H', 0xC0EE: 'Q7L', 0xC0EF: 'Q7H',
    0xC300: 'VIDEX_C300', 0xC600: 'DISK2_BOOT', 0xCFFF: 'CLRROM',
    0x03F0: 'BRKV', 0x03F2: 'SOFTEV', 0x03F3: 'SOFTEV_H', 0x03F4: 'PWREDGE',
    0x03F8: 'USRADR', 0x03FB: 'NMI', 0x03FE: 'IRQLOC',
}
MONITOR = {
    0xF800: 'PLOT', 0xF819: 'HLINE', 0xF828: 'VLINE', 0xF832: 'CLRSCR', 0xF836: 'CLRTOP',
    0xF847: 'GBASCALC', 0xF864: 'SETCOL', 0xF871: 'SCRN', 0xF941: 'PRNTAX', 0xF948: 'PRBLNK',
    0xFA40: 'IRQ', 0xFA62: 'RESET', 0xFAA6: 'PWRUP', 0xFB1E: 'PREAD', 0xFB2F: 'INIT',
    0xFB39: 'SETTXT', 0xFB40: 'SETGR', 0xFB5B: 'TABV', 0xFBDD: 'BELL1', 0xFBFD: 'VIDOUT',
    0xFC10: 'BS', 0xFC1A: 'UP', 0xFC22: 'VTAB', 0xFC42: 'CLREOP', 0xFC58: 'HOME',
    0xFC62: 'CR', 0xFC66: 'LF', 0xFC70: 'SCROLL', 0xFC9C: 'CLREOL', 0xFCA8: 'WAIT',
    0xFD0C: 'RDKEY', 0xFD1B: 'KEYIN', 0xFD35: 'RDCHAR', 0xFD67: 'GETLNZ', 0xFD6A: 'GETLN',
    0xFD8B: 'CROUT1', 0xFD8E: 'CROUT', 0xFDDA: 'PRBYTE', 0xFDE3: 'PRHEX', 0xFDED: 'COUT',
    0xFDF0: 'COUT1', 0xFE2C: 'MOVE', 0xFE80: 'SETINV', 0xFE84: 'SETNORM', 0xFE89: 'SETKBD',
    0xFE93: 'SETVID', 0xFF2D: 'PRERR', 0xFF3A: 'BELL', 0xFF3F: 'RESTORE', 0xFF4A: 'SAVE',
    0xFF59: 'OLDRST', 0xFF65: 'MON', 0xFF69: 'MONZ',
}
MAIN_SYMS = {**APPLE_IO, **MONITOR}

# U64 (second 6502) local bus, docs/13 section 2.
U64_SYMS = {
    0x0400: 'KEYOUT_LATCH', 0x0800: 'CTRL_LATCH', 0x0C00: 'MODE_LATCH',
    0x8800: 'SWITCHES',
}
for k in range(13):
    U64_SYMS[0x8000 + k] = 'KBD_ROW%d' % k


def u64_sym(a):
    if a in U64_SYMS:
        return U64_SYMS[a]
    if 0x4000 <= a <= 0x43FF:
        return 'U68_ODD+$%03X' % (a - 0x4000)      # main $E000 + 2k + 1
    if 0x5000 <= a <= 0x53FF:
        return 'U68_EVEN+$%03X' % (a - 0x5000)     # main $E000 + 2k
    return None


def main_sym(a):
    return MAIN_SYMS.get(a)


# ---------- disassembly ----------

def disasm(data, base, sym, addr_labels, data_ranges=(), vectors=False):
    out = []
    n = len(data)
    i = 0
    end_code = n - 6 if vectors else n
    while i < n:
        a = base + i
        lab = addr_labels.get(a)
        tail = ' ; [%s]' % lab if lab else ''
        dr = next((r for r in data_ranges if r[0] <= i < r[1]), None)
        if i >= end_code:
            w = data[i] | data[i + 1] << 8
            name = {0: 'NMI_VECTOR', 2: 'RESET_VECTOR', 4: 'IRQ_VECTOR'}[i - end_code]
            out.append('$%04X:  %02X %02X     .WORD $%04X ; [%s]' % (a, data[i], data[i + 1], w, name))
            i += 2
            continue
        if dr:
            chunk = data[i:min(i + 8, dr[1])]
            txt = ''.join(chr(c & 0x7F) if 0x20 <= (c & 0x7F) < 0x7F else '.' for c in chunk)
            out.append('$%04X:  %-9s .BYTE %s ; "%s"%s' % (
                a, ' '.join('%02X' % c for c in chunk[:3]) + ('+' if len(chunk) > 3 else ''),
                ','.join('$%02X' % c for c in chunk), txt, tail))
            i += len(chunk)
            continue
        op = data[i]
        if op not in OPS or i + MODES[OPS[op][1]] > end_code:
            out.append('$%04X:  %02X        .BYTE $%02X%s' % (a, op, op, tail))
            i += 1
            continue
        name, mode = OPS[op]
        size = MODES[mode]
        b = data[i:i + size]
        hexs = ' '.join('%02X' % x for x in b)
        v8 = b[1] if size > 1 else 0
        v16 = (b[1] | b[2] << 8) if size == 3 else 0
        note = None
        if mode == 'imp':
            text = name
        elif mode == 'acc':
            text = name
        elif mode == 'imm':
            text = '%s #$%02X' % (name, v8)
            if 0x20 <= (v8 & 0x7F) < 0x7F:
                text += " ('%s')" % chr(v8 & 0x7F)
        elif mode in ('zp', 'zpx', 'zpy'):
            text = '%s $%02X%s' % (name, v8, {'zp': '', 'zpx': ',X', 'zpy': ',Y'}[mode])
        elif mode == 'izx':
            text = '%s ($%02X,X)' % (name, v8)
        elif mode == 'izy':
            text = '%s ($%02X),Y' % (name, v8)
        elif mode == 'rel':
            t = (a + 2 + (v8 - 256 if v8 > 127 else v8)) & 0xFFFF
            text = '%s $%04X' % (name, t)
            note = addr_labels.get(t)
        else:
            text = '%s %s$%04X%s' % (name, '(' if mode == 'ind' else '', v16,
                                      {'abs': '', 'abx': ',X', 'aby': ',Y', 'ind': ')'}[mode])
            note = sym(v16) or addr_labels.get(v16)
        line = '$%04X:  %-9s %s' % (a, hexs, text)
        if note:
            line += ' ; ' + note
        out.append(line + tail)
        i += size
    return out


def write(name, header, lines):
    path = os.path.join(ROOT, 'disasm', name)
    with open(path, 'w', encoding='utf-8', newline='\r\n') as f:   # the repo keeps these CRLF
        f.write('\n'.join(header + [''] + lines) + '\n')
    print('wrote', path, len(lines), 'lines')


def rom(name):
    return open(os.path.join(ROOT, 'rom', name), 'rb').read()


HDR_TOOL = '; Generated by tools/disasm6502.py (linear: data may show as code, undocumented opcodes as .BYTE)'

if __name__ == '__main__':
    # U45: $C000-$DFFF. $C000-$C0FF of the chip is never visible (I/O page) -> no labels there.
    u45_labels = {0xC300: 'VIDEX_C300_ENTRY', 0xC600: 'DISK2_BOOT_ENTRY', 0xC800: 'VIDEX_C800_ROM'}
    write('U45_CD8.asm', [
        '; ======================================================================',
        '; 정원 HART U45 (2764 "C/D8", 8KB) 메인 6502 시스템 ROM: $C000-$DFFF',
        ';   $C000-$C0FF: 칩에는 있으나 이 주소는 I/O 영역이라 CPU에 보이지 않음 (내용 무시)',
        ';   $C100-$C7FF: 내장 슬롯 ROM ($C300 Videx 80컬럼, $C600 Disk II 16-섹터 부트)',
        ';   $C800-$CFFF: Videx VideoTerm 호환 80컬럼 확장 펌웨어 (2KB)',
        ';   $D000-$DFFF: Applesoft BASIC 전반부 (4KB)',
        ';   보이는 조건: U35 2Y0(/CE)·U36 O3(A12)가 고름 (docs/13 3.2.1)',
        '; Base Address: $C000 - $DFFF (8192 bytes)',
        HDR_TOOL,
        '; ======================================================================',
    ], disasm(rom('U45_CD8.bin'), 0xC000, main_sym, u45_labels))

    u46_labels = dict(MONITOR)
    write('U46_EF5.asm', [
        '; ======================================================================',
        '; 정원 HART U46 (2764 "EF5", 8KB) 메인 6502 시스템 ROM: $E000-$FFFF',
        ';   $E000-$F7FF: Applesoft BASIC 후반부 (6KB)',
        ';   $F800-$FFFF: Apple II+ Autostart Monitor (2KB)',
        ';   $FAA6: 콜드 리셋 - 슬롯 검색 생략, 내장 FDD 슬롯 6($C600) 즉시 부팅',
        ';   $FFFA-$FFFF: 6502 벡터 (NMI $03FB, RESET $FA62, IRQ $FA40)',
        ';   보이는 조건: U35 2Y1(/CE)·U36 O3(A12)가 고름 (docs/13 3.2.1)',
        '; Base Address: $E000 - $FFFF (8192 bytes)',
        HDR_TOOL,
        '; ======================================================================',
    ], disasm(rom('U46_EF5.bin'), 0xE000, main_sym, u46_labels, vectors=True))

    u65 = rom('U65_VD5.bin')
    write('U65_VD5.asm', [
        '; ======================================================================',
        '; 정원 HART U65 (2764 "VD5", 8KB) U64(두 번째 6502) 펌웨어',
        ';   U64 로컬 버스 $C000-$DFFF (리셋 벡터 $C000; $E000-$FFFF에도 비쳐 벡터를 읽음, docs/13 2절)',
        ';   오퍼랜드 주석은 U64 주소 맵: $0400 메인으로 가는 키 래치, $0800/$0C00 래치,',
        ';   $4000/$5000 U68 홀수/짝수 칸(메인 $E000+2k+1 / +2k), $8000-$800C 키보드 행, $8800 스위치',
        ';   오프셋 0x1300-0x14FF ($D300-$D4FF): 화면 하단 기능키(F1-F12) 라벨 표 (Apple 3세트 + CP/M 1세트)',
        '; Base Address: $C000 - $DFFF (8192 bytes)',
        HDR_TOOL,
        '; ======================================================================',
    ], disasm(u65, 0xC000, u64_sym, {0xC000: 'RESET'}, data_ranges=[(0x1300, 0x1500)], vectors=True))
