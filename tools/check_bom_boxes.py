# -*- coding: utf-8 -*-
"""Check data/bom.csv chip boxes against the pin pads in the front layout photo.

    python tools/check_bom_boxes.py            report
    python tools/check_bom_boxes.py --fix      also rewrite boxes that are off
    python tools/check_bom_boxes.py --draw OUT draw found pads and new boxes

Photo: photos/overview/front/202813_front-flat_layout-ref.jpg, BOM grid = x/2.09, y/2.11.
A DIP is found as two straight rows of pads, n/2 pads each, 0.1" pitch (~33.8 px),
0.3" or 0.6" apart (~99 / ~198 px), nearest the BOM box. The box written back is
the pad extent plus a margin. Chips where that fails are listed for an eye check.
"""
import csv
import os
import sys

import cv2
import numpy as np

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SX, SY = 2.09, 2.11
PITCH = 33.8
MARGIN = 8
WIDE = ('2764', 'HM6116', 'UM6502', 'Z80')         # 0.6" packages
PINS = {
    '2764': 28, 'HM6116': 24, 'UM6502': 40, 'Z80': 40, 'MN4164': 16, '82S129': 16, '82S123': 16,
    'LM339': 14, 'NE558': 16,
    '00': 14, '02': 14, '04': 14, '05': 14, '08': 14, '10': 14, '32': 14, '74': 14, '393': 14,
    '109': 16, '138': 16, '139': 16, '153': 16, '157': 16, '163': 16, '166': 16, '174': 16, '175': 16,
    '195': 16, '251': 16, '257': 16, '259': 16, '367': 16,
    '244': 20, '245': 20, '273': 20, '323': 20, '373': 20, '374': 20,
}


def pin_count(part):
    for k in ('2764', 'HM6116', 'UM6502', 'Z80', 'MN4164', '82S129', '82S123', 'LM339', 'NE558'):
        if k in part:
            return PINS[k]
    if part.startswith('74'):
        return PINS.get(''.join(ch for ch in part[2:] if ch.isdigit()))
    return None


def find_pads(img, vmin=165, smax=90):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    v, s = hsv[..., 2].astype(int), hsv[..., 1].astype(int)
    mask = ((v > vmin) & (s < smax)).astype(np.uint8)
    n, lab, st, cen = cv2.connectedComponentsWithStats(mask, 8)
    keep = []
    for i in range(1, n):
        x, y, w, h, a = st[i]
        if 20 <= a <= 600 and 4 <= w <= 34 and 4 <= h <= 34:
            keep.append((cen[i][0], cen[i][1], x, y, w, h))
    return np.array(keep, float)


def best_run(vals, n):
    """Indices of n values (sorted) forming the most regular 0.1" run."""
    order = np.argsort(vals)
    v = vals[order]
    best = None
    for i in range(0, len(v) - n + 1):
        seg = v[i:i + n]
        steps = np.diff(seg)
        err = np.abs(steps - PITCH).max() if n > 1 else 0
        if err < 6 and (best is None or err < best[0]):
            best = (err, order[i:i + n])
    return None if best is None else best[1]


def measure_grid(P, box, npins, wide):
    """Fallback for chips with hidden pads: pick the two pad rows, fit the 0.1" grid
    to the pads that are visible and take the n/2-pin window nearest the BOM box."""
    x0, y0, x1, y1 = box
    vertical = (y1 - y0) >= (x1 - x0)
    a, b = (0, 1) if vertical else (1, 0)
    lo, hi = (x0, x1) if vertical else (y0, y1)
    alo, ahi = (y0, y1) if vertical else (x0, x1)
    span = 198 if wide else 99
    half = npins // 2
    sel = P[(P[:, b] > alo - 60) & (P[:, b] < ahi + 60) & (P[:, a] > lo - 70) & (P[:, a] < hi + 70)]
    if len(sel) < 6:
        return None
    pos = np.round(sel[:, a] / 4) * 4
    u, cnt = np.unique(pos, return_counts=True)
    cols = [(c, n) for c, n in zip(u, cnt) if n >= 3]
    centre = (lo + hi) / 2
    best = None
    for c1, n1 in cols:
        for c2, n2 in cols:
            if c2 <= c1 or abs((c2 - c1) - span) > 14:
                continue
            score = abs((c1 + c2) / 2 - centre) - 2 * (n1 + n2)
            if best is None or score < best[0]:
                best = (score, c1, c2)
    if best is None:
        return None
    rows = [sel[np.abs(sel[:, a] - c) < 8] for c in best[1:]]
    along = np.concatenate([r[:, b] for r in rows])
    off = np.angle(np.mean(np.exp(2j * np.pi * along / PITCH))) / (2 * np.pi) * PITCH   # grid phase
    k = np.round((along - off) / PITCH)
    mid = (alo + ahi) / 2
    starts = range(int(k.min()) - half + 1, int(k.max()) + 1)
    def cost(s):
        inside = ((k >= s) & (k < s + half)).sum()
        return (-inside, abs(off + (s + (half - 1) / 2) * PITCH - mid))
    s = min(starts, key=cost)
    first, last = off + s * PITCH, off + (s + half - 1) * PITCH
    pw = np.median(np.concatenate([r[:, 4 if vertical else 5] for r in rows]))   # pad size across
    pl = np.median(np.concatenate([r[:, 5 if vertical else 4] for r in rows]))   # pad size along
    c1, c2 = (np.median(r[:, a]) for r in rows)
    if vertical:
        bb = (c1 - pw / 2 - MARGIN, first - pl / 2 - MARGIN, c2 + pw / 2 + MARGIN, last + pl / 2 + MARGIN)
    else:
        bb = (first - pl / 2 - MARGIN, c1 - pw / 2 - MARGIN, last + pl / 2 + MARGIN, c2 + pw / 2 + MARGIN)
    return bb, np.vstack(rows)


