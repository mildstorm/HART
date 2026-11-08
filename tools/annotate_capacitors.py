"""의심 커패시터 위치 그림 (앞면 기준 사진 202813, bom 1/2 좌표).
사용: python tools/annotate_capacitors.py analysis/capacitor_suspects.jpg
보드에 큰 전해 커패시터는 없음. 주황 납작한 것 = 세라믹 디스크(바이패스, 고장 드묾).
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
im = ImageOps.exif_transpose(Image.open("photos/overview/front/202813_front-flat_layout-ref.jpg")).convert("RGB")
im = im.resize((im.width // 2, im.height // 2), Image.LANCZOS)
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
LM, TOP, RM, BOT = 20, 110, 470, 200
cv = Image.new("RGB", (LM + im.width + RM, TOP + im.height + BOT), "white")
cv.paste(im, (LM, TOP))
d = ImageDraw.Draw(cv)
P = lambda x, y: (LM + x, TOP + y)
RED, ORG, GRY, BLK = (220, 20, 20), (235, 120, 0), (110, 110, 110), (0, 0, 0)

items = [  # (x, y, r, 색, 번호, 제목, 설명, 라벨 y)
    (106, 858, 30, RED, "C1", "노란 탄탈 (U30 왼쪽 아래)", "메인 CPU 바로 옆. 리셋·전원 쪽 후보", 820),
    (940, 103, 26, RED, "C2", "주황 탄탈 (LM339 옆, Z80 오른쪽)", "LM339 비교기와 저항 묶음 옆.\n리셋 타이밍 후보 (추정)", 60),
    (965, 1248, 26, GRY, "C3", "초록 원통 (CHRP4 오른쪽 위)", "커패시터 아님: 코일(인덕터) 추정.\n0.3Ω = 정상 (2026-11-08 측정·사진)", 1180),
    (42, 1420, 34, ORG, "T1", "트리머 (U64 왼쪽, 수정 발진 옆)", "14MHz 발진 조정용. 클럭이 늦게\n시작하는 문제와 관련 가능 (추정)", 1400),
    (922, 560, 40, GRY, "참고", "연두 납작 4개 (NE558 위)", "세라믹, 게임 패들 타이밍용. 무관", 520),
]
tx = LM + im.width + 20
for x, y, r, col, no, title, desc, ly in items:
    cx, cy = P(x, y)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=6)
    l, t, rr, b = d.textbbox((0, 0), f"{no} {title}", font=F(22))
    d.rectangle((tx - 6, TOP + ly - 4, tx + (rr - l) + 6, TOP + ly + 30), fill=col)
    d.text((tx, TOP + ly - 2), f"{no} {title}", font=F(22), fill="white")
    d.text((tx, TOP + ly + 38), desc, font=F(18), fill=BLK, spacing=4)
    d.line((cx + r, cy, tx - 8, TOP + ly + 13), fill=col, width=3)

d.text((20, 14), "의심 커패시터 위치 (앞면, 확장 슬롯이 위)", font=F(36), fill=BLK)
d.text((20, 62), "큰 전해 커패시터는 없음. 주황 납작한 것들 = 세라믹(바이패스), 고장 드묾. 빨강 = 탄탈(오래되면 누설·단락 잦음)", font=F(20), fill=BLK)
y = TOP + im.height + 16
for i, (t, c) in enumerate([
    ("확인 (전원 끄고, Ω): 각 커패시터 두 다리 사이 저항 → 수십 Ω 이하면 단락·누설 의심", BLK),
    ("확인 (전원 끄고, 도통): C1·C2 다리 ↔ U30 핀 40(RES) → 연결되면 그게 리셋 커패시터", RED),
    ("켜 둔 채 손등으로: 탄탈이 뜨거우면 거의 확실히 불량 (바로 끄기)", RED),
    ("역할은 사진으로 본 추정. 회로 연결은 측정으로 확인해야 함", GRY),
]):
    d.text((20, y + i * 40), t, font=F(21), fill=c)

# --- 아래: C2 확대와 재는 방법 (같은 그림에 붙임) ---
z = ImageOps.exif_transpose(Image.open("photos/zoom/front/20261108_215334_C2-tantalum_STC-22uF-16V.jpg")).convert("RGB")
z = z.resize((2000, 1500), Image.LANCZOS).crop((300, 250, 1700, 1250))  # 1400x1000
z = z.resize((cv.width - 40, int(1000 * (cv.width - 40) / 1400)), Image.LANCZOS)
ZS = (cv.width - 40) / 1400
ZT = 70
full = Image.new("RGB", (cv.width, cv.height + ZT + z.height + 330), "white")
full.paste(cv, (0, 0))
oy = cv.height + ZT
full.paste(z, (20, oy))
d = ImageDraw.Draw(full)
d.line((0, cv.height + 10, cv.width, cv.height + 10), fill=(180, 180, 180), width=3)
d.text((20, cv.height + 20), "C2 확대 (STC 22µF 16V 탄탈, LM339·트랜지스터 C1815 옆) — 재는 곳", font=F(30), fill=BLK)
ZP = lambda x, y: (20 + (x - 300) * ZS, oy + (y - 250) * ZS)
BLU = (30, 90, 230)
for (x, y), lab in (((705, 770), "다리 A"), ((822, 846), "다리 B")):
    cx, cy = ZP(x, y)
    d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=BLU, width=6)
    l, t, r, b = d.textbbox((0, 0), lab, font=F(24))
    tx = cx - (r - l) - 40 if lab.endswith("A") else cx + 34
    d.rectangle((tx - 6, cy - 18 + t, tx + (r - l) + 6, cy - 18 + b + 6), fill=BLU)
    d.text((tx, cy - 18), lab, font=F(24), fill="white")
y = oy + z.height + 16
for i, (t, c) in enumerate([
    ("다리 A·B = 탄탈 몸통 아래 두 납땜 구멍 (사진상 위치, 몸통에 가려 추정)", GRY),
    ("① 전원 끄고 Ω: A ↔ B → 삐 소리 / 몇 Ω 이하면 단락 (교체). 숫자가 천천히 올라가면 정상", BLK),
    ("② 전원 끄고 도통: A ↔ U30 40번, B ↔ U30 40번 → 삐 나면 리셋 회로 커패시터, 둘 다 조용하면 리셋과 무관", RED),
    ("③ 전원 켜고 DC V: 검정 = 슬롯 26번(GND), 빨강 = A 다음 B → 전압이 높은 쪽 = + 다리 (교체할 때 방향)", BLU),
    ("U30 40번 = 메인 CPU 위 줄 맨 왼쪽 핀 (analysis/u30_pins.jpg)", GRY),
]):
    d.text((20, y + i * 42), t, font=F(22), fill=c)
cv = full
cv.save(OUT, quality=88)
print(cv.size)
