# -*- coding: utf-8 -*-
"""Chip-pull plan for the slot A12 short hunt (2026-11-27) -> analysis/a12_pull_plan.jpg

Grey = already pulled, red = group 1 (pull now), orange = group 2 (pull with group 1),
blue = group 3 (only if the short stays). Boxes from data/bom.csv.
"""
import csv
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
SX, SY, K = 2.09, 2.11, 0.62
FONT = 'C:/Windows/Fonts/malgunbd.ttf'

DONE = 'U30 U64 U2 U33 U5 U4 U36 U43 U44 U56 U57'.split()
G1 = 'U6 U7 U1 U31 U32 U29'.split()
G2 = 'U38 U50 U51 U22 U23 U24 U21 U35 U77 U45 U46'.split()
G3 = 'U34 U48 U60 U49 U61 U62 U39 U40 U41 U42 U52 U53 U54 U55'.split()
GREY, RED, ORG, BLU = (150, 150, 150), (235, 30, 30), (255, 150, 0), (40, 120, 255)

bom = {r[0]: r for r in csv.reader(open(os.path.join(ROOT, 'data/bom.csv'), encoding='utf-8')) if r}
src = Image.open(os.path.join(ROOT, 'photos/overview/front/202813_front-flat_layout-ref.jpg')).convert('RGB')
im = src.resize((int(src.width * K), int(src.height * K)), Image.LANCZOS)
im = Image.blend(im, Image.new('RGB', im.size, (0, 0, 0)), 0.3)
top, side = 120, 430
cv = Image.new('RGB', (im.width + side, im.height + top), (255, 255, 255))
cv.paste(im, (0, top))
d = ImageDraw.Draw(cv)
f = lambda s: ImageFont.truetype(FONT, s)

d.text((12, 8), '슬롯 A12 단락 찾기 — 뽑을 칩 (소켓 칩만, 납땜된 칩은 건너뜀)', font=f(26), fill=(0, 0, 0))
d.text((12, 48), '매번 U33 소켓 9번 ↔ GND(U30 소켓 1번) 저항. 0.8Ω에서 수 kΩ 이상으로 바뀌면 풀린 것.', font=f(17), fill=(0, 0, 0))
d.text((12, 76), '추천: 빨강·주황을 한 번에 뽑고 측정 → 풀리면 절반씩 다시 꽂아 범인 찾기.', font=f(17), fill=(0, 0, 0))


def box(ref, col, w=4, fill=None):
    x0, y0, x1, y1 = (int(v) for v in bom[ref][5:9])
    b = (x0 * SX * K, y0 * SY * K + top, x1 * SX * K, y1 * SY * K + top)
    if fill:
        ov = Image.new('RGBA', cv.size, (0, 0, 0, 0))
        ImageDraw.Draw(ov).rectangle(b, fill=fill)
        cv.paste(Image.alpha_composite(cv.convert('RGBA'), ov).convert('RGB'))
    dd = ImageDraw.Draw(cv)
    dd.rectangle(b, outline=col, width=w)
    dd.text(((b[0] + b[2]) / 2, (b[1] + b[3]) / 2), ref, font=f(17), fill=(255, 255, 255),
            anchor='mm', stroke_width=3, stroke_fill=col)


for r in DONE:
    box(r, GREY, 3, fill=(120, 120, 120, 150))
for r in G3:
    box(r, BLU)
for r in G2:
    box(r, ORG)
for r in G1:
    box(r, RED)

d = ImageDraw.Draw(cv)
x, y = im.width + 18, top + 10
for t, c, s in [
    ('회색 = 이미 뺌 (11개)', GREY, 19), ('  ' + ' '.join(DONE[:6]), (0, 0, 0), 15), ('  ' + ' '.join(DONE[6:]), (0, 0, 0), 15), ('', 0, 10),
    ('빨강 = 1군, 지금 뺌 (6개)', RED, 19), ('  ' + ' '.join(G1), (0, 0, 0), 15),
    ('  Z80 버스 칩(U6·U7·U1),', (0, 0, 0), 15), ('  메인 버스(U31·U32·U29)', (0, 0, 0), 15), ('', 0, 10),
    ('주황 = 2군, 1군과 함께 뺌 (11개)', ORG, 19), ('  ' + ' '.join(G2[:6]), (0, 0, 0), 15), ('  ' + ' '.join(G2[6:]), (0, 0, 0), 15),
    ('  디코드 PROM·디코더·롬', (0, 0, 0), 15), ('  A12를 입력으로 받을 수 있어 유력', (0, 0, 0), 15), ('', 0, 10),
    ('파랑 = 3군, 그래도 안 풀릴 때만 (14개)', BLU, 19), ('  게이트 U34·U48·U60', (0, 0, 0), 15), ('  래치 U49·U61·U62', (0, 0, 0), 15),
    ('  DRAM U39–U42·U52–U55', (0, 0, 0), 15), ('', 0, 10),
    ('주의', (0, 0, 0), 19), ('· 뺄 때 다리가 접혀 있지 않은지 확인', (0, 0, 0), 15),
    ('· 같은 부품 많음: 자리 번호 적어 보관', (0, 0, 0), 15), ('· PROM·롬은 반드시 제자리', (0, 0, 0), 15),
    ('· 다시 꽂기: docs/16, chip_placement_map', (0, 0, 0), 15),
    ('· 다 빼도 단락이면 기판·슬롯 커넥터 쪽', (0, 0, 0), 15),
]:
    if t:
        d.text((x, y), t, font=f(s), fill=c)
    y += s + 10
out = os.path.join(ROOT, 'analysis/a12_pull_plan.jpg')
cv.save(out, quality=90)
print('wrote', out, cv.size)
