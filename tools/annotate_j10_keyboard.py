"""J10(키보드 단자) 주변 뒷면 배선 판독 그림.
뒷면 확대 사진(20261105_212435)을 앞면 기준 좌표(202813)로 옮겨(보드를 앞에서 투시한 방향) 표시.
사용: python tools/annotate_j10_keyboard.py analysis/j10_keyboard_back.jpg
좌표는 앞면 기준 사진(2089x3363) 픽셀. 판독 2026-11-07.
"""
import json, sys
import numpy as np, cv2
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
R = json.load(open("data/front_back_registration.json", encoding="utf-8"))
Z = json.load(open("data/back_zoom_registration.json", encoding="utf-8"))
NAME = "20261105_212435.jpg"
FX0, FY0, FX1, FY1, S = 900, 2900, 1360, 3290, 2.0

def polyv(c, x, y):
    x, y = x / 1000, y / 1000
    T = np.stack([np.ones_like(x), x, y, x*x, x*y, y*y, x**3, x*x*y, x*y*y, y**3], -1)
    c = np.array(c)
    return T @ c[:, 0], T @ c[:, 1]

ph = np.array(ImageOps.exif_transpose(Image.open("photos/zoom/back/" + NAME)).convert("RGB"))
Hi = np.linalg.inv(np.array(Z["photos"][NAME]["H_photo_to_scan"]))
W, H = int((FX1 - FX0) * S), int((FY1 - FY0) * S)
uu, vv = np.meshgrid(np.arange(W), np.arange(H))
bx, by = polyv(R["front_to_back"], FX0 + uu / S, FY0 + vv / S)
P = np.stack([bx, by, np.ones_like(bx)], -1) @ Hi.T
back = cv2.remap(ph, (P[..., 0] / P[..., 2]).astype(np.float32), (P[..., 1] / P[..., 2]).astype(np.float32), cv2.INTER_CUBIC)

F, FB = "C:/Windows/Fonts/malgun.ttf", "C:/Windows/Fonts/malgunbd.ttf"
font = lambda sz, b=False: ImageFont.truetype(FB if b else F, sz)
BLK, WHITE, RED, YEL, BLUE, GRN, ORG, GRY = (0,0,0), (255,255,255), (230,20,20), (255,220,0), (0,90,230), (0,160,60), (255,130,0), (120,120,120)

im = Image.fromarray(back)
TOP = 110
cv = Image.new("RGB", (W + 40, H + TOP + 430), WHITE)
cv.paste(im, (20, TOP))
d = ImageDraw.Draw(cv)
M = lambda x, y: (20 + (x - FX0) * S, TOP + (y - FY0) * S)

def ring(c, r, col, w=4, dash=False):
    d.ellipse((c[0]-r, c[1]-r, c[0]+r, c[1]+r), outline=col, width=w)
def label(xy, text, sz=17, fg=BLK, bg=WHITE, anchor="mm"):
    f = font(sz, True)
    bb = d.textbbox(xy, text, font=f, anchor=anchor)
    d.rectangle((bb[0]-4, bb[1]-3, bb[2]+4, bb[3]+3), fill=bg, outline=BLK)
    d.text(xy, text, font=f, fill=fg, anchor=anchor)

# J10 패드 (앞면 좌표): 열 A = SIP·U80 쪽, 열 B = U81 쪽. 행 1 = GND 끝(케이스 반대쪽), 행 8 = 케이스 쪽
XA, XB = 1187.7, 1222.3
ROWS = [2950, 2984, 3018, 3053, 3088, 3120, 3155, 3190]
for i, y in enumerate(ROWS, 1):
    for x in (XA, XB):
        ring(M(x, y), 15, YEL, 3)
    label((M(XB, y)[0] + 42, M(XB, y)[1]), str(i), 15, fg=BLK, bg=YEL)
for x in (XA, XB):
    ring(M(x, ROWS[0]), 19, RED, 6)
