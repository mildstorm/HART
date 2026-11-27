# -*- coding: utf-8 -*-
"""U50 (82S129, label "1") as logic: minimise its four outputs from the dump
and write a GAL16V8 source (galasm .pld) for the replacement.

    python tools/u50_logic.py            print equations, write gal/U50.pld,
                                         check them against all 256 entries

The dump rom/U50_1.bin is in standard 82S129 order: address bit k = input Ak,
data bits 0-3 = O1-O4. Pins: A0=5 A1=6 A2=7 A3=4 A4=3 A5=2 A6=1 A7=15,
O1=12 O2=11 O3=10 O4=9, /CE1=13 /CE2=14 (tied to GND on the board).
"""
import itertools
import os

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
DUMP = os.path.join(ROOT, 'rom/U50_1.bin')

# The board signals on each input (docs/03, docs/13): for the comments.
SIGNALS = {
    0: 'A13 (buffered, U33-7)',
    1: 'A12 (buffered slot A12, U33-9)',
    2: 'U49 2Q (LC write enable)',
    3: 'A0 (U33-3)',
    4: 'R/W (buffered, U33-11)',
    5: 'A1 (U33-13)',
    6: 'NAND(A15,A14) (U34-3)',
    7: 'U49 1Q (LC pre-write)',
}


def minimise(ones, n=8):
    """Quine-McCluskey prime implicants + a greedy cover. Terms are (value, mask)
    with mask bits set where the variable is 'don't care'."""
    terms = {(m, 0) for m in ones}
    primes = set()
    while terms:
        merged, used = set(), set()
        tl = sorted(terms)
        for a, b in itertools.combinations(tl, 2):
            if a[1] == b[1]:
                diff = a[0] ^ b[0]
                if diff and diff & (diff - 1) == 0:
                    merged.add((a[0] & ~diff, a[1] | diff))
                    used.add(a)
                    used.add(b)
        primes |= terms - used
        terms = merged
    covered, cover = set(), []
    def covers(p, m):
        return (m & ~p[1]) == p[0]
    while covered != set(ones):
        best = max(primes, key=lambda p: (len([m for m in ones if covers(p, m) and m not in covered]),
                                          bin(p[1]).count('1')))
        cover.append(best)
        covered |= {m for m in ones if covers(best, m)}
    return cover


def term_str(p, names):
    parts = []
    for k in range(8):
        if not (p[1] >> k) & 1:
            parts.append(names[k] if (p[0] >> k) & 1 else '/' + names[k])
    return ' * '.join(parts) if parts else 'VCC'


def main():
    data = open(DUMP, 'rb').read()
    names = ['A0', 'A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7']
    eqs = {}
    for o in range(4):
        ones = [a for a in range(256) if (data[a] >> o) & 1]
        cov = minimise(ones)
        eqs[o] = cov
        print('O%d = %s   (%d terms)' % (o + 1, '\n     + '.join(term_str(p, names) for p in cov), len(cov)))
    # check
    for a in range(256):
        for o in range(4):
            v = any((a & ~p[1]) == p[0] for p in eqs[o])
            assert v == bool((data[a] >> o) & 1), (a, o)
    assert all(len(c) <= 8 for c in eqs.values()), 'more than 8 product terms'
    print('all 256 entries match; every output fits in 8 product terms')

    # GAL16V8 pins: inputs A0-A7 on 2-9, outputs O1-O4 on 12-15, 1 and 11 unused.
    pin_in = {'A0': 2, 'A1': 3, 'A2': 4, 'A3': 5, 'A4': 6, 'A5': 7, 'A6': 8, 'A7': 9}
    pin_out = {1: 12, 2: 13, 3: 14, 4: 15}
    pins = ['NC'] * 21
    for n, p in pin_in.items():
        pins[p] = n
    for o, p in pin_out.items():
        pins[p] = 'O%d' % o
    pins[10], pins[20], pins[1], pins[11] = 'GND', 'VCC', 'NC', 'NC'
    os.makedirs(os.path.join(ROOT, 'gal'), exist_ok=True)
    lines = ['GAL16V8', 'U50HART', '',
             ' '.join(pins[1:11]),
             ' '.join(pins[11:21]), '']
    for o in range(4):
        terms = [term_str(p, names) for p in eqs[o]]
        lines.append('O%d = %s' % (o + 1, '\n   + '.join(terms)))
        lines.append('')
    lines += ['DESCRIPTION', '',
              'Zung Won HART U50 (82S129 label 1) replacement, from rom/U50_1.bin (tools/u50_logic.py).',
              'Inputs A0-A7 = 82S129 pins 5 6 7 4 3 2 1 15, outputs O1-O4 = pins 12 11 10 9.',
              'Board signals: ' + ', '.join('A%d %s' % (k, s) for k, s in SIGNALS.items()) + '.', '']
    path = os.path.join(ROOT, 'gal/U50.pld')
    open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    print('wrote', path)


if __name__ == '__main__':
    main()
