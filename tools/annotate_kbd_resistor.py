"""키보드 부품면 저항 위치 표시.
사용: python tools/annotate_kbd_resistor.py photos/keyboard/20261107_145413_kbd-component_ICs-connector-keys.jpg analysis/kbd_resistor_location.jpg
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, X1, Y1 = 1760, 660, 3000, 2520
im = src.crop((X0, Y0, X1, Y1))
d = ImageDraw.Draw(im)
font = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
RED, YEL, BLK, WHITE = (220, 20, 20), (255, 215, 0), (0, 0, 0), (255, 255, 255)

def p(x, y):  # 원본 좌표 → 잘라낸 그림 좌표
    return x - X0, y - Y0

def label(xy, text, size, color):
    x, y = xy
    f = font(size)
    l, t, r, b = d.textbbox((x, y), text, font=f)
    d.rectangle((l - 8, t - 6, r + 8, b + 6), fill=WHITE, outline=BLK, width=2)
    d.text((x, y), text, font=f, fill=color)

# 저항 (세로로 서 있는 작은 베이지색 부품, 색 띠)
ax, ay = p(2040, 1860); bx, by = p(2160, 2310)
d.ellipse((ax, ay, bx, by), outline=RED, width=10)
label(p(1790, 2340), "저항 (다리 2개: 위·아래)", 52, RED)
# 참고용 칩·단자
label(p(2280, 760), "74LS145", 44, BLK)
label(p(2280, 1240), "74LS03", 44, BLK)
label(p(2420, 2430), "JAE 16P 단자", 44, BLK)
label(p(1790, 680), "부품면 (키캡 쪽)", 44, BLK)
im.save(OUT, quality=90)
