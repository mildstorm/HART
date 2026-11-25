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
     {p: ('FF', f'SHIFT {n}', _195ctl) for p, n in [(15, 'QA'), (14, 'QB'), (13, 'QC'), (12, 'QD'), (11, '/QD')]})

_259ctl = {'S0': 1, 'S1': 2, 'S2': 3, 'D': 13, '/G': 14, '/CLR': 15}
part('74LS259', {1: ('S0', 'in'), 2: ('S1', 'in'), 3: ('S2', 'in'), 4: ('Q0', 'out'), 5: ('Q1', 'out'), 6: ('Q2', 'out'), 7: ('Q3', 'out'),
                 8: ('GND', 'gnd'), 9: ('Q4', 'out'), 10: ('Q5', 'out'), 11: ('Q6', 'out'), 12: ('Q7', 'out'), 13: ('D', 'in'),
                 14: ('/G', 'in'), 15: ('/CLR', 'in'), 16: ('VCC', 'vcc')},
     {p: ('FF', f'LATCH Q{n}', _259ctl) for n, p in enumerate([4, 5, 6, 7, 9, 10, 11, 12])})

_163ctl = {'CLK': 2, '/CLR': 1, '/LOAD': 9, 'ENP': 7, 'ENT': 10, 'A': 3, 'B': 4, 'C': 5, 'D': 6}
part('74LS163', {1: ('/CLR', 'in'), 2: ('CLK', 'in'), 3: ('A', 'in'), 4: ('B', 'in'), 5: ('C', 'in'), 6: ('D', 'in'), 7: ('ENP', 'in'),
                 8: ('GND', 'gnd'), 9: ('/LOAD', 'in'), 10: ('ENT', 'in'), 11: ('QD', 'out'), 12: ('QC', 'out'), 13: ('QB', 'out'),
                 14: ('QA', 'out'), 15: ('RCO', 'out'), 16: ('VCC', 'vcc')},
     {p: ('FF', f'COUNTER {n}', _163ctl) for p, n in [(14, 'QA'), (13, 'QB'), (12, 'QC'), (11, 'QD'), (15, 'RCO')]})

_166ctl = {'SH/LD': 15, 'CLK': 7, 'CLK INH': 6, '/CLR': 9, 'SER': 1}
part('74LS166', {1: ('SER', 'in'), 2: ('A', 'in'), 3: ('B', 'in'), 4: ('C', 'in'), 5: ('D', 'in'), 6: ('CLK INH', 'in'), 7: ('CLK', 'in'),
                 8: ('GND', 'gnd'), 9: ('/CLR', 'in'), 10: ('E', 'in'), 11: ('F', 'in'), 12: ('G', 'in'), 13: ('QH', 'out'), 14: ('H', 'in'),
                 15: ('SH/LD', 'in'), 16: ('VCC', 'vcc')},
     {13: ('FF', 'SHIFT QH', _166ctl)})

_323ctl = {'S0': 1, 'S1': 19, 'CP': 12, '/CLR': 9, 'DS0': 11, 'DS7': 18, '/OE1': 2, '/OE2': 3}
_p = {1: ('S0', 'in'), 2: ('/OE1', 'in'), 3: ('/OE2', 'in'), 8: ('Q0', 'out'), 9: ('/CLR', 'in'), 10: ('GND', 'gnd'), 11: ('DS0', 'in'),
      12: ('CP', 'in'), 17: ('Q7', 'out'), 18: ('DS7', 'in'), 19: ('S1', 'in'), 20: ('VCC', 'vcc')}
for io, p in [(6, 4), (4, 5), (2, 6), (0, 7), (1, 13), (3, 14), (5, 15), (7, 16)]:
    _p[p] = (f'I/O{io}', 'bi')
part('74LS323', _p, {8: ('FF', 'SHIFT Q0', _323ctl), 17: ('FF', 'SHIFT Q7', _323ctl)})

