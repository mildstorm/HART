"""U30 아래 1kΩ 저항 양쪽 다리의 앞면·뒷면 위치.
사용: python tools/annotate_u30_resistor.py photos/zoom/back/225321_back-U30-area_left-edge.jpg photos/zoom/front/230758_U30-pin1-side_traces.jpg analysis/u30_resistor_legs.jpg
좌표는 원본(4000x3000) 기준, 사진 확대로 판독 (2026-11-07).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

BACK, FRONT, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
bk = Image.open(BACK).convert("RGB")
fr = Image.open(FRONT).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,160,60)

W, H = 1700, 1150
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
def label(xy, text, sz=18, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)
def ring(c, r, col, w=5):
    d.ellipse((c[0]-r, c[1]-r, c[0]+r, c[1]+r), outline=col, width=w)

d.text((20, 12), "U30 아래 1kΩ 저항 (갈·흑·적) 다리 위치", font=font(30, True), fill=BLK)
d.text((20, 56), "① = U30 핀 37 패턴이 붙은 다리,  ② = 반대쪽 다리.  앞면 사진 230758, 뒷면 사진 225321 확대 판독", font=font(18), fill=BLK)

# front
FX0, FY0, FX1, FY1 = 600, 900, 3000, 2200
fs = 0.33
fim = fr.crop((FX0, FY0, FX1, FY1)).resize((int((FX1-FX0)*fs), int((FY1-FY0)*fs)), Image.LANCZOS)
fa = (20, 130)
cv.paste(fim, fa)
d.text((20, 98), "앞면 (노치 왼쪽, 아래 줄 왼쪽부터 핀 1, 2, 3 …)", font=font(20, True), fill=BLK)
FM = lambda x, y: (fa[0] + (x-FX0)*fs, fa[1] + (y-FY0)*fs)
for n, x in enumerate([890, 1170, 1450, 1720, 2000, 2280, 2560], start=1):
    cx, cy = FM(x, 1060)
    label((cx, cy - 26), str(n), 14)
L2, L1 = FM(1430, 1850), FM(2615, 1885)
ring(L2, 20, GRN); label((L2[0], L2[1] + 42), "② → GND", 17, fg=WHITE, bg=GRN)
ring(L1, 20, RED); label((L1[0], L1[1] + 42), "① 핀 37 쪽", 17, fg=WHITE, bg=RED)

# back
BX0, BY0, BX1, BY1 = 1980, 1750, 3060, 2450
bs = 0.78
bim = bk.crop((BX0, BY0, BX1, BY1)).resize((int((BX1-BX0)*bs), int((BY1-BY0)*bs)), Image.LANCZOS)
ba = (870, 130)
cv.paste(bim, ba)
d.text((870, 98), "뒷면 (좌우 반전: 아래 줄 오른쪽 끝 = 핀 1)", font=font(20, True), fill=BLK)
BM = lambda x, y: (ba[0] + (x-BX0)*bs, ba[1] + (y-BY0)*bs)
for n, x in {1: 2935, 2: 2815, 3: 2700, 4: 2580, 5: 2460, 6: 2340, 7: 2225, 8: 2105}.items():
    cx, cy = BM(x, 1915)
    label((cx, cy - 34), str(n), 14, fg=WHITE if n == 1 else BLK, bg=GRN if n == 1 else WHITE)
b2, b1, via = BM(2715, 2270), BM(2170, 2285), BM(2565, 2310)
ring(b2, 22, GRN); label((b2[0] - 10, b2[1] + 48), "② 납땜점", 17, fg=WHITE, bg=GRN)
ring(b1, 22, RED); label((b1[0], b1[1] + 48), "① 납땜점", 17, fg=WHITE, bg=RED)
ring(via, 14, BLUE, 4); label((via[0] - 20, via[1] - 40), "핀 37 비아", 15, fg=WHITE, bg=BLUE)
cap = BM(2880, 2145)
d.line([BM(2935, 1915), cap, b2], fill=YEL, width=4)
label((cap[0] - 40, cap[1] - 10), "굵은 선 → 핀 1(GND)", 15, bg=YEL, anchor="rm")

ty = 640
for t, b, c in [
    ("판독 결과 (확실성: 중간–높음, 사진 판독)", True, BLK),
    ("• ② 다리 뒷면 납땜점은 굵은 선으로 U30 핀 1(GND, 6502의 VSS)에 연결 → 저항은 핀 37을 GND로 당기는 1kΩ 풀다운", False, BLK),
    ("   (앞서 잰 '핀 37 ↔ GND = 1kΩ'과 맞음)", False, BLK),
    ("• ① 다리 뒷면 납땜점에는 뒷면 선이 없음 → ①의 연결은 모두 앞면 쪽", False, BLK),
    ("• 따라서 클럭(Φ0)은 저항이 아니라, 앞면에서 ① 또는 핀 37 비아로 이어지는 '다른 선'으로 들어와야 함", True, RED),
    ("", False, BLK),
    ("측정 (전원 끄고, 저항 모드) — 이것으로 확정", True, BLK),
    ("1. ② 납땜점 ↔ GND(U72 핀 7) : 0Ω 근처면 위 판독 확정", False, BLK),
    ("2. ① 납땜점 ↔ U30 핀 37 : 0Ω 근처", False, BLK),
    ("3. ① 납땜점 ↔ 슬롯 핀 40 : 0Ω이면 클럭선과 직결(끊김 없음), 끊김이면 클럭선 쪽 앞면 패턴 끊김", False, BLK),
    ("4. 앞면에서 ① 다리에서 오른쪽 위로 나가는 가는 선을 눈으로 따라가기 → 어느 칩으로 가는지", False, BLK),
    ("", False, BLK),
    ("뒷면 위치 찾는 법: ① 납땜점은 핀 7·8 아래 약 3칸(7–8mm), ② 납땜점은 핀 3 아래 약 3칸.", True, BLK),
    ("헷갈리면 앞면 저항 다리에 한쪽 프로브, 뒷면 납땜점을 하나씩 대서 삐 소리로 찾기.", False, BLK),
]:
    d.text((20, ty), t, font=font(19, b), fill=c); ty += 34

cv.save(OUT, quality=92)
print(cv.size, ty)
