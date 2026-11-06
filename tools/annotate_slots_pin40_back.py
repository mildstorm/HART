"""뒷면 전체 사진에서 슬롯 1–4 핀 40 납땜점과 뒷면 연결.
사용: python tools/annotate_slots_pin40_back.py photos/overview/back/203240_back-flat_registration-ref.jpg analysis/slots_pin40_back.jpg
뒷면 좌우 반전: 오른쪽부터 슬롯1, 2, 3, 4. 각 슬롯 오른쪽 줄 = 26(위)–50(아래), 핀 40 = 위에서 15번째.
좌표는 원본(2121x3369) 기준 (2026-11-07 판독).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN, ORG = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,160,60), (255,130,0)

X0, Y0, X1, Y1 = 1150, 30, 2121, 960
sc = 0.95
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
W, H = im.width + 40, im.height + 560
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
ax, ay = 20, 100
cv.paste(im, (ax, ay))
M = lambda x, y: (ax + (x-X0)*sc, ay + (y-Y0)*sc)
def label(xy, text, sz=16, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)
def ring(c, r, col, w=4):
    d.ellipse((c[0]-r, c[1]-r, c[0]+r, c[1]+r), outline=col, width=w)

d.text((20, 12), "슬롯 1–4 핀 40 뒷면 납땜점 (뒷면 전체 사진 203240)", font=font(28, True), fill=BLK)
d.text((20, 56), "뒷면은 좌우 반전: 오른쪽부터 슬롯1, 2, 3, 4. 각 슬롯 오른쪽 줄 위에서 15번째 = 핀 40", font=font(18), fill=BLK)

slots = {1: (1930, 575), 2: (1720, 582), 3: (1515, 582), 4: (1305, 582)}
for n, (x, y) in slots.items():
    c = M(x, y)
    ring(c, 13, RED, 5)
    label(M(x - 35, 75), f"슬롯{n}", 17, fg=WHITE, bg=ORG)
    label((c[0] + 4, c[1] + 34), "40", 14, fg=WHITE, bg=RED)
via = M(1282, 570)
ring(via, 10, BLUE, 4)
label((via[0] - 40, via[1] - 30), "비아", 14, fg=WHITE, bg=BLUE)

ty = ay + im.height + 20
for t, b, c in [
    ("판독 결과 (사진 확대, 확실성 중간)", True, BLK),
    ("• 슬롯 1·2·3 핀 40: 뒷면 납땜점에 연결된 뒷면 선 없음", False, BLK),
    ("• 슬롯 4 핀 40: 짧은 뒷면 선이 바로 옆 비아(파란 원)로 가서 앞면으로 넘어감", False, BLK),
    ("• 결론: 슬롯끼리 묶는 핀 40 선(Φ0)은 앞면, 슬롯 커넥터 사이의 가로 선 다발로 지나감", False, BLK),
    ("   → 뒷면 사진으로는 이 선이 U30 핀 37 쪽으로 어떻게 가는지 더 따라갈 수 없음", False, RED),
    ("", False, BLK),
    ("측정으로 좁히기 (전원 끄고, 도통)", True, BLK),
    ("1. 슬롯1 핀 40 ↔ 슬롯 2, 3, 4 핀 40 : 모두 삐 (안 나는 슬롯이 있으면 그 사이가 끊김)", False, BLK),
    ("2. U30 핀 37 ↔ 슬롯 2, 3, 4 핀 40, ↔ 파란 원 비아 : 하나라도 삐면 그쪽으로 이어진 것", False, BLK),
    ("3. 모두 안 되면 → U30 핀 37 앞면 선이 중간에 끊긴 것. 점퍼선(뒷면 슬롯1 핀 40 ↔ U30 핀 37)으로 대신", False, BLK),
]:
    d.text((20, ty), t, font=font(18, b), fill=c); ty += 32

cv.save(OUT, quality=92)
print(cv.size, ty)
