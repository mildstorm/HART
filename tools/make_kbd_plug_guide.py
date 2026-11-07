"""키보드 케이블을 J10에 꽂는 방향 그림.
사용: python tools/make_kbd_plug_guide.py analysis/kbd_plug_direction.jpg
근거 (2026-11-07 사용자 측정): J10 케이스 반대쪽 끝 2핀 = GND, 케이스 쪽 끝 왼쪽(U81 쪽, SIP 반대쪽) 핀 = +5V(슬롯1 25번과 통전).
케이블 커넥터: 글자(JAE…) 면 쪽 줄 양 끝 = GND / +5V.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHITE, RED, ORG, BLU = (0, 0, 0), (255, 255, 255), (220, 20, 20), (230, 120, 0), (30, 100, 240)

j = Image.open("analysis/j10_gnd_pins_zoom.jpg").convert("RGB")  # 840x1400
d = ImageDraw.Draw(j)
d.rectangle((14, 58, 460, 112), fill=WHITE, outline=BLK, width=2)  # 원본의 '(미확인)' 글자 덮기
d.text((26, 62), "케이스(뒤판) 쪽 끝", font=F(34), fill=BLK)
# +5V = 케이스 쪽 끝 왼쪽 핀 (노란 점선 원 안 왼쪽)
d.ellipse((215, 180, 305, 250), outline=ORG, width=8)
d.rectangle((40, 270, 360, 330), fill=WHITE, outline=BLK, width=2)
d.text((52, 274), "+5V (측정 확인)", font=F(38), fill=ORG)
# 줄 표시
d.rectangle((20, 600, 230, 700), fill=WHITE, outline=BLK, width=2)
d.text((30, 605), "왼쪽 줄\n= 글자 면 줄", font=F(32), fill=BLU)
d.rectangle((560, 470, 830, 570), fill=WHITE, outline=BLK, width=2)
d.text((570, 475), "오른쪽 줄\n(SIP·U80 쪽)", font=F(30), fill=BLK)

W = j.width + 900
canvas = Image.new("RGB", (W, j.height + 160), WHITE)
cd = ImageDraw.Draw(canvas)
cd.text((30, 20), "키보드 케이블 꽂는 방향 (J10)", font=F(48), fill=BLK)
cd.text((30, 90), "사진: J10을 위에서 본 모습 (위 = 케이스 뒤판 쪽)", font=FR(30), fill=BLK)
canvas.paste(j, (30, 150))
tx, ty = j.width + 70, 170
steps = [
    ("꽂는 법", F(40), BLK),
    ("① 커넥터 글자(JAE…) 면을 왼쪽으로", F(34), BLU),
    ("    → 글자 면 줄이 J10 왼쪽 줄에 들어감", FR(30), BLK),
    ("② GND 구멍 끝을 아래(빨간 원, 케이스 반대쪽)", F(34), RED),
    ("③ +5V 구멍 끝을 위(주황 원, 케이스 쪽)", F(34), ORG),
    ("", FR(20), BLK),
    ("꽂은 뒤, 전원 켜기 전 확인 (통전 모드)", F(36), BLK),
    ("• 키보드 단자 9 ↔ 슬롯1 25번 : 삑 해야 함", FR(30), BLK),
    ("• 키보드 단자 16 ↔ 슬롯1 26번 : 삑 해야 함", FR(30), BLK),
    ("• 키보드 단자 9 ↔ 단자 16 : 삑 하면 안 됨", FR(30), RED),
    ("", FR(20), BLK),
    ("셋 다 맞으면 전원을 켜도 됩니다.", F(32), BLK),
    ("켠 뒤: 74LS145 16번 ↔ 8번 전압 약 5V 확인", FR(30), BLK),
]
for t, f, c in steps:
    cd.text((tx, ty), t, font=f, fill=c)
    ty += 58 if t else 24
canvas.save(OUT, quality=90)
