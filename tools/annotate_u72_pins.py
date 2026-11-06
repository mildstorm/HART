"""U72 (74LS04) 핀 번호 그림.
사용: python tools/annotate_u72_pins.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/u72_pins.jpg
U72는 정면 사진에서 U64 바로 아래, 트리머 콘덴서 오른쪽. 노치 왼쪽 → 1번 핀 왼쪽 아래.
"""
import sys
from PIL import Image, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
src = Image.open(SRC).convert("RGB")
F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
def font(sz, bold=False):
    return ImageFont.truetype(FB if bold else F, sz)

BLK, WHITE, RED, GRN, BLUE, GRAY, YEL = (0,0,0), (255,255,255), (220,20,20), (0,150,60), (0,100,220), (110,110,110), (255,220,0)
W, H = 1500, 1260
cv = Image.new("RGB", (W, H), WHITE)
d = ImageDraw.Draw(cv)

def label(xy, text, sz=18, fg=BLK, bg=WHITE, anchor="mm", bold=True):
    f = font(sz, bold)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-5, bb[1]-3, bb[2]+5, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

d.text((20, 12), "U72 (74LS04, 인버터 6개) 핀 번호 — 정면, 슬롯이 위쪽", font=font(30, True), fill=BLK)
d.text((20, 54), "위치: U64(아래쪽 UM6502) 바로 아래 왼쪽, 트리머 콘덴서(둥근 금속) 오른쪽. 칩 글자 'M74LS04P'.  노치(반달 홈) 왼쪽 → 1번 핀 = 왼쪽 아래",
       font=font(17), fill=BLK)

# locator
LX0, LY0, LX1, LY1 = 0, 2380, 900, 3060
loc = src.crop((LX0, LY0, LX1, LY1)).resize((450, 340))
cv.paste(loc, (20, 95))
ls = 0.5
d.rectangle((20 + (130-LX0)*ls, 95 + (2770-LY0)*ls, 20 + (400-LX0)*ls, 95 + (2920-LY0)*ls), outline=RED, width=4)
d.text((20 + (420-LX0)*ls, 95 + (2800-LY0)*ls), "← U72", font=font(22, True), fill=RED)
d.text((20 + (300-LX0)*ls, 95 + (2440-LY0)*ls), "U64", font=font(22, True), fill=YEL)

# big chip photo
X0, Y0, X1, Y1 = 115, 2760, 410, 2930
sc = 2.6
im = src.crop((X0, Y0, X1, Y1)).resize((int((X1-X0)*sc), int((Y1-Y0)*sc)), Image.LANCZOS)
ax, ay = 560, 150
cv.paste(im, (ax, ay))
d.rectangle((ax-1, ay-1, ax+im.size[0], ay+im.size[1]), outline=BLK, width=2)
def M(x, y):
    return (ax + (x-X0)*sc, ay + (y-Y0)*sc)

x1, pitch, yt, yb = 158, 34.8, 2797, 2893
func = {1: "1A 입력", 2: "1Y 출력", 3: "2A 입력", 4: "2Y 출력", 5: "3A 입력", 6: "3Y 출력", 7: "GND",
        8: "4Y 출력", 9: "4A 입력", 10: "5Y 출력", 11: "5A 입력", 12: "6Y 출력", 13: "6A 입력", 14: "+5V"}
def color(n):
    return GRN if n == 7 else (RED if n == 14 else BLUE)
for n in range(1, 8):          # bottom row, left -> right
    cx, cy = M(x1 + (n-1)*pitch, yb)
    label((cx, cy + 48), str(n), 22, fg=WHITE, bg=color(n))
    label((cx, cy + 84), func[n], 14, fg=color(n), bg=WHITE)
for i, n in enumerate(range(14, 7, -1)):   # top row, left -> right: 14..8
    cx, cy = M(x1 + i*pitch, yt)
    label((cx, cy - 48), str(n), 22, fg=WHITE, bg=color(n))
    label((cx, cy - 84), func[n], 14, fg=color(n), bg=WHITE)
cx, cy = M(x1, yb)
label((cx - 30, cy + 120), "↑ 1번 핀 (노치 쪽)", 16, bg=YEL, anchor="lm")

# gate table
tx, ty = 20, 660
d.text((tx, ty), "내부 연결 (입력 → 출력, 출력 = 입력의 반대)", font=font(22, True), fill=BLK); ty += 40
rows = [("인버터 1", "핀 1 → 핀 2"), ("인버터 2", "핀 3 → 핀 4   (측정: 핀 4 = 3V 이상, 2026-11-06)"),
        ("인버터 3", "핀 5 → 핀 6"), ("인버터 4", "핀 9 → 핀 8"),
        ("인버터 5", "핀 11 → 핀 10"), ("인버터 6", "핀 13 → 핀 12"),
        ("전원", "핀 14 = +5V,  핀 7 = GND (검정 프로브 기준점)")]
for a, b in rows:
    d.text((tx + 10, ty), a, font=font(19, True), fill=BLK)
    d.text((tx + 130, ty), b, font=font(19), fill=BLK)
    ty += 32

ty += 20
d.text((tx, ty), "이 칩의 역할 (추정)", font=font(22, True), fill=BLK); ty += 40
for t in [
    "X1 수정 발진자·트리머·저항 2개와 붙어 있어 14.318MHz 발진용으로 추정 (배치로 판단, 결선 미확인).",
    "어느 인버터가 X1에 붙어 있는지는 아직 모름 → 수리 기록 C2 (전원 끄고 X1 다리 ↔ U72 핀 도통).",
    "",
    "전원 켜고 DC로 잴 때: 발진 중인 인버터는 입력·출력 모두 약 1–3V.",
    "  0V 근처나 3.5V 이상에 붙어 있으면 그 인버터는 발진하지 않는 것.",
    "Hz로 잴 때: 발진 출력 핀에서 약 14.3MHz (테스터가 이 대역을 재지 못할 수도 있음).",
]:
    d.text((tx + 10, ty), t, font=font(18), fill=BLK); ty += 30

ty += 10
d.text((tx, ty), "주의: 14.3MHz 발진 회로는 프로브를 대는 것만으로 멈추거나 흔들릴 수 있음. 값이 이상하면 한 번 더 잴 것.",
       font=font(18, True), fill=RED)

cv.save(OUT, quality=92)
print(cv.size, ty)
