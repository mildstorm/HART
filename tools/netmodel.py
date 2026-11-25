#!/usr/bin/env python3
"""HART board net model built from measured continuity.

Reads data/bom.csv (which part sits at which ref) and data/netlist.csv (measured
pin-to-pin continuity), groups connected pins into nets with a union-find, and
uses a pin-function library of the logic parts on the board to:

  * tell for every net which pins drive it and which only listen,
  * flag nets with no known driver (next thing to measure) and nets with two
    totem-pole drivers (likely a measurement or recording mistake),
  * trace a signal back through gates, buffers, muxes and decoders into a
    readable logic expression, stopping at flip-flops, PROMs and CPU pins.

Assumptions (kept explicit so a wrong one is easy to spot):
  * every IC's VCC/GND pins sit on the +5V/GND nets (standard pinouts),
  * slot pins other than the per-slot ones (1, 20, 41, 23, 24, 27, 28) are
    common to all four slots,
  * rows whose result is only a photo trace or a via are not used as
    connections; they are listed separately.

Usage:
  python tools/netmodel.py               write docs/15-nets.md
  python tools/netmodel.py --trace 64-37 print the trace of one pin
The schematic generator (schematic/src/gen.py) imports render_html().
"""
import csv, os, re, sys, html
from collections import defaultdict

ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))

# ---------------------------------------------------------------------------
# pin-function library
# kinds: in, out (totem pole), tri (3-state out), oc (open collector out),
#        bi (bidirectional), vcc, gnd, nc, ? (unknown)
# funcs: output pin -> description used by the tracer
# ---------------------------------------------------------------------------
LIB = {}

def part(name, pins, funcs=None, alias=()):
    d = {'pins': pins, 'funcs': funcs or {}}
    LIB[name] = d
    for a in alias:
        LIB[a] = d

def quad2(op, out_kind='out', layout='00'):
    # 74LS00/08/32 layout; 74LS02 has its own
    if layout == '00':
        g = [(1, 2, 3), (4, 5, 6), (9, 10, 8), (12, 13, 11)]   # (a, b, y)
        names = {1: '1A', 2: '1B', 3: '1Y', 4: '2A', 5: '2B', 6: '2Y', 9: '3A', 10: '3B', 8: '3Y', 12: '4A', 13: '4B', 11: '4Y'}
    else:  # 74LS02
        g = [(2, 3, 1), (5, 6, 4), (8, 9, 10), (11, 12, 13)]
        names = {1: '1Y', 2: '1A', 3: '1B', 4: '2Y', 5: '2A', 6: '2B', 10: '3Y', 8: '3A', 9: '3B', 13: '4Y', 11: '4A', 12: '4B'}
    pins = {7: ('GND', 'gnd'), 14: ('VCC', 'vcc')}
    funcs = {}
    for a, b, y in g:
        pins[a] = (names[a], 'in'); pins[b] = (names[b], 'in'); pins[y] = (names[y], out_kind)
        funcs[y] = (op, [a, b])
    return pins, funcs

part('74LS00', *quad2('NAND'))
part('74LS08', *quad2('AND'))
part('74LS32', *quad2('OR'))
part('74LS02', *quad2('NOR', layout='02'))

def hex_inv(kind):
    pairs = [(1, 2), (3, 4), (5, 6), (9, 8), (11, 10), (13, 12)]
    pins = {7: ('GND', 'gnd'), 14: ('VCC', 'vcc')}
    funcs = {}
    for i, (a, y) in enumerate(pairs, 1):
        pins[a] = (f'{i}A', 'in'); pins[y] = (f'{i}Y', kind)
        funcs[y] = ('NOT', [a])
    return pins, funcs

part('74LS04', *hex_inv('out'))
part('74LS05', *hex_inv('oc'))

part('74LS10', {1: ('1A', 'in'), 2: ('1B', 'in'), 13: ('1C', 'in'), 12: ('1Y', 'out'),
                3: ('2A', 'in'), 4: ('2B', 'in'), 5: ('2C', 'in'), 6: ('2Y', 'out'),
                9: ('3A', 'in'), 10: ('3B', 'in'), 11: ('3C', 'in'), 8: ('3Y', 'out'),
                7: ('GND', 'gnd'), 14: ('VCC', 'vcc')},
     {12: ('NAND', [1, 2, 13]), 6: ('NAND', [3, 4, 5]), 8: ('NAND', [9, 10, 11])})

part('74LS74', {1: ('/CLR1', 'in'), 2: ('D1', 'in'), 3: ('CLK1', 'in'), 4: ('/PRE1', 'in'), 5: ('Q1', 'out'), 6: ('/Q1', 'out'),
                7: ('GND', 'gnd'), 8: ('/Q2', 'out'), 9: ('Q2', 'out'), 10: ('/PRE2', 'in'), 11: ('CLK2', 'in'), 12: ('D2', 'in'),
                13: ('/CLR2', 'in'), 14: ('VCC', 'vcc')},
     {5: ('FF', 'D-FF 1 Q', {'D': 2, 'CLK': 3, '/PRE': 4, '/CLR': 1}),
      6: ('FF', 'D-FF 1 /Q', {'D': 2, 'CLK': 3, '/PRE': 4, '/CLR': 1}),
      9: ('FF', 'D-FF 2 Q', {'D': 12, 'CLK': 11, '/PRE': 10, '/CLR': 13}),
      8: ('FF', 'D-FF 2 /Q', {'D': 12, 'CLK': 11, '/PRE': 10, '/CLR': 13})})

