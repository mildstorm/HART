# -*- coding: utf-8 -*-
"""Front layout picture for the U33 pin 9 (slot A12) short hunt, 2026-11-26/27.

    python tools/annotate_a12_short.py   ->  analysis/a12_short_chips.jpg

Chip boxes come from data/bom.csv (1000x1600 grid) scaled onto the front layout
photo; slot pin 14 positions are read on the back scan and moved to the front
with data/front_back_registration.json.
"""
import csv
import json
import os

from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..')
FRONT = os.path.join(ROOT, 'photos/overview/front/202813_front-flat_layout-ref.jpg')
OUT = os.path.join(ROOT, 'analysis/a12_short_chips.jpg')
SX, SY = 2.09, 2.11            # bom grid -> front photo pixels (fit on U33, U49, U72)
K = 0.42                       # output scale

F, FB = 'C:/Windows/Fonts/malgun.ttf', 'C:/Windows/Fonts/malgunbd.ttf'


def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)


RED, ORG, GRY, BLU, BLK, WHT = (230, 20, 20), (255, 140, 0), (120, 120, 120), (0, 90, 230), (0, 0, 0), (255, 255, 255)

bom = {d['ref']: d for d in csv.DictReader(open(os.path.join(ROOT, 'data/bom.csv'), encoding='utf-8'))}
reg = json.load(open(os.path.join(ROOT, 'data/front_back_registration.json'), encoding='utf-8'))


def poly(c, x, y):
    x /= 1000; y /= 1000
    t = [1, x, y, x * x, x * y, y * y, x ** 3, x * x * y, x * y * y, y ** 3]
    return sum(a[0] * b for a, b in zip(c, t)), sum(a[1] * b for a, b in zip(c, t))


def b2f(x, y):
    return poly(reg['back_to_front'], x, y)


src = Image.open(FRONT).convert('RGB')
im = src.resize((int(src.width * K), int(src.height * K)), Image.LANCZOS)
PAD = 470
cv = Image.new('RGB', (im.width + PAD, im.height + 120), WHT)
cv.paste(im, (0, 110))
d = ImageDraw.Draw(cv)


def P(x, y):                    # front photo px -> canvas
    return x * K, 110 + y * K


def box(ref, col, tag, width=5):
    b = bom[ref]
    x0, y0 = P(int(b['x0']) * SX, int(b['y0']) * SY)
    x1, y1 = P(int(b['x1']) * SX, int(b['y1']) * SY)
    d.rectangle((x0, y0, x1, y1), outline=col, width=width)
    f = font(16, True)
    t = f'{tag} {ref}'
    bb = d.textbbox((x0, y0 - 2), t, font=f, anchor='lb')
    d.rectangle((bb[0] - 3, bb[1] - 2, bb[2] + 3, bb[3] + 2), fill=col)
    d.text((x0, y0 - 2), t, font=f, fill=WHT, anchor='lb')


d.text((14, 10), '슬롯 A12 단락(U33 핀 9 ↔ GND 0.7Ω) 찾기 — 뽑을 칩과 다시 꽂는 순서', font=font(26, True), fill=BLK)
d.text((14, 50), '앞면, 슬롯이 위쪽. 전원 끄고 작업. 매번 U33 소켓 9번 ↔ U30 핀 1(GND) 저항을 잰다.', font=font(17), fill=BLK)
d.text((14, 76), '빨강 = A12 선 후보(먼저), 주황 = 가능성 낮은 후보, 파랑 S1-14 = 슬롯1 핀 14 위치(뒷면 정합으로 옮김, 추정)', font=font(17), fill=BLK)

MAG = (200, 0, 200)
for ref, tag in (('J1', '전원'), ('J2', 'FDD'), ('J3', 'FDD'), ('J9', '빈 소켓'), ('J10', '키보드')):
    box(ref, MAG, tag, width=4)

box('U33', RED, '0 (이미 뺌)')
box('U5', RED, '1')
box('U4', RED, '2')
box('U36', RED, '3')
for i, r in enumerate(('U43', 'U44', 'U56', 'U57'), 4):
    box(r, ORG, str(i))

# slot pin 14 on the back: left column of each slot, 12th from the top (pin 25 at top)
for n, xb in ((1, 1855), (2, 1648), (3, 1442), (4, 1250)):
    fx, fy = b2f(xb, 470)
    cx, cy = P(fx, fy)
    d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), outline=BLU, width=4)
    f = font(14, True)
    t = f'S{n}-14'
    bb = d.textbbox((cx, cy + 14), t, font=f, anchor='mt')
    d.rectangle((bb[0] - 2, bb[1] - 1, bb[2] + 2, bb[3] + 1), fill=WHT)
    d.text((cx, cy + 14), t, font=f, fill=BLU, anchor='mt')

x = im.width + 60
y = 130
for t, b, c in [
    ('순서', True, BLK),
    ('1. 소켓 칩 전부 사진(방향) 찍기', False, BLK),
    ('2. 슬롯 카드·소켓 칩 모두 뽑기', False, BLK),
    ('3. 소켓 9번 ↔ GND 측정', False, BLK),
    ('   0.7Ω 그대로 → 기판·커넥터', False, RED),
    ('   (슬롯 핀14 저항 비교로)', False, RED),
    ('   커짐 → 칩이 원인, 4번으로', False, BLU),
    ('4. 번호 순서로 하나씩 꽂으며', False, BLK),
    ('   매번 측정', False, BLK),
    ('   0.7Ω으로 돌아온 칩 = 원인', False, BLU),
    ('', False, BLK),
    ('후보 이유', True, BLK),
    ('U33: 이 선의 출발(버퍼 A12)', False, BLK),
    ('U5: Z80 변환 PROM, O4 =', False, BLK),
    ('    Z80 쪽 A12 출력', False, BLK),
    ('U4: Z80 버스 버퍼 74LS244', False, BLK),
    ('U36: 롬 디코드 PROM(A12 입력)', False, BLK),
    ('U43·U44·U56·U57: DRAM 주소', False, BLK),
    ('    MUX. 이 선이면 RAM이 깨져', False, BLK),
    ('    가능성 낮음', False, BLK),
    ('', False, BLK),
    ('나머지 소켓 칩은 이 다음에', False, GRY),
    ('아무 순서로 꽂으며 확인', False, GRY),
    ('82S129·82S123 자리 혼동 주의', False, RED),
    ('', False, BLK),
    ('자주색 = 커넥터 (참고용)', False, MAG),
    ('키보드(J10)·FDD(J2·J3) 케이블도', False, BLK),
    ('뽑은 상태에서 측정', False, BLK),
]:
    d.text((x, y), t, font=font(17, b), fill=c)
    y += 27

os.makedirs(os.path.dirname(OUT), exist_ok=True)
cv.save(OUT, quality=90)
print('wrote', OUT, cv.size)
