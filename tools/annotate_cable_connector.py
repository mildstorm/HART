"""본체 쪽 키보드 케이블 커넥터(구멍 면) 번호 그림.
사용: python tools/annotate_cable_connector.py photos/keyboard/20261107_131132_J10-header_connector-unplugged.jpg analysis/kbd_cable_connector_holes.jpg
번호 규칙은 키보드 그림(kbd_measure_simple.jpg)과 같음: 오른쪽 줄 맨 위 = 1, 오른쪽 줄 아래로 1–8,
이어서 왼쪽 줄 아래→위 9–16. 사진처럼 놓았을 때(구멍 면이 보이고, 케이블 묶음이 위쪽 끝으로 넘어감) 기준.
이 번호는 측정 보고용이며 J10이나 키보드 단자 번호와 같다는 뜻이 아님.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, S = 460, 1000, 1.6
im = src.crop((X0, Y0, X0 + 600, Y0 + 700)).resize((int(600 * S), int(700 * S)), Image.LANCZOS)
pad_top = 170
canvas = Image.new("RGB", (im.width + 80, im.height + pad_top + 120), (255, 255, 255))
canvas.paste(im, (40, pad_top))
d = ImageDraw.Draw(canvas)
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
YEL, BLK, RED = (255, 215, 0), (0, 0, 0), (220, 20, 20)

right = [(235, 160), (275, 228), (318, 288), (358, 348), (398, 404), (438, 458), (475, 512), (510, 560)]
left = [(170, 210), (215, 270), (255, 330), (298, 385), (338, 442), (378, 498), (415, 548), (450, 600)]

def P(x, y):
    return 40 + x * S, pad_top + y * S

def tag(xy, n):
    x, y = xy
    f = F(30)
    t = str(n)
    l, tp, r, b = d.textbbox((x, y), t, font=f)
    d.rectangle((l - 6, tp - 4, r + 6, b + 4), fill=YEL, outline=BLK, width=2)
    d.text((x, y), t, font=f, fill=BLK)

for i, (x, y) in enumerate(right):
    cx, cy = P(x, y)
    d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=YEL, width=5)
    tag((cx + 34, cy - 20), i + 1)
for i, (x, y) in enumerate(reversed(left)):
    cx, cy = P(x, y)
    d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=YEL, width=5)
    tag((cx - 34 - (40 if i + 9 >= 10 else 22), cy - 20), i + 9)
cx, cy = P(*right[0])
d.ellipse((cx + 14, cy - 40, cx + 30, cy - 24), fill=YEL, outline=BLK)

d.text((30, 18), "본체 쪽 케이블 커넥터 구멍 번호", font=F(42), fill=BLK)
d.text((30, 76), "구멍 면이 보이게, 케이블 묶음이 위쪽 끝으로 넘어가게 들었을 때 (사진과 같은 모양)", font=FR(26), fill=BLK)
d.text((30, 114), "규칙: 오른쪽 줄 맨 위(● 표시) = 1, 아래로 1–8 → 왼쪽 줄 아래에서 위로 9–16", font=FR(26), fill=BLK)
y = pad_top + im.height + 20
d.text((30, y), "키보드 단자 16(GND)·9(+5V)와 삑 하는 구멍 번호를 알려 주세요.", font=F(30), fill=RED)
d.text((30, y + 50), "헷갈리면 'G'·'5' 테이프를 붙이고 이 각도로 사진을 찍어 보내도 됩니다.", font=FR(26), fill=BLK)
canvas.save(OUT, quality=90)