label((M(XA, ROWS[0])[0] - 10, M(XA, ROWS[0])[1] - 46), "GND (측정 확인)", 18, fg=WHITE, bg=RED)
ring(M(XB, ROWS[7]), 19, ORG, 6)
label((M(XB, ROWS[7])[0] + 100, M(XB, ROWS[7])[1] + 4), "+5V 추정", 18, fg=WHITE, bg=ORG)
# 보드 가장자리 전원선과 U81 핀 16
u81p16 = M(1307.7, 3184.6)
ring(u81p16, 17, ORG, 5)
label((u81p16[0] + 10, u81p16[1] - 40), "U81 핀16(Vcc)", 15, fg=WHITE, bg=ORG)
bus_y = M(0, 3236.5)[1]
d.line((M(XB, 3205)[0], bus_y, u81p16[0], bus_y), fill=ORG, width=5)
label((M(1150, 0)[0], bus_y + 26), "보드 가장자리 전원선 (U81 핀16과 같은 선)", 15, fg=BLK, bg=(255, 220, 180))
# 미실장 구멍 열
XU = 1118
for y in [2950, 2984, 3018, 3053, 3088, 3121, 3191]:
    ring(M(XU, y), 14, BLUE, 3)
label((M(XU, 2925)[0], M(XU, 2925)[1]), "미실장 구멍 7개", 15, fg=WHITE, bg=BLUE)
label((M(XU, 3155)[0] - 6, M(XU, 3155)[1]), "7행 없음", 13, fg=WHITE, bg=BLUE)
# SIP 저항 어레이
x0, y0 = M(1030, 2975); x1, y1 = M(1062, 3272)
d.rectangle((x0, y0, x1, y1), outline=GRN, width=4)
label(((x0 + x1) / 2 - 20, y0 - 22), "SIP 9핀 (저항 어레이 추정)", 15, fg=WHITE, bg=GRN)
label((M(940, 2925)[0], M(940, 2925)[1]), "U80 74LS257", 16, fg=BLK, bg=YEL)
label((M(1300, 2925)[0], M(1300, 2925)[1]), "U81 74LS257", 16, fg=BLK, bg=YEL)

d.text((20, 10), "J10 키보드 단자 — 뒷면 배선 (앞에서 투시한 방향, 뒷면 사진 212435)", font=font(26, True), fill=BLK)
d.text((20, 52), "사진 위쪽 = U66·U67·U68 쪽(GND 끝),  아래쪽 = 보드 가장자리·케이스 쪽.  사용자 사진(케이스가 위)과는 180° 돌아간 방향", font=font(16), fill=BLK)
d.text((20, 78), "열 A = SIP·U80 쪽,  열 B = U81 쪽.  숫자 = 행 번호 (1 = GND 끝)", font=font(16), fill=BLK)

ty = TOP + H + 18
for t, b, c in [
    ("판독 결과", True, BLK),
    ("• 행1 두 핀 = GND: 슬롯1 핀 26과 도통 (사용자 측정, 확실)", False, BLK),
    ("• 행8 열B = +5V 추정: 뒷면 선이 보드 가장자리 선으로 내려가고,", False, BLK),
    ("   같은 선에 U81 핀16(Vcc)이 붙음 (U81 핀 번호는 칩 글자 방향으로 판단)", False, BLK),
    ("• 미실장 구멍 7개: J10 행과 같은 간격(7행만 없음) → 다른 키보드용 단자 자리 추정", False, BLK),
    ("• SIP 9핀 저항 어레이: 키보드 데이터선 풀업 추정.", False, BLK),
    ("   옆의 U80·U81(74LS257)이 키보드 데이터를 데이터 버스로 읽는 칩일 가능성", False, BLK),
    ("• 나머지 13핀: 대부분 앞면 선으로 나감. 앞면은 핀헤더 몸체가 가려 판독 불가", False, RED),
    ("", False, BLK),
    ("측정으로 확정할 것", True, BLK),
    ("1. 전원 켜고(검정 GND): 16핀 전압. 행8 열B가 약 5V인지, 다른 전원 핀이 있는지", False, BLK),
    ("2. 전원 끄고(도통): 각 핀 ↔ U80·U81 입력 핀(2,3,5,6,10,11,13,14), ↔ SIP 각 핀", False, BLK),
]:
    d.text((20, ty), t, font=font(17, b), fill=c); ty += 30

cv = cv.crop((0, 0, cv.width, ty + 10))
cv.save(OUT, quality=92)
print(cv.size)
