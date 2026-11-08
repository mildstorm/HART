"""나머지 타이밍 칩(U78 74LS74, U60 74LS00, U61·U62 74LS74) 위치와 출력 핀 그림.
사용: python tools/annotate_timing_chips2.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/timing_chips2.jpg
세로 칩은 글자가 아래→위로 읽힘 → 1번 핀 = 오른쪽 아래로 추정 (노치 확인 필요).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN = (0,0,0), (255,255,255), (220,20,20), (255,220,0), (0,100,220), (0,150,60)

W, H = 1700, 1250
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
def label(xy, text, sz=18, fg=BLK, bg=WHITE, anchor="mm", bold=True):
    f = font(sz, bold)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-5, bb[1]-3, bb[2]+5, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "나머지 타이밍 칩: U78, U60, U61, U62 (정면, 슬롯이 위쪽)", font=font(30, True), fill=BLK)
d.text((20, 54), "U30 핀 37(CPU 클럭 입력)이 어느 칩 출력에 붙어 있는지 찾기 위한 그림. 도통 측정은 반드시 전원 끄고.", font=font(18), fill=BLK)

# overview
s = 0.20
ov = src.resize((int(src.width*s), int(src.height*s)))
px, py = 20, 95
cv.paste(ov, (px, py))
def O(x, y):
    return (px + x*s, py + y*s)
chips = [
    ("U78", "74LS74", (605, 2980, 730, 3290), RED),
    ("U60", "74LS00", (1650, 2145, 1765, 2410), BLUE),
    ("U61", "74LS74", (1790, 2145, 1905, 2410), RED),
    ("U62", "74LS74", (1925, 2145, 2045, 2410), RED),
    ("U30", "CPU", (170, 1420, 900, 1660), GRN),
    ("U72", "", (125, 2775, 400, 2915), (120, 120, 120)),
]
for name, part, (a, b, c, e), col in chips:
    p, q = O(a, b), O(c, e)
    d.rectangle((p[0], p[1], q[0], q[1]), outline=col, width=3)
    label(((p[0]+q[0])/2, q[1] + 12), name, 13, fg=WHITE, bg=col)

def zoom(box, sc, at, items, pin1):
    x0, y0, x1, y1 = box
    im = src.crop(box).resize((int((x1-x0)*sc), int((y1-y0)*sc)), Image.LANCZOS)
    cv.paste(im, at)
    d.rectangle((at[0]-1, at[1]-1, at[0]+im.size[0], at[1]+im.size[1]), outline=BLK, width=2)
    Z = lambda x, y: (at[0] + (x-x0)*sc, at[1] + (y-y0)*sc)
    for name, part, (a, b, c, e), col in items:
        p, q = Z(a, b), Z(c, e)
        d.rectangle((p[0], p[1], q[0], q[1]), outline=col, width=3)
        label(((p[0]+q[0])/2, q[1] + 16), f"{name} {part}", 15, fg=WHITE, bg=col)
    for x, y in pin1:
        cx, cy = Z(x, y)
        d.ellipse((cx-9, cy-9, cx+9, cy+9), outline=YEL, width=4)
    return im.size

# zoom A: U78 (bottom-left, right of U76)
d.text((700, 95), "① U78 (U76 74LS109 오른쪽 두 번째)", font=font(19, True), fill=BLK)
zoom((300, 2900, 900, 3310), 0.75, (700, 125), [chips[0]], [(718, 3270)])
# zoom B: U60–U62 (right side, below U49)
d.text((1180, 95), "② U60·U61·U62 (오른쪽, U49 아래 줄)", font=font(19, True), fill=BLK)
zoom((1600, 1820, 2089, 2440), 0.9, (1180, 125), chips[1:4], [(1755, 2395), (1893, 2395), (2033, 2395)])
d.text((700, 470), "노란 원 = 1번 핀 (추정, 오른쪽 아래).\n글자 방향으로 추정한 것이라 노치(반달 홈)로 확인.\n"
       "②의 위 줄 왼쪽 5070D0 칩이 U49(74LS175).", font=font(16, True), fill=BLK)

# table
tx, ty = 470, 720
d.text((tx, ty), "출력 핀 (14핀 칩: 1–7 한쪽 줄, 맞은편 8–14 / 1번 맞은편이 14번)", font=font(22, True), fill=BLK); ty += 40
for a, b, c, e in [
    ("U78, U61, U62", "74LS74 (D 플립플롭)", "출력 5, 6, 8, 9", "클럭 입력 3, 11 / GND 7, +5V 14"),
    ("U60", "74LS00 (NAND)", "출력 3, 6, 8, 11", "GND 7, +5V 14"),
]:
    d.text((tx + 10, ty), a, font=font(19, True), fill=RED)
    d.text((tx + 190, ty), b, font=font(19), fill=BLK)
    d.text((tx + 420, ty), c, font=font(19, True), fill=BLUE)
    d.text((tx + 620, ty), e, font=font(17), fill=BLK)
    ty += 34
ty += 20
d.text((tx, ty), "측정 순서 (모두 전원 끄고, 도통/저항 모드. 한쪽 프로브는 U30 핀 37에 고정)", font=font(22, True), fill=BLK); ty += 40
for t, b in [
    ("1. U30 핀 37 ↔ U78·U61·U62 핀 5, 6, 8, 9 / U60 핀 3, 6, 8, 11 → 삐 소리 나는 칩·핀 기록", True),
    ("2. U30 핀 37 ↔ 슬롯 4 핀 35 (3.58M, 왼쪽 줄 위에서 10번째)", True),
    ("3. 저항 모드: U30 핀 37 ↔ GND(U72 핀 7), U30 핀 37 ↔ +5V(U30 핀 8)", True),
    ("   둘 다 끊김(OL/수 MΩ)이고 1번에서도 아무 데도 안 붙으면 → 핀 37이 떠 있음 = 패턴 끊김 유력", False),
    ("4. 슬롯 핀 40 ↔ 위 1번의 같은 출력 핀들 → 원래 Φ0가 나오는 핀 찾기", True),
]:
    d.text((tx, ty), t, font=font(18, b), fill=BLK); ty += 30

cv.save(OUT, quality=92)
print(cv.size, ty)
