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
for (x, y), lab in (((705, 770), "다리 A (-)"), ((822, 846), "다리 B (+)")):
    cx, cy = ZP(x, y)
    d.ellipse((cx - 22, cy - 22, cx + 22, cy + 22), outline=BLU, width=6)
    l, t, r, b = d.textbbox((0, 0), lab, font=F(24))
    tx = cx - (r - l) - 40 if "A" in lab else cx + 34
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

# --- 맨 아래: C2 뒷면 위치 (앞면·뒷면 정합 data/front_back_registration.json, 평균 오차 약 2px) ---
import json
reg = json.load(open("data/front_back_registration.json", encoding="utf-8"))
CF = reg["front_to_back"]
def f2b(x, y):
    u, v = x / 1000, y / 1000
    t = [1, u, v, u * u, u * v, v * v, u ** 3, u * u * v, u * v * v, v ** 3]
    return sum(c[0] * w for c, w in zip(CF, t)), sum(c[1] * w for c, w in zip(CF, t))
fr = ImageOps.exif_transpose(Image.open(reg["front"])).convert("RGB")
bk = ImageOps.exif_transpose(Image.open(reg["back"])).convert("RGB")
FX, FY, W0, H0 = 1730, 120, 300, 250          # 앞면 창 (기준 사진 픽셀)
bx, by = f2b(FX + W0 / 2, FY + H0 / 2)
BX, BY = int(bx) - W0 // 2, int(by) - H0 // 2
K = (cv.width - 60) / 2 / W0
fcrop = fr.crop((FX, FY, FX + W0, FY + H0)).resize((int(W0 * K), int(H0 * K)), Image.LANCZOS)
bcrop = bk.crop((BX, BY, BX + W0, BY + H0)).resize((int(W0 * K), int(H0 * K)), Image.LANCZOS)
SEC = 90
full = Image.new("RGB", (cv.width, cv.height + SEC + fcrop.height + 300), "white")
full.paste(cv, (0, 0))
oy = cv.height + SEC
full.paste(fcrop, (20, oy)); full.paste(bcrop, (40 + fcrop.width, oy))
d = ImageDraw.Draw(full)
d.line((0, cv.height + 10, cv.width, cv.height + 10), fill=(180, 180, 180), width=3)
d.text((20, cv.height + 20), "C2 위치: 왼쪽 = 앞면, 오른쪽 = 뒷면 (같은 자리, 뒷면은 좌우 반전)", font=F(28), fill=BLK)
d.text((20, cv.height + 56), "뒷면 위치는 앞·뒷면 사진 정합으로 옮긴 것 (평균 오차 약 2px)", font=F(20), fill=GRY)
GRN2 = (0, 170, 80)
# 앞면 표시: C2 몸통, LM339 맨 위 두 핀(기준점)
def fp(x, y): return 20 + (x - FX) * K, oy + (y - FY) * K
def bp(x, y): return 40 + fcrop.width + (x - BX) * K, oy + (y - BY) * K
cx, cy = fp(1882, 208)
d.ellipse((cx - 40, cy - 40, cx + 40, cy + 40), outline=RED, width=6)
d.text((cx - 30, cy - 80), "C2", font=F(28), fill=RED)
for (x, y) in ((1900, 266), (1802, 266)):
    px, py = fp(x, y); d.ellipse((px - 12, py - 12, px + 12, py + 12), outline=GRN2, width=4)
    qx, qy = f2b(x, y); px, py = bp(qx, qy); d.ellipse((px - 16, py - 16, px + 16, py + 16), outline=GRN2, width=4)
d.text(fp(1790, 300), "LM339 맨 위 핀 (기준)", font=F(20), fill=GRN2)
# 뒷면: C2 다리 납땜점 2개 (몸통 아래 패드, 정합 사진에서 판독)
BLU = (30, 90, 230)
legs = [(BX + 565 / 4, BY + 380 / 4, "① +"), (BX + 700 / 4, BY + 380 / 4, "② -")]
for x, y, lab in legs:
    px, py = bp(x, y)
    d.ellipse((px - 22, py - 22, px + 22, py + 22), outline=BLU, width=6)
    d.text((px - 34, py + 26), lab, font=F(22), fill=BLU)
