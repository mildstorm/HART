"""타이밍 칩(U72–U76, U49) 위치와 출력 핀 그림.
사용: python tools/annotate_timing_chips.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/timing_chips.jpg
세로 칩(U74, U75, U76, U49)은 글자가 아래→위로 읽힘 → 1번 핀 = 오른쪽 아래로 추정 (노치 확인 필요).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN = (0,0,0), (255,255,255), (220,20,20), (255,220,0), (0,100,220), (0,150,60)

W, H = 1700, 1330
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
def label(xy, text, sz=18, fg=BLK, bg=WHITE, anchor="mm", bold=True):
    f = font(sz, bold)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-5, bb[1]-3, bb[2]+5, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "타이밍 칩 위치와 출력 핀 (정면, 슬롯이 위쪽)", font=font(30, True), fill=BLK)
d.text((20, 54), "슬롯 핀 37(Q3)·40(Φ0)이 어느 칩 출력에서 나오는지 찾기 위한 그림. 도통 측정은 반드시 전원 끄고.", font=font(18), fill=BLK)

# overview (lower half + right side)
OX0, OY0, OX1, OY1 = 0, 1650, 2089, 3363
s = 0.38
ov = src.crop((OX0, OY0, OX1, OY1)).resize((int((OX1-OX0)*s), int((OY1-OY0)*s)))
px, py = 20, 95
cv.paste(ov, (px, py))
def O(x, y):
    return (px + (x-OX0)*s, py + (y-OY0)*s)
chips = [
    ("U72", "74LS04", (125, 2775, 400, 2915), GRN),
    ("U73", "74LS175", (425, 2775, 705, 2915), RED),
    ("U74", "74LS08", (50, 2940, 165, 3205), RED),
    ("U75", "74LS195", (185, 2950, 305, 3215), RED),
    ("U76", "74LS109", (330, 2950, 445, 3215), RED),
    ("U49", "74LS175", (1640, 1835, 1765, 2115), RED),
    ("U64", "UM6502", (25, 2490, 760, 2750), YEL),
]
for name, part, (a, b, c, e), col in chips:
    p, q = O(a, b), O(c, e)
    d.rectangle((p[0], p[1], q[0], q[1]), outline=col, width=4)
    label(((p[0]+q[0])/2, p[1] - 12 if name not in ("U74", "U75", "U76") else q[1] + 14), name, 15,
          fg=WHITE if col != YEL else BLK, bg=col)

# zoom of bottom-left cluster
ZX0, ZY0, ZX1, ZY1 = 30, 2760, 720, 3230
zs = 1.15
zim = src.crop((ZX0, ZY0, ZX1, ZY1)).resize((int((ZX1-ZX0)*zs), int((ZY1-ZY0)*zs)), Image.LANCZOS)
zx, zy = 880, 95
cv.paste(zim, (zx, zy))
d.rectangle((zx-1, zy-1, zx+zim.size[0], zy+zim.size[1]), outline=BLK, width=2)
def Z(x, y):
    return (zx + (x-ZX0)*zs, zy + (y-ZY0)*zs)
for name, part, (a, b, c, e), col in chips:
    if name in ("U49", "U64"):
        continue
    p, q = Z(a, b), Z(c, e)
    d.rectangle((p[0], p[1], q[0], q[1]), outline=col, width=3)
    label(((p[0]+q[0])/2, (p[1]+q[1])/2), f"{name}\n{part}", 15, fg=WHITE, bg=col)
# pin-1 markers (estimated)
for name, (x, y) in {"U72": (158, 2893), "U73": (455, 2893), "U74": (150, 3190), "U75": (292, 3200), "U76": (432, 3200)}.items():
    cx, cy = Z(x, y)
    d.ellipse((cx-9, cy-9, cx+9, cy+9), outline=YEL, width=4)
d.text((zx, zy + zim.size[1] + 8), "노란 원 = 1번 핀 (추정). 가로 칩은 왼쪽 아래, 세로 칩은 오른쪽 아래.\n세로 칩은 글자 방향으로 추정한 것이라 노치(반달 홈)로 한 번 확인할 것.",
       font=font(16, True), fill=BLK)

# table
tx, ty = 20, 770
d.text((tx, ty), "출력 핀 (여기서 슬롯 핀 37·40과 도통되는 핀을 찾는다)", font=font(22, True), fill=BLK); ty += 40
rows = [
    ("U73, U49", "74LS175 (16핀)", "출력 2, 3, 6, 7, 10, 11, 14, 15", "GND 8, +5V 16, 클럭 입력 9"),
    ("U75", "74LS195 (16핀)", "출력 15, 14, 13, 12, 11", "GND 8, +5V 16, 클럭 입력 10"),
    ("U76", "74LS109 (16핀)", "출력 6, 7, 10, 9", "GND 8, +5V 16, 클럭 입력 4, 12"),
    ("U74", "74LS08 (14핀)", "출력 3, 6, 8, 11", "GND 7, +5V 14"),
]
for a, b, c, e in rows:
    d.text((tx + 10, ty), a, font=font(19, True), fill=RED)
    d.text((tx + 130, ty), b, font=font(19), fill=BLK)
    d.text((tx + 330, ty), c, font=font(19, True), fill=BLUE)
    d.text((tx + 700, ty), e, font=font(17), fill=BLK)
    ty += 34
ty += 10
d.text((tx, ty), "16핀 칩 번호: 1번부터 한쪽 줄 1–8, 맞은편 줄 9–16 (8번 맞은편이 9번, 1번 맞은편이 16번).", font=font(18), fill=BLK); ty += 30
d.text((tx, ty), "14핀 칩(U72, U74): 1–7, 맞은편 8–14.", font=font(18), fill=BLK); ty += 30
d.text((tx, ty), "세로 칩(U74·U75·U76·U49): 오른쪽 줄 아래→위로 1, 2, 3 …,  왼쪽 줄 위→아래로 이어짐 (오른쪽 아래 1번 바로 왼쪽이 마지막 번호).",
       font=font(18, True), fill=BLK); ty += 50

d.text((tx, ty), "측정 순서", font=font(22, True), fill=BLK); ty += 38
for t, b in [
    ("1. (전원 끄고, 도통) 슬롯 핀 37 ↔ U64 핀 37 : U64 박자(69kHz)와 같은 선인지", True),
    ("2. (전원 끄고, 도통) 슬롯 핀 37 ↔ 위 표의 출력 핀을 하나씩 → 삐 소리 나는 칩·핀 기록", True),
    ("3. (전원 끄고, 도통) 슬롯 핀 40 ↔ 위 표의 출력 핀을 하나씩 → 삐 소리 나는 칩·핀 기록", True),
    ("   검정 프로브를 슬롯 핀에 꽂아 두고 빨강 프로브로 칩 핀을 훑으면 빠름.", False),
    ("4. (전원 켜고) 찾은 출력 핀과 그 칩의 클럭 입력 핀을 Hz로 → 입력은 정상인데 출력이 이상하면 그 칩 고장 유력", True),
]:
    d.text((tx, ty), t, font=font(18, b), fill=BLK); ty += 30
ty += 10
d.text((tx, ty), "주의: 도통·저항 모드는 전원 끈 상태에서만. 전원 켤 때는 다이얼을 먼저 Hz/DC로 돌려 둘 것.", font=font(18, True), fill=RED)

cv.save(OUT, quality=92)
print(cv.size, ty)
