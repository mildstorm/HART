"""슬롯1 50핀 번호 그림 생성.
사용: python tools/annotate_slot1_pins.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/slot1_pins.jpg
배치 근거: 사용자 표시(2026-11-07) 위쪽 왼쪽 GND, 위쪽 오른쪽 +5V, 아래 왼쪽 +12V,
왼쪽 줄 위에서 8·9번째 -12V·-5V → 왼쪽 줄 = 26(위)~50(아래), 오른쪽 줄 = 25(위)~1(아래).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)

BLK, WHITE = (0, 0, 0), (255, 255, 255)
RED, ORG, BLUE = (220, 20, 20), (255, 130, 0), (0, 110, 230)
GRN, GRAY, YEL = (0, 150, 60), (120, 120, 120), (255, 220, 0)

W, H = 1500, 1260
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)

def label(xy, text, sz=17, fg=BLK, bg=WHITE, anchor="mm", bold=True):
    f = font(sz, bold)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "슬롯1 핀 번호 (정면, 슬롯이 위쪽)", font=font(32, True), fill=BLK)
d.text((20, 56), "사용자 표시(위 왼쪽 GND, 위 오른쪽 +5V, 아래 왼쪽 +12V)를 기준으로 Apple II 슬롯 배치를 적용",
       font=font(18), fill=BLK)

# --- small locator ---
loc = src.crop((0, 0, 1060, 1100)).resize((318, 330))
cv.paste(loc, (20, 100))
s = 0.3
d.rectangle((20 + 140*s, 100 + 20*s, 20 + 230*s, 100 + 1000*s), outline=RED, width=3)
d.text((20, 438), "빨간 박스 = 슬롯1\n(왼쪽 끝 슬롯)", font=font(17, True), fill=RED)

# --- big slot ---
X0, Y0, X1, Y1 = 120, 40, 245, 975
sc = 1.18
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
ax, ay = 640, 110
cv.paste(im, (ax, ay))
d.rectangle((ax-1, ay-1, ax+im.size[0], ay+im.size[1]), outline=BLK, width=2)
def M(x, y):
    return (ax + (x-X0)*sc, ay + (y-Y0)*sc)

colL, colR, y1, pitch = 162, 203, 92, 34.92
special = {
    40: ("Φ0  ← 측정", RED), 35: ("3.58M (COLOR REF)", ORG), 36: ("7M", BLUE),
    37: ("Q3", GRAY), 38: ("Φ1", GRAY),
    26: ("GND", GRN), 25: ("+5V", GRN), 50: ("+12V", GRN), 33: ("-12V", GRN), 34: ("-5V", GRN),
    1: ("I/O SELECT", GRAY),
}
for r in range(25):
    y = y1 + r*pitch
    for col, pin, side in ((colL, 26 + r, -1), (colR, 25 - r, 1)):
        cx, cy = M(col, y)
        bx = cx + side*48
        sp = special.get(pin)
        if sp:
            name, c = sp
            label((bx, cy), str(pin), 16, fg=WHITE, bg=c)
            d.line((cx + side*8, cy, bx - side*16, cy), fill=c, width=2)
            tx = bx + side*26
            d.text((tx, cy), name, font=font(17, True), fill=c, anchor="rm" if side < 0 else "lm")
            if pin in (40, 35, 36):
                d.ellipse((cx-9, cy-9, cx+9, cy+9), outline=c, width=3)
        else:
            label((bx, cy), str(pin), 14, bold=False)
label((M(colL, 0)[0] - 48, ay - 22), "왼쪽 줄 26→50", 15, bg=YEL)
label((M(colR, 0)[0] + 48, ay - 22), "오른쪽 줄 25→1", 15, bg=YEL)

# --- instructions ---
tx, ty = 20, 520
lines = [
    ("측정 순서 (검정 프로브 = U72 핀 7)", True, BLK),
    ("", False, BLK),
    ("0. 확인: 왼쪽 줄 맨 아래(50) = 약 +12V", True, GRN),
    ("   왼쪽 줄 맨 위(26) = 0V, 오른쪽 줄 맨 위(25) = 약 +5V", False, BLK),
    ("   → 다르면 멈추고 알려 줄 것", False, BLK),
    ("", False, BLK),
    ("1. 핀 40 (Φ0) Hz", True, RED),
    ("   왼쪽 줄 위에서 15번째 (아래에서 11번째)", False, BLK),
    ("   정상 1.023MHz", False, BLK),
    ("", False, BLK),
    ("2. 핀 35 (3.58M) Hz", True, ORG),
    ("   왼쪽 줄 위에서 10번째 / 정상 약 3.58MHz", False, BLK),
    ("", False, BLK),
    ("3. 핀 36 (7M) Hz", True, BLUE),
    ("   왼쪽 줄 위에서 11번째 / 정상 약 7.16MHz", False, BLK),
    ("", False, BLK),
    ("주의: 핀 35·36·40은 서로 가까움.", True, RED),
    ("프로브가 이웃 핀에 같이 닿지 않게.", False, RED),
    ("핀 50(+12V)은 맨 아래 왼쪽 모서리.", False, RED),
]
for t, b, c in lines:
    d.text((tx, ty), t, font=font(19, b), fill=c)
    ty += 31

cv.save(OUT, quality=92)
print(cv.size)
