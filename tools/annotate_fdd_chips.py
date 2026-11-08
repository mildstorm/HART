"""내장 FDD 컨트롤러 칩 U16–U20과 드라이브 단자 위치 그림.
사용: python tools/annotate_fdd_chips.py photos/zoom/front/211032_J2-J3-headers_U16-U20.jpg analysis/fdd_u16_u20.jpg
사진은 보드를 90° 돌려 찍은 것 (슬롯이 오른쪽에 가로로 보임).
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
im = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
im = im.crop((0, 1150, 3000, 3700)).resize((1500, 1275), Image.LANCZOS)  # 위쪽 바닥 부분 잘라냄
def P(x, y):  # 1500x2000 표시 좌표 → 잘라낸 그림 좌표
    return x, y - 575
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
TOP, BOT = 90, 150
cv = Image.new("RGB", (im.width, im.height + TOP + BOT), "white")
cv.paste(im, (0, TOP))
d = ImageDraw.Draw(cv)
RED, YEL, BLK, WHT = (230, 20, 20), (255, 200, 0), (0, 0, 0), (255, 255, 255)

def box(x0, y0, x1, y1, col, label, sub):
    a = P(x0, y0); b = P(x1, y1)
    d.rectangle((a[0], a[1] + TOP, b[0], b[1] + TOP), outline=col, width=6)
    t = f"{label}  {sub}"
    l, t0, r, bb = d.textbbox((0, 0), t, font=F(30))
    tx, ty = b[0] + 20, (a[1] + b[1]) / 2 + TOP - 20
    if tx + (r - l) > cv.width - 10:
        tx = cv.width - (r - l) - 20
    d.rectangle((tx - 8, ty - 4, tx + (r - l) + 8, ty + (bb - t0) + 12), fill=WHT, outline=col, width=3)
    d.text((tx, ty), t, font=F(30), fill=col)

box(185, 845, 605, 995, RED, "U16", "74LS323 (데이터 레지스터)")
box(285, 1020, 610, 1165, RED, "U17", "82S129 PROM")
box(285, 1185, 610, 1335, RED, "U18", "PROM 라벨 M")
box(295, 1345, 615, 1495, RED, "U19", "74LS174 (상태 래치)")
box(300, 1500, 615, 1655, RED, "U20", "74LS259 (모터·헤드)")
for x0, x1 in ((240, 705), (780, 1250)):
    a = P(x0, 680); b = P(x1, 770)
    d.rectangle((a[0], a[1] + TOP, b[0], b[1] + TOP), outline=YEL, width=6)
d.text((420, P(0, 640)[1] + TOP - 40), "드라이브 20핀 단자 2개 (J2·J3)", font=F(30), fill=(200, 140, 0))

d.text((16, 12), "내장 FDD 컨트롤러 칩 U16–U20 (앞면, 보드를 90° 돌려 찍은 사진 211032)", font=F(34), fill=BLK)
d.text((16, 54), "U30(메인 6502) 오른쪽 세로 줄, 확장 슬롯 왼쪽. 칩 이름은 BOM(docs/03) 기준", font=F(22), fill=BLK)
y = TOP + im.height + 14
d.text((16, y), "드라이브 연결 후 오래 켜 두면 화면이 지글거릴 때: 이 다섯 칩과 드라이브 단자 주변을", font=F(26), fill=BLK)
d.text((16, y + 40), "손등으로 잠깐 대 보고 유난히 뜨거운 칩이 있는지 확인. U20은 드라이브 모터·헤드 신호를 내보냄 (추정)", font=F(26), fill=BLK)
d.text((16, y + 80), "칩 역할은 Disk II 카드 구성에서 추정한 것 (U16·U19·U20 형명은 확인, 역할은 추정)", font=F(22), fill=(90, 90, 90))
cv.save(OUT, quality=90)
print(cv.size)
