"""메인 6502 ↔ U64 연결 확인용 측정 핀 그림 (docs/13-u64-interface.md 5절).
사용: python tools/annotate_u64_interface.py analysis/u64_interface_measure.jpg
앞면 기준 사진 202813 원본 좌표. 다리 간격 34.47px (annotate_u30_pins.py와 같음).
가로 칩(U30, U64): 노치 왼쪽 → 아래 줄 왼쪽→오른쪽 1–20, 위 줄 오른쪽→왼쪽 21–40.
세로 칩(U65, U68, U80, U81): 글씨가 아래→위로 읽힘 = 노치 아래 → 1번 = 오른쪽 아래,
  오른쪽 줄 아래→위 1..N/2, 왼쪽 줄 위→아래 N/2+1..N.
"""
import sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

OUT = sys.argv[1]
src = ImageOps.exif_transpose(Image.open("photos/overview/front/202813_front-flat_layout-ref.jpg")).convert("RGB")
P = 34.47
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)
FR = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgun.ttf", s)
BLK, WHT, RED, BLU, GRN, ORG, MAG, GRY = (0, 0, 0), (255, 255, 255), (230, 20, 20), (0, 90, 230), (0, 150, 60), (230, 120, 0), (200, 0, 180), (110, 110, 110)


def horiz(x1, ytop, ybot, n):
    """40핀 가로 칩: 핀 번호 → (x, y, 라벨 방향)"""
    return (x1 + (n - 1) * P, ybot, +1) if n <= 20 else (x1 + (40 - n) * P, ytop, -1)


def vert(xr, xl, ytop, pins, n):
    """세로 칩(노치 아래): 오른쪽 줄 아래→위 1..h, 왼쪽 줄 위→아래 h+1..pins"""
    h = pins // 2
    ybot = ytop + (h - 1) * P
    return (xr, ybot - (n - 1) * P, +1) if n <= h else (xl, ytop + (n - h - 1) * P, -1)


def panel(box, scale, title, marks, chips):
    x0, y0, x1, y1 = box
    im = src.crop(box).resize((int((x1 - x0) * scale), int((y1 - y0) * scale)), Image.LANCZOS)
    top = 56
    cv = Image.new("RGB", (im.width, im.height + top), WHT)
    cv.paste(im, (0, top))
    d = ImageDraw.Draw(cv)
    M = lambda x, y: ((x - x0) * scale, (y - y0) * scale + top)
    d.text((10, 8), title, font=F(30), fill=BLK)
    for ref, (a, b, c, e), col in chips:
        p, q = M(a, b), M(c, e)
        d.rectangle((p[0], p[1], q[0], q[1]), outline=col, width=4)
        bb = d.textbbox((p[0] + 6, p[1] + 4), ref, font=F(26))
        d.rectangle((bb[0] - 4, bb[1] - 2, bb[2] + 4, bb[3] + 2), fill=col)
        d.text((p[0] + 6, p[1] + 4), ref, font=F(26), fill=WHT)
    for (x, y, side), text, col, horizontal in marks:
        cx, cy = M(x, y)
        r = 15 * scale
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=col, width=5)
        if not text:
            continue
        f = F(22)
        if horizontal:
            tx, ty, anc = cx, cy + side * 42 * scale, "mm"
        else:
            tx, ty, anc = cx + side * 26 * scale, cy, "lm" if side > 0 else "rm"
        bb = d.textbbox((tx, ty), text, font=f, anchor=anc)
        d.rectangle((bb[0] - 4, bb[1] - 2, bb[2] + 4, bb[3] + 2), fill=col)
        d.text((tx, ty), text, font=f, fill=WHT, anchor=anc)
    return cv


