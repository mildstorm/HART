"""U30 오른쪽 칩 줄(U31–U37)과 아래 줄(U47, U48) 출력 핀 그림 — 핀 37 구동원 찾기용.
사용: python tools/annotate_u31_u48.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/u31_u48_outputs.jpg
세로 칩은 글자가 아래→위로 읽히고 새 사진(add/20261107_005000)에서 노치가 아래쪽 → 1번 핀 = 오른쪽 아래.
좌표는 앞면 기준 사진(202813) 픽셀.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,160,60)

X0, Y0, X1, Y1 = 380, 1400, 2089, 2135
sc = 1.0
im = src.crop((X0, Y0, X1, Y1))
W, H = im.width + 40, im.height + 470
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
ax, ay = 20, 100
cv.paste(im, (ax, ay))
M = lambda x, y: (ax + (x-X0)*sc, ay + (y-Y0)*sc)
def label(xy, text, sz=13, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-3, bb[1]-2, bb[2]+3, bb[3]+2), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 10), "핀 37 구동원 찾기: U30 오른쪽 칩들의 출력 핀 (앞면)", font=font(28, True), fill=BLK)
d.text((20, 52), "빨간 숫자 = 출력 핀. 노란 원 = 1번 핀(오른쪽 아래, 노치 아래쪽). 한쪽 프로브는 저항 ① 다리에 고정하고 빨간 핀을 하나씩.", font=font(17), fill=BLK)

P = 34.3
chips = [  # name, part, x0, x1, ybot(pin1 row), npins, outputs
    ("U31", "74LS367", 945, 1060, 1745, 16, [3, 5, 7, 9, 11, 13]),
    ("U32", "74LS367", 1085, 1195, 1745, 16, [3, 5, 7, 9, 11, 13]),
    ("U33", "74LS367", 1220, 1340, 1745, 16, [3, 5, 7, 9, 11, 13]),
    ("U34", "74LS00", 1360, 1475, 1742, 14, [3, 6, 8, 11]),
    ("U35", "74LS139", 1505, 1620, 1745, 16, [4, 5, 6, 7, 9, 10, 11, 12]),
    ("U36", "82S129", 1645, 1760, 1745, 16, [9, 10, 11, 12]),
    ("U37", "74LS174", 1785, 1900, 1745, 16, [2, 5, 7, 10, 12, 15]),
    ("U47", "74LS157", 1360, 1485, 2097, 16, [4, 7, 9, 12]),
    ("U48", "74LS02", 1505, 1625, 2100, 14, [1, 4, 10, 13]),
]
for name, part, x0, x1, yb, n, outs in chips:
    half = n // 2
    xr, xl = x1 - 13, x0 + 13
    ytop = yb - (half - 1) * P
    a, b = M(x0, ytop - 22), M(x1, yb + 22)
    d.rectangle((a[0], a[1], b[0], b[1]), outline=BLUE, width=3)
    label(((a[0]+b[0])/2, a[1] - 14), f"{name} {part}", 13, fg=WHITE, bg=BLUE)
    for p in range(1, n + 1):
        if p <= half:
            x, y = xr, yb - (p - 1) * P
            tx = -22
        else:
            x, y = xl, ytop + (p - half - 1) * P
            tx = 22
        cx, cy = M(x, y)
        if p == 1:
            d.ellipse((cx-10, cy-10, cx+10, cy+10), outline=YEL, width=3)
        if p in outs:
            label((cx + tx, cy), str(p), 12, fg=WHITE, bg=RED)
r1 = M(443, 1738)
d.ellipse((r1[0]-12, r1[1]-12, r1[0]+12, r1[1]+12), outline=GRN, width=4)
label((r1[0] - 50, r1[1] + 30), "저항 ① 다리 (프로브 고정)", 14, fg=WHITE, bg=GRN, anchor="lm")

ty = ay + im.height + 20
for t, b, c in [
    ("측정 (주의: 전원 끄고, 도통 모드)", True, BLK),
    ("검정 프로브: 저항 ① 다리(초록 원). 빨강 프로브: 빨간 숫자 핀을 하나씩 → 삐 소리 나는 칩·핀 기록", False, BLK),
    ("하나도 안 나면: 같은 방법으로 각 칩의 나머지 핀도 훑기 (출력이 아닌 핀에 붙어 있을 수도 있음)", False, BLK),
    ("", False, BLK),
    ("U36(82S129, '3' 라벨)은 PROM: 출력 9–12. U47·U48은 아래 줄(EPROM 오른쪽).", False, BLK),
    ("1번 핀 위치는 노치로 한 번 확인: 칩 아래쪽 끝에 반달 홈이 있으면 그림대로.", True, RED),
    ("", False, BLK),
    ("왜 이 칩들인가: 정합 사진에서 저항 ① 다리의 앞면 선이 U30 아래 가로 선 다발을 따라 이 칩 줄 쪽으로 감.", False, BLK),
    ("핀 37은 GND로 1kΩ이 달려 있는데도 전원 켜면 3.38V·3.585MHz → 어떤 칩 출력이 실제로 구동 중일 가능성이 큼.", False, BLK),
]:
    d.text((20, ty), t, font=font(17, b), fill=c); ty += 30
cv.save(OUT, quality=92)
print(cv.size, ty)
