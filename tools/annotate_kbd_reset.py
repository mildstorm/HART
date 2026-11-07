"""키보드 납땜면에서 RESET 키 스위치 패드 후보 위치 표시.
사용: python tools/annotate_kbd_reset.py photos/keyboard/Scan_20261107_144256_kbd-solder-side_flat.jpg analysis/kbd_reset_solder.jpg

판단 근거: 앞면 사진(Scan_..._144416)에서 RESET = 키보드 오른쪽 아래 모서리 키(단자·칩 판 쪽 가장자리 줄, 맨 아래 줄).
납땜면은 앞면을 좌우로 뒤집은 모양(칩·단자 판이 왼쪽으로 옴, 위아래는 그대로) → RESET = 납땜면 왼쪽 아래 모서리.
바로 위 = Del, 오른쪽(안쪽) = '/' (숫자 패드 쪽 화살표 묶음). 키 하나 간격 약 145px(원본 사진 픽셀).
패드 쌍까지는 사진으로 확정 못 함 → 표시는 '후보 구역'. 누른 채 통전으로 확정.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, X1, Y1 = 520, 2150, 1560, 3264
im = src.crop((X0, Y0, X1, Y1))
d = ImageDraw.Draw(im)
font = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
RED, YEL, BLU, BLK, WHITE = (230, 20, 20), (255, 215, 0), (40, 120, 255), (0, 0, 0), (255, 255, 255)

def p(x, y):
    return x - X0, y - Y0

def label(xy, text, size, color):
    x, y = xy
    f = font(size)
    l, t, r, b = d.textbbox((x, y), text, font=f)
    d.rectangle((l - 8, t - 6, r + 8, b + 6), fill=WHITE, outline=BLK, width=2)
    d.text((x, y), text, font=f, fill=color)

# RESET 후보 구역 (납땜면 왼쪽 아래 모서리)
d.rectangle((*p(830, 2990), *p(1040, 3190)), outline=RED, width=9)
label(p(560, 3200 - 10), "RESET 후보", 46, RED)
# 이웃 키 (방향 잡기용)
d.rectangle((*p(830, 2830), *p(1040, 2990)), outline=YEL, width=5)
label(p(560, 2880), "Del (위)", 38, BLK)
d.rectangle((*p(1040, 2990), *p(1250, 3190)), outline=BLU, width=5)
label(p(1080, 3200 - 10), "'/' (오른쪽)", 38, BLU)
label(p(560, 2170), "납땜면 · 위쪽 = 칩·단자 쪽", 40, BLK)
im.save(OUT, quality=90)