part('74LS109', {1: ('/CLR1', 'in'), 2: ('J1', 'in'), 3: ('/K1', 'in'), 4: ('CLK1', 'in'), 5: ('/PRE1', 'in'), 6: ('Q1', 'out'),
                 7: ('/Q1', 'out'), 8: ('GND', 'gnd'), 9: ('/Q2', 'out'), 10: ('Q2', 'out'), 11: ('/PRE2', 'in'), 12: ('CLK2', 'in'),
                 13: ('/K2', 'in'), 14: ('J2', 'in'), 15: ('/CLR2', 'in'), 16: ('VCC', 'vcc')},
     {6: ('FF', 'JK-FF 1 Q', {'J': 2, '/K': 3, 'CLK': 4, '/PRE': 5, '/CLR': 1}),
      7: ('FF', 'JK-FF 1 /Q', {'J': 2, '/K': 3, 'CLK': 4, '/PRE': 5, '/CLR': 1}),
      10: ('FF', 'JK-FF 2 Q', {'J': 14, '/K': 13, 'CLK': 12, '/PRE': 11, '/CLR': 15}),
      9: ('FF', 'JK-FF 2 /Q', {'J': 14, '/K': 13, 'CLK': 12, '/PRE': 11, '/CLR': 15})})

part('74LS138', {1: ('A', 'in'), 2: ('B', 'in'), 3: ('C', 'in'), 4: ('/G2A', 'in'), 5: ('/G2B', 'in'), 6: ('G1', 'in'),
                 7: ('Y7', 'out'), 8: ('GND', 'gnd'), 9: ('Y6', 'out'), 10: ('Y5', 'out'), 11: ('Y4', 'out'), 12: ('Y3', 'out'),
                 13: ('Y2', 'out'), 14: ('Y1', 'out'), 15: ('Y0', 'out'), 16: ('VCC', 'vcc')},
     {p: ('DEC', n, [1, 2, 3], {'G1': 6, '/G2A': 4, '/G2B': 5}) for n, p in enumerate([15, 14, 13, 12, 11, 10, 9, 7])})

part('74LS139', {1: ('/1G', 'in'), 2: ('1A', 'in'), 3: ('1B', 'in'), 4: ('1Y0', 'out'), 5: ('1Y1', 'out'), 6: ('1Y2', 'out'),
                 7: ('1Y3', 'out'), 8: ('GND', 'gnd'), 9: ('2Y3', 'out'), 10: ('2Y2', 'out'), 11: ('2Y1', 'out'), 12: ('2Y0', 'out'),
                 13: ('2B', 'in'), 14: ('2A', 'in'), 15: ('/2G', 'in'), 16: ('VCC', 'vcc')},
     dict([(p, ('DEC', n, [2, 3], {'/G': 1})) for n, p in enumerate([4, 5, 6, 7])] +
          [(p, ('DEC', n, [14, 13], {'/G': 15})) for n, p in enumerate([12, 11, 10, 9])]))

_153 = ({1: ('/1G', 'in'), 2: ('B', 'in'), 3: ('1C3', 'in'), 4: ('1C2', 'in'), 5: ('1C1', 'in'), 6: ('1C0', 'in'), 7: ('1Y', 'out'),
         8: ('GND', 'gnd'), 9: ('2Y', 'out'), 10: ('2C0', 'in'), 11: ('2C1', 'in'), 12: ('2C2', 'in'), 13: ('2C3', 'in'), 14: ('A', 'in'),
         15: ('/2G', 'in'), 16: ('VCC', 'vcc')},
        {7: ('MUX4', [14, 2], [6, 5, 4, 3], 1), 9: ('MUX4', [14, 2], [10, 11, 12, 13], 15)})
part('74LS153', *_153, alias=('74S153',))

def mux157(kind):
    pins = {1: ('S', 'in'), 2: ('1A', 'in'), 3: ('1B', 'in'), 4: ('1Y', kind), 5: ('2A', 'in'), 6: ('2B', 'in'), 7: ('2Y', kind),
            8: ('GND', 'gnd'), 9: ('3Y', kind), 10: ('3B', 'in'), 11: ('3A', 'in'), 12: ('4Y', kind), 13: ('4B', 'in'), 14: ('4A', 'in'),
            15: ('/G', 'in'), 16: ('VCC', 'vcc')}
    funcs = {4: ('MUX2', 1, 2, 3), 7: ('MUX2', 1, 5, 6), 9: ('MUX2', 1, 11, 10), 12: ('MUX2', 1, 14, 13)}
    return pins, funcs
part('74LS157', *mux157('out'))
part('74LS257', *mux157('tri'))

part('74LS367', {1: ('/G1', 'in'), 2: ('A1', 'in'), 3: ('Y1', 'tri'), 4: ('A2', 'in'), 5: ('Y2', 'tri'), 6: ('A3', 'in'), 7: ('Y3', 'tri'),
                 8: ('GND', 'gnd'), 9: ('Y4', 'tri'), 10: ('A4', 'in'), 11: ('Y5', 'tri'), 12: ('A5', 'in'), 13: ('Y6', 'tri'),
                 14: ('A6', 'in'), 15: ('/G2', 'in'), 16: ('VCC', 'vcc')},
     {3: ('BUF', 2), 5: ('BUF', 4), 7: ('BUF', 6), 9: ('BUF', 10), 11: ('BUF', 12), 13: ('BUF', 14)})