part('74LS393', {1: ('1A', 'in'), 2: ('1CLR', 'in'), 3: ('1QA', 'out'), 4: ('1QB', 'out'), 5: ('1QC', 'out'), 6: ('1QD', 'out'), 7: ('GND', 'gnd'),
                 8: ('2QD', 'out'), 9: ('2QC', 'out'), 10: ('2QB', 'out'), 11: ('2QA', 'out'), 12: ('2CLR', 'in'), 13: ('2A', 'in'), 14: ('VCC', 'vcc')},
     dict([(p, ('FF', f'COUNTER1 {n}', {'CLK': 1, 'CLR': 2})) for p, n in [(3, 'QA'), (4, 'QB'), (5, 'QC'), (6, 'QD')]] +
          [(p, ('FF', f'COUNTER2 {n}', {'CLK': 13, 'CLR': 12})) for p, n in [(11, 'QA'), (10, 'QB'), (9, 'QC'), (8, 'QD')]]))

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

GATE_SHAPES = ('AND', 'NAND', 'OR', 'NOR', 'NOT', 'BUF', 'CMP')

def unit_defs(part):
    """Split one part into drawable units: single gates, flip-flop groups,
    mux sections, decoders, PROMs.  Parts without a function table become one
    box.  Returns {key: {'type', 'title', 'ins': [...], 'outs': [...]}}."""
    lib = LIB.get(part)
    units = {}
    if not lib or not lib['funcs']:
        return None
    for p, f in sorted(lib['funcs'].items()):
        t = f[0]
        if t in ('NAND', 'AND', 'OR', 'NOR'):
            units[('G', p)] = {'type': t, 'title': '', 'ins': list(f[1]), 'outs': [p]}
        elif t == 'NOT':
            units[('G', p)] = {'type': 'NOT', 'title': '', 'ins': list(f[1]), 'outs': [p]}
        elif t == 'BUF':
            units[('G', p)] = {'type': 'BUF', 'title': '', 'ins': [f[1]], 'outs': [p]}
        elif t == 'CMP':
            units[('G', p)] = {'type': 'CMP', 'title': '', 'ins': [f[1], f[2]], 'outs': [p]}
        elif t == 'MUX2':
            units[('M', p)] = {'type': 'BOX', 'title': 'MUX', 'ins': [f[1], f[2], f[3]], 'outs': [p]}
        elif t == 'MUX4':
            units[('M', p)] = {'type': 'BOX', 'title': 'MUX4', 'ins': list(f[1]) + list(f[2]) + [f[3]], 'outs': [p]}
        elif t == 'MUX8':
            k = ('M8',)
            u = units.setdefault(k, {'type': 'BOX', 'title': 'MUX8', 'ins': list(f[1]) + list(f[2]) + [f[3]], 'outs': []})
            u['outs'].append(p)
        elif t == 'DEC':
            k = ('D', tuple(f[2]), tuple(f[3].values()))
            u = units.setdefault(k, {'type': 'BOX', 'title': 'DECODER', 'ins': list(f[2]) + list(f[3].values()), 'outs': []})
            u['outs'].append(p)
        elif t == 'PROM':
            u = units.setdefault(('P',), {'type': 'BOX', 'title': 'PROM', 'ins': list(f[2]), 'outs': []})
            u['outs'].append(p)
        elif t == 'FF':
            k = ('F', tuple(sorted(f[2].items())))
            title = re.sub(r'\s*/?Q\w*$|\s*bit\d+$|\s*[A-D]$', '', f[1].split(' Q')[0]).strip()
            u = units.setdefault(k, {'type': 'BOX', 'title': title, 'ins': list(f[2].values()), 'outs': []})
            u['outs'].append(p)
    return units

def _pinsort(s):
    return (not s.isdigit(), int(s) if s.isdigit() else 0, s)

