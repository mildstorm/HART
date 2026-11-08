"""키보드 측정용 그림 (납땜면): 단자·74LS03·74LS145 모두 같은 방식으로 번호 매김.
사용: python tools/annotate_kbd_measure.py photos/keyboard/20261107_145239_kbd-solder-side_connector-ICs.jpg analysis/kbd_measure_simple.jpg

번호 규칙 (칩과 단자 모두 동일, 납땜면에서 본 모습):
  1번 = 오른쪽 줄 맨 위. 오른쪽 줄을 위→아래로 1, 2, 3 ...
  이어서 왼쪽 줄 맨 아래부터 위로 올라가며 계속. 왼쪽 줄 맨 위가 마지막 번호.
  (DIP 칩 번호를 납땜면에서 본 모양. 단자 번호는 측정용으로 정한 것이며 JAE 커넥터 공식 번호와 다를 수 있음)
이전 이름 대응: 단자 1–8 = K8밖…K1밖(위→아래), 단자 9–16 = K1안…K8안(아래→위). 측정으로 GND 확인된 패드 = 단자 16.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, X1, Y1, sc = 2120, 960, 2860, 2600, 1.0
im = src.crop((X0, Y0, X1, Y1))
FB = "C:/Windows/Fonts/malgunbd.ttf"
font = lambda s: ImageFont.truetype(FB, s)
BLK, WHITE, RED, YEL, BLUE, GRN, GRY = (0,0,0), (255,255,255), (220,20,20), (255,215,0), (30,100,240), (0,140,60), (90,90,90)
LM, RM, TOP = 90, 110, 96
cv = Image.new("RGB", (im.width + LM + RM, im.height + TOP + 20), WHITE)
cv.paste(im, (LM, TOP))
d = ImageDraw.Draw(cv)
M = lambda x, y: (LM + (x - X0) * sc, TOP + (y - Y0) * sc)

def tag(xy, t, fg, bg, sz=17):
    f = font(sz)
    bb = d.textbbox(xy, t, font=f, anchor="mm")
    d.rectangle((bb[0]-4, bb[1]-2, bb[2]+4, bb[3]+2), fill=bg, outline=BLK, width=1)
    d.text(xy, t, font=f, fill=fg, anchor="mm")
def ring(x, y, col, r=12, w=3):
    c = M(x, y); d.ellipse((c[0]-r, c[1]-r, c[0]+r, c[1]+r), outline=col, width=w)

def part(xl, xr, ys, col, fg, title, title_xy, gap=34):
    n = len(ys)
    for i, y in enumerate(ys):
        right_no = i + 1
        left_no = 2 * n - i
        for x, no, side in ((xr, right_no, 1), (xl, left_no, -1)):
            ring(x, y, col)
            cx, cy = M(x, y)
            tx = cx + side * gap
            d.line((cx + side * 12, cy, tx - side * 14, cy), fill=col, width=2)
            tag((tx, cy), str(no), fg, col, 16)
    cx, cy = M(xr, ys[0])
    d.ellipse((cx + 14, cy - 22, cx + 24, cy - 12), fill=col, outline=BLK)
    tag(M(*title_xy), title, fg, col, 17)

ROWS = [1247, 1300, 1342, 1382, 1425, 1467, 1510, 1550]
part(2565, 2615, ROWS, YEL, BLK, "단자 (1–16)", (2590, 1205))
part(2480, 2605, [1795, 1835, 1880, 1920, 1965, 2005, 2050], BLUE, WHITE, "74LS03 (1–14)", (2542, 1752))
part(2470, 2595, [2245, 2290, 2330, 2370, 2410, 2450, 2490, 2530], RED, WHITE, "74LS145 (1–16)", (2532, 2580))

# 74LS145 입력 A·B·C·D (15·14·13·12번) — 본체가 보내는 행 번호, 2026-11-08 Hz 측정으로 확인
PINK = (230, 0, 200)
for no, name in ((15, "A"), (14, "B"), (13, "C"), (12, "D")):
    y = [2245, 2290, 2330, 2370, 2410, 2450, 2490, 2530][16 - no]
    ring(2470, y, PINK, 15, 4)
    cx, cy = M(2470, y)
    tag((cx - 82, cy), f"{name}", WHITE, PINK, 17)
tag((M(2470, 2245)[0] - 150, M(2470, 2245)[1]), "행 번호 입력 ↓", WHITE, PINK, 15)

ring(2238, 1023, BLK, 15, 4); ring(2238, 1077, GRN, 15, 4)
tag((M(2238, 1023)[0] - 62, M(2238, 1023)[1] - 4), "검정 선", WHITE, BLK, 16)
tag((M(2238, 1077)[0] - 62, M(2238, 1077)[1] + 20), "초록 선", WHITE, GRN, 16)
tag((M(2560, 1180)[0] - 150, M(2560, 1180)[1]), "단자 16 = GND (확인)", WHITE, GRY, 15)

d.text((14, 10), "키보드 납땜면 측정 그림 (케이블 단자가 위)", font=font(24), fill=BLK)
d.text((14, 42), "번호 규칙은 셋 다 같음: 오른쪽 줄 맨 위(● 표시)가 1번,", font=font(16), fill=BLK)
d.text((14, 66), "오른쪽 줄 아래로 1, 2, 3… → 왼쪽 줄 아래에서 위로 이어서 셈", font=font(16), fill=BLK)
cv.save(OUT, quality=92)
print(cv.size)