qx, qy = bp(*f2b(1882, 208))
d.text((qx - 20, qy - 70), "C2 자리", font=F(22), fill=RED)
y = oy + fcrop.height + 14
for i, (t, c) in enumerate([
    ("파랑 ①·② = 뒷면 C2 다리 납땜점 (도통 확인: 앞면 A = 뒷면 ②, 앞면 B = 뒷면 ①). 극성: ① = +, ② = - (몸통 + 표시, 육안 확인)", BLU),
    ("극성 먼저 (전원 켜고, DC V): 검정 = 슬롯 26번(GND), 빨강 = ① 다음 ② → 전압 높은 쪽 = +다리, 낮은(0V) 쪽 = -다리", RED),
    ("Ω 잴 때 (전원 끄고): 빨간 프로브 = +다리, 검정 프로브 = -다리 (테스터 Ω 모드에서 빨강이 + 쪽). 반대로 대도 고장나진 않음", RED),
    ("뒷면에서 재기: ① ↔ ② Ω(단락 확인), ①·② 각각 ↔ U30 40번 도통(리셋 연결 확인, 극성 무관)", BLK),
    ("초록 = LM339 맨 위 두 핀 (앞·뒤 같은 핀, 위치 맞추는 기준)", GRN2),
]):
    d.text((20, y + i * 40), t, font=F(22), fill=c)
cv = full

# --- 맨 아래: 뒷면 위쪽 띠 전체 — 극성 재는 곳 (C2 ①②, 슬롯1 핀 26 GND) ---
SX0, SY0, SX1, SY1 = 0, 0, 2121, 420                  # 뒷면 기준 사진 위쪽 띠
ks = (cv.width - 40) / (SX1 - SX0)
strip = bk.crop((SX0, SY0, SX1, SY1)).resize((int((SX1 - SX0) * ks), int((SY1 - SY0) * ks)), Image.LANCZOS)
full = Image.new("RGB", (cv.width, cv.height + 100 + strip.height + 260), "white")
full.paste(cv, (0, 0))
oy = cv.height + 100
full.paste(strip, (20, oy))
d = ImageDraw.Draw(full)
d.line((0, cv.height + 10, cv.width, cv.height + 10), fill=(180, 180, 180), width=3)
d.text((20, cv.height + 20), "C2 극성 재기 — 뒷면에서 (뒷면 위쪽 띠, 오른쪽 = 슬롯1, 왼쪽 위 = C2)", font=F(28), fill=BLK)
d.text((20, cv.height + 58), "전원 켜고 테스터 DC V. 보드를 뒤집어 뒷면에서 재도 됨", font=F(20), fill=GRY)
S = lambda x, y: (20 + (x - SX0) * ks, oy + (y - SY0) * ks)
# 슬롯1 핀 26 (뒷면: 슬롯1 오른쪽 줄 맨 위, slots_pin40_back 기준 핀 40 (1930,575)에서 14칸 위)
gx, gy = S(1930, 93)
d.ellipse((gx - 14, gy - 14, gx + 14, gy + 14), outline=BLK, width=5)
d.rectangle((gx - 250, gy + 22, gx + 10, gy + 56), fill=BLK)
d.text((gx - 244, gy + 24), "검정 프로브: 슬롯1 핀 26 (GND)", font=F(20), fill="white")
for x, y, lab in legs:
    px, py = S(x, y)
    d.ellipse((px - 12, py - 12, px + 12, py + 12), outline=BLU, width=5)
c1x, c1y = S(*legs[0][:2]); c2x, c2y = S(*legs[1][:2])
d.rectangle((c1x - 10, c1y + 20, c1x + 330, c1y + 54), fill=BLU)
d.text((c1x - 4, c1y + 22), "빨간 프로브: ① 다음 ② (C2 다리)", font=F(20), fill="white")
d.text((c1x - 20, c1y - 40), "①", font=F(22), fill=BLU); d.text((c2x + 6, c2y - 40), "②", font=F(22), fill=BLU)
y = oy + strip.height + 14
for i, (t, c) in enumerate([
    ("① 전압 > ② 전압 → ① = +, ② = -   /   ② 전압 > ① 전압 → ② = +, ① = -", RED),
    ("한쪽이 0V 근처면 그쪽이 - (GND 쪽). 음수가 나오면 그 다리가 -", BLK),
    ("극성이 정해지면: Ω 잴 때 빨강 → +다리, 검정 → -다리. 교체할 때 새 탄탈의 + 를 같은 구멍에", BLK),
    ("①② 위치 확인됨 (2026-11-08 도통). 앞면 다리 A = 뒷면 ②, 앞면 다리 B = 뒷면 ①", GRY),
]):
    d.text((20, y + i * 40), t, font=F(22), fill=c)
