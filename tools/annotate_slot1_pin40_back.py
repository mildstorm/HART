"""뒷면 전체 사진에서 슬롯1 핀 40과 U30 핀 37 납땜점 위치.
사용: python tools/annotate_slot1_pin40_back.py photos/overview/back/203240_back-flat_registration-ref.jpg analysis/slot1_pin40_back.jpg
뒷면은 좌우 반전: 슬롯1 = 오른쪽 끝 슬롯(J1 바로 왼쪽). 앞면 왼쪽 줄(26-50)이 뒷면 오른쪽 줄.
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

X0, Y0, X1, Y1 = 1450, 0, 2121, 1800
sc = 0.62
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
W, H = im.width + 700, max(im.height + 120, 1000)
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

d.text((20, 12), "슬롯1 핀 40 · U30 핀 37 뒷면 납땜점 (뒷면 전체 사진 203240)", font=font(28, True), fill=BLK)
d.text((20, 54), "뒷면은 좌우 반전. 슬롯1 = 오른쪽 끝 슬롯(전원 커넥터 J1 바로 왼쪽).", font=font(18), fill=BLK)

# slot1 columns on back: right col = 26..50 (top->bottom), left col = 25..1
colR, colL, y26, pitch = 1930, 1860, 95, 34.4
for k, n in ((0, 26), (14, 40), (24, 50)):
    c = M(colR, y26 + k*pitch)
    ring(c, 9 if n != 40 else 12, RED if n == 40 else ORG, 4 if n != 40 else 5)
    label((c[0] + 60, c[1]), {26: "26 (GND)", 40: "40 (Φ0)", 50: "50 (+12V)"}[n], 15,
          fg=WHITE if n == 40 else BLK, bg=RED if n == 40 else YEL, anchor="lm")
c = M(colL, y26)
label((c[0] - 30, c[1]), "25", 14, anchor="rm")
label(M(1895, 1040), "슬롯1", 18, fg=WHITE, bg=ORG)

# U30 back: top row right end = pin 40, pin 37 = 4th from right
p37 = M(1789, 1425)
ring(p37, 12, BLUE, 5)
label((p37[0] - 20, p37[1] - 34), "U30 핀 37", 15, fg=WHITE, bg=BLUE)
label(M(1895, 1395), "40", 13)
label(M(1895, 1665), "1", 13)

# suggested jumper
s40 = M(colR, y26 + 14*pitch)
n = 18
for i in range(n):
    if i % 2 == 0:
        a = (s40[0] + (p37[0]-s40[0])*i/n, s40[1] + (p37[1]-s40[1])*i/n)
        b = (s40[0] + (p37[0]-s40[0])*(i+1)/n, s40[1] + (p37[1]-s40[1])*(i+1)/n)
        d.line((a, b), fill=YEL, width=4)

tx, ty = im.width + 50, 110
for t, b, c in [
    ("판독 결과", True, BLK),
    ("• 슬롯1 핀 40 뒷면 납땜점에는 뒷면 선이 없음", False, BLK),
    ("  → 핀 40의 연결(U78, 다른 슬롯)은 모두 앞면,", False, BLK),
    ("    슬롯 커넥터 몸통 아래로 지나감", False, BLK),
    ("  → 사진으로는 더 따라갈 수 없음", False, BLK),
    ("• U30 핀 37도 뒷면은 비아까지만, 나머지는 앞면", False, BLK),
    ("  → 두 선이 끊긴 곳은 앞면 쪽일 가능성", False, BLK),
    ("", False, BLK),
    ("뒷면에서 찾는 법", True, BLK),
    ("• 슬롯1: J1(5핀) 바로 왼쪽의 긴 두 줄", False, BLK),
    ("• 오른쪽 줄 위에서 15번째 = 핀 40", False, RED),
    ("  (오른쪽 줄 맨 위 26 = GND, 맨 아래 50 = +12V)", False, BLK),
    ("• U30: 위 줄 오른쪽에서 4번째 = 핀 37", False, BLUE),
    ("", False, BLK),
    ("확인 (전원 끄고, 도통)", True, BLK),
    ("1. 앞면 슬롯1 핀 40 ↔ 뒷면 빨간 원 → 삐", False, BLK),
    ("2. 앞면 U30 핀 37 ↔ 뒷면 파란 원 → 삐", False, BLK),
    ("   (위치 확인용. 삐 소리 나야 맞는 점)", False, BLK),
    ("", False, BLK),
    ("노란 점선 = 점퍼선을 단다면 이 두 납땜점 사이", True, (170, 140, 0)),
    ("  길이 약 6–7cm. 100Ω 저항 직렬 권장.", False, BLK),
    ("  옆 납땜점(핀 39·41, U30 핀 36·38)에", False, BLK),
    ("  납이 붙지 않게.", False, BLK),
]:
    d.text((tx, ty), t, font=font(18, b), fill=c); ty += 30

cv.save(OUT, quality=92)
print(cv.size, ty)
