"""보드 J1 전원 커넥터에 꽂힌 SMPS 선별 전압 그림.
사용: python tools/annotate_j1_power.py photos/case/20261108_171356_J1-power-connector_wired.jpg analysis/j1_power_pins.jpg
선 색 → 전압은 SMPS 단자 실물 확인(2026-11-06, docs/05)에 따른 것. J1 핀에서 직접 전압을 잰 것은 아님.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
im = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB").resize((1500, 2000), Image.LANCZOS)
X0, Y0, X1, Y1 = 0, 650, 1100, 1650
im = im.crop((X0, Y0, X1, Y1))
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
TOP, RM, BOT = 110, 520, 120
cv = Image.new("RGB", (im.width + RM, im.height + TOP + BOT), "white")
cv.paste(im, (0, TOP))
d = ImageDraw.Draw(cv)
P = lambda x, y: (x - X0, y - Y0 + TOP)

RED, ORG, BLU, GRN, BLK, WHT = (220, 20, 20), (245, 120, 0), (30, 80, 230), (0, 140, 60), (0, 0, 0), (255, 255, 255)
pins = [  # (선이 J1에 들어가는 점, 색, 전압, 선 색 이름)
    ((578, 1022), BLK, "GND (0V)", "검정"),
    ((592, 1100), RED, "+12V", "빨강"),
    ((606, 1152), BLU, "-5V", "파랑"),
    ((608, 1205), GRN, "-12V", "초록"),
    ((618, 1268), ORG, "+5V", "주황"),
]
tx = im.width + 30
for i, ((x, y), col, volt, cname) in enumerate(pins):
    cx, cy = P(x, y)
    d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), outline=col, width=5)
    ty = TOP + 260 + i * 105
    d.line((cx + 16, cy, tx - 12, ty + 22), fill=col, width=4)
    l, t, r, b = d.textbbox((0, 0), volt, font=F(38))
    d.rectangle((tx - 8, ty - 4 + t, tx + (r - l) + 8, ty + b + 8), fill=col)
    d.text((tx, ty), volt, font=F(38), fill=WHT if col != ORG else BLK)
    d.text((tx + (r - l) + 24, ty + 8), f"{cname} 선", font=F(28), fill=col)

d.text((16, 12), "J1 전원 커넥터 (보드 왼쪽 위, 슬롯1 옆) — 선별 전압", font=F(36), fill=BLK)
d.text((16, 60), "위에서부터 GND · +12V · -5V · -12V · +5V (사진 2026-11-08, 커넥터에 꽂힌 상태)", font=F(24), fill=BLK)
y = TOP + im.height + 14
d.text((16, y), "주의: 빨강 = +12V, 주황 = +5V (일반 관례와 다름). 전압은 선 색으로 정한 것 (SMPS 단자에서 색 확인, J1 핀 직접 측정은 아님)", font=F(22), fill=RED)
d.text((16, y + 40), "SMPS = DAE HAN ENGINEERING (DE) 제품. 단자·재는 곳 전체 그림: analysis/power_reference.jpg", font=FR(22), fill=BLK)
cv.save(OUT, quality=90)
print(cv.size)