def logic_units(m):
    """Every IC on the board split into its units, plus slot / passive boxes
    for measured pins outside any IC unit.  Returns (units, pin→unit, wires).

    Chips are placed even before any of their pins is measured, so the
    drawing shows the whole board and fills in as wires are found."""
    units, pin_unit = {}, {}
    with open(os.path.join(ROOT, 'data', 'bom.csv'), encoding='utf-8') as f:
        block = {r['ref']: r['block'] for r in csv.DictReader(f)}
    for ref in sorted(m.bom, key=lambda r: sort_key((r, '0'))):
        part = m.bom[ref]
        lib = LIB.get(part)
        if not ref.startswith('U'):
            continue
        if not lib:                     # no pin table yet (e.g. NE558): placeholder box
            units[ref] = {'id': ref, 'ref': ref, 'part': part, 'type': 'BOX', 'title': '핀 기능표 없음',
                          'ins': [], 'outs': [], 'whole': True, 'block': block.get(ref, '')}
            continue
        defs = unit_defs(part)
        if defs:
            for key, d in defs.items():
                uid = f'{ref}:{"/".join(map(str, key[:2] if key[0] != "F" else key[:1]))}:{min(d["outs"])}'
                units[uid] = {'id': uid, 'ref': ref, 'part': part, 'type': d['type'], 'title': d['title'],
                              'ins': [str(p) for p in dict.fromkeys(d['ins'])],
                              'outs': sorted({str(p) for p in d['outs']}, key=_pinsort),
                              'whole': False, 'block': block.get(ref, '')}
                for p in units[uid]['ins'] + units[uid]['outs']:
                    pin_unit[(ref, p)] = uid
        else:
            pins = [p for p, (nm, k) in sorted(lib['pins'].items()) if k not in ('vcc', 'gnd', 'nc')]
            units[ref] = {'id': ref, 'ref': ref, 'part': part, 'type': 'BOX', 'title': '',
                          'ins': [str(p) for p in pins if lib['pins'][p][1] == 'in'],
                          'outs': [str(p) for p in pins if lib['pins'][p][1] != 'in'],
                          'whole': True, 'block': block.get(ref, '')}
            for p in units[ref]['ins'] + units[ref]['outs']:
                pin_unit[(ref, p)] = ref
    # measured pins that are in no IC unit: slot, resistor, a chip's shared enable ...
    extra = set()
    for lab, st, mem, drv in net_rows(m):
        extra.update(n for n in mem if n[0] in m.bom or n[0] == 'SL')
    for n in sorted(extra, key=sort_key):
        ref, pin = n
        if n in pin_unit or m.pin_info(n)[1] in ('vcc', 'gnd'):
            continue
        uid = 'SL' if ref == 'SL' else f'{ref}:etc'
        u = units.setdefault(uid, {'id': uid, 'ref': ref, 'part': ('Apple 슬롯' if ref == 'SL' else m.bom.get(ref, '')),
                                   'type': 'BOX', 'title': ('' if ref == 'SL' or not ref.startswith('U') else '기타 핀'),
                                   'ins': [], 'outs': [], 'whole': True, 'block': block.get(ref, '확장')})
        name, kind = m.pin_info(n)
        (u['ins'] if kind in ('in', '?') else u['outs']).append(pin)
        pin_unit[n] = uid
    for u in units.values():
        if u['whole']:
            u['ins'] = sorted(dict.fromkeys(u['ins']), key=_pinsort)
            u['outs'] = sorted(dict.fromkeys(u['outs']), key=_pinsort)
    wires = []
    for lab, st, mem, drv in net_rows(m):
        board = [n for n in mem if n in pin_unit]
        if len(board) < 2 and not (board and st == 'nodrv'):
            continue
        src = [d for d in drv if d in pin_unit] or [n for n in board if m.pin_info(n)[1] == 'bi'][:1]
        wires.append({'net': lab, 'src': src[0] if src else None,
                      'dst': [n for n in board if not src or n != src[0]], 'nodrv': not src})
    return units, pin_unit, wires

