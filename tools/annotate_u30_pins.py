"""U30 (메인 UM6502) 40핀 번호와 측정 핀 그림.
사용: python tools/annotate_u30_pins.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/u30_pins.jpg
앞면 기준 사진 좌표. 노치 왼쪽 → 아래 줄 왼쪽→오른쪽 1–20, 위 줄 오른쪽→왼쪽 21–40.
칩 다리 x: 핀 1·40 = 207, 간격 34.47 (사진상 다리 위치).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN, ORG, GRAY = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,150,60), (230,120,0), (120,120,120)

X0, Y0, X1, Y1 = 150, 1380, 940, 1690
sc = 1.9
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
W, H = im.width + 40, im.height + 560
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
ax, ay = 20, 150
cv.paste(im, (ax, ay))
M = lambda x, y: (ax + (x-X0)*sc, ay + (y-Y0)*sc)
def label(xy, text, sz=15, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-3, bb[1]-2, bb[2]+3, bb[3]+2), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 10), "U30 (메인 CPU UM6502) 핀 번호 — 앞면", font=font(30, True), fill=BLK)
d.text((20, 52), "반달 홈(노치) 왼쪽. 아래 줄: 왼쪽부터 1→20.  위 줄: 오른쪽부터 21→40 (왼쪽 끝이 40).", font=font(18), fill=BLK)
d.text((20, 80), "검정 프로브는 핀 1(GND)에 대면 가까워서 편함 (U72 핀 7과 같은 GND).", font=font(18, True), fill=GRN)

hl = {1: ("GND (검정)", GRN), 8: ("+5V", ORG), 25: ("A15", RED), 7: ("SYNC", BLUE), 39: ("Φ2 출력", BLUE), 37: ("Φ0 입력", GRAY), 40: ("RES", GRAY)}
x1, P, yt, yb = 207, 34.47, 1437, 1642
for n in range(1, 41):
    if n <= 20:
        x, y, off = x1 + (n-1)*P, yb, 30
    else:
        x, y, off = x1 + (40-n)*P, yt, -30
    cx, cy = M(x, y)
    if n in hl:
        t, c = hl[n]
        d.ellipse((cx-13, cy-13, cx+13, cy+13), outline=c, width=4)
        label((cx, cy + off), str(n), 15, fg=WHITE, bg=c)
        label((cx, cy + off*2.1), t, 14, fg=c)
    else:
        label((cx, cy + off), str(n), 12)

ty = ay + im.height + 30
for t, b, c in [
    ("측정 (전원 켜고, 검정 프로브 = 핀 1 고정)", True, BLK),
    ("1. DC 전압 모드, 빨강 → 핀 25 (A15): 위 줄 오른쪽 끝에서 5번째.  3V 이상이면 CPU가 ROM 실행 중 (예전 0.7V)", False, RED),
    ("2. DC 전압 모드, 빨강 → 핀 7 (SYNC): 아래 줄 왼쪽에서 7번째.  0V·5V가 아닌 중간값(약 0.5–1.5V)이면 CPU가 명령을 읽는 중", False, BLUE),
    ("3. Hz 모드, 빨강 → 핀 39 (Φ2 출력): 위 줄 왼쪽에서 2번째.  약 1MHz면 CPU 클럭 회로 동작 (값이 안정될 때까지 기다리기)", False, BLUE),
    ("4. DC 전압 모드, 빨강 → 핀 8 (+5V): 아래 줄 왼쪽에서 8번째.  4.75–5.25V 확인", False, ORG),
    ("", False, BLK),
    ("주의: 핀 간격이 좁음. 빨강 프로브 끝을 칩 다리 위쪽(칩 몸통 가까이)에 수직으로 대고 옆 다리에 닿지 않게.", True, RED),
    ("핀 1은 아래 줄 맨 왼쪽(노치 아래). 집게가 있으면 핀 1 대신 U72 핀 7이나 슬롯 핀 26(GND)에 물려도 됨.", False, BLK),
]:
    d.text((20, ty), t, font=font(18, b), fill=c); ty += 32
cv.save(OUT, quality=92)
print(cv.size, ty)
