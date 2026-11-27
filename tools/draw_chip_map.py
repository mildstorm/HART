# -*- coding: utf-8 -*-
"""Re-insertion map: every chip with its ref, part and notch side, on the front photo.

    python tools/draw_chip_map.py   ->  analysis/chip_placement_map.jpg, docs/16-chip-placement.md

Notch side follows the board rule checked chip by chip (tools/make_pins.py):
a chip lying across has its notch on the left (pin 1 bottom-left), a chip
standing up has its notch at the bottom (pin 1 bottom-right).
"""
import csv
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SX, SY = 2.09, 2.11
K = 0.62
FONT = 'C:/Windows/Fonts/malgunbd.ttf'

rows = [r for r in csv.reader(open(os.path.join(ROOT, 'data/bom.csv'), encoding='utf-8'))
        if r and r[0].startswith('U')]
src = Image.open(os.path.join(ROOT, 'photos/overview/front/202813_front-flat_layout-ref.jpg')).convert('RGB')
im = src.resize((int(src.width * K), int(src.height * K)), Image.LANCZOS)
im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), 0.35)
top = 90
cv = Image.new('RGB', (im.width, im.height + top), (255, 255, 255))
cv.paste(im, (0, top))
d = ImageDraw.Draw(cv)
f1, f2 = ImageFont.truetype(FONT, 17), ImageFont.truetype(FONT, 12)
d.text((12, 8), 'HART 칩 다시 꽂기 배치도 — 노치(반원 홈) 방향과 1번 핀', font=ImageFont.truetype(FONT, 26), fill=(0, 0, 0))
d.text((12, 46), '노란 반원 = 노치 쪽, 빨간 점 = 1번 핀. 가로 칩은 노치 왼쪽, 세로 칩은 노치 아래 (모든 칩 같음, 2026-11-27 칩마다 확인).',
       font=ImageFont.truetype(FONT, 16), fill=(0, 0, 0))

lines = ['# 16. 칩 배치와 방향 (다시 꽂기용)', '',
         '앞면, 슬롯이 위쪽 기준. 가로 칩은 노치 왼쪽·1번 핀 왼쪽 아래, 세로 칩은 노치 아래·1번 핀 오른쪽 아래. '
         '2026-11-27 칩마다 글씨 방향으로 확인했고 예외 없음(U17·U84는 글씨가 없어 미확인). '
         '그림: [`analysis/chip_placement_map.jpg`](../analysis/chip_placement_map.jpg), 핀별 좌표: [`data/pins.csv`](../data/pins.csv).', '',
         '| 자리 | 부품 | 표기 | 놓인 방향 | 노치 | 같은 부품이 있는 자리 (서로 바꿔 꽂지 말 것) |',
         '| --- | --- | --- | --- | --- | --- |']
same = {}
for r in rows:
    same.setdefault(r[1], []).append(r[0])

for r in rows:
    x0, y0, x1, y1 = (int(v) for v in r[5:9])
    X0, Y0, X1, Y1 = x0 * SX * K, y0 * SY * K + top, x1 * SX * K, y1 * SY * K + top
    across = (X1 - X0) > (Y1 - Y0)
    d.rectangle((X0, Y0, X1, Y1), outline=(0, 230, 0), width=2)
    if across:                           # notch on the left edge, pin 1 bottom-left
        cy = (Y0 + Y1) / 2
        d.pieslice((X0 - 10, cy - 10, X0 + 10, cy + 10), 270, 90, fill=(255, 220, 0))
        p1 = (X0 + 6, Y1 - 6)
    else:                                # notch on the bottom edge, pin 1 bottom-right
        cx = (X0 + X1) / 2
        d.pieslice((cx - 10, Y1 - 10, cx + 10, Y1 + 10), 180, 360, fill=(255, 220, 0))
        p1 = (X1 - 6, Y1 - 6)
    d.ellipse((p1[0] - 4, p1[1] - 4, p1[0] + 4, p1[1] + 4), fill=(255, 0, 0))
    cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
    for t, f, dy in ((r[0], f1, -9), (r[1].replace(' EPROM', '').replace('-3', ''), f2, 9)):
        d.text((cx, cy + dy), t, font=f, fill=(255, 255, 0), anchor='mm', stroke_width=2, stroke_fill=(0, 0, 0))
    others = [o for o in same[r[1]] if o != r[0]]
    lines.append(f"| {r[0]} | {r[1]} | {r[2]} | {'가로' if across else '세로'} | {'왼쪽' if across else '아래'} | "
                 f"{', '.join(others) if others else '-'} |")

cv.save(os.path.join(ROOT, 'analysis/chip_placement_map.jpg'), quality=90)
lines += ['', '같은 부품끼리는 전기적으로 바꿔 꽂아도 되는 경우가 많지만, **PROM(82S129·82S123)과 롬(2764)은 내용이 달라 반드시 제자리**에 꽂아야 합니다.', '']
open(os.path.join(ROOT, 'docs/16-chip-placement.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('wrote map and docs/16, chips:', len(rows))
