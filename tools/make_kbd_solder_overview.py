"""키보드 뒷면(납땜면) 전체 + 칩·단자 번호 그림을 한 장으로.
사용: python tools/make_kbd_solder_overview.py analysis/kbd_solder_overview.jpg
재료: photos/keyboard/Scan_20261107_144256_kbd-solder-side_flat.jpg (전체), analysis/kbd_measure_simple.jpg (번호)

방향: 번호 그림(kbd_measure_simple)은 "케이블 단자가 위". 스캔 사진은 그와 180° 돌아가 있으므로
(스캔에서 104 콘덴서가 74LS145 왼쪽 위, 번호 그림에서는 오른쪽 아래) 전체 사진을 180° 돌려 방향을 맞춤.
RESET 패드: 스캔 좌표 (870, 3095), 사용자 측정 확정 (74LS145 3번, 누르면 단자 10).
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHITE, RED, YEL, BLU = (0, 0, 0), (255, 255, 255), (230, 20, 20), (255, 200, 0), (30, 100, 240)

board = ImageOps.exif_transpose(Image.open("photos/keyboard/Scan_20261107_144256_kbd-solder-side_flat.jpg")).convert("RGB")
W0, H0 = board.size
board = board.rotate(180)
S = 0.5
board = board.resize((int(W0 * S), int(H0 * S)), Image.LANCZOS)

def R(x, y):  # 스캔 원본 좌표 → 180° 돌린 축소 좌표
    return (W0 - x) * S, (H0 - y) * S

num = Image.open("analysis/kbd_measure_simple.jpg").convert("RGB")
nh = board.height
num = num.resize((int(num.width * nh / num.height), nh), Image.LANCZOS)

TOP, GAP, M = 150, 70, 20
canvas = Image.new("RGB", (M + board.width + GAP + num.width + M, TOP + nh + 110), WHITE)
bx, by = M, TOP
nx, ny = M + board.width + GAP, TOP
canvas.paste(board, (bx, by))
canvas.paste(num, (nx, ny))
d = ImageDraw.Draw(canvas)

d.text((20, 14), "키보드 뒷면(납땜면) 전체 + 칩·단자 번호", font=F(44), fill=BLK)
d.text((20, 74), "왼쪽 = 뒷면 전체 (케이블 단자가 위로 오게 돌린 모습), 오른쪽 = 노란 칸 확대. 번호는 오른쪽 그림 기준.", font=FR(26), fill=BLK)
d.text((20, 110), "번호 규칙: 칩·단자 모두 오른쪽 줄 맨 위(● 표시) = 1, 오른쪽 줄 아래로 → 왼쪽 줄 아래에서 위로.", font=FR(26), fill=BLK)

# 칩·단자 구역 (스캔 원본 좌표 560–780 × 1760–2500)
x0, y0 = R(780, 2500); x1, y1 = R(560, 1760)
x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1))
d.rectangle((bx + x0, by + y0, bx + x1, by + y1), outline=YEL, width=7)
d.line((bx + x1, by + y0, nx, ny), fill=YEL, width=4)
d.line((bx + x1, by + y1, nx, ny + nh), fill=YEL, width=4)
lab = "칩·단자 (오른쪽 그림)"
f = F(30)
l, t, r, b = d.textbbox((0, 0), lab, font=f)
tx, ty = bx + x0 - (r - l) - 20, by + y0 - 10
d.rectangle((tx - 8, ty - 6, tx + (r - l) + 8, ty + (b - t) + 14), fill=WHITE, outline=BLK, width=2)
d.text((tx, ty), lab, font=f, fill=BLK)

# RESET 패드
rx, ry = R(870, 3095)
rx, ry = bx + rx, by + ry
d.ellipse((rx - 22, ry - 22, rx + 22, ry + 22), outline=RED, width=7)
lab = "RESET (확정): 74LS145 3번 · 누르면 단자 10"
l, t, r, b = d.textbbox((0, 0), lab, font=F(28))
tx, ty = rx - (r - l) - 40, ry + 40
d.line((rx - 16, ry + 16, tx + (r - l), ty), fill=RED, width=4)
d.rectangle((tx - 8, ty - 6, tx + (r - l) + 8, ty + (b - t) + 14), fill=WHITE, outline=RED, width=3)
d.text((tx, ty), lab, font=F(28), fill=RED)

# 아래 요약
y = TOP + nh + 18
d.text((20, y), "단자: 16 GND · 9 +5V · 8/12/7/6 = 행 번호 A/B/C/D (74LS145 15/14/13/12번) · 2–5, 10, 13–15 = 열 8가닥 (10 = RESET 열) · 1, 11 = 케이블 선 없음", font=F(28), fill=BLK)
d.text((20, y + 46), "케이블 본체 쪽 구멍 번호: analysis/kbd_cable_holes_numbered.jpg · J10 핀별 신호: docs/05-interface-pinouts.md", font=FR(26), fill=BLK)
canvas.save(OUT, quality=88)
