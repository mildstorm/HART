"""앞면·뒷면 정합 결과로 U30 핀 37 경로 표시 (앞면 좌표).
사용: python tools/annotate_pin37_overlay.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/back_on_front.jpg analysis/u30_pin37_overlay.jpg
back_on_front.jpg 는 tools/register_front_back.py 출력 (뒷면을 앞면 좌표로 맞춘 것).
"""
import sys
from PIL import Image, ImageDraw, ImageFont

FR, BK, OUT = sys.argv[1:4]
fr = Image.open(FR).convert("RGB"); bk = Image.open(BK).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,160,60)

X0, Y0, X1, Y1 = 150, 1380, 620, 1800
sc = 1.6
pw, ph = int((X1-X0)*sc), int((Y1-Y0)*sc)
W, H = pw*3 + 80, ph + 470
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)
ov = Image.blend(fr, bk, 0.5)
panels = [(fr, "앞면"), (bk, "뒷면 (앞면 좌표로 맞춤, 비친 것처럼)"), (ov, "겹친 그림 (50:50)")]
def label(xy, text, sz=15, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 10), "U30 핀 37 경로 — 앞면·뒷면 정합 사진 (같은 좌표)", font=font(28, True), fill=BLK)
d.text((20, 50), "정합: 양면 비아 205개로 맞춤, 평균 오차 약 2px(핀 간격의 1/17). 세 그림은 같은 위치. 칩 다리처럼 높이 솟은 것은 사진 각도 때문에 조금 어긋나 보임", font=font(17), fill=BLK)
marks = {
    "p37": (321, 1429, "핀 37", RED),
    "via": (332, 1750, "비아", BLUE),
    "r1": (443, 1738, "저항 ①", RED),
    "r2": (288, 1737, "저항 ② (GND)", GRN),
    "p1": (218, 1634, "핀 1 (GND)", GRN),
}
for i, (img, title) in enumerate(panels):
    ox, oy = 20 + i*(pw + 20), 120
    cv.paste(img.crop((X0, Y0, X1, Y1)).resize((pw, ph), Image.LANCZOS), (ox, oy))
    d.text((ox, oy - 30), title, font=font(18, True), fill=BLK)
    M = lambda x, y: (ox + (x-X0)*sc, oy + (y-Y0)*sc)
    for key, (x, y, t, c) in marks.items():
        cx, cy = M(x, y)
        d.ellipse((cx-11, cy-11, cx+11, cy+11), outline=c, width=4)
        if i == 0 or key in ("via", "p37"):
            label((cx, cy - 26 if key != "r2" else cy + 26), t, 13, fg=WHITE, bg=c)
    if i == 1:
        d.line([M(321, 1429), M(318, 1540), M(304, 1634), M(308, 1690), M(332, 1750)], fill=YEL, width=3)

ty = oy + ph + 20
for t, b, c in [
    ("경로 (정합 사진 판독, 확실성 중간–높음)", True, BLK),
    ("1. 핀 37 → 뒷면 선이 아래로 내려가 핀 3·4 사이를 지남 → 비아(파랑)에서 앞면으로", False, BLK),
    ("2. 비아는 앞면에서 저항 몸통 왼쪽 아래에 가려 있음 → 앞면 선으로 저항 ① 다리(오른쪽)에 연결 (사용자 확인과 일치)", False, BLK),
    ("3. 저항 ② 다리(왼쪽)는 뒷면 굵은 선으로 U30 핀 1(GND)에 연결 → 이 저항은 핀 37의 1kΩ 풀다운", False, BLK),
    ("4. 저항 ① 다리에서 앞면 가는 선이 오른쪽 위로 나가 U30 아래 가로 선 다발로 합류 → 이 선이 박자(Φ0)가 들어와야 할 길", True, RED),
    ("   다발 속에서는 선이 촘촘해 사진으로 끝까지 따라가기 어려움", False, BLK),
    ("", False, BLK),
    ("다음 측정 (전원 끄고, 도통): 저항 ① 다리 ↔ 슬롯 핀 40.  삐 소리 안 나면 ① 다리에서 나가는 앞면 선을 손전등으로 따라가며 끊긴 곳 찾기", True, BLK),
]:
    d.text((20, ty), t, font=font(17, b), fill=c); ty += 30
cv.save(OUT, quality=92)
print(cv.size, ty)
