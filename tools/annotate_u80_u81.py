"""J10 옆 74LS257 두 개(U80·U81, 키보드 열 선 읽기 추정) 위치 표시 — 소켓 꾹 누르기 안내.
사용: python tools/annotate_u80_u81.py photos/keyboard/20261107_131132_J10-header_connector-unplugged.jpg analysis/u80_u81_press.jpg
U80 = J10 오른쪽(SIP 쪽) M74LS257AP, U81 = J10 왼쪽 M74LS257AP (사진에서는 뽑은 커넥터에 일부 가려짐).
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, X1, Y1 = 0, 900, 3000, 2700
im = src.crop((X0, Y0, X1, Y1)).resize((1500, 900), Image.LANCZOS)
S = 0.5
d = ImageDraw.Draw(im)
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
RED, BLU, BLK, WHITE, YEL = (230, 20, 20), (30, 100, 240), (0, 0, 0), (255, 255, 255), (255, 215, 0)

def P(x, y):
    return (x - X0) * S, (y - Y0) * S

def label(xy, text, size, color):
    x, y = xy
    f = F(size)
    l, t, r, b = d.textbbox((x, y), text, font=f)
    d.rectangle((l - 6, t - 4, r + 6, b + 4), fill=WHITE, outline=BLK, width=2)
    d.text((x, y), text, font=f, fill=color)

# U80 (J10 오른쪽, M74LS257AP 503000)
d.rectangle((*P(1500, 1250), *P(1780, 1700)), outline=RED, width=7)
label(P(1500, 1720), "U80 74LS257", 30, RED)
# U81 (J10 왼쪽, 커넥터에 일부 가려짐)
d.rectangle((*P(860, 1370), *P(1080, 1830)), outline=RED, width=7)
label(P(380, 1870), "U81 74LS257 (커넥터 밑)", 30, RED)
# J10
d.rectangle((*P(1150, 1330), *P(1320, 1860)), outline=YEL, width=5)
label(P(1170, 1240), "J10", 30, BLK)
label((20, 15), "전원 끄고: 빨간 칸 칩 2개를 엄지로 수직으로 꾹", 34, RED)
im.save(OUT, quality=90)
