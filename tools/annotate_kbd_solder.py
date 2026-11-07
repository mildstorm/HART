"""키보드(ZPC-40) 기판 납땜면: JAE 16P 단자·74LS03·74LS145 핀 번호 안내 그림.
사용: python tools/annotate_kbd_solder.py photos/keyboard/20261107_145239_kbd-solder-side_connector-ICs.jpg analysis/kbd_solder_pinguide.jpg
좌표는 EXIF 회전을 적용한 원본(3000x4000) 픽셀. 판독 2026-11-07.

핀 번호 판단: 부품면 사진(145419)에서 두 칩 글자가 아래→위로 읽힘 = 노치가 아래 → 부품면 기준 1번 핀 오른쪽 아래.
납땜면은 부품면을 위아래로 뒤집은 모양이므로 1번 핀 = 오른쪽 위, 오른쪽 줄을 따라 아래로 1..8(또는 1..7).
검증: 104 콘덴서가 LS145 16번(Vcc)과 LS03 7번(GND) 사이에 연결됨 → 전원 바이패스로 맞음.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
X0, Y0, X1, Y1, sc = 1900, 900, 2900, 2700, 0.85
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
font = lambda s, b=False: ImageFont.truetype(FB if b else F, s)
BLK, WHITE, RED, YEL, BLUE, GRN, ORG, PUR = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,150,60), (255,130,0), (150,60,200)
TOP, PADL = 110, 300
cv = Image.new("RGB", (im.width + PADL + 20, im.height + TOP + 330), WHITE)
cv.paste(im, (PADL, TOP))
d = ImageDraw.Draw(cv)
M = lambda x, y: (PADL + (x - X0) * sc, TOP + (y - Y0) * sc)

def lab(xy, t, sz=14, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, t, font=f, anchor=anchor)
    d.rectangle((bb[0]-3, bb[1]-2, bb[2]+3, bb[3]+2), fill=bg, outline=BLK)
    d.text(xy, t, font=f, fill=fg, anchor=anchor)
def ring(x, y, col, r=12, w=3):
    c = M(x, y); d.ellipse((c[0]-r, c[1]-r, c[0]+r, c[1]+r), outline=col, width=w)

# JAE 16P 단자 패드: 안쪽 열(기판 안쪽) / 바깥 열(기판 가장자리), 행 1 = 74LS03 쪽 끝(부품면 ▼ 표시 쪽)
CI, CO = 2565, 2615
CROWS = [1550, 1510, 1467, 1425, 1382, 1342, 1300, 1247]   # 행 1..8 (아래 = LS03 쪽부터)
for n, y in enumerate(CROWS, 1):
    ring(CI, y, YEL); ring(CO, y, YEL)
    lab((M(CI, y)[0] - 40, M(CI, y)[1]), f"K{n}안", 12, bg=YEL)
    lab((M(CO, y)[0] + 42, M(CO, y)[1]), f"K{n}밖", 12, bg=YEL)
lab((M(2590, 1200)[0], M(2590, 1200)[1] - 10), "JAE 16P 단자 (케이블)", 15, fg=WHITE, bg=ORG)

# 74LS03: 오른쪽 줄 위→아래 1..7, 왼쪽 줄 위→아래 14..8
L03, R03 = 2480, 2605
Y03 = [1795, 1835, 1880, 1920, 1965, 2005, 2050]
names03 = {1: "1A", 2: "1B", 3: "1Y", 4: "2A", 5: "2B", 6: "2Y", 7: "GND", 14: "Vcc", 13: "4B", 12: "4A", 11: "4Y", 10: "3B", 9: "3A", 8: "3Y"}
for i, y in enumerate(Y03):
    r, l = i + 1, 14 - i
    ring(R03, y, BLUE, 10); ring(L03, y, BLUE, 10)
    lab((M(R03, y)[0] + 40, M(R03, y)[1]), f"{r} {names03[r]}", 11, fg=WHITE, bg=BLUE)
    lab((M(L03, y)[0] - 42, M(L03, y)[1]), f"{l} {names03[l]}", 11, fg=WHITE, bg=BLUE)
lab((M(2540, 1760)[0], M(2540, 1760)[1] - 6), "74LS03 (오픈 컬렉터 NAND)", 14, fg=WHITE, bg=BLUE)

# 74LS145: 오른쪽 줄 위→아래 1..8, 왼쪽 줄 위→아래 16..9
L45, R45 = 2470, 2595
Y45 = [2245, 2290, 2330, 2370, 2410, 2450, 2490, 2530]
names45 = {1: "Y0", 2: "Y1", 3: "Y2", 4: "Y3", 5: "Y4", 6: "Y5", 7: "Y6", 8: "GND",
           16: "Vcc", 15: "A", 14: "B", 13: "C", 12: "D", 11: "Y9", 10: "Y8", 9: "Y7"}
for i, y in enumerate(Y45):
    r, l = i + 1, 16 - i
    col_l = RED if l in (12, 13, 14, 15) else GRN
    ring(R45, y, GRN, 10); ring(L45, y, col_l, 10)
    lab((M(R45, y)[0] + 42, M(R45, y)[1]), f"{r} {names45[r]}", 11, fg=WHITE, bg=GRN)
    lab((M(L45, y)[0] - 44, M(L45, y)[1]), f"{l} {names45[l]}", 11, fg=WHITE, bg=col_l)
lab((M(2530, 2580)[0], M(2530, 2580)[1] + 14), "74LS145 (행 선택, 오픈 컬렉터)", 14, fg=WHITE, bg=GRN)
ring(2690, 2230, ORG, 26, 4)
lab((M(2690, 2230)[0] + 10, M(2690, 2230)[1] - 38), "104 콘덴서: LS145 16 ↔ LS03 7", 12, fg=WHITE, bg=ORG)

# 초록·검정 직결 선
ring(2238, 1023, BLK, 16, 4); ring(2238, 1077, GRN, 16, 4)
lab((M(2238, 1023)[0] - 70, M(2238, 1023)[1] - 26), "검정 선", 13, fg=WHITE, bg=BLK)
lab((M(2238, 1077)[0] - 70, M(2238, 1077)[1] + 24), "초록 선", 13, fg=WHITE, bg=GRN)

d.text((20, 10), "ZPC-40 키보드 납땜면 — 단자·칩 핀 번호 (사진 145239)", font=font(24, True), fill=BLK)
d.text((20, 48), "단면 기판: 배선은 모두 이 면, 부품면에는 점퍼선만 있음.  K1 = 74LS03 쪽 끝 (부품면 ▼ 표시 쪽으로 추정)", font=font(15), fill=BLK)
d.text((20, 74), "칩 1번 핀 = 오른쪽 위 (부품면 글자 방향으로 판단, 콘덴서 연결로 검증)", font=font(15), fill=BLK)
side = [("왼쪽 열", True), ("빨강 = 74LS145", False), ("행 선택 입력", False), ("A·B·C·D", False), ("(15·14·13·12)", False),
        ("→ 본체에서 오는", False), ("4비트 행 번호", False), ("", False), ("초록 = 출력 Y0–Y9", False), ("→ 키 매트릭스 행", False)]
yy = TOP + 700
for t, b in side:
    d.text((16, yy), t, font=font(15, b), fill=BLK); yy += 24
ty = TOP + im.height + 16
for t, b, c in [
    ("확인된 것", True, BLK),
    ("• 키보드 기판은 단면. 키 매트릭스·칩 배선이 모두 납땜면에 있음", False, BLK),
    ("• 74LS145 16번(Vcc)과 74LS03 7번(GND) 사이에 104 콘덴서 → 칩 핀 번호 방향이 맞음", False, BLK),
    ("• 74LS145 출력(오른쪽 줄 1–7, 왼쪽 9–11)은 아래쪽 키 매트릭스로, 입력 A–D(왼쪽 15–12)는 단자 쪽으로 감", False, BLK),
    ("• 초록·검정 선은 JAE 단자를 거치지 않고 단자 위쪽 패드 두 개에 직접 납땜", False, BLK),
    ("", False, BLK),
    ("측정으로 확정 (케이블을 본체에서 뺀 채, 통전 모드)", True, BLK),
    ("JAE 단자 각 칸(K1–K8 안·밖) ↔ 74LS145 15·14·13·12·16·8, 74LS03 14·7, 초록·검정 선", False, RED),
]:
    d.text((20, ty), t, font=font(16, b), fill=c); ty += 28
cv = cv.crop((0, 0, cv.width, ty + 10))
cv.save(OUT, quality=92)
print(cv.size)
