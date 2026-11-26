# -*- coding: utf-8 -*-
"""Draw every data/bom.csv box on the front layout photo -> analysis/bom_boxes_check.jpg.

    python tools/draw_bom_boxes.py

Green = chips placed from their pin pads (tools/check_bom_boxes.py), orange = chips
checked by eye, magenta = connectors, slots, transistors and other parts.
"""
import csv
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SX, SY = 2.09, 2.11
BY_EYE = set('U2 U3 U25 U30 U39 U40 U41 U45 U46 U52 U53 U54 U55 U63 U64 U65 U67 U70 U85'.split())

im = Image.open(os.path.join(ROOT, 'photos/overview/front/202813_front-flat_layout-ref.jpg')).convert('RGB')
d = ImageDraw.Draw(im)
f = ImageFont.truetype('C:/Windows/Fonts/malgunbd.ttf', 24)
for r in csv.reader(open(os.path.join(ROOT, 'data/bom.csv'), encoding='utf-8')):
    if not r or r[0] == 'ref':
        continue
    try:
        x0, y0, x1, y1 = (int(v) for v in r[5:9])
    except ValueError:
        continue
    b = (x0 * SX, y0 * SY, x1 * SX, y1 * SY)
    if not r[0].startswith('U'):
        col = (220, 0, 220)
    else:
        col = (255, 160, 0) if r[0] in BY_EYE else (0, 230, 0)
    d.rectangle(b, outline=col, width=4)
    d.text((b[0] + 3, b[1] + 2), r[0], font=f, fill=(255, 255, 0), stroke_width=2, stroke_fill=(0, 0, 0))
d.text((20, 3290), '초록 = 다리 위치로 맞춘 칩, 주황 = 눈으로 확인한 칩, 자주 = 커넥터·슬롯·트랜지스터·기타',
       font=f, fill=(255, 255, 255), stroke_width=3, stroke_fill=(0, 0, 0))
out = os.path.join(ROOT, 'analysis/bom_boxes_check.jpg')
im.resize((im.width // 2, im.height // 2)).save(out, quality=88)
print('wrote', out)