def _shape(t, x, y, w, h):
    """SVG for a gate body occupying (x, y, w, h); output at x+w, y+h/2."""
    bub = t in ('NAND', 'NOR', 'NOT')
    bw = w - (7 if bub else 0)
    cy = y + h / 2
    if t in ('AND', 'NAND'):
        r = h / 2
        d = f'M{x},{y}H{x + bw - r}A{r},{r} 0 0 1 {x + bw - r},{y + h}H{x}Z'
    elif t in ('OR', 'NOR'):
        d = (f'M{x},{y}Q{x + bw * .35},{cy} {x},{y + h}Q{x + bw * .75},{y + h} {x + bw},{cy}'
             f'Q{x + bw * .75},{y} {x},{y}Z')
    else:  # NOT, BUF, CMP: triangle
        d = f'M{x},{y}L{x + bw},{cy}L{x},{y + h}Z'
    s = f'<path class="sym" d="{d}"/>'
    if bub:
        s += f'<circle class="sym" cx="{x + bw + 3.5}" cy="{cy}" r="3.5"/>'
    if t == 'CMP':
        s += f'<text class="pl" x="{x + 3}" y="{y + h * .32 + 3}">+</text><text class="pl" x="{x + 3}" y="{y + h * .72 + 3}">−</text>'
    return s