def measure(P, box, npins, wide):
    x0, y0, x1, y1 = box
    vertical = (y1 - y0) >= (x1 - x0)
    a, b = (0, 1) if vertical else (1, 0)      # a = across rows, b = along a row
    lo, hi = (x0, x1) if vertical else (y0, y1)
    alo, ahi = (y0, y1) if vertical else (x0, x1)
    span = 198 if wide else 99
    sel = P[(P[:, b] > alo - 60) & (P[:, b] < ahi + 60) & (P[:, a] > lo - 70) & (P[:, a] < hi + 70)]
    if len(sel) < npins:
        return None
    # candidate row positions = clusters of the across-coordinate
    xs = np.sort(sel[:, a])
    groups, cur = [], [xs[0]]
    for t in xs[1:]:
        if t - cur[-1] < 5:
            cur.append(t)
        else:
            groups.append(cur); cur = [t]
    groups.append(cur)
    cands = [np.median(g) for g in groups if len(g) >= npins // 2]
    centre = (lo + hi) / 2
    best = None
    for c1 in cands:
        for c2 in cands:
            if c2 <= c1 or abs((c2 - c1) - span) > 14:
                continue
            score = abs((c1 + c2) / 2 - centre)
            if best is None or score < best[0]:
                best = (score, c1, c2)
    if best is None:
        return None
    rows = []
    for c in best[1:]:
        r = sel[np.abs(sel[:, a] - c) < 7]
        idx = best_run(r[:, b], npins // 2)
        if idx is None:
            return None
        rows.append(r[idx])
    allp = np.vstack(rows)
    bx0 = (allp[:, 2]).min() - MARGIN
    by0 = (allp[:, 3]).min() - MARGIN
    bx1 = (allp[:, 2] + allp[:, 4]).max() + MARGIN
    by1 = (allp[:, 3] + allp[:, 5]).max() + MARGIN
    return (bx0, by0, bx1, by1), allp


def main():
    fix = '--fix' in sys.argv
    draw = sys.argv[sys.argv.index('--draw') + 1] if '--draw' in sys.argv else None
    img = cv2.imread(os.path.join(ROOT, 'photos/overview/front/202813_front-flat_layout-ref.jpg'))
    P = find_pads(img)
    P2 = find_pads(img, 135, 120)          # looser, for pads in shadow or dull sockets
    tol = 2
    path = os.path.join(ROOT, 'data/bom.csv')
    rows = list(csv.DictReader(open(path, encoding='utf-8')))
    fields = list(rows[0].keys())
    changed, failed = 0, []
    canvas = img.copy() if draw else None
    for r in rows:
        if not r['ref'].startswith('U'):
            continue
        b = [int(r[k]) for k in ('x0', 'y0', 'x1', 'y1')]
        box = (b[0] * SX, b[1] * SY, b[2] * SX, b[3] * SY)
        npins = pin_count(r['part'])
        wide = any(k in r['part'] for k in WIDE)
        m, how = None, ''
        if npins:
            for how, fn, pp in (('rows', measure, P), ('rows*', measure, P2), ('grid', measure_grid, P2)):
                m = fn(pp, box, npins, wide)
                if m:
                    break
        if not m:
            failed.append(r['ref'])
            print(f"{r['ref']:4} {r['part']:10} NOT FOUND  bom {b}")
            if canvas is not None:
                cv2.rectangle(canvas, (int(box[0]), int(box[1])), (int(box[2]), int(box[3])), (0, 0, 255), 3)
            continue
        (mx0, my0, mx1, my1), allp = m
        nb = [round(mx0 / SX), round(my0 / SY), round(mx1 / SX), round(my1 / SY)]
        d = max(abs(p - q) for p, q in zip(nb, b))
        print(f"{r['ref']:4} {r['part']:10} {how:5} bom {b}  pads {nb}  diff {d} {'OFF' if d > tol else 'ok'}")
        if canvas is not None:
            for p in allp:
                cv2.circle(canvas, (int(p[0]), int(p[1])), 5, (255, 255, 0), 2)
            cv2.rectangle(canvas, (int(mx0), int(my0)), (int(mx1), int(my1)), (0, 255, 0), 3)
            cv2.putText(canvas, r['ref'], (int(mx0), int(my0) - 4), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
        if fix and d > tol:
            r['x0'], r['y0'], r['x1'], r['y1'] = map(str, nb)
            changed += 1
    print('not found:', ' '.join(failed) or '-')
    if fix and changed:
        # rewrite only the four coordinate fields of each changed line, so rows with
        # extra columns and the original quoting stay untouched
        new = {r['ref']: (r['x0'], r['y0'], r['x1'], r['y1']) for r in rows}
        lines = open(path, encoding='utf-8', newline='').read().split('\n')
        for i, line in enumerate(lines):
            ref = line.split(',', 1)[0]
            if not ref.startswith('U') or ref not in new:
                continue
            fld = next(csv.reader([line]))
            if [fld[5], fld[6], fld[7], fld[8]] == list(new[ref]):
                continue
            old = ','.join(fld[5:9])
            lines[i] = line.replace(',' + old + ',', ',' + ','.join(new[ref]) + ',', 1)
        open(path, 'w', encoding='utf-8', newline='').write('\n'.join(lines))
        print('rewrote', changed, 'boxes')
    if canvas is not None:
        cv2.imwrite(draw, canvas)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
