import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F = "C:/Windows/Fonts/malgun.ttf"
FB = "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)

RED = (230, 30, 30)
BLK = (0, 0, 0)
YEL = (255, 220, 0)
CYAN = (0, 200, 255)
WHITE = (255, 255, 255)

W, H = 1760, 2560
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)

def label(dr, xy, text, sz=20, fg=BLK, bg=YEL, bold=True, anchor="la"):
    f = font(sz, bold)
    bb = dr.textbbox(xy, text, font=f, anchor=anchor)
    dr.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    dr.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "HART 보드 측정 위치 (정면, 슬롯이 위쪽)", font=font(34, True), fill=BLK)
d.text((20, 58), "검정 프로브 = U72 핀 7 (GND).  빨강 프로브 = 아래 빨간 원 위치.  사진 202813 기준",
       font=font(20), fill=BLK)

# ---------- left overview ----------
OX0, OY0, OX1, OY1 = 0, 0, 1060, 3060
s0 = 0.62
ov = src.crop((OX0, OY0, OX1, OY1)).resize((int((OX1-OX0)*s0), int((OY1-OY0)*s0)))
px, py = 20, 100
cv.paste(ov, (px, py))
def O(x, y):
    return (px + (x-OX0)*s0, py + (y-OY0)*s0)
def obox(x0, y0, x1, y1, col, w=4):
    a, b = O(x0, y0), O(x1, y1)
    d.rectangle((a[0], a[1], b[0], b[1]), outline=col, width=w)

slot_x = [(145, 225), (330, 410), (545, 625), (760, 875)]
for i, (a, b) in enumerate(slot_x):
    obox(a, 20, b, 1000, CYAN, 3)
    label(d, O((a+b)/2, 990), f"슬롯{i+1}", 16, anchor="mt", bg=CYAN)
obox(170, 1420, 900, 1660, RED, 5)
label(d, O(520, 1395), "U30 메인 CPU", 20, anchor="mb")
obox(25, 2490, 760, 2750, RED, 5)
label(d, O(400, 2470), "U64", 20, anchor="mb")
obox(130, 2770, 400, 2920, (0, 160, 0), 5)
label(d, O(265, 2935), "U72 (GND)", 18, anchor="mt", bg=(150, 255, 150))
d.text((px, py + ov.size[1] + 8), "슬롯 번호(1–4)는 왼쪽부터 센 것. SL1–SL4 실크 표기와\n같은지는 미확인. 이번 측정은 어느 슬롯이든 같음.",
       font=font(17), fill=BLK)

RX = 700  # right column start

# ---------- inset helper ----------
def inset(box, scale, at):
    x0, y0, x1, y1 = box
    im = src.crop(box).resize((int((x1-x0)*scale), int((y1-y0)*scale)), Image.LANCZOS)
    cv.paste(im, at)
    d.rectangle((at[0]-1, at[1]-1, at[0]+im.size[0], at[1]+im.size[1]), outline=BLK, width=2)
    return lambda x, y: (at[0] + (x-x0)*scale, at[1] + (y-y0)*scale)

def pinnum(M, x, y, n, below, hl=False, sz=13):
    cx, cy = M(x, y)
    off = 26 if below else -26
    if hl:
        r = 20
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=RED, width=5)
    label(d, (cx, cy+off), str(n), 15, fg=WHITE if hl else BLK, bg=RED if hl else WHITE, anchor="mm")

# ---------- U30 inset ----------
d.text((RX, 100), "① U30 (메인 CPU, UM6502) — 빨강 프로브: 핀 37 (Φ0)", font=font(24, True), fill=BLK)
M = inset((150, 1385, 930, 1700), 1.22, (RX, 140))
x1, pitch, ytop, ybot = 207, 34.47, 1437, 1642
for n in range(1, 21):
    pinnum(M, x1 + (n-1)*pitch, ybot, n, True, hl=(n in ()))
for n in range(21, 41):
    pinnum(M, x1 + (40-n)*pitch, ytop, n, False, hl=(n == 37))
cx, cy = M(x1 + 3*pitch, ytop)
label(d, (cx + 60, cy + 45), "← 핀 37 = Φ0 (정상 1.023MHz)", 20, fg=WHITE, bg=RED, anchor="lm")
cx, cy = M(x1, ybot)
label(d, (cx + 20, cy - 45), "↙ 1번 핀 (왼쪽 아래)", 17, anchor="lm")

# ---------- U64 + U72 inset ----------
yb = 140 + int(315*1.22) + 60
d.text((RX, yb), "② U64 핀 37 (비교용)   ③ U72 핀 7 = GND (검정 프로브)", font=font(24, True), fill=BLK)
M2 = inset((15, 2480, 800, 2925), 1.22, (RX, yb + 40))
x1, pitch, ytop, ybot = 52, 34.7, 2518, 2728
for n in range(1, 21):
    pinnum(M2, x1 + (n-1)*pitch, ybot, n, True)
for n in range(21, 41):
    pinnum(M2, x1 + (40-n)*pitch, ytop, n, False, hl=(n == 37))
cx, cy = M2(x1 + 3*pitch, ytop)
label(d, (cx + 60, cy + 45), "← U64 핀 37", 20, fg=WHITE, bg=RED, anchor="lm")
# U72 74LS04: pins 1..7 bottom row left->right, 14..8 top row left->right
ux1, upitch, uyt, uyb = 158, 34.8, 2797, 2893
for n in range(1, 8):
    cx, cy = M2(ux1 + (n-1)*upitch, uyb)
    if n == 7:
        r = 18
        d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=(0, 140, 0), width=5)
        label(d, (cx + 26, cy), "핀 7 = GND", 18, bg=(150, 255, 150), anchor="lm")
    else:
        label(d, (cx, cy+26), str(n), 14, bg=WHITE, anchor="mm")

