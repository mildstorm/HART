"""키보드 케이블 단선 검사 안내 + 기록표 (한 장).
사용: python tools/make_kbd_cable_check.py analysis/kbd_cable_check.jpg
재료: analysis/kbd_measure_simple.jpg (키보드 단자 번호), analysis/kbd_cable_holes_numbered.jpg (본체 쪽 커넥터 구멍 번호)
"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHITE, RED, GRN, BLU, GRY, YEL = (0, 0, 0), (255, 255, 255), (220, 20, 20), (0, 140, 60), (30, 100, 240), (120, 120, 120), (255, 245, 200)

term = Image.open("analysis/kbd_measure_simple.jpg").convert("RGB").crop((440, 320, 680, 720))
term = term.resize((int(term.width * 2.0), int(term.height * 2.0)), Image.LANCZOS)
holes = Image.open("analysis/kbd_cable_holes_numbered.jpg").convert("RGB")
holes = holes.resize((int(holes.width * term.height / holes.height), term.height), Image.LANCZOS)

W = 2000
TOP = 360
canvas = Image.new("RGB", (W, TOP + term.height + 80 + 900), WHITE)
d = ImageDraw.Draw(canvas)
d.text((30, 20), "키보드 케이블 단선 검사 (전원 끔 · 테스터 통전 모드)", font=F(48), fill=BLK)
steps = [
    "준비: 케이블을 본체 J10에서 뽑는다. 키보드 쪽은 꽂힌 그대로, 키보드 뒷면이 보이게 연다.",
    "침 A = 키보드 단자(왼쪽 그림 번호) 에 고정.   침 B = 점퍼선을 본체 쪽 커넥터 구멍(오른쪽 그림 번호)에 꽂고 그 끝에 댄다.",
    "① 먼저 확인용: 단자 16 → 구멍 8 또는 9 (GND),  단자 9 → 구멍 1 (+5V). 둘 다 삑 하면 검사 방법이 맞는 것.",
    "② 단자 하나씩: 구멍 2–7, 10–16 을 차례로 대 보고 삑 하는 구멍 번호를 표에 적는다. (이미 짝이 나온 구멍은 건너뜀)",
    "③ 삑 할 때 코일 선을 양 끝 근처에서 구부려 본다. 소리가 끊겼다 났다 하면 '반쯤 끊김'.",
]
y = 95
for s in steps:
    d.text((30, y), s, font=FR(28) if not s.startswith("①") else F(28), fill=BLK)
    y += 50

canvas.paste(term, (30, TOP))
canvas.paste(holes, (30 + term.width + 60, TOP))
d.text((30, TOP + term.height + 10), "키보드 단자 (뒷면)", font=F(30), fill=BLK)
d.text((30 + term.width + 60, TOP + term.height + 10), "본체 쪽 커넥터 구멍 (구멍 면)", font=F(30), fill=BLK)

# 판정 박스 (오른쪽)
jx = 30 + term.width + 60 + holes.width + 50
jy = TOP
d.rectangle((jx, jy, W - 30, jy + 520), fill=YEL, outline=BLK, width=2)
d.text((jx + 20, jy + 15), "판정", font=F(36), fill=BLK)
judge = [
    ("구멍 1개와 삑", "정상", GRN),
    ("어느 구멍과도 안 삑", "끊김 (또는 선 없음)", RED),
    ("구멍 2개 이상과 삑", "선끼리 붙음(합선)", RED),
    ("  ※ 단자 16(GND)은 8·9 둘 다 삑 = 정상", "", GRY),
    ("흔들면 끊겼다 났다", "반쯤 끊김", RED),
]
yy = jy + 75
for a, b, c in judge:
    d.text((jx + 20, yy), a, font=F(28) if b else FR(24), fill=BLK if b else GRY)
    if b:
        d.text((jx + 20, yy + 38), "→ " + b, font=F(28), fill=c)
        yy += 90
    else:
        yy += 50

# 기록표
ty = TOP + term.height + 80
d.text((30, ty), "기록표 (구멍 번호를 적어 주세요)", font=F(34), fill=BLK)
rows = [
    ("16", "GND", "8·9 (확인용)"), ("9", "+5V", "1 (확인용)"),
    ("8", "행 A", ""), ("12", "행 B", ""), ("7", "행 C", ""), ("6", "행 D", ""),
    ("10", "열 (RESET)", ""), ("11", "추가 선택선", ""),
    ("1", "열 후보", ""), ("2", "열 후보", ""), ("3", "열 후보", ""), ("4", "열 후보", ""),
    ("5", "열 후보", ""), ("13", "열 후보", ""), ("14", "열 후보", ""), ("15", "열 후보", ""),
]
cols = [(30, "키보드 단자"), (250, "뜻"), (480, "구멍 번호"), (760, "흔들기")]
half = 8
for blk in range(2):
    ox = blk * 980
    y0 = ty + 55
    for cx, h in cols:
        d.text((ox + cx + 10, y0), h, font=F(26), fill=BLK)
    d.line((ox + 30, y0 + 40, ox + 950, y0 + 40), fill=BLK, width=2)
    for i, (t, m, v) in enumerate(rows[blk * half:(blk + 1) * half]):
        ry = y0 + 50 + i * 88
        col = BLU if t in ("8", "12", "7", "6", "10", "11") else BLK
        d.text((ox + 40, ry + 10), "단자 " + t, font=F(30), fill=col)
        d.text((ox + 260, ry + 14), m, font=FR(26), fill=BLK)
        d.rectangle((ox + 480, ry, ox + 730, ry + 66), outline=GRY, width=2)
        if v:
            d.text((ox + 492, ry + 14), v, font=FR(24), fill=GRN)
        d.rectangle((ox + 760, ry, ox + 940, ry + 66), outline=GRY, width=2)
d.text((30, ty + 55 + 50 + 8 * 88 + 10), "파란 글씨 단자(8·12·7·6·10·11)를 먼저. 키보드가 Disp 말고 반응이 없으니 여기가 끊겼을 가능성이 가장 큼.", font=F(26), fill=BLU)
canvas = canvas.crop((0, 0, W, ty + 55 + 50 + 8 * 88 + 60))
canvas.save(OUT, quality=90)
