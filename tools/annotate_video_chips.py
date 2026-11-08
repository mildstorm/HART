"""비디오 쪽 칩 확대 그림 (화면 지글거림 점검용, 앞면 기준 사진 202813).
단독 파일로 저장하지 않음: tools/annotate_jitter_check.py 가 불러서 analysis/jitter_check_points.jpg 아래쪽에 붙임.
좌표는 data/bom.csv 배치 좌표(202813의 1/2 크기)를 씀.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
im = ImageOps.exif_transpose(Image.open("photos/overview/front/202813_front-flat_layout-ref.jpg")).convert("RGB")
im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
X0, Y0, X1, Y1, S = 330, 1120, 1010, 1645, 2.2
im = im.crop((X0, Y0, X1, Y1)).resize((int((X1 - X0) * S), int((Y1 - Y0) * S)), Image.LANCZOS)
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
TOP, BOT = 120, 330
cv = Image.new("RGB", (im.width, im.height + TOP + BOT), "white")
cv.paste(im, (0, TOP))
d = ImageDraw.Draw(cv)
P = lambda x, y: ((x - X0) * S, (y - Y0) * S + TOP)
MAG, BLU, BLK, WHT = (220, 0, 200), (30, 90, 230), (0, 0, 0), (255, 255, 255)

chips = [  # ref, x0,y0,x1,y1, 이름, 색
    ("U65", 365, 1185, 460, 1425, "VD5 롬", MAG),
    ("U66", 480, 1205, 535, 1370, "74LS374", MAG),
    ("U67", 545, 1205, 600, 1370, "74LS245", MAG),
    ("U68", 610, 1190, 710, 1420, "6116 메모리", MAG),
    ("U69", 725, 1205, 780, 1370, "74LS273", MAG),
    ("U70", 795, 1155, 890, 1390, "CHR P4 롬", MAG),
    ("U71", 910, 1230, 965, 1375, "74LS166", MAG),
    ("U80", 420, 1400, 480, 1550, "74LS257", BLU),
    ("U81", 620, 1400, 680, 1550, "74LS257", BLU),
    ("U82", 690, 1400, 745, 1550, "74LS393", BLU),
]
# bom 좌표는 대략값이라 이 확대 사진에서 칩 몸체를 눈으로 맞춘 픽셀 좌표로 덮어씀
PIX = {"U65": (95, 390, 335, 955), "U66": (340, 425, 450, 825), "U67": (480, 425, 595, 825),
       "U68": (685, 395, 840, 905), "U69": (885, 425, 1000, 825), "U70": (1125, 315, 1340, 895),
       "U71": (1345, 425, 1470, 825), "U80": (200, 960, 335, 1250), "U81": (690, 905, 790, 1250),
       "U82": (835, 905, 945, 1250)}
for ref, x0, y0, x1, y1, name, col in chips:
    px = PIX[ref]
    a, b = (px[0], px[1]), (px[2], px[3])  # 화면 좌표 (TOP 포함)
    d.rectangle((a[0], a[1], b[0], b[1]), outline=col, width=6)
    cx = (a[0] + b[0]) / 2
    l, t, r, bb = d.textbbox((0, 0), ref, font=F(30))
    tx, ty = cx - (r - l) / 2, a[1] + 8
    d.rectangle((tx - 6, ty - 2 + t, tx + (r - l) + 6, ty + bb + 6), fill=col)
    d.text((tx, ty), ref, font=F(30), fill=WHT)

d.text((16, 12), "화면 지글거림 점검: 비디오 쪽 칩 (보드 아래쪽, 확대)", font=F(38), fill=BLK)
d.text((16, 62), "앞면, 확장 슬롯이 위인 방향. 왼쪽 밖 = 한글 CPU U64, 오른쪽 끝 = 보드 오른쪽 가장자리", font=F(24), fill=BLK)
y = TOP + im.height + 16
lines = [
    ("분홍 = 화면 글자를 만드는 칩 7개 (U65–U71). 큰 칩 U65(라벨 VDS)·U70(라벨 CHRP4)·U68(가운데 큰 칩)이 찾기 쉬운 기준", MAG),
    ("파랑 = 아래 줄 칩 3개 (U80–U82). 비디오 카운터·키보드 읽기 추정", BLU),
    ("1. 지글거릴 때 손등으로 칩을 하나씩 잠깐 대 보기 → 유난히 뜨거운 칩 찾기", BLK),
    ("2. 플라스틱 볼펜 뒤쪽으로 칩을 하나씩 톡톡 → 화면이 더 지글거리거나 멈추는 칩 찾기", BLK),
    ("3. 그런 칩이 있으면: 전원 끄고 그 칩을 엄지로 수직으로 꾹 누르기 (소켓 접촉)", BLK),
    ("금속 드라이버로 두드리지 말 것 (합선 위험). 칩 역할은 추정, 위치는 부품표(data/bom.csv) 기준", (90, 90, 90)),
]
for i, (t, c) in enumerate(lines):
    d.text((16, y + i * 48), t, font=F(24) if i < 5 else FR(22), fill=c)
cv.save(OUT, quality=90)
print(cv.size)