# ---------- slot inset ----------
ys = yb + 40 + int(445*1.22) + 50
d.text((RX, ys), "④ 슬롯 (그림은 오른쪽 끝 슬롯. 네 슬롯 모두 같은 방법)", font=font(24, True), fill=BLK)
ss = 0.78
SX0, SY0, SX1, SY1 = 745, 45, 890, 975
sat = (RX + 70, ys + 45)
M3 = inset((SX0, SY0, SX1, SY1), ss, sat)
colL, colR = 795, 838
for k in range(25):
    y = 88 + k*35
    cx, cy = M3(colL, y)
    d.text((cx - 62, cy), f"{k+1}", font=font(15, True), fill=BLK, anchor="rm")
d.text((sat[0] - 60, sat[1] + 2), "줄", font=font(15, True), fill=BLK, anchor="rm")
for name, col, k in (("A", colL, 0), ("B", colR, 0), ("C", colL, 24), ("D", colR, 24)):
    cx, cy = M3(col, 88 + k*35)
    r = 9
    d.ellipse((cx-r, cy-r, cx+r, cy+r), outline=RED, width=3)
    dx = -1 if col == colL else 1
    label(d, (cx + dx*(40 if col == colL else 55), cy), name, 18, fg=WHITE, bg=RED, anchor="mm")

tx = RX + 260
lines = [
    ("1단계: 전원 켜고 DC 전압으로 모서리 A·B·C·D를 잰다", True),
    ("  약 +12V 나오는 모서리 = 50번", False),
    ("  같은 세로줄 반대쪽 끝 = 26번 (0V)", False),
    ("  50번 옆 줄 같은 끝 = 1번,  26번 옆 = 25번(+5V)", False),
    ("", False),
    ("2단계: 50번이 있는 세로줄에서 Hz로 잰다", True),
    ("  +12V가 위쪽(A 또는 B)이면:", True),
    ("    핀 40 Φ0 = 그 줄 11번째", False),
    ("    핀 36 7M = 15번째,  핀 35 3.58M = 16번째", False),
    ("  +12V가 아래쪽(C 또는 D)이면:", True),
    ("    핀 40 Φ0 = 그 줄 15번째", False),
    ("    핀 36 7M = 11번째,  핀 35 3.58M = 10번째", False),
    ("  (줄 번호는 왼쪽 숫자, 위에서부터 센 것)", False),
    ("", False),
    ("정상값: 핀40 1.023MHz, 핀36 약 7.16MHz,", True),
    ("        핀35 약 3.58MHz", True),
    ("", False),
    ("주의: 50번(+12V) 근처에서 프로브가 두 핀에", True),
    ("동시에 닿지 않게. 슬롯 1번이 어느 끝인지는", False),
    ("사진으로 확인 못 함 → 반드시 1단계로 확인.", False),
]
yy = ys + 50
for t, b in lines:
    d.text((tx, yy), t, font=font(19, b), fill=RED if t.startswith("주의") else BLK)
    yy += 30

# ---------- J1 power connector ----------
j1_pins = [175, 280, 350, 418, 483]  # orig y, x ~ 62
obox(30, 130, 110, 520, (255, 120, 0), 4)
label(d, O(115, 120), "J1 전원", 16, anchor="lb", bg=(255, 170, 80))

yj = 2090
d.line((20, yj - 15, W - 20, yj - 15), fill=BLK, width=2)
d.text((20, yj), "⑤ J1 전원 커넥터 (왼쪽 위, 5핀) — 핀별 전압은 아직 확인 안 됨", font=font(24, True), fill=BLK)
MJ = inset((0, 120, 200, 540), 1.0, (40, yj + 45))
for i, y in enumerate(j1_pins):
    cx, cy = MJ(62, y)
    d.ellipse((cx-10, cy-10, cx+10, cy+10), outline=RED, width=3)
    label(d, (cx + 170, cy), f"J1-{'abcde'[i]}:  ?  V", 18, bg=WHITE, anchor="lm")
    d.line((cx + 12, cy, cx + 150, cy), fill=RED, width=2)
jt = [
    ("하네스 선 색 → 전압 (PSU 단자에서 확인, 2026-11-06)", True),
    ("  빨강 = +12V   주황 = +5V   검정 = GND(0V)", False),
    ("  파랑 = -5V    초록 = -12V", False),
    ("  ※ 빨강이 +5V가 아니라 +12V임에 주의", True),
    ("", False),
    ("확정 방법 (둘 중 하나)", True),
    ("  1) 커넥터를 꽂은 채로 J1-a부터 e까지 선 색을 읽는다", False),
    ("  2) 전원 켜고 검정 프로브 U72 핀 7, 빨강 프로브로", False),
    ("     J1 각 핀 DC 전압 (커넥터 뺀 상태면 PSU 쪽 단자를 잴 것)", False),
    ("", False),
    ("하네스 사진(225533)의 하우징 선 순서는 검정·빨강·파랑·초록·주황", False),
    ("으로 보이지만, 보드에 어느 방향으로 꽂히는지 확인 안 됨.", False),
]
yy2 = yj + 55
for t, b in jt:
    d.text((520, yy2), t, font=font(19, b), fill=RED if t.startswith("  ※") else BLK)
    yy2 += 30

cv.save(OUT, quality=92)
print(cv.size, yy)
