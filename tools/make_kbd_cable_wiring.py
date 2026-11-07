"""키보드 케이블 결선표: 측정된 대응 + 규칙으로 예상한 원래 결선.
사용: python tools/make_kbd_cable_wiring.py analysis/kbd_cable_wiring_expected.jpg

측정(2026-11-07, 사용자): 구멍→단자 1→9, 3→6, 4→12, 5→13, 6→14, 8→16(9도 GND), 10→2, 11→3, 12→4, 13→5, 15→7, 16→8.
규칙: 구멍 n(1–8) ↔ 단자 n+8, 구멍 n(9–16) ↔ 단자 n−8. 측정 12개 중 10개가 이 규칙 (3→6, 9=GND 빈칸만 예외).
→ 예상: 구멍 2 ↔ 단자 10 (RESET 열), 구멍 7 ↔ 단자 15 (둘 다 뒤에 선 있음 → 끊김 추정).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHITE, GRN, RED, ORG, GRY, BLU = (0, 0, 0), (255, 255, 255), (0, 140, 60), (215, 20, 20), (220, 110, 0), (120, 120, 120), (30, 100, 240)
LGRN, LRED, LORG, LGRY = (225, 245, 230), (255, 228, 228), (255, 238, 215), (240, 240, 240)

# (구멍, 측정 단자, 규칙상 단자, 신호, 상태, 메모)
rows = [
    (1, "9", 9, "+5V", "ok", ""),
    (2, "—", 10, "열 · RESET", "cut", "뒤에 선 있음 → 끊김 추정. 원래 단자 10"),
    (3, "6", 11, "행 D", "diff", "규칙상 단자 11(선택선) 자리"),
    (4, "12", 12, "행 B", "ok", ""),
    (5, "13", 13, "열", "ok", ""),
    (6, "14", 14, "열", "ok", ""),
    (7, "—", 15, "열", "cut", "뒤에 선 있음 → 끊김 추정. 원래 단자 15"),
    (8, "16", 16, "GND", "ok", ""),
    (9, "(GND)", 1, "GND", "none", "뒤에 선 없음. J10에서 8과 같은 GND"),
    (10, "2", 2, "열", "ok", ""),
    (11, "3", 3, "열", "ok", ""),
    (12, "4", 4, "열", "ok", ""),
    (13, "5", 5, "열", "ok", ""),
    (14, "—", 6, "(행 D?)", "none", "뒤에 선 없음. 규칙상 단자 6(D) 자리"),
    (15, "7", 7, "행 C", "ok", ""),
    (16, "8", 8, "행 A", "ok", ""),
]
st = {"ok": (LGRN, GRN, "정상"), "cut": (LRED, RED, "끊김?"), "diff": (LORG, ORG, "규칙과 다름"), "none": (LGRY, GRY, "선 없음")}

W = 1900
RH = 62
TOP = 230
H = TOP + 60 + RH * 16 + 330
img = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(img)
d.text((30, 20), "키보드 케이블 결선표 (측정 + 예상)", font=F(46), fill=BLK)
d.text((30, 84), "구멍 = 본체 쪽 커넥터 (analysis/kbd_cable_holes_numbered.jpg),  단자 = 키보드 뒷면 (analysis/kbd_measure_simple.jpg)", font=FR(26), fill=BLK)
d.text((30, 124), "찾은 규칙: 단자 번호 = 구멍 번호 + 8 (16을 넘으면 −16) → 구멍 1–8 ↔ 단자 9–16, 구멍 9–16 ↔ 단자 1–8 (두 쪽 번호가 180° 돌아간 관계)", font=F(27), fill=BLU)
d.text((30, 162), "측정된 12개 중 10개가 이 규칙과 맞음. 그래서 끊긴 구멍 2·7에 원래 이어져 있던 단자를 예상할 수 있음.", font=FR(26), fill=BLK)

cols = [(30, "구멍"), (170, "측정된 단자"), (390, "규칙상 단자"), (600, "신호"), (830, "상태"), (1050, "메모")]
for x, h in cols:
    d.text((x + 10, TOP), h, font=F(28), fill=BLK)
d.line((30, TOP + 48, W - 30, TOP + 48), fill=BLK, width=3)
for i, (hole, m, rule, s, k, memo) in enumerate(rows):
    y = TOP + 60 + i * RH
    bg, fg, word = st[k]
    d.rectangle((30, y, W - 30, y + RH - 6), fill=bg)
    d.text((50, y + 10), str(hole), font=F(32), fill=BLK)
    d.text((190, y + 10), m, font=F(30), fill=BLK)
    d.text((410, y + 10), str(rule), font=F(30), fill=fg if k != "ok" else BLK)
    d.text((610, y + 12), s, font=FR(28), fill=BLK)
    d.text((840, y + 10), word, font=F(28), fill=fg)
    d.text((1060, y + 14), memo, font=FR(24), fill=BLK)

y = TOP + 60 + 16 * RH + 20
lines = [
    ("예상 결론", F(32), BLK),
    ("• 구멍 2 ↔ 단자 10 (RESET 열), 구멍 7 ↔ 단자 15 선이 끊김 → RESET과 그 두 열의 키가 안 먹음.", FR(27), RED),
    ("• 고치기: 끊긴 두 선을 다시 납땜 (또는 새 선으로 단자 10 → 구멍 2, 단자 15 → 구멍 7).", FR(27), BLK),
    ("• 주의: 행 D가 규칙과 달리 구멍 3에 있음 (규칙상 구멍 14, 빈칸). 누가 케이블을 다시 만들며 옮겼을 수 있음.", FR(27), ORG),
    ("  D가 본체에서 원래 기대하는 핀과 다르면 행 번호가 틀어짐 → 끊긴 선을 고친 뒤에도 안 되면 이 부분 확인.", FR(27), ORG),
]
for t, f, c in lines:
    d.text((30, y), t, font=f, fill=c)
    y += 52
img = img.crop((0, 0, W, y + 20))
img.save(OUT, quality=90)
