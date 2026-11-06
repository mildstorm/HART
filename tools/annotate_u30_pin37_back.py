"""뒷면 사진에서 U30 핀 37 패턴 경로 표시.
사용: python tools/annotate_u30_pin37_back.py photos/zoom/back/225321_back-U30-area_left-edge.jpg analysis/u30_pin37_back.jpg
뒷면은 앞면과 좌우 반전: 위 줄 오른쪽 끝 = 핀 40, 아래 줄 오른쪽 끝 = 핀 1.
좌표는 원본(4000x3000) 기준, 사진 확대로 판독 (2026-11-07).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230)

X0, Y0, X1, Y1 = 1950, 950, 3150, 2500
sc = 0.8
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
W, H = im.width + 640, im.height + 120
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
ax, ay = 20, 100
cv.paste(im, (ax, ay))
M = lambda x, y: (ax + (x-X0)*sc, ay + (y-Y0)*sc)
def label(xy, text, sz=18, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "U30 핀 37 뒷면 패턴 (뒷면, 좌우 반전)", font=font(30, True), fill=BLK)
d.text((20, 56), "사진 225321 확대 판독. 핀 37 납땜점 → 아래로 곧게 → 핀 4·3 사이 통과 → 비아(구멍)로 앞면으로 넘어감", font=font(18), fill=BLK)

# pin labels (top row: 40 at right; bottom row: 1 at right)
top_y, bot_y = 1200, 1915
top = {40: 2905, 39: 2790, 38: 2680, 37: 2560, 36: 2440, 35: 2325, 34: 2215}
bot = {1: 2935, 2: 2815, 3: 2695, 4: 2580, 5: 2460, 6: 2340, 7: 2225}
for n, x in top.items():
    cx, cy = M(x, top_y)
    label((cx, cy - 40), str(n), 16, fg=WHITE if n == 37 else BLK, bg=RED if n == 37 else WHITE)
for n, x in bot.items():
    cx, cy = M(x, bot_y)
    label((cx, cy + 40), str(n), 16)

# path
path = [(2560, 1200), (2562, 1550), (2600, 1750), (2637, 1900), (2640, 2150), (2565, 2310)]
pts = [M(*p) for p in path]
d.line(pts, fill=YEL, width=5)
cx, cy = M(2560, 1200)
d.ellipse((cx-22, cy-22, cx+22, cy+22), outline=RED, width=5)
vx, vy = M(2565, 2310)
d.ellipse((vx-22, vy-22, vx+22, vy+22), outline=BLUE, width=5)

tx = im.width + 50
lines = [
    ("빨간 원 = 핀 37 납땜점", True, RED),
    ("  (위 줄 오른쪽에서 4번째)", False, BLK),
    ("", False, BLK),
    ("노란 선 = 핀 37 패턴", True, (170, 140, 0)),
    ("  아래로 내려가 핀 4와 3 사이를", False, BLK),
    ("  지나감 (핀 4·3과 붙지 않음)", False, BLK),
    ("", False, BLK),
    ("파란 원 = 비아(작은 구멍)", True, BLUE),
    ("  핀 4 아래 약 8–9mm.", False, BLK),
    ("  여기서 앞면으로 넘어감.", False, BLK),
    ("  뒷면에는 이 비아 너머 선 없음", False, BLK),
    ("", False, BLK),
    ("측정 (전원 끄고, 도통)", True, BLK),
    ("1. U30 핀 37 ↔ 파란 원 비아", True, BLK),
    ("   삐 → 뒷면 패턴 정상,", False, BLK),
    ("        끊긴 곳은 앞면 쪽", False, BLK),
    ("   안 삐 → 노란 선 어딘가 끊김", False, BLK),
    ("        (손전등·돋보기로 확인)", False, BLK),
    ("2. 파란 원 비아 ↔ 슬롯 핀 40", True, BLK),
    ("", False, BLK),
    ("판독 확실성: 중간–높음", True, RED),
    ("(사진 확대로 본 것. 비아에", False, BLK),
    (" 프로브를 대 보면 확정)", False, BLK),
]
ty = 110
for t, b, c in lines:
    d.text((tx, ty), t, font=font(19, b), fill=c); ty += 31

cv.save(OUT, quality=92)
print(cv.size)
