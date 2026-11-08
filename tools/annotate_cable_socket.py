"""본체 쪽 키보드 케이블 커넥터(소켓 접속면, 점퍼선 없음) 사진 20261107_224136에 소켓 번호 매기기. ← 본체 쪽 커넥터 번호 기준 그림
사용: python tools/annotate_cable_socket.py photos/keyboard/20261107_224136_cable-connector_holes_clear.jpg analysis/kbd_cable_socket_numbered.jpg
번호 규칙 = kbd_measure_simple.jpg 와 같음: 오른쪽 줄 맨 위 = 1, 오른쪽 줄 아래로 1–8, 이어서 왼쪽 줄 아래→위 9–16.
사진 기준: 소켓 접속면, 글자(JAE…) 면과 케이블 묶음이 오른쪽, 묶음이 붙은 끝이 위.
+5V = 1번: 같은 각도로 찍은 사진 223843에서 흰 점퍼선(+5V, 사용자 확인)이 꽂힌 자리.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, S = 1000, 1200, 1.2
crop = src.crop((X0, Y0, X0 + 800, Y0 + 1000))
crop = crop.resize((int(800 * S), int(1000 * S)), Image.LANCZOS)
TOP, BOT, LM = 170, 110, 40
canvas = Image.new("RGB", (crop.width + LM * 2, crop.height + TOP + BOT), (255, 255, 255))
canvas.paste(crop, (LM, TOP))
d = ImageDraw.Draw(canvas)
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
YEL, BLK, RED = (255, 215, 0), (0, 0, 0), (230, 20, 20)

right = [(220, 95), (255, 205), (295, 325), (330, 435), (365, 548), (400, 655), (432, 765), (465, 875)]
left_bottom_up = [(375, 888), (340, 778), (305, 670), (278, 565), (245, 455), (205, 343), (160, 225), (128, 102)]

def P(x, y):
    return LM + x * S, TOP + y * S

def tag(x, y, n, color):
    f = F(30)
    t = str(n)
    l, tp, r, b = d.textbbox((x, y), t, font=f)
    d.rectangle((l - 6, tp - 4, r + 6, b + 4), fill=color, outline=BLK, width=2)
    d.text((x, y), t, font=f, fill=BLK if color == YEL else (255, 255, 255))

def hole(n, x, y, side):
    cx, cy = P(x, y)
    r = 24
    col = RED if n == 1 else YEL
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=5)
    if side == "R":
        tag(cx + 34, cy - 20, n, col)
    else:
        tag(cx - 34 - (40 if n >= 10 else 22), cy - 20, n, col)

for i, (x, y) in enumerate(right):
    hole(i + 1, x, y, "R")
for i, (x, y) in enumerate(left_bottom_up):
    hole(i + 9, x, y, "L")
cx, cy = P(*right[0])
d.text((cx + 90, cy - 22), "= +5V", font=F(32), fill=RED)
# 8·9번 = GND (사용자 확인: 슬롯 GND와 도통) — J10의 GND 2핀(케이스 반대쪽 끝)에 들어가는 줄
GRN = (0, 150, 60)
for (x, y) in (right[7], left_bottom_up[0]):
    gx, gy = P(x, y)
    d.ellipse((gx - 30, gy - 30, gx + 30, gy + 30), outline=GRN, width=6)
gx, gy = P(*right[7])
d.text((gx + 80, gy - 22), "8·9 = GND", font=F(32), fill=GRN)

d.text((20, 14), "본체 쪽 케이블 소켓 번호 (기준 그림)", font=F(36), fill=BLK)
d.text((20, 66), "오른쪽 줄 맨 위 = 1, 아래로 1–8 → 왼쪽 줄 아래에서 위로 9–16 (키보드 그림과 같은 규칙)", font=FR(24), fill=BLK)
d.text((20, 102), "소켓 접속면을 보고, 글자(JAE…) 면·케이블 묶음이 오른쪽, 묶음 붙은 끝이 위로 오게 들었을 때", font=FR(24), fill=BLK)
y = TOP + crop.height + 14
d.text((20, y), "+5V = 1번 (흰 점퍼선 자리) · GND = 8·9번 (슬롯 GND와 도통, 사용자 확인)", font=F(26), fill=RED)
d.text((20, y + 44), "측정 결과는 '키보드 단자 ○ → 소켓 ○번'으로 알려 주세요.", font=FR(24), fill=BLK)
canvas.save(OUT, quality=90)