cv = full

# --- 맨 아래: C1 앞면·뒷면 (U30 왼쪽 아래 탄탈) ---
CB = reg["back_to_front"]
def b2f(x, y):
    u, v = x / 1000, y / 1000
    t = [1, u, v, u * u, u * v, v * v, u ** 3, u * u * v, u * v * v, v ** 3]
    return sum(c[0] * w for c, w in zip(CB, t)), sum(c[1] * w for c, w in zip(CB, t))
FX, FY = 100, 1600
bx, by = f2b(FX + W0 / 2, FY + H0 / 2)
BX, BY = int(bx) - W0 // 2, int(by) - H0 // 2
fcrop = fr.crop((FX, FY, FX + W0, FY + H0)).resize((int(W0 * K), int(H0 * K)), Image.LANCZOS)
bcrop = bk.crop((BX, BY, BX + W0, BY + H0)).resize((int(W0 * K), int(H0 * K)), Image.LANCZOS)
full = Image.new("RGB", (cv.width, cv.height + SEC + fcrop.height + 260), "white")
full.paste(cv, (0, 0))
oy = cv.height + SEC
full.paste(fcrop, (20, oy)); full.paste(bcrop, (40 + fcrop.width, oy))
d = ImageDraw.Draw(full)
d.line((0, cv.height + 10, cv.width, cv.height + 10), fill=(180, 180, 180), width=3)
d.text((20, cv.height + 20), "C1 (STC 22µF 16V, U30 왼쪽 아래): 왼쪽 = 앞면, 오른쪽 = 뒷면", font=F(28), fill=BLK)
d.text((20, cv.height + 56), "극성: 아래 다리 = + (사용자 육안 확인). 뒷면 위치는 앞·뒷면 정합 (오차 약 2px)", font=F(20), fill=GRY)
def fp(x, y): return 20 + (x - FX) * K, oy + (y - FY) * K
def bp(x, y): return 40 + fcrop.width + (x - BX) * K, oy + (y - BY) * K
C1LEGS = [((BX + 665 / 4, BY + 415 / 4), "-", BLK), ((BX + 665 / 4, BY + 565 / 4), "+", RED)]   # 뒷면 납땜점
for (x, y), sgn, col in C1LEGS:
    px, py = bp(x, y)
    d.ellipse((px - 22, py - 22, px + 22, py + 22), outline=col, width=6)
    d.text((px + 28, py - 18), sgn, font=F(34), fill=col)
    qx, qy = fp(*b2f(x, y))
    d.ellipse((qx - 16, qy - 16, qx + 16, qy + 16), outline=col, width=5)
    d.text((qx - 50, qy - 20), sgn, font=F(34), fill=col)
rx, ry = bp(BX + 450 / 4, BY + 555 / 4)
d.text((rx - 60, ry + 26), "저항 R1 다리", font=F(18), fill=GRY)
y = oy + fcrop.height + 14
for i, (t, c) in enumerate([
    ("빨강 + = 아래 다리, 검정 - = 위 다리 (앞면·뒷면 같은 표시)", RED),
    ("뒷면: - 다리는 굵은 선으로 R1(1kΩ) 다리·U30 핀 1(GND)과 이어짐 → +5V 바이패스 커패시터로 보임 (리셋과 무관 추정)", BLK),
    ("확인: 전원 켜고 DC V (검정 = 슬롯 26) → + 다리 약 5V, - 다리 0V 이면 +5V 바이패스 확정", BLK),
    ("단락 검사: 전원 끄고 방전 후 + ↔ - 도통 → 계속 삐 = 단락(+5V가 GND에 붙음, 보드 안 켜짐)", BLK),
]):
    d.text((20, y + i * 40), t, font=F(21), fill=c)
cv = full
cv.save(OUT, quality=88)
print(cv.size)