def logic_svg(m):
    """Gate-level logic diagram of the measured part of the board.

    Every chip is split into its gates / flip-flops / mux sections; each is
    drawn with its logic symbol (boxes for registers, decoders, PROMs, CPUs).
    Columns follow signal flow (longest path after cutting loops), rows are
    ordered by barycentre.  Wires are drawn first, symbols on top."""
    esc = html.escape
    units, pin_unit, wires = logic_units(m)
    succ = defaultdict(set)
    for w in wires:
        if w['src']:
            s = pin_unit[w['src']]
            for d in w['dst']:
                t = pin_unit[d]
                if s != t:
                    succ[s].add(t)
    # loop cut + longest-path layering
    order, state, back = [], {}, set()
    sys.setrecursionlimit(10000)
    def dfs(u):
        state[u] = 1
        for v in sorted(succ[u]):
            if state.get(v) == 1:
                back.add((u, v))
            elif v not in state:
                dfs(v)
        state[u] = 2
        order.append(u)
    wired = set()
    for w in wires:
        if w['src']:
            wired.add(pin_unit[w['src']])
        wired.update(pin_unit[d] for d in w['dst'])
    for u in sorted(wired, key=lambda x: (-len(succ[x]), x)):
        if u not in state:
            dfs(u)
    layer = {u: 0 for u in wired}
    for u in reversed(order):
        for v in succ[u]:
            if (u, v) not in back:
                layer[v] = max(layer[v], layer[u] + 1)
    L = max(layer.values()) + 1 if layer else 1
    cols = [sorted(u for u in wired if layer[u] == i) for i in range(L)]
    nb = defaultdict(set)
    for u in succ:
        for v in succ[u]:
            nb[u].add(v); nb[v].add(u)
    for it in range(10):
        pos = {u: i for c in cols for i, u in enumerate(c)}
        rng = range(1, L) if it % 2 == 0 else range(L - 2, -1, -1)
        for i in rng:
            refl = i - 1 if it % 2 == 0 else i + 1
            def bc(u):
                ns = [pos[v] for v in nb[u] if layer[v] == refl]
                return sum(ns) / len(ns) if ns else pos[u]
            cols[i].sort(key=bc)
    # unit geometry
    PH, VGAP = 14, 30
    geo = {}
    for uid, u in units.items():
        if u['type'] in GATE_SHAPES:
            n = max(len(u['ins']), 1)
            h = max(28, n * 13 + 4)
            geo[uid] = {'w': 44, 'h': h, 'top': 14, 'bottom': 14}
        else:
            rows = max(len(u['ins']), len(u['outs']), 1)
            geo[uid] = {'w': 150 if u['whole'] else 118, 'h': rows * PH + 30, 'top': 0, 'bottom': 0}
    colw = [max(geo[u]['w'] for u in c) if c else 60 for c in cols]
    # wire channels to the right of each column
    chan_nets = defaultdict(list)
    for w in wires:
        c = layer[pin_unit[w['src']]] if w['src'] else max(0, min(layer[pin_unit[d]] for d in w['dst']) - 1)
        w['col'] = c
        chan_nets[c].append(w)
    xcol, x = [], 40
    for i in range(L):
        xcol.append(x)
        x += colw[i] + 70 + 7 * len(chan_nets[i]) + 40
    totw = x + 40
    xy, toth = {}, 0
    for i, c in enumerate(cols):
        y = 60
        for u in c:
            y += geo[u]['top']
            xy[u] = (xcol[i] + (colw[i] - geo[u]['w']) / 2 + 30, y)
            y += geo[u]['h'] + geo[u]['bottom'] + VGAP
        toth = max(toth, y)
    totw = max(totw, 2600)
    toph = toth + 20                    # height of the wired part, used as the first view
    heads = [f'<text class="blk" x="40" y="36">측정으로 연결된 회로 (신호 흐름 순서, 왼쪽 → 오른쪽)</text>']
    # units with no wire yet: parked below, grouped by board block, one chip's units together
    idle = [u for u in units if u not in wired]
    blocks = defaultdict(list)
    for u in idle:
        blocks[units[u]['block'] or '기타'].append(u)
    y = toth + 80
    heads.append(f'<line class="sep" x1="20" x2="{totw - 20}" y1="{y - 40}" y2="{y - 40}"/>'
                 f'<text class="blk" x="40" y="{y - 14}">아직 연결을 측정하지 않은 칩 (기능 블록별)</text>')
    for bname in sorted(blocks):
        lst = sorted(blocks[bname], key=lambda u: (sort_key((units[u]['ref'], '0')), u))
        y += 24
        heads.append(f'<text class="blk2" x="40" y="{y}">{esc(bname)}</text>')
        y += 22
        x, rowh, prev = 60, 0, None
        for u in lst:
            g = geo[u]
            gap = 24 if units[u]['ref'] == prev else 56
            need = g['w'] + 60
            if x + need > totw - 40:
                x, y, rowh = 60, y + rowh + 40, 0
            elif prev is not None:
                x += gap
            xy[u] = (x + 18, y + g['top'])
            x += need - 24
            rowh = max(rowh, g['top'] + g['h'] + g['bottom'])
            prev = units[u]['ref']
        y += rowh + 30
    toth = y + 30
    # pin coordinates
    pxy = {}
    parts_svg = []
    for uid, u in units.items():
        g = geo[uid]
        x0, y0 = xy[uid]
        w, h = g['w'], g['h']
        ref = u['ref']
        s = [f'<g class="unit{"" if uid in wired else " idle"}" data-ref="{esc(ref)}"><title>{esc(ref)} {esc(u["part"])}</title>']
        if u['type'] in GATE_SHAPES:
            s.append(_shape(u['type'], x0, y0, w, h))
            n = len(u['ins'])
            for i, p in enumerate(u['ins']):
                py = y0 + h * (i + 1) / (n + 1)
                pxy[(ref, p)] = (x0 - 12, py)
                s.append(f'<path class="stub" d="M{x0 - 12},{py}H{x0 + (4 if u["type"] in ("OR", "NOR") else 0)}"/>')
                s.append(f'<text class="pn" x="{x0 - 12}" y="{py - 2}">{esc(p)}</text>')
            for p in u['outs']:
                pxy[(ref, p)] = (x0 + w + 12, y0 + h / 2)
                s.append(f'<path class="stub" d="M{x0 + w},{y0 + h / 2}H{x0 + w + 12}"/>')
                s.append(f'<text class="pn" x="{x0 + w + 12}" y="{y0 + h / 2 - 2}" text-anchor="end">{esc(p)}</text>')
            s.append(f'<text class="cap" x="{x0 + w / 2 - 4}" y="{y0 + h + 11}" text-anchor="middle">{esc(ref)}</text>')
        else:
            s.append(f'<rect class="sym" x="{x0}" y="{y0}" width="{w}" height="{h}" rx="2"/>')
            head = f'{ref} {u["title"]}'.strip() if not u['whole'] else ref
            s.append(f'<text class="cap b" x="{x0 + w / 2}" y="{y0 + 12}" text-anchor="middle">{esc(head)}</text>')
            s.append(f'<text class="cap" x="{x0 + w / 2}" y="{y0 + 23}" text-anchor="middle">{esc(u["part"])}</text>')
            for side, lst in (('W', u['ins']), ('E', u['outs'])):
                for i, p in enumerate(lst):
                    py = y0 + 30 + i * PH + 5
                    name, kind = m.pin_info((ref, p))
                    if side == 'W':
                        pxy[(ref, p)] = (x0 - 12, py)
                        s.append(f'<path class="stub" d="M{x0 - 12},{py}H{x0}"/>')
                        clk = name.startswith('CLK') or name in ('CP', 'LE')
                        if clk:
                            s.append(f'<path class="sym" d="M{x0},{py - 4}L{x0 + 6},{py}L{x0},{py + 4}"/>')
                        s.append(f'<text class="pl" x="{x0 + (9 if clk else 4)}" y="{py + 3}">{esc(name)}</text>')
                        s.append(f'<text class="pn" x="{x0 - 12}" y="{py - 2}">{esc(p)}</text>')
                    else:
                        pxy[(ref, p)] = (x0 + w + 12, py)
                        s.append(f'<path class="stub" d="M{x0 + w},{py}H{x0 + w + 12}"/>')
                        s.append(f'<text class="pl" x="{x0 + w - 4}" y="{py + 3}" text-anchor="end">{esc(name)}</text>')
                        s.append(f'<text class="pn" x="{x0 + w + 12}" y="{py - 2}" text-anchor="end">{esc(p)}</text>')
        # unmeasured inputs and power-tied pins
        for p in u['ins'] + u['outs']:
            n = (ref, p)
            if n not in pxy:
                continue
            px, py = pxy[n]
            r, mem = m.net_of(n)
            pw = m.power(mem)
            west = p in u['ins']
            if pw:
                s.append(f'<text class="pw" x="{px - 2 if west else px + 2}" y="{py + 3}" text-anchor="{"end" if west else "start"}">{pw}</text>')
            elif len(mem) <= 1 and n not in m.measured and uid in wired:
                s.append(f'<text class="unk" x="{px - 2 if west else px + 2}" y="{py + 3}" text-anchor="{"end" if west else "start"}">?</text>')
        s.append('</g>')
        parts_svg.append(''.join(s))
    # wires
    wsvg = []
    for c in range(L):
        for k, w in enumerate(chan_nets[c]):
            cx = xcol[c] + colw[c] + 30 + 30 + 7 * k
            pts = [pxy[d] for d in w['dst'] if d in pxy]
            if w['src']:
                sx, sy = pxy[w['src']]
                d = f'M{sx:.0f},{sy:.0f}H{cx:.0f}'
                ys = [sy]
            else:
                sy = sum(p[1] for p in pts) / len(pts)
                d = ''
                ys = []
                wsvg.append(f'<g class="junc"><circle cx="{cx:.0f}" cy="{sy:.0f}" r="6"/><text x="{cx:.0f}" y="{sy + 3:.0f}" text-anchor="middle">?</text></g>')
                ys.append(sy)
            for tx, ty in pts:
                ys.append(ty)
                d += f'M{cx:.0f},{ty:.0f}H{tx:.0f}'
            d += f'M{cx:.0f},{min(ys):.0f}V{max(ys):.0f}'
            cls = 'wire nodrv' if w['nodrv'] else 'wire'
            wsvg.insert(0, f'<path class="{cls}" data-net="{esc(w["net"])}" d="{d}"><title>{esc(w["net"])}</title></path>')
            if len(ys) > 2:
                wsvg.append(f'<circle class="dot" cx="{cx:.0f}" cy="{ys[0]:.0f}" r="2.5"/>')
    return (f'<svg id="logic" class="logic" viewBox="0 0 {totw:.0f} {toph:.0f}" data-w="{totw:.0f}" data-h="{toth:.0f}" data-top="{toph:.0f}" role="img" '
            f'aria-label="보드의 모든 칩을 게이트·플립플롭 단위로 놓고 측정으로 확인한 연결을 이은 논리 회로도">'
            f'<g class="heads">{"".join(heads)}</g><g class="wires">{"".join(wsvg)}</g><g class="units">{"".join(parts_svg)}</g></svg>')

