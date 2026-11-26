# -*- coding: utf-8 -*-
"""Per-pin coordinates of every DIP chip -> data/pins.csv.

    python tools/make_pins.py               write data/pins.csv
    python tools/make_pins.py --draw REFS   also draw those chips' pins on the front
                                            photo and the back scan (analysis/pins_check_*.jpg)

Columns: ref, pin, front_x, front_y (px in photos/overview/front/202813_front-flat_layout-ref.jpg),
back_x, back_y (px in photos/overview/back/203240_back-flat_registration-ref.jpg), snapped
(1 = the pin sits on a pad found in the photo, 0 = placed on the 0.1" grid only).

Pin numbering follows the board rule (docs/02, docs/05): a chip lying across
(wider than tall) has its notch on the left, pin 1 at the bottom-left, pins
counting left to right on the bottom row and right to left on the top row; a
chip standing up has its notch at the bottom, pin 1 at the bottom-right, pins
counting upward on the right row and downward on the left row. Chip boxes come
from data/bom.csv (tools/check_bom_boxes.py fits them to the pad rows).
"""
import csv
import json
import os
import sys

import cv2
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check_bom_boxes as cb  # noqa: E402

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FRONT = os.path.join(ROOT, 'photos/overview/front/202813_front-flat_layout-ref.jpg')
BACK = os.path.join(ROOT, 'photos/overview/back/203240_back-flat_registration-ref.jpg')
REG = json.load(open(os.path.join(ROOT, 'data/front_back_registration.json'), encoding='utf-8'))


def f2b(x, y):
    c = REG['front_to_back']
    x, y = x / 1000, y / 1000
    t = [1, x, y, x * x, x * y, y * y, x ** 3, x * x * y, x * y * y, y ** 3]
    return sum(a[0] * b for a, b in zip(c, t)), sum(a[1] * b for a, b in zip(c, t))


def chip_pins(P, box, npins, wide):
    """Return [(pin, x, y, snapped)] for one chip box in front-photo pixels."""
    x0, y0, x1, y1 = box
    vertical = (y1 - y0) >= (x1 - x0)
    half = npins // 2
    inset = cb.MARGIN + 7                      # box edge -> pad centre (pads ~14 px wide)
    if vertical:
        rows = (x1 - inset, x0 + inset)        # right row first (pins 1..half)
        along0, along1 = y0 + cb.MARGIN + 10, y1 - cb.MARGIN - 10
    else:
        rows = (y1 - inset, y0 + inset)        # bottom row first
        along0, along1 = x0 + cb.MARGIN + 10, x1 - cb.MARGIN - 10
    step = (along1 - along0) / (half - 1)
    out = []
    for side, across in enumerate(rows):
        for i in range(half):
            if vertical:
                # right row: pin 1 at the bottom going up; left row: pin half+1 at the top going down
                along = along1 - i * step if side == 0 else along0 + i * step
                x, y = across, along
            else:
                # bottom row: pin 1 at the left going right; top row: pin half+1 at the right going left
                along = along0 + i * step if side == 0 else along1 - i * step
                x, y = along, across
            pin = i + 1 + side * half
            near = P[(np.abs(P[:, 0] - x) < 9) & (np.abs(P[:, 1] - y) < 9)]
            snapped = 0
            if len(near):
                j = np.argmin((near[:, 0] - x) ** 2 + (near[:, 1] - y) ** 2)
                x, y, snapped = near[j, 0], near[j, 1], 1
            out.append((pin, x, y, snapped))
    return out


def main():
    img = cv2.imread(FRONT)
    P = np.vstack([cb.find_pads(img), cb.find_pads(img, 135, 120)])
    rows = []
    for r in csv.reader(open(os.path.join(ROOT, 'data/bom.csv'), encoding='utf-8')):
        if not r or not r[0].startswith('U'):
            continue
        npins = cb.pin_count(r[1])
        if not npins:
            continue
        b = [int(v) for v in r[5:9]]
        box = (b[0] * cb.SX, b[1] * cb.SY, b[2] * cb.SX, b[3] * cb.SY)
        wide = any(k in r[1] for k in cb.WIDE)
        for pin, x, y, s in chip_pins(P, box, npins, wide):
            bx, by = f2b(x, y)
            rows.append((r[0], pin, round(x, 1), round(y, 1), round(bx, 1), round(by, 1), s))
    out = os.path.join(ROOT, 'data/pins.csv')
    with open(out, 'w', encoding='utf-8', newline='') as f:
        w = csv.writer(f, lineterminator='\n')
        w.writerow(['ref', 'pin', 'front_x', 'front_y', 'back_x', 'back_y', 'snapped'])
        w.writerows(rows)
    n = len(rows)
    print('wrote', out, n, 'pins,', sum(r[6] for r in rows), 'on a found pad')

    if '--draw' in sys.argv:
        refs = sys.argv[sys.argv.index('--draw') + 1].split(',')
        fr = cv2.imread(FRONT)
        bk = cv2.imread(BACK)
        for ref, pin, x, y, bx, by, s in rows:
            if ref not in refs:
                continue
            col = (0, 255, 255) if pin == 1 else (255, 255, 0)
            for im, (u, v), sc in ((fr, (x, y), 1.0), (bk, (bx, by), 1.0)):
                cv2.circle(im, (int(u), int(v)), 9 if pin == 1 else 6, col, 2)
                cv2.putText(im, str(pin), (int(u) + 7, int(v) - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.45, col, 1)
        cv2.imwrite(os.path.join(ROOT, 'analysis/pins_check_front.jpg'), fr)
        cv2.imwrite(os.path.join(ROOT, 'analysis/pins_check_back.jpg'), bk)


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()