_244_pairs = [(2, 18, '1A1', '1Y1'), (4, 16, '1A2', '1Y2'), (6, 14, '1A3', '1Y3'), (8, 12, '1A4', '1Y4'),
              (11, 9, '2A1', '2Y1'), (13, 7, '2A2', '2Y2'), (15, 5, '2A3', '2Y3'), (17, 3, '2A4', '2Y4')]
_p = {1: ('/1G', 'in'), 19: ('/2G', 'in'), 10: ('GND', 'gnd'), 20: ('VCC', 'vcc')}
for a, y, na, ny in _244_pairs:
    _p[a] = (na, 'in'); _p[y] = (ny, 'tri')
part('74LS244', _p, {y: ('BUF', a) for a, y, _, _ in _244_pairs})

_p = {1: ('DIR', 'in'), 19: ('/G', 'in'), 10: ('GND', 'gnd'), 20: ('VCC', 'vcc')}
for i in range(1, 9):
    _p[i + 1] = (f'A{i}', 'bi'); _p[19 - i] = (f'B{i}', 'bi')
part('74LS245', _p)

def octal_reg(name, ctl, clr):
    dq = [(3, 2), (4, 5), (7, 6), (8, 9), (13, 12), (14, 15), (17, 16), (18, 19)]
    kind = 'out' if clr else 'tri'
    pins = {10: ('GND', 'gnd'), 20: ('VCC', 'vcc'), 11: (ctl, 'in'), 1: ('/CLR' if clr else '/OE', 'in')}
    funcs = {}
    for i, (d, q) in enumerate(dq, 1):
        pins[d] = (f'{i}D', 'in'); pins[q] = (f'{i}Q', kind)
        funcs[q] = ('FF', f'{name} bit{i}', {'D': d, ctl: 11, ('/CLR' if clr else '/OE'): 1})
    return pins, funcs
part('74LS373', *octal_reg('latch', 'LE', False))
part('74LS374', *octal_reg('reg', 'CLK', False))
part('74LS273', *octal_reg('reg', 'CLK', True))

_174 = [(3, 2), (4, 5), (6, 7), (11, 10), (13, 12), (14, 15)]
_p = {1: ('/CLR', 'in'), 9: ('CLK', 'in'), 8: ('GND', 'gnd'), 16: ('VCC', 'vcc')}
_f = {}
for i, (d, q) in enumerate(_174, 1):
    _p[d] = (f'{i}D', 'in'); _p[q] = (f'{i}Q', 'out')
    _f[q] = ('FF', f'D-FF {i}', {'D': d, 'CLK': 9, '/CLR': 1})
part('74LS174', _p, _f)

_175 = [(4, 2, 3), (5, 7, 6), (12, 10, 11), (13, 15, 14)]
_p = {1: ('/CLR', 'in'), 9: ('CLK', 'in'), 8: ('GND', 'gnd'), 16: ('VCC', 'vcc')}
_f = {}
for i, (d, q, nq) in enumerate(_175, 1):
    _p[d] = (f'{i}D', 'in'); _p[q] = (f'{i}Q', 'out'); _p[nq] = (f'/{i}Q', 'out')
    _f[q] = ('FF', f'D-FF {i} Q', {'D': d, 'CLK': 9, '/CLR': 1})
    _f[nq] = ('FF', f'D-FF {i} /Q', {'D': d, 'CLK': 9, '/CLR': 1})
part('74LS175', _p, _f)

_195ctl = {'J': 2, '/K': 3, 'A': 4, 'B': 5, 'C': 6, 'D': 7, 'SH/LD': 9, 'CLK': 10, '/CLR': 1}
part('74LS195', {1: ('/CLR', 'in'), 2: ('J', 'in'), 3: ('/K', 'in'), 4: ('A', 'in'), 5: ('B', 'in'), 6: ('C', 'in'), 7: ('D', 'in'),
                 8: ('GND', 'gnd'), 9: ('SH/LD', 'in'), 10: ('CLK', 'in'), 11: ('/QD', 'out'), 12: ('QD', 'out'), 13: ('QC', 'out'),
                 14: ('QB', 'out'), 15: ('QA', 'out'), 16: ('VCC', 'vcc')},
     {p: ('FF', f'시프트 레지스터 {n}', _195ctl) for p, n in [(15, 'QA'), (14, 'QB'), (13, 'QC'), (12, 'QD'), (11, '/QD')]})

_259ctl = {'S0': 1, 'S1': 2, 'S2': 3, 'D': 13, '/G': 14, '/CLR': 15}
part('74LS259', {1: ('S0', 'in'), 2: ('S1', 'in'), 3: ('S2', 'in'), 4: ('Q0', 'out'), 5: ('Q1', 'out'), 6: ('Q2', 'out'), 7: ('Q3', 'out'),
                 8: ('GND', 'gnd'), 9: ('Q4', 'out'), 10: ('Q5', 'out'), 11: ('Q6', 'out'), 12: ('Q7', 'out'), 13: ('D', 'in'),
                 14: ('/G', 'in'), 15: ('/CLR', 'in'), 16: ('VCC', 'vcc')},
     {p: ('FF', f'어드레서블 래치 Q{n}', _259ctl) for n, p in enumerate([4, 5, 6, 7, 9, 10, 11, 12])})

