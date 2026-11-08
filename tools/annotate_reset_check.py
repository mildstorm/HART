"""리셋 회로 찾기 도통 측정 그림: U30 핀 40 ↔ LM339(U3) 출력, 74LS05(U10) 출력.
사용: python tools/annotate_reset_check.py analysis/reset_check.jpg
재료: analysis/u30_pins.jpg (U30 핀 번호), 사용자 사진 224802(LM339), 230032(74LS05).
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
BLK, WHT, RED, BLU, GRN, GRY = (0, 0, 0), (255, 255, 255), (220, 20, 20), (30, 90, 230), (0, 150, 60), (110, 110, 110)

# --- A: U30 (기존 핀 번호 그림에서 왼쪽 부분)
u30 = Image.open("analysis/u30_pins.jpg").convert("RGB")
sx = u30.width / 1540
a = u30.crop((0, int(140 * sx), int(720 * sx), int(740 * sx))).resize((720, 600), Image.LANCZOS)
da = ImageDraw.Draw(a)
da.ellipse((128 - 30, 118 - 30, 128 + 30, 118 + 30), outline=RED, width=7)   # 핀 40 (원 그림 128,258 → 잘라낸 좌표)

# --- B: LM339 (사진 224802, 반달 홈 왼쪽, 글자 똑바로 = 1번 왼쪽 아래)
b = ImageOps.exif_transpose(Image.open("photos/zoom/front/20261108_224802_LM339_resistors-diode_C2.jpg")).convert("RGB")
b = b.resize((2000, 1500), Image.LANCZOS).crop((1000, 560, 1760, 1020))
db = ImageDraw.Draw(b)
def pin(d, x, y, no, col, dashed=False, side="below"):
    r = 22
    if dashed:
        for k in range(0, 360, 30):
            d.arc((x - r, y - r, x + r, y + r), k, k + 15, fill=col, width=6)
    else:
        d.ellipse((x - r, y - r, x + r, y + r), outline=col, width=6)
    t = str(no); l, tt, rr, bb = d.textbbox((0, 0), t, font=F(26))
    tx, ty = x - (rr - l) / 2, (y + 30 if side == "below" else y - 62)
    if side == "left":
        tx, ty = x - r - (rr - l) - 16, y - 18
    if side == "right":
        tx, ty = x + r + 10, y - 18
    d.rectangle((tx - 5, ty + tt - 2, tx + (rr - l) + 5, ty + bb + 4), fill=col)
    d.text((tx, ty), t, font=F(26), fill=WHT)
pin(db, 85, 275, 1, BLU, side="below"); pin(db, 175, 275, 2, BLU, side="below")
pin(db, 85, 40, 14, BLU, dashed=True, side="right"); pin(db, 175, 40, 13, BLU, dashed=True, side="right")

# --- C: 74LS05 (사진 230032, 반달 홈 아래, 글자가 아래→위 = 1번 오른쪽 아래)
c = ImageOps.exif_transpose(Image.open("photos/zoom/front/20261108_230032_U4-U15_U21-U28_rows.jpg")).convert("RGB")
c = c.resize((1500, 2000), Image.LANCZOS).crop((300, 540, 560, 900)).resize((780, 1080), Image.LANCZOS)
dc = ImageDraw.Draw(c)
RY = [945, 820, 695, 570, 440, 315, 190]          # 오른쪽 줄 아래→위 = 1..7
for no in (2, 4, 6):
    pin(dc, 540, RY[no - 1], no, GRN, side="right")
LY = [190, 315, 440, 570, 695, 820, 945]          # 왼쪽 줄 위→아래 = 8..14
for no in (8, 10, 12):
    pin(dc, 178, LY[no - 8], no, GRN, side="left")
dc.ellipse((300, 900, 380, 990), outline=GRY, width=4)

# --- 합치기
W = 1560
cv = Image.new("RGB", (W, 120 + 640 + 70 + 1100 + 300), WHT)
d = ImageDraw.Draw(cv)
d.text((20, 14), "리셋 회로 찾기 — 도통 측정 (전원 끄고, 삐 모드)", font=F(38), fill=BLK)
d.text((20, 64), "프로브 하나는 U30 핀 40에 고정, 다른 하나로 파랑·초록 핀을 하나씩. 삐 나는 칩 = 리셋을 만드는 칩", font=F(22), fill=BLK)
y0 = 120
cv.paste(a, (20, y0)); d.text((30, y0 + 610), "① U30 (메인 CPU): 빨강 = 핀 40 (위 줄 맨 왼쪽)", font=F(24), fill=RED)
cv.paste(b, (W - 20 - b.width, y0 + 40)); d.text((W - 20 - b.width, y0), "② LM339 (U3): 반달 홈 왼쪽 기준", font=F(24), fill=BLU)
d.text((W - 20 - b.width, y0 + 40 + b.height + 8), "파랑 실선 = 아래 줄 1·2번. 점선 = 위 줄 14·13번\n(사진에서 칩에 가려 안 보임, 1·2번 바로 위)", font=F(20), fill=BLU, spacing=6)
y1 = y0 + 690
cv.paste(c, (20, y1)); d.text((820, y1 + 10), "③ 74LS05 (U10)", font=F(28), fill=GRN)
for i, t in enumerate([
    "확장 슬롯 옆 칩 줄, 74LS04 왼쪽",
    "사진처럼 반달 홈이 아래일 때:",
    "  오른쪽 줄 아래→위 = 1~7번",
    "  왼쪽 줄 위→아래 = 8~14번",
    "초록 = 출력 핀 2·4·6 (오른쪽)",
    "           8·10·12 (왼쪽)",
    "회색 원 = 반달 홈",
]):
    d.text((820, y1 + 60 + i * 40), t, font=F(22), fill=GRN if i in (0, 4, 5) else BLK)
y2 = y1 + 1100
for i, (t, col) in enumerate([
    ("결과: LM339 쪽에서 삐 → 리셋 = LM339 + C2(22µF) + 저항·다이오드 회로. 74LS05 쪽에서 삐 → 리셋 = 74LS05 (Z80·키보드 쪽)", BLK),
    ("둘 다 안 삐 → 다른 칩. 그때 U30 핀 40 ↔ 슬롯 핀 31(RES)도 확인", BLK),
    ("주의: 전원 반드시 끄고. 프로브 끝이 옆 핀에 같이 닿지 않게", RED),
]):
    d.text((20, y2 + i * 42), t, font=F(22), fill=col)
cv.save(OUT, quality=88)
print(cv.size)
