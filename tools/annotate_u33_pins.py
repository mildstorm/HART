"""U33 (74LS367) 핀 번호·기능 그림. 저항 ①(U30 핀 37 클럭선)이 U33 핀 5에 연결됨 (2026-11-07 측정).
사용: python tools/annotate_u33_pins.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/u33_pins.jpg
세로 칩, 노치 아래쪽 → 1번 핀 = 오른쪽 아래. 오른쪽 줄 아래→위 1–8, 왼쪽 줄 위→아래 9–16.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN, GRAY, ORG = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,150,60), (110,110,110), (230,120,0)

X0, Y0, X1, Y1 = 1150, 1470, 1410, 1780
sc = 2.6
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
W, H = 1500, 1260
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
ax, ay = 420, 110
cv.paste(im, (ax, ay))
M = lambda x, y: (ax + (x-X0)*sc, ay + (y-Y0)*sc)
def label(xy, text, sz=16, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "U33 (74LS367, 버퍼 6개) 핀 번호 — 앞면", font=font(30, True), fill=BLK)
d.text((20, 56), "U30 오른쪽 칩 줄의 세 번째(74LS367 셋 중 오른쪽). 노치 아래쪽 → 1번 핀 = 오른쪽 아래.", font=font(18), fill=BLK)

func = {1: "/G1 (버퍼1–4 인에이블, 0V여야 동작)", 2: "A1 입력", 3: "Y1 출력", 4: "A2 입력 ← 클럭 들어올 곳",
        5: "Y2 출력 → U30 핀 37", 6: "A3 입력", 7: "Y3 출력", 8: "GND",
        9: "Y4 출력", 10: "A4 입력", 11: "Y5 출력", 12: "A5 입력", 13: "Y6 출력", 14: "A6 입력",
        15: "/G2 (버퍼5–6 인에이블)", 16: "+5V"}
col = {1: ORG, 4: RED, 5: RED, 8: GRN, 16: GRN}
P, yb, xr, xl = 34.3, 1745, 1327, 1233
for p in range(1, 17):
    if p <= 8:
        x, y = xr, yb - (p-1)*P; side = 1
    else:
        x, y = xl, yb - 7*P + (p-9)*P; side = -1
    cx, cy = M(x, y)
    c = col.get(p, GRAY)
    label((cx + side*55, cy), str(p), 17, fg=WHITE, bg=c if p in col else BLUE)
    label((cx + side*85, cy), func[p], 15, fg=c, anchor="lm" if side > 0 else "rm")
cx, cy = M(xr, yb)
d.ellipse((cx-12, cy-12, cx+12, cy+12), outline=YEL, width=4)

ty = ay + im.height + 30
for t, b, c in [
    ("측정 결과: 저항 ① 다리(U30 핀 37 클럭선) ↔ U33 핀 5 도통 (2026-11-07)", True, RED),
    ("→ CPU 클럭은 슬롯 Φ0를 U33 버퍼(입력 핀 4 → 출력 핀 5)를 거쳐 받는 구조로 보임. 선 끊김이 아니었음.", False, BLK),
    ("", False, BLK),
    ("다음 측정", True, BLK),
    ("1. (끄고, 도통) U33 핀 4 ↔ 슬롯 핀 40", False, BLK),
    ("2. (켜고, DC) U33 핀 1 : 0V 근처여야 버퍼가 켜짐.  핀 16 : 약 5V,  핀 8 : 0V", False, BLK),
    ("3. (켜고, Hz) U33 핀 4(입력)과 핀 5(출력)", False, BLK),
    ("   입력 1.023MHz인데 출력 3.58MHz → U33 고장 유력(교체: 74LS367)", False, BLK),
    ("   입력부터 3.58MHz → 핀 4로 들어오는 선을 따라 더 앞쪽을 봄", False, BLK),
]:
    d.text((20, ty), t, font=font(18, b), fill=c); ty += 31
cv.save(OUT, quality=92)
print(cv.size, ty)