_163ctl = {'CLK': 2, '/CLR': 1, '/LOAD': 9, 'ENP': 7, 'ENT': 10, 'A': 3, 'B': 4, 'C': 5, 'D': 6}
part('74LS163', {1: ('/CLR', 'in'), 2: ('CLK', 'in'), 3: ('A', 'in'), 4: ('B', 'in'), 5: ('C', 'in'), 6: ('D', 'in'), 7: ('ENP', 'in'),
                 8: ('GND', 'gnd'), 9: ('/LOAD', 'in'), 10: ('ENT', 'in'), 11: ('QD', 'out'), 12: ('QC', 'out'), 13: ('QB', 'out'),
                 14: ('QA', 'out'), 15: ('RCO', 'out'), 16: ('VCC', 'vcc')},
     {p: ('FF', f'카운터 {n}', _163ctl) for p, n in [(14, 'QA'), (13, 'QB'), (12, 'QC'), (11, 'QD'), (15, 'RCO')]})

_166ctl = {'SH/LD': 15, 'CLK': 7, 'CLK INH': 6, '/CLR': 9, 'SER': 1}
part('74LS166', {1: ('SER', 'in'), 2: ('A', 'in'), 3: ('B', 'in'), 4: ('C', 'in'), 5: ('D', 'in'), 6: ('CLK INH', 'in'), 7: ('CLK', 'in'),
                 8: ('GND', 'gnd'), 9: ('/CLR', 'in'), 10: ('E', 'in'), 11: ('F', 'in'), 12: ('G', 'in'), 13: ('QH', 'out'), 14: ('H', 'in'),
                 15: ('SH/LD', 'in'), 16: ('VCC', 'vcc')},
     {13: ('FF', '시프트 레지스터 QH', _166ctl)})

_323ctl = {'S0': 1, 'S1': 19, 'CP': 12, '/CLR': 9, 'DS0': 11, 'DS7': 18, '/OE1': 2, '/OE2': 3}
_p = {1: ('S0', 'in'), 2: ('/OE1', 'in'), 3: ('/OE2', 'in'), 8: ('Q0', 'out'), 9: ('/CLR', 'in'), 10: ('GND', 'gnd'), 11: ('DS0', 'in'),
      12: ('CP', 'in'), 17: ('Q7', 'out'), 18: ('DS7', 'in'), 19: ('S1', 'in'), 20: ('VCC', 'vcc')}
for io, p in [(6, 4), (4, 5), (2, 6), (0, 7), (1, 13), (3, 14), (5, 15), (7, 16)]:
    _p[p] = (f'I/O{io}', 'bi')
part('74LS323', _p, {8: ('FF', '시프트 레지스터 Q0', _323ctl), 17: ('FF', '시프트 레지스터 Q7', _323ctl)})

part('74LS393', {1: ('1A', 'in'), 2: ('1CLR', 'in'), 3: ('1QA', 'out'), 4: ('1QB', 'out'), 5: ('1QC', 'out'), 6: ('1QD', 'out'), 7: ('GND', 'gnd'),
                 8: ('2QD', 'out'), 9: ('2QC', 'out'), 10: ('2QB', 'out'), 11: ('2QA', 'out'), 12: ('2CLR', 'in'), 13: ('2A', 'in'), 14: ('VCC', 'vcc')},
     dict([(p, ('FF', f'카운터 1 {n}', {'CLK': 1, 'CLR': 2})) for p, n in [(3, 'QA'), (4, 'QB'), (5, 'QC'), (6, 'QD')]] +
          [(p, ('FF', f'카운터 2 {n}', {'CLK': 13, 'CLR': 12})) for p, n in [(11, 'QA'), (10, 'QB'), (9, 'QC'), (8, 'QD')]]))

_251 = {4: 'D0', 3: 'D1', 2: 'D2', 1: 'D3', 15: 'D4', 14: 'D5', 13: 'D6', 12: 'D7'}
_p = {p: (n, 'in') for p, n in _251.items()}
_p.update({5: ('Y', 'tri'), 6: ('W', 'tri'), 7: ('/G', 'in'), 8: ('GND', 'gnd'), 9: ('C', 'in'), 10: ('B', 'in'), 11: ('A', 'in'), 16: ('VCC', 'vcc')})
part('74LS251', _p, {5: ('MUX8', [11, 10, 9], [4, 3, 2, 1, 15, 14, 13, 12], 7, False),
                     6: ('MUX8', [11, 10, 9], [4, 3, 2, 1, 15, 14, 13, 12], 7, True)})

# 82S129 256x4 bipolar PROM (3-state). Bit names follow the dumps: O1 = bit0 ... O4 = bit3.
_p = {1: ('A6', 'in'), 2: ('A5', 'in'), 3: ('A4', 'in'), 4: ('A3', 'in'), 5: ('A0', 'in'), 6: ('A1', 'in'), 7: ('A2', 'in'), 8: ('GND', 'gnd'),
      9: ('O4', 'tri'), 10: ('O3', 'tri'), 11: ('O2', 'tri'), 12: ('O1', 'tri'), 13: ('/CE1', 'in'), 14: ('/CE2', 'in'), 15: ('A7', 'in'), 16: ('VCC', 'vcc')}
part('82S129', _p, {p: ('PROM', b, [5, 6, 7, 4, 3, 2, 1, 15]) for p, b in [(12, 0), (11, 1), (10, 2), (9, 3)]})
_p = {i: (f'O{i}', 'tri') for i in range(1, 8)}
_p.update({8: ('GND', 'gnd'), 9: ('O8', 'tri'), 10: ('A0', 'in'), 11: ('A1', 'in'), 12: ('A2', 'in'), 13: ('A3', 'in'), 14: ('A4', 'in'),
           15: ('/CE', 'in'), 16: ('VCC', 'vcc')})
part('82S123', _p, {p: ('PROM', b, [10, 11, 12, 13, 14]) for b, p in enumerate([1, 2, 3, 4, 5, 6, 7, 9])})