LOGIC_VIEW = r'''
<div class="logic-wrap">
  <div class="logic-bar">
    <span id="logic-info" class="dim">선에 마우스를 올리면 넷 이름이 나오고 같은 넷이 강조됩니다. 휠로 확대, 끌어서 이동.</span>
    <span><button type="button" id="logic-wired">연결된 부분</button> <button type="button" id="logic-fit">전체 보기</button></span>
  </div>
  %%SVG%%
</div>
<script>
(function(){
  const svg=document.getElementById('logic'), info=document.getElementById('logic-info');
  const W=+svg.dataset.w, H=+svg.dataset.h, T=+svg.dataset.top;
  let vb=[0,0,W,T]; const set=()=>svg.setAttribute('viewBox',vb.join(' '));
  const fit=()=>{vb=[0,0,W,H];set();}; document.getElementById('logic-fit').onclick=fit;
  document.getElementById('logic-wired').onclick=()=>{vb=[0,0,W,T];set();};
  svg.addEventListener('mouseover',ev=>{const w=ev.target.closest('.wire'); if(!w) return;
    info.textContent='넷: '+w.dataset.net;
    svg.querySelectorAll('.wire').forEach(x=>x.classList.toggle('hi',x.dataset.net===w.dataset.net));});
  svg.addEventListener('wheel',ev=>{ev.preventDefault(); const r=svg.getBoundingClientRect();
    const s=Math.max(vb[2]/r.width, vb[3]/r.height), k=ev.deltaY>0?1.15:1/1.15;
    const ox=(r.width*s-vb[2])/2, oy=(r.height*s-vb[3])/2;
    const mx=vb[0]-ox+(ev.clientX-r.left)*s, my=vb[1]-oy+(ev.clientY-r.top)*s;
    vb=[mx-(mx-vb[0])*k, my-(my-vb[1])*k, vb[2]*k, vb[3]*k]; set();},{passive:false});
  let drag=null;
  svg.addEventListener('pointerdown',ev=>{drag=[ev.clientX,ev.clientY]; svg.setPointerCapture(ev.pointerId);});
  svg.addEventListener('pointermove',ev=>{if(!drag) return; const r=svg.getBoundingClientRect();
    const s=Math.max(vb[2]/r.width, vb[3]/r.height);
    vb[0]-=(ev.clientX-drag[0])*s; vb[1]-=(ev.clientY-drag[1])*s; drag=[ev.clientX,ev.clientY]; set();});
  svg.addEventListener('pointerup',()=>drag=null);
})();
</script>
'''

