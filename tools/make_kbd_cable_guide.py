"""키보드 케이블 꽂는 방향 정하기 안내 그림 (GND·+5V 구멍 찾기).
사용: python tools/make_kbd_cable_guide.py analysis/kbd_cable_orientation_guide.jpg
재료: analysis/kbd_measure_simple.jpg, photos/keyboard/20261107_133005_connector-wiring-side.jpg,
      analysis/j10_gnd_pins_zoom.jpg, analysis/slot1_pins.jpg
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHITE, RED, BLU, GRN, ORG = (0, 0, 0), (255, 255, 255), (220, 20, 20), (30, 100, 240), (0, 140, 60), (230, 120, 0)

def load(p):
    return ImageOps.exif_transpose(Image.open(p)).convert("RGB")

def fit_h(im, h):
    return im.resize((round(im.width * h / im.height), h), Image.LANCZOS)

W, PH = 1900, 640
canvas = Image.new("RGB", (W, 2300), WHITE)
d = ImageDraw.Draw(canvas)

d.text((30, 20), "키보드 케이블 꽂는 방향 정하기 (전원 끔, 테스터 통전 모드)", font=F(46), fill=BLK)
d.text((30, 86), "목표: 케이블 본체 쪽 커넥터에서 GND 구멍과 +5V 구멍을 찾고, J10의 GND·+5V 핀에 맞춰 꽂기.", font=FR(30), fill=BLK)
d.text((30, 128), "이 둘만 맞으면 거꾸로 꽂아서 칩을 태울 위험은 없음. 나머지 선 대응은 나중에.", font=FR(30), fill=BLK)

def step_title(y, n, text, color):
    d.rounded_rectangle((30, y, 90, y + 60), 12, fill=color)
    d.text((47, y + 4), str(n), font=F(42), fill=WHITE)
    d.text((110, y + 6), text, font=F(36), fill=color)

# ── 1단계: 키보드 쪽 단자 16, 9 ─────────────────────────
y = 200
step_title(y, 1, "키보드 납땜면: 단자 16(GND)과 단자 9(+5V)에 프로브를 댈 준비", RED)
k = load("analysis/kbd_measure_simple.jpg").crop((470, 320, 650, 720))
k = fit_h(k, PH - 80)
kd = ImageDraw.Draw(k)
s = k.height / 400
for (x, yy, c) in ((535, 383, RED), (535, 686, ORG)):
    cx, cy = (x - 470) * s, (yy - 320) * s
    kd.ellipse((cx - 34, cy - 34, cx + 34, cy + 34), outline=c, width=7)
canvas.paste(k, (40, y + 80))
tx = 40 + k.width + 40
d.text((tx, y + 100), "케이블은 키보드에 꽂힌 그대로 둡니다.", font=FR(32), fill=BLK)
d.text((tx, y + 150), "● 단자 16 = GND (왼쪽 줄 맨 위)", font=F(34), fill=RED)
d.text((tx, y + 200), "● 단자 9 = +5V (왼쪽 줄 맨 아래)", font=F(34), fill=ORG)
d.text((tx, y + 270), "번호는 늘 쓰던 kbd_measure_simple.jpg 그대로.", font=FR(28), fill=BLK)

# ── 2단계: 본체 쪽 커넥터 구멍 ─────────────────────────
y = 940
step_title(y, 2, "본체 쪽 커넥터(본체에서 뽑은 상태) 구멍 16개를 하나씩", BLU)
c = load("photos/keyboard/20261107_133005_connector-wiring-side.jpg").crop((1120, 1600, 1720, 2440))
c = fit_h(c, PH - 80)
cd = ImageDraw.Draw(c)
cs = c.height / 840
cd.ellipse(((1290 - 1120) * cs, (1980 - 1600) * cs, (1660 - 1120) * cs, (2420 - 1600) * cs), outline=BLU, width=8)
canvas.paste(c, (40, y + 80))
tx = 40 + c.width + 40
lines = [
    ("구멍 면(검은 커넥터 끝, 파란 원)에 핀을 꽂아 재요.", BLK, F(32)),
    ("테스터 침이 굵어 안 들어가면: 바늘·옷핀·점퍼선 끝을", BLK, FR(30)),
    ("구멍에 살짝 꽂고 그 위에 테스터 침을 댑니다.", BLK, FR(30)),
    ("", BLK, FR(20)),
    ("한 침 = 키보드 단자 16 고정, 다른 침 = 구멍 하나씩", RED, F(30)),
    ("→ 삑 하는 구멍 = GND 구멍. 매직·테이프로 'G' 표시", RED, F(30)),
    ("한 침 = 키보드 단자 9 고정, 다른 침 = 구멍 하나씩", ORG, F(30)),
    ("→ 삑 하는 구멍 = +5V 구멍. '5' 표시", ORG, F(30)),
    ("", BLK, FR(20)),
    ("GND 구멍은 2개 나올 수 있음(정상). 몇 개인지 알려 주세요.", BLK, FR(28)),
]
yy = y + 95
for t, col, f in lines:
    d.text((tx, yy), t, font=f, fill=col)
    yy += 46 if t else 18

# ── 3단계: J10 +5V 핀 찾기 ─────────────────────────
y = 1680 - 0
step_title(y, 3, "본체 J10: 슬롯1 25번(+5V)과 통하는 핀 찾기", GRN)
j = fit_h(load("analysis/j10_gnd_pins_zoom.jpg"), 360)
canvas.paste(j, (40, y + 75))
sl = load("analysis/slot1_pins.jpg").crop((560, 110, 900, 260))
sl = fit_h(sl, 150)
canvas.paste(sl, (40 + j.width + 30, y + 75))
tx = 40 + j.width + 30
yy = y + 245
for t, col, f in [
    ("한 침 = 슬롯1 25번(오른쪽 줄 맨 위, +5V)", GRN, F(30)),
    ("다른 침 = J10 핀 16개를 하나씩. 삑 하는 핀 = J10 +5V", GRN, F(30)),
    ("(케이스 쪽 끝 노란 원 근처일 것으로 추정, 미확인)", BLK, FR(26)),
]:
    d.text((tx, yy), t, font=f, fill=col)
    yy += 44

canvas = canvas.crop((0, 0, W, y + 75 + 360 + 30))
# ── 4단계 안내는 맨 아래 띠로 ─────────────────────────
band = Image.new("RGB", (W, 200), (255, 245, 210))
bd = ImageDraw.Draw(band)
bd.text((30, 18), "4  꽂기: 'G' 구멍 → J10 GND 끝(빨간 원 쪽), '5' 구멍 → J10 +5V 핀", font=F(36), fill=BLK)
bd.text((30, 75), "두 개가 동시에 맞는 방향이 하나 있으면 그 방향으로 꽂으면 됩니다.", font=FR(30), fill=BLK)
bd.text((30, 120), "어느 방향으로도 둘 다 맞지 않으면 꽂지 말고 결과(구멍 위치)를 알려 주세요.", font=F(30), fill=RED)
final = Image.new("RGB", (W, canvas.height + band.height), WHITE)
final.paste(canvas, (0, 0))
final.paste(band, (0, canvas.height))
final.save(OUT, quality=90)