_p = {1: ('VPP', 'in'), 2: ('A12', 'in'), 3: ('A7', 'in'), 4: ('A6', 'in'), 5: ('A5', 'in'), 6: ('A4', 'in'), 7: ('A3', 'in'), 8: ('A2', 'in'),
      9: ('A1', 'in'), 10: ('A0', 'in'), 11: ('O0', 'tri'), 12: ('O1', 'tri'), 13: ('O2', 'tri'), 14: ('GND', 'gnd'), 15: ('O3', 'tri'),
      16: ('O4', 'tri'), 17: ('O5', 'tri'), 18: ('O6', 'tri'), 19: ('O7', 'tri'), 20: ('/CE', 'in'), 21: ('A10', 'in'), 22: ('/OE', 'in'),
      23: ('A11', 'in'), 24: ('A9', 'in'), 25: ('A8', 'in'), 26: ('NC', 'nc'), 27: ('/PGM', 'in'), 28: ('VCC', 'vcc')}
part('2764 EPROM', _p)
_p = {1: ('A7', 'in'), 2: ('A6', 'in'), 3: ('A5', 'in'), 4: ('A4', 'in'), 5: ('A3', 'in'), 6: ('A2', 'in'), 7: ('A1', 'in'), 8: ('A0', 'in'),
      9: ('D0', 'bi'), 10: ('D1', 'bi'), 11: ('D2', 'bi'), 12: ('GND', 'gnd'), 13: ('D3', 'bi'), 14: ('D4', 'bi'), 15: ('D5', 'bi'),
      16: ('D6', 'bi'), 17: ('D7', 'bi'), 18: ('/CS', 'in'), 19: ('A10', 'in'), 20: ('/OE', 'in'), 21: ('/WE', 'in'), 22: ('A9', 'in'),
      23: ('A8', 'in'), 24: ('VCC', 'vcc')}
part('HM6116LP-3', _p)
part('MN4164', {1: ('NC', 'nc'), 2: ('D', 'in'), 3: ('/WE', 'in'), 4: ('/RAS', 'in'), 5: ('A0', 'in'), 6: ('A2', 'in'), 7: ('A1', 'in'),
                8: ('VCC', 'vcc'), 9: ('A7', 'in'), 10: ('A5', 'in'), 11: ('A4', 'in'), 12: ('A3', 'in'), 13: ('A6', 'in'), 14: ('Q', 'tri'),
                15: ('/CAS', 'in'), 16: ('GND', 'gnd')})

_p = {1: ('VSS', 'gnd'), 2: ('RDY', 'in'), 3: ('Φ1', 'out'), 4: ('/IRQ', 'in'), 5: ('NC', 'nc'), 6: ('/NMI', 'in'), 7: ('SYNC', 'out'),
      8: ('VCC', 'vcc'), 21: ('VSS', 'gnd'), 34: ('R/W', 'out'), 35: ('NC', 'nc'), 36: ('NC', 'nc'), 37: ('Φ0', 'in'), 38: ('SO', 'in'),
      39: ('Φ2', 'out'), 40: ('/RES', 'in')}
for i in range(12):
    _p[9 + i] = (f'A{i}', 'out')
for i, p in enumerate([22, 23, 24, 25], 12):
    _p[p] = (f'A{i}', 'out')
for i in range(8):
    _p[33 - i] = (f'D{i}', 'bi')
part('UM6502', _p)

_p = {6: ('CLK', 'in'), 11: ('VCC', 'vcc'), 16: ('/INT', 'in'), 17: ('/NMI', 'in'), 18: ('/HALT', 'out'), 19: ('/MREQ', 'tri'),
      20: ('/IORQ', 'tri'), 21: ('/RD', 'tri'), 22: ('/WR', 'tri'), 23: ('/BUSACK', 'out'), 24: ('/WAIT', 'in'), 25: ('/BUSREQ', 'in'),
      26: ('/RESET', 'in'), 27: ('/M1', 'out'), 28: ('/RFSH', 'out'), 29: ('GND', 'gnd')}
for i, p in enumerate(range(30, 41)):
    _p[p] = (f'A{i}', 'tri')
for i, p in enumerate([1, 2, 3, 4, 5], 11):
    _p[p] = (f'A{i}', 'tri')
for i, p in enumerate([14, 15, 12, 8, 7, 9, 10, 13]):
    _p[p] = (f'D{i}', 'bi')
part('Z80A CPU', _p)

part('LM339', {1: ('OUT2', 'oc'), 2: ('OUT1', 'oc'), 3: ('VCC', 'vcc'), 4: ('IN1-', 'in'), 5: ('IN1+', 'in'), 6: ('IN2-', 'in'),
               7: ('IN2+', 'in'), 8: ('IN3-', 'in'), 9: ('IN3+', 'in'), 10: ('IN4-', 'in'), 11: ('IN4+', 'in'), 12: ('GND', 'gnd'),
               13: ('OUT4', 'oc'), 14: ('OUT3', 'oc')},
     {2: ('CMP', 5, 4), 1: ('CMP', 7, 6), 14: ('CMP', 9, 8), 13: ('CMP', 11, 10)})

