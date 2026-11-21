"""ROM·PROM 덤프 대상 11개 위치 그림 (docs/11-rom-dump-list.md 용).
사용: python tools/annotate_rom_dump.py photos/overview/front/202813_front-flat_layout-ref.jpg analysis/rom_dump_locations.jpg
칩 위치는 data/bom.csv 의 1000x1600 격자 좌표를 앞면 기준 사진 크기로 늘려서 씀 (보정값 SX, SY, OX, OY).
"""
import csv, sys
from PIL import Image, ImageOps, ImageDraw, ImageFont

SRC, OUT = sys.argv[1], sys.argv[2]
BOM = "data/bom.csv"
im = ImageOps.exif_transpose(Image.open(SRC)).convert("RGB")
W0, H0 = im.size
SX, SY, OX, OY = W0 / 1000, H0 / 1600, 0, 0
SCALE = 1300 / W0
im = im.resize((round(W0 * SCALE), round(H0 * SCALE)), Image.LANCZOS)

# ref: (순위, 표시 라벨, 종류)
TARGETS = {
    "U45": (1, "C/D8", "2764"), "U46": (1, "EF5", "2764"),
    "U65": (2, "VD5", "2764"), "U70": (2, "CHR P4", "2764"),
    "U50": (3, "1", "82S129"), "U51": (3, "2", "82S129"),
    "U36": (3, "3", "82S129"), "U38": (3, "", "82S129"),
    "U18": (4, "M", "82S129"), "U17": (4, "?", "미확정"), "U5": (4, "", "82S123"),
}
COL = {1: (230, 20, 20), 2: (255, 140, 0), 3: (0, 110, 230), 4: (150, 40, 190)}
F = lambda s: ImageFont.truetype("C:/Windows/Fonts/malgunbd.ttf", s)

TOP, BOT = 110, 190
cv = Image.new("RGB", (im.width, im.height + TOP + BOT), "white")
cv.paste(im, (0, TOP))
d = ImageDraw.Draw(cv)

def P(x, y):
    return (x * SX + OX) * SCALE, (y * SY + OY) * SCALE + TOP

rows = {r["ref"]: r for r in csv.DictReader(open(BOM, encoding="utf-8"))}
for ref, (rank, lab, kind) in TARGETS.items():
    r = rows[ref]
    a = P(float(r["x0"]), float(r["y0"])); b = P(float(r["x1"]), float(r["y1"]))
    col = COL[rank]
    d.rectangle((a[0], a[1], b[0], b[1]), outline=col, width=6)
    t = ref + (f" {lab}" if lab else "")
    l, t0, rr, bb = d.textbbox((0, 0), t, font=F(28), anchor="lt")
    tw, th = rr - l, bb - t0
    cx, cy = (a[0] + b[0]) / 2, (a[1] + b[1]) / 2
    pos = {"U17": "left", "U18": "right", "U50": "below", "U51": "below2", "U38": "above"}.get(ref, "above")
    if pos == "above":
        tx, ty = cx - tw / 2, a[1] - th - 16
    elif pos == "below":
        tx, ty = cx - tw / 2 - 30, b[1] + 10
    elif pos == "below2":
        tx, ty = cx - tw / 2 + 10, b[1] + 10 + th + 18
    elif pos == "left":
        tx, ty = a[0] - tw - 18, cy - th / 2
    else:
        tx, ty = b[0] + 14, cy - th / 2
    tx = min(max(tx, 8), cv.width - tw - 12)
    d.rectangle((tx - 7, ty - 6, tx + tw + 7, ty + th + 6), fill=(255, 255, 255), outline=col, width=3)
    d.text((tx, ty), t, font=F(28), fill=col, anchor="lt")

d.text((16, 10), "ROM·PROM 덤프 대상 11개 위치 (본체 보드 앞면, 슬롯이 위)", font=F(36), fill=(0, 0, 0))
d.text((16, 60), "칩 위 글자 = 참조번호와 칩에 붙은 라벨. 색 = 읽는 순서 (docs/11-rom-dump-list.md)", font=F(24), fill=(0, 0, 0))
y = TOP + im.height + 14
legend = [(1, "1순위: U45·U46 시스템 ROM (2764)"), (2, "2순위: U65·U70 비디오·문자 ROM (2764)"),
          (3, "3순위: U50·U51·U36·U38 주소 디코드 PROM (82S129)"),
          (4, "4순위: U18·U17 FDD, U5 Z80 (U17은 PROM인지 미확정 → 먼저 도통 확인)")]
for i, (rank, text) in enumerate(legend):
    yy = y + i * 40
    d.rectangle((16, yy + 6, 46, yy + 30), outline=COL[rank], width=5)
    d.text((60, yy), text, font=F(24), fill=COL[rank])
cv.save(OUT, quality=88)
print(cv.size)
