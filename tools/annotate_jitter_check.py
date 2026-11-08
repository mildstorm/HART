"""화면 지글거림 점검 위치 그림 (앞면 기준 사진 202813).
사용: python tools/annotate_jitter_check.py analysis/jitter_check_points.jpg
좌표는 data/bom.csv 배치 좌표(= 202813 사진의 1/2 크기 좌표)를 따름.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
im = ImageOps.exif_transpose(Image.open("photos/overview/front/202813_front-flat_layout-ref.jpg")).convert("RGB")
im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)  # bom 좌표와 같은 크기
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
LM, TOP, RM, BOT = 20, 110, 430, 230
cv = Image.new("RGB", (LM + im.width + RM, TOP + im.height + BOT), "white")
cv.paste(im, (LM, TOP))
d = ImageDraw.Draw(cv)
P = lambda x, y: (LM + x, TOP + y)
RED, BLU, ORG, MAG, GRN, BLK = (230, 20, 20), (30, 100, 240), (255, 130, 0), (220, 0, 200), (0, 150, 60), (0, 0, 0)

def label(xy, text, col, size=26, anchor_pt=None):
    l, t, r, b = d.textbbox((0, 0), text, font=F(size))
    x, y = xy
    d.rectangle((x - 8, y - 5, x + (r - l) + 8, y + (b - t) + 12), fill="white", outline=col, width=3)
    d.text((x, y), text, font=F(size), fill=col)
    if anchor_pt:
        d.line((x - 8, y + 15, *anchor_pt), fill=col, width=4)

def rect(x0, y0, x1, y1, col, w=6):
    d.rectangle((*P(x0, y0), *P(x1, y1)), outline=col, width=w)

def ring(x, y, col, r=11):
    c = P(x, y); d.ellipse((c[0] - r, c[1] - r, c[0] + r, c[1] + r), outline=col, width=5)

# ① +5V: 슬롯1 맨 위 두 핀 (왼쪽 줄 위 = 26 GND, 오른쪽 줄 위 = 25 +5V)
ring(77, 22, BLK); ring(106, 22, RED)
label((LM + im.width + 20, TOP + 10), "① +5V 재는 곳 (슬롯1 맨 위)", RED, 26, P(106, 22))
d.text((LM + im.width + 20, TOP + 55), "검정 프로브 = 왼쪽 핀 (26, GND)\n빨간 프로브 = 오른쪽 핀 (25, +5V)\nDC: 4.75V 이상\nAC: 거의 0V (0.1V 넘으면 잡음)", font=F(20), fill=BLK, spacing=6)

# ② 영상 단자 J7 (VIDEO RCA)
rect(850, 0, 912, 58, BLU)
label((LM + im.width + 20, TOP + 220), "② 영상 단자 (VIDEO)", BLU, 26, P(912, 30))
d.text((LM + im.width + 20, TOP + 265), "케이블을 살짝 흔들어 보기", font=F(20), fill=BLK)

# ③ 전원 커넥터 J1
rect(12, 65, 60, 250, ORG)
label((LM + im.width + 20, TOP + 330), "③ 전원 들어오는 곳 (J1)", ORG, 26, P(60, 160))
d.text((LM + im.width + 20, TOP + 375), "케이블 꽉 꽂혔는지, 전원부(SMPS)\n겉면이 뜨거운지 손등으로", font=F(20), fill=BLK, spacing=6)

# ④ 비디오 칩 영역 U65–U71, U80–U82
rect(362, 1170, 1005, 1620, MAG)  # 비디오 칩 10개(U65–U71, U80–U82)를 사각형 하나로
label((LM + im.width + 20, TOP + 1240), "④ 비디오 쪽 칩", MAG, 26, P(1005, 1300))
d.text((LM + im.width + 20, TOP + 1285), "U65 VD5 · U66 · U67 · U68 6116\n· U69 · U70 CHR P4 · U71\n아래 줄 U80–U82\n뜨거운 칩 찾기, 볼펜으로 톡톡", font=F(20), fill=BLK, spacing=6)

# 참고: 두 CPU
rect(85, 705, 445, 830, GRN, 4)
label((LM + im.width + 20, TOP + 760), "참고: 메인 CPU U30", GRN, 22, P(445, 770))
rect(10, 1245, 372, 1370, GRN, 4)
label((LM + im.width + 20, TOP + 1110), "참고: 한글 CPU U64", GRN, 22, P(372, 1310))

d.text((20, 14), "화면 지글거림 점검 위치 (앞면, 확장 슬롯이 위)", font=F(36), fill=BLK)
d.text((20, 62), "지글거리는 동안 ① → ② → ③ → ④ 순서로. 손등은 아주 잠깐만.", font=F(24), fill=BLK)
y = TOP + im.height + 16
d.text((20, y), "① +5V가 4.75V 아래거나 AC가 0.1V 넘음 → 전원부 문제", font=F(24), fill=RED)
d.text((20, y + 40), "② 흔들 때 화면이 변함 → 영상 케이블·단자 접촉", font=F(24), fill=BLU)
d.text((20, y + 80), "④ 두드릴 때 화면이 변하는 칩 → 그 칩 소켓 접촉 (전원 끄고 꾹 누르기)", font=F(24), fill=MAG)
d.text((20, y + 120), "모두 정상인데 지글거림 → 모니터 쪽 (V-HOLD·H-HOLD 조정, 다른 모니터로 비교)", font=F(24), fill=BLK)
# 아래에 비디오 칩 확대(④ 상세)를 붙여 한 장으로 (tools/annotate_video_chips.py 출력)
import subprocess, tempfile, os
tmp = os.path.join(tempfile.gettempdir(), "_video_chips.jpg")
subprocess.run([sys.executable, "-I", "tools/annotate_video_chips.py", tmp], check=True, capture_output=True)
vz = Image.open(tmp).convert("RGB")
vz = vz.resize((cv.width, int(vz.height * cv.width / vz.width)), Image.LANCZOS)
full = Image.new("RGB", (cv.width, cv.height + 30 + vz.height), "white")
full.paste(cv, (0, 0))
ImageDraw.Draw(full).line((0, cv.height + 14, cv.width, cv.height + 14), fill=(180, 180, 180), width=3)
full.paste(vz, (0, cv.height + 30))
os.remove(tmp)
cv = full
cv.save(OUT, quality=88)
print(cv.size)