SLOT = {1: '/I/O SELECT', 18: 'R/W', 19: 'SYNC', 20: '/I/O STROBE', 21: 'RDY', 22: '/DMA', 23: 'INT OUT', 24: 'DMA OUT', 25: '+5V',
        26: 'GND', 27: 'DMA IN', 28: 'INT IN', 29: '/NMI', 30: '/IRQ', 31: '/RES', 32: '/INH', 33: '-12V', 34: '-5V', 35: 'COLOR REF',
        36: '7M', 37: 'Q3', 38: 'Φ1', 39: 'USER 1', 40: 'Φ0', 41: '/DEVICE SELECT', 50: '+12V'}
for i in range(16):
    SLOT[2 + i] = f'A{i}'
for i in range(8):
    SLOT[49 - i] = f'D{i}'
SLOT_LOCAL = {1, 20, 41, 23, 24, 27, 28}

CPU_NAME = {'U30': '메인', 'U64': 'U64', 'U2': 'Z80'}

# ---------------------------------------------------------------------------
# loading
# ---------------------------------------------------------------------------
def load_bom():
    with open(os.path.join(ROOT, 'data', 'bom.csv'), encoding='utf-8') as f:
        return {r['ref']: r['part'] for r in csv.DictReader(f)}

def norm_node(ref, pin):
    ref, pin = ref.strip(), pin.strip()
    m = re.fullmatch(r'SL(\d)(?:-SL\d)?', ref)
    if m:
        p = int(pin) if pin.isdigit() else None
        if p is not None and p not in SLOT_LOCAL:
            return ('SL', pin)
        return (ref if '-' not in ref else 'SL', pin)
    return (ref, pin)

def is_conn(result):
    r = result.strip()
    return '도통' in r and '불통' not in r and '아님' not in r

def single(tok):
    tok = tok.strip()
    return bool(tok) and tok != '-' and not re.search(r'[,/–]| ', tok)

class Model:
    def __init__(self):
        self.bom = load_bom()
        self.parent = {}
        self.rows = []
        self.pending = []      # photo traces / vias, not used as connections
        self.measured = set()  # nodes that appear in a connection row
        with open(os.path.join(ROOT, 'data', 'netlist.csv'), encoding='utf-8') as f:
            for r in csv.DictReader(f):
                self.rows.append(r)
                fr, fp, tr, tp, res = r['from_ref'], r['from_pin'], r['to_ref'], r['to_pin'], r['result']
                if not (single(fp) and single(tp) and single(tr) and fr.strip() not in ('-', '')):
                    if '사진' in res or '비아' in res:
                        self.pending.append(r)
                    continue
                a, b = norm_node(fr, fp), norm_node(tr, tp)
                if is_conn(res):
                    self.union(a, b)
                    self.measured.update([a, b])
                    # rows filed under a power net name tie the pins to that rail
                    rail = {'GND': 'GND', '+5V': '+5V', 'VCC': '+5V'}.get(r['net'].strip())
                    if rail:
                        self.union(a, ('PWR', rail))
                elif '사진' in res or '비아' in res:
                    self.pending.append(r)
        # implicit power pins of every known IC
        for ref, p in self.bom.items():
            lib = LIB.get(p)
            if not lib:
                continue
            for pin, (name, kind) in lib['pins'].items():
                if kind == 'vcc':
                    self.union((ref, str(pin)), ('PWR', '+5V'))
                elif kind == 'gnd':
                    self.union((ref, str(pin)), ('PWR', 'GND'))
        self.union(('SL', '25'), ('PWR', '+5V'))
        self.union(('SL', '26'), ('PWR', 'GND'))
        self.nets = defaultdict(set)
        for n in list(self.parent):
            self.nets[self.find(n)].add(n)

    # union-find
    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb

    # pin info
    def pin_info(self, node):
        ref, pin = node
        if ref == 'PWR':
            return (pin, 'pwr')
        if ref == 'SL':
            return (SLOT.get(int(pin), '?') if pin.isdigit() else '?', 'slot')
        p = self.bom.get(ref)
        lib = LIB.get(p)
        if lib and pin.isdigit() and int(pin) in lib['pins']:
            return lib['pins'][int(pin)]
        return ('?', '?')

    def net_of(self, node):
        r = self.find(node)
        return r, self.nets.get(r, {node})

    def has_net(self, node):
        r = self.find(node)
        return len(self.nets.get(r, ())) > 1

    def drivers(self, members):
        return sorted([m for m in members if self.pin_info(m)[1] in ('out', 'tri', 'oc')], key=sort_key)

    def power(self, members):
        for m in members:
            if m[0] == 'PWR':
                return m[1]
        return None

    def net_label(self, root, members=None):
        members = members or self.nets.get(root, {root})
        pw = self.power(members)
        if pw:
            return pw
        for m in sorted(members, key=sort_key):
            ref, pin = m
            name, kind = self.pin_info(m)
            if ref in CPU_NAME and kind == 'out':
                return f'{CPU_NAME[ref]} {name}'
        for m in sorted(members, key=sort_key):
            if m[0] == 'SL':
                return f'슬롯 {m[1]} {self.pin_info(m)[0]}'
        drv = self.drivers(members)
        if drv:
            return pin_label(self, drv[0])
        return pin_label(self, sorted(members, key=sort_key)[0])

    # tracing
    def expr(self, node, depth=8, seen=None, seq=False):
        """Logic expression of the signal on node's net.

        Combinational parts are expanded; a flip-flop / register / counter is
        expanded one level (its control inputs) and any further flip-flop met
        inside that expansion is shown by its pin label only (seq=True)."""
        seen = set() if seen is None else seen
        root, members = self.net_of(node)
        if len(members) <= 1 and node not in self.measured:
            nm, _ = self.pin_info(node)
            return f'?{short(node)}({nm})'
        pw = self.power(members)
        if pw:
            return pw
        if root in seen:
            return f'↺{self.net_label(root, members)}'
        drv = self.drivers(members)
        if not drv:
            return f'[{self.net_label(root, members)}: 구동원 미확인]'
        parts = [self.expr_out(d, depth, seen | {root}, seq) for d in drv]
        return parts[0] if len(parts) == 1 else '(' + ' | '.join(parts) + ')'

    def expr_out(self, d, depth, seen, seq=False):
        ref, pin = d
        name, kind = self.pin_info(d)
        if ref in CPU_NAME:
            return f'{CPU_NAME[ref]} {name}'
        lib = LIB.get(self.bom.get(ref))
        f = lib['funcs'].get(int(pin)) if lib and pin.isdigit() else None
        lab = pin_label(self, d)
        if f is None or depth <= 0:
            return lab
        t = f[0]
        if t == 'FF' and seq:
            return lab
        sub = lambda p: self.expr((ref, str(p)), depth - 1, seen, seq or t == 'FF')
        if t in ('NAND', 'AND', 'OR', 'NOR'):
            return f'{t}(' + ', '.join(sub(p) for p in f[1]) + ')'
        if t == 'NOT':
            return f'NOT({sub(f[1][0])})'
        if t == 'BUF':
            return sub(f[1])
        if t == 'MUX2':
            _, s, a, b = f
            return f'MUX[{lab}](S={sub(s)}: S=0→{sub(a)}, S=1→{sub(b)})'
        if t == 'DEC':
            _, n, sel, en = f
            sels = ', '.join(f'{self.pin_info((ref, str(p)))[0]}={sub(p)}' for p in sel)
            ens = ', '.join(f'{k}={sub(p)}' for k, p in en.items())
            return f'DEC[{lab}](Low when 입력={n:0{len(sel)}b}; {sels}; {ens})'
        if t == 'MUX4':
            _, sel, data, g = f
            return f'MUX4[{lab}](A={sub(sel[0])}, B={sub(sel[1])}; /G={sub(g)})'
        if t == 'MUX8':
            return f'MUX8[{lab}]'
        if t == 'PROM':
            _, bit, ins = f
            known = ', '.join(f'A{i}={sub(p)}' for i, p in enumerate(ins) if self.has_net((ref, str(p))))
            return f'PROM[{lab} bit{bit}]({known or "입력 미측정"})'
        if t == 'CMP':
            return f'CMP[{lab}](+={sub(f[1])}, −={sub(f[2])})'
        if t == 'FF':
            _, desc, ctl = f
            inner = ', '.join(f'{k}={sub(p)}' for k, p in ctl.items())
            return f'{ref} {desc}{{{inner}}}'
        return lab