# 비디오 쪽 (원본 좌표, 눈으로 맞춘 다리 위치)
U64 = dict(x1=57, ytop=2514, ybot=2724)
U65 = dict(xr=970, xl=770, ytop=2518, pins=28)
U68 = dict(xr=1500, xl=1293, ytop=2520, pins=24)
h64 = lambda n: horiz(U64["x1"], U64["ytop"], U64["ybot"], n)
v65 = lambda n: vert(U65["xr"], U65["xl"], U65["ytop"], U65["pins"], n)
v68 = lambda n: vert(U68["xr"], U68["xl"], U68["ytop"], U68["pins"], n)
video = panel(
    (0, 2400, 1760, 3290), 1.0, "비디오 쪽: U64(보조 CPU) · U65(VD5 롬) · U68(6116 화면 메모리)",
    [
        (v68(8), "① U68-8 (A0)", RED, False),
        (v68(19), "① U68-19 (A10)", RED, False),
        (h64(33), "② U64-33 (D0)", BLU, True),
        (h64(22), "③ U64-25·24·23·22 (A15·A14·A13·A12)", GRN, True),
        (h64(23), "", GRN, True),
        (h64(24), "", GRN, True),
        (h64(25), "", GRN, True),
        (h64(20), "", GRN, True),
        (h64(19), "③ U64-19·20 (A10·A11)", GRN, True),
        (h64(1), "1 (GND)", GRY, True),
        (v65(20), "④ U65-20 (/CE)", ORG, False),
        (v65(2), "④ U65-2 (A12)", ORG, False),
    ],
    # 칩 몸체: 이 사진에서 눈으로 맞춘 원본 좌표 (U80·U81은 annotate_video_chips.py의 PIX와 같은 자리)
    [("U64", (20, 2480, 735, 2760), MAG), ("U65", (740, 2490, 1000, 3000), MAG),
     ("U68", (1270, 2490, 1525, 2935), MAG),
     ("U80", (842, 3004, 964, 3268), BLU), ("U81", (1286, 2954, 1378, 3268), BLU)],
)

U30 = dict(x1=207, ytop=1437, ybot=1642)
h30 = lambda n: horiz(U30["x1"], U30["ytop"], U30["ybot"], n)
main = panel(
    (150, 1380, 940, 1700), 1.25, "메인 CPU U30 (비교 대상 핀)",
    [(h30(9), "① U30-9 (A0)", RED, True), (h30(33), "② U30-33 (D0)", BLU, True),
     (h30(1), "1 (GND)", GRY, True)],
    [],
)

lines = [
    ("전원 끄고 멀티미터 도통(삑) 모드. 결과는 \"U68-8 → U81-4\"처럼 칩-핀으로 적어 주세요.", BLK, True),
    ("① 빨강: U68 핀 8(A0)·19(A10)이 어느 칩 몇 번에 붙는지. U80·U81(74LS257, 파랑 상자)일 가능성 큼 →", RED, True),
    ("     그 칩이면 입력 두 개가 U30-9(메인 A0)와 U64-22(U64 A12)에 붙는지 확인 = 짝/홀 칸 분할 확정", RED, False),
    ("② 파랑: U64-33(D0)이 붙는 칩들 중 U30-33(메인 D0)에도 붙는 칩(래치 74LS374/273·버퍼 245)이 있는지 = 키 코드 래치", BLU, True),
    ("③ 초록: U64 주소선 19·20·22·23·24·25번이 각각 어느 칩 몇 번으로 가는지 = U64 주소 디코드", GRN, True),
    ("④ 주황: U65 롬 20번(/CE)·2번(A12)이 어디로 가는지 = 롬이 $C000·$E000 두 곳에 보이는지", ORG, True),
    ("세로 칩은 노치가 아래(글씨가 아래→위로 읽힘): 1번 = 오른쪽 아래. 핀 위치는 사진에서 추정이라 칩 끝에서 개수로 한 번 더 세어 주세요.", GRY, False),
]
W = max(video.width, main.width)
H = video.height + main.height + 30 + len(lines) * 40 + 20
cv = Image.new("RGB", (W, H), WHT)
cv.paste(video, (0, 0))
cv.paste(main, (0, video.height + 10))
d = ImageDraw.Draw(cv)
y = video.height + main.height + 30
for t, c, b in lines:
    d.text((12, y), t, font=F(22) if b else FR(22), fill=c)
    y += 40
cv.save(OUT, quality=90)
print(cv.size)
