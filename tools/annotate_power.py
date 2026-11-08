"""전원 기준 그림: SMPS 단자·선 색 + 보드에서 전압 재는 곳.
사용: python tools/annotate_power.py analysis/power_reference.jpg
재료: photos/case/225522_PSU-terminals.jpg (단자 표기), photos/overview/front/202813_front-flat_layout-ref.jpg (보드)
선 색은 2026-11-06 실물 확인 (docs/05 전원 절).
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHT = (0, 0, 0), (255, 255, 255)
RED, ORG, GRY, BLU, GRN = (220, 20, 20), (245, 120, 0), (60, 60, 60), (30, 80, 230), (0, 140, 60)

# --- SMPS 사진 (표시 좌표 1500x2000 기준으로 잘라 씀) ---
psu = ImageOps.exif_transpose(Image.open("photos/case/225522_PSU-terminals.jpg")).convert("RGB")
psu = psu.resize((1500, 2000), Image.LANCZOS).crop((380, 300, 1200, 1400))  # 820x1100
PX, PY = 20, 120
# 단자 나사 위치 (1500x2000 좌표)
terms = [
    ("FG", (670, 465), GRY, "FG (외함 접지)", ""),
    ("AC", (680, 600), RED, "AC 입력 220V", "만지지 말 것"),
    ("AC", (670, 735), RED, "AC 입력 220V", "만지지 말 것"),
    ("+12V", (665, 845), RED, "+12V", "빨강 선"),
    ("+5V", (665, 955), ORG, "+5V", "주황 선 (굵은 선, 검정 수축튜브)"),
    ("GND", (655, 1050), BLK, "GND", "검정 선"),
    ("-5V", (650, 1155), BLU, "-5V", "파랑 선"),
    ("-12V", (640, 1250), GRN, "-12V", "초록 선"),
]

board = ImageOps.exif_transpose(Image.open("photos/overview/front/202813_front-flat_layout-ref.jpg")).convert("RGB")
board = board.resize((board.width // 2, board.height // 2), Image.LANCZOS).crop((0, 0, 520, 520))  # 왼쪽 위: J1·슬롯1
board = board.resize((780, 780), Image.LANCZOS)
S = 780 / 520
BX, BY = 20 + 820 + 40 + 560, 120

W, H = BX + 780 + 20, 120 + 1100 + 330
cv = Image.new("RGB", (W, H), WHT)
cv.paste(psu, (PX, PY))
cv.paste(board, (BX, BY))
d = ImageDraw.Draw(cv)

def tag(x, y, text, col, size=26, fg=WHT):
    l, t, r, b = d.textbbox((0, 0), text, font=F(size))
    d.rectangle((x - 6, y - 4 + t, x + (r - l) + 6, y + b + 8), fill=col, outline=BLK, width=1)
    d.text((x, y), text, font=F(size), fill=fg)
    return x + (r - l) + 6

tx = PX + 820 + 30
for name, (x, y), col, lab, sub in terms:
    cx, cy = PX + x - 380, PY + y - 300
    d.ellipse((cx - 30, cy - 30, cx + 30, cy + 30), outline=col, width=6)
    d.line((cx + 30, cy, tx - 10, cy), fill=col, width=4)
    e = tag(tx, cy - 20, lab, col, 26, WHT if col != ORG else BLK)
    if sub:
        d.text((e + 14, cy - 16), sub, font=F(20), fill=col if col != BLK else GRY)

# --- 보드 쪽: J1, 슬롯1 측정 핀 (bom 배치 좌표 = 1/2 크기 좌표) ---
def B(x, y):
    return BX + x * S, BY + y * S
x0, y0 = B(12, 65); x1, y1 = B(60, 250)
d.rectangle((x0, y0, x1, y1), outline=ORG, width=6)
tag(x1 + 12, y0 + 10, "J1 전원 커넥터 (SMPS 5가닥 들어옴)", ORG, 22, BLK)
for (px, py), col, lab in (((77, 22), BLK, "26 GND"), ((106, 22), ORG, "25 +5V")):
    cx, cy = B(px, py)
    d.ellipse((cx - 13, cy - 13, cx + 13, cy + 13), outline=col, width=5)
cx, cy = B(106, 22)
tag(cx + 30, cy - 18, "슬롯1 맨 위: 왼쪽 26 GND · 오른쪽 25 +5V", RED, 22)

# 제목·표
d.text((20, 14), "전원 기준 그림 — SMPS 단자, 선 색, 보드에서 재는 곳", font=F(40), fill=BLK)
d.text((20, 68), "주의: 이 기계는 빨강 = +12V, 주황 = +5V (일반 관례와 다름). 전원 교체·선 연결 때 반드시 이 그림으로 확인.", font=F(24), fill=RED)

y = PY + 1100 + 20
rows = [
    ("전압", "SMPS 단자 선 색", "보드에서 재는 곳 (검정 프로브 = 슬롯 26번 GND)", "정상 범위"),
    ("+5V", "주황", "슬롯 25번, U30 핀 8", "4.75–5.25V (지금 4.8V, 하한 근처)"),
    ("+12V", "빨강", "슬롯 50번", "약 +12V (확인)"),
    ("-5V", "파랑", "슬롯 34번", "미측정"),
    ("-12V", "초록", "슬롯 33번", "미측정"),
    ("GND", "검정", "슬롯 26번, U30 핀 1, U72 핀 7", "-"),
]
cols = [20, 200, 420, 1150]
for i, row in enumerate(rows):
    f = F(24) if i == 0 else FR(24)
    for c, txt in zip(cols, row):
        d.text((c, y + i * 44), txt, font=f, fill=BLK)
    d.line((20, y + i * 44 + 38, W - 20, y + i * 44 + 38), fill=(200, 200, 200), width=1)
d.text((20, y + len(rows) * 44 + 8), "슬롯 핀 방향: 앞면 슬롯이 위일 때 왼쪽 줄 26(위)→50(아래), 오른쪽 줄 25(위)→1(아래). 슬롯1 = 왼쪽 끝. SMPS: 상표 DE, 한국산, AC 90–130/180–260V 겸용", font=FR(20), fill=GRY)
cv.save(OUT, quality=90)
print(cv.size)