def sort_key(n):
    ref, pin = n
    m = re.match(r'([A-Za-z_]+)(\d*)', ref)
    return (m.group(1), int(m.group(2) or 0), int(pin) if pin.isdigit() else 999, pin)

def short(node):
    ref, pin = node
    if ref.startswith('U') and ref[1:].isdigit():
        return f'{ref[1:]}-{pin}'
    if ref == 'SL':
        return f'슬롯{pin}'
    return f'{ref}-{pin}'

def pin_label(m, node):
    name, _ = m.pin_info(node)
    return f'{short(node)}({name})'

# ---------------------------------------------------------------------------
# report
# ---------------------------------------------------------------------------
TRACE = [
    ('U64', '37', 'U64 클럭 (Φ0 입력)'),
    ('U75', '10', 'U75 클럭'),
    ('U75', '9', 'U75 SH/LD'),
    ('U47', '1', 'U68 주소 MUX SELECT'),
    ('U47', '11', 'U68 A8 (U64 쪽 입력)'),
    ('U62', '8', 'U62 Videx 스위치 /Q2'),
    ('U22', '12', 'U22 Y3 ($C3xx)'),
    ('U30', '37', '메인 CPU Φ0 입력'),
    ('U30', '40', '메인 CPU /RES'),
]

def build():
    return Model()

def net_rows(m):
    out = []
    for root, members in m.nets.items():
        if m.power(members) or len(members) < 2:
            continue
        if not any(n[0] in m.bom or n[0] == 'SL' for n in members):
            continue   # off-board (keyboard cable etc.), kept in netlist.csv only
        drv = m.drivers(members)
        kinds = [m.pin_info(d)[1] for d in drv]
        status = 'ok'
        if not drv:
            status = 'nodrv'
        elif kinds.count('out') > 1 or ('out' in kinds and len(drv) > 1):
            status = 'conflict'
        out.append((m.net_label(root, members), status, sorted(members, key=sort_key), drv))
    out.sort(key=lambda x: ({'conflict': 0, 'nodrv': 1, 'ok': 2}[x[1]], sort_key(x[2][0])))
    return out

def member_text(m, n):
    name, kind = m.pin_info(n)
    tag = {'out': '출력', 'tri': '출력(3상태)', 'oc': '출력(OC)', 'in': '입력', 'bi': '양방향', 'slot': '슬롯', 'pwr': '전원'}.get(kind, '?')
    part = m.bom.get(n[0], '')
    return f'{short(n)} {name} [{tag}]' + (f' {part}' if part and n[0] not in ('SL', 'PWR') else '')