def render_html(m=None):
    m = m or build()
    rows = net_rows(m)
    esc = html.escape
    nod = [r for r in rows if r[1] == 'nodrv']
    con = [r for r in rows if r[1] == 'conflict']
    h = [f'<p class="dim">도통 측정({len(m.rows)}줄)을 묶은 넷 {len(rows)}개. 구동원 미확인 {len(nod)}개, 출력 충돌 {len(con)}개. '
         '<code>tools/netmodel.py</code>가 칩 핀 기능표로 신호를 거슬러 올라가 논리식을 만듭니다. '
         '<span class="mono">?75-2(J)</span> = 아직 모르는 핀, <span class="mono">[… 구동원 미확인]</span> = 출력을 못 찾은 선.</p>']
    h.append('<h3>통합 논리 회로도 (보드 전체 칩, 측정된 연결)</h3>'
             '<p class="dim">보드의 칩 85개를 모두 게이트·플립플롭 단위로 올려 두었습니다. 위쪽 = 측정으로 연결이 확인된 부분(신호 흐름 순서), '
             '아래쪽 = 아직 연결을 측정하지 않은 칩(흐리게, 기능 블록별). 측정이 늘면 다시 생성할 때 아래에서 위로 옮겨 가며 이어집니다. '
             '빨간 <b>?</b> = 연결된 게이트의 아직 모르는 입력, 빨간 점선 = 구동원을 못 찾은 선, <span class="mono">+5V</span>·<span class="mono">GND</span> = 전원에 묶인 핀.</p>')
    h.append(LOGIC_VIEW.replace('%%SVG%%', logic_svg(m)))
    h.append('<h3>신호 추적 (논리식)</h3>')
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