def render_md(m):
    rows = net_rows(m)
    nod = [r for r in rows if r[1] == 'nodrv']
    con = [r for r in rows if r[1] == 'conflict']
    L = ['# 15. 측정된 넷과 논리식 (자동 생성)', '',
         '> 이 문서는 `python tools/netmodel.py`가 `data/netlist.csv`·`data/bom.csv`와 칩 핀 기능표로 만든 것입니다. 직접 고치지 말고 측정을 netlist에 적은 뒤 다시 생성하세요.',
         '', '표기: `72-2(1Y)` = U72 핀 2(기능 이름). `?75-2(J)` = 아직 어느 넷인지 모르는 핀. `[… 구동원 미확인]` = 그 선을 구동하는 출력을 아직 못 찾음.',
         '가정: 모든 IC의 VCC·GND 핀은 +5V·GND 넷에 있음(표준 핀배치), 슬롯 핀은 슬롯별 핀(1, 20, 23, 24, 27, 28, 41)을 빼고 네 슬롯 공통.', '',
         f'- 넷 {len(rows)}개 (전원 제외), 구동원 미확인 {len(nod)}개, 출력 충돌 {len(con)}개', '']
    L += ['## 1. 신호 추적', '']
    for ref, pin, title in TRACE:
        node = (ref, pin)
        L += [f'### {title} — {short(node)}', '', '```', m.expr(node), '```', '']
    L += ['## 2. 출력 충돌 (측정·기록 실수 의심)', '']
    L += [f'- **{lab}**: ' + ', '.join(member_text(m, n) for n in mem) for lab, _, mem, _ in con] or ['- 없음']
    L += ['', '## 3. 구동원 미확인 넷 (다음에 출력을 찾을 곳)', '']
    L += [f'- **{lab}**: ' + ', '.join(member_text(m, n) for n in mem) for lab, _, mem, _ in nod] or ['- 없음']
    L += ['', '## 4. 전체 넷', '', '| 넷 | 구동 | 연결된 핀 |', '| --- | --- | --- |']
    for lab, st, mem, drv in rows:
        d = ', '.join(short(x) for x in drv) or '—'
        L.append(f'| {lab} | {d} | ' + '<br>'.join(member_text(m, n) for n in mem) + ' |')
    if m.pending:
        L += ['', '## 5. 넷에 넣지 않은 기록 (사진 추적·비아, 측정 확인 필요)', '']
        for r in m.pending:
            L.append(f"- {r['from_ref']}-{r['from_pin']} ↔ {r['to_ref']}-{r['to_pin']}: {r['result']} — {r['note']}")
    return '\n'.join(L) + '\n'

def render_html(m=None):
    m = m or build()
    rows = net_rows(m)
    esc = html.escape
    nod = [r for r in rows if r[1] == 'nodrv']
    con = [r for r in rows if r[1] == 'conflict']
    h = [f'<p class="dim">도통 측정({len(m.rows)}줄)을 묶은 넷 {len(rows)}개. 구동원 미확인 {len(nod)}개, 출력 충돌 {len(con)}개. '
         '<code>tools/netmodel.py</code>가 칩 핀 기능표로 신호를 거슬러 올라가 논리식을 만듭니다. '
         '<span class="mono">?75-2(J)</span> = 아직 모르는 핀, <span class="mono">[… 구동원 미확인]</span> = 출력을 못 찾은 선.</p>']
    h.append('<div class="traces">')
    for ref, pin, title in TRACE:
        h.append(f'<div class="trace"><div class="tt">{esc(title)} <span class="mono dim">{esc(short((ref, pin)))}</span></div>'
                 f'<pre>{esc(m.expr((ref, pin)))}</pre></div>')
    h.append('</div>')
    def lst(items):
        if not items:
            return '<p class="dim">없음</p>'
        return '<ul class="netlist">' + ''.join(
            f'<li><b class="mono">{esc(lab)}</b> — ' + ', '.join(esc(member_text(m, n)) for n in mem) + '</li>' for lab, _, mem, _ in items) + '</ul>'
    h.append('<h3>출력 충돌 (측정·기록 실수 의심)</h3>' + lst(con))
    h.append('<h3>구동원 미확인 넷 (다음 측정 후보)</h3>' + lst(nod))
    body = ''.join(f'<tr><td class="mono">{esc(lab)}</td><td class="mono">{esc(", ".join(short(x) for x in drv) or "—")}</td>'
                   f'<td>{"<br>".join(esc(member_text(m, n)) for n in mem)}</td></tr>' for lab, _, mem, drv in rows)
    h.append('<details><summary>전체 넷 보기</summary><div class="tbl-wrap"><table class="bom"><thead><tr><th>넷</th><th>구동</th><th>연결된 핀</th></tr></thead>'
             f'<tbody>{body}</tbody></table></div></details>')
    return '\n'.join(h)

def parse_pin(s):
    s = s.strip()
    m = re.fullmatch(r'U?(\d+)-(\w+)', s)
    if not m:
        raise SystemExit(f'pin like 64-37 expected, got {s!r}')
    return (f'U{m.group(1)}', m.group(2))

if __name__ == '__main__':
    m = build()
    if len(sys.argv) >= 3 and sys.argv[1] == '--trace':
        for a in sys.argv[2:]:
            n = parse_pin(a)
            print(f'{short(n)}: {m.expr(n)}')
        sys.exit()
    out = os.path.join(ROOT, 'docs', '15-nets.md')
    with open(out, 'w', encoding='utf-8', newline='\n') as f:
        f.write(render_md(m))
    rows = net_rows(m)
    print(f'wrote {out}: {len(rows)} nets, '
          f'{sum(1 for r in rows if r[1] == "nodrv")} without driver, {sum(1 for r in rows if r[1] == "conflict")} conflicts')
