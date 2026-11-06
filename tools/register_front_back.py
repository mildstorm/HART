"""앞면 기준 사진과 뒷면 기준 사진을 같은 좌표로 맞춤.
뒷면을 좌우 반전·변형해 앞면 사진과 같은 크기(앞면 좌표)로 만든다.

사용: python tools/register_front_back.py <앞면.jpg> <뒷면.jpg> <출력.json> <출력폴더/>
출력:
  <출력.json>                  변환 계수 (뒷면→앞면, 앞면→뒷면 3차 다항식)
  <출력폴더>/back_on_front.jpg  앞면과 같은 크기로 맞춘 뒷면 (좌우 반전됨)
  <출력폴더>/front_back_overlay.jpg  앞면 50% + 뒷면 50%

방법 (2026-11-07):
 1) 수동 대응점 12개(네 모서리 고정 구멍, U30·U64·슬롯1 끝 핀)로 초기 호모그래피
 2) 양면에 똑같이 보이는 비아 구멍을 자동 검출, 가장 가까운 짝끼리 맞춰
    3차 다항식으로 반복 보정 (상호 최근접 + 이상치 제거)
수동 대응점은 판독 오차가 10px 안팎이라 초기값으로만 쓴다. 최종 정확도는 비아 짝 잔차로 본다.
"""
import sys, json
import numpy as np, cv2
from scipy.spatial import cKDTree

FRONT, BACK, OUTJ, OUTD = sys.argv[1:5]
PTS = [
    ((63, 83), (2046, 68)), ((2014, 52), (70, 70)), ((77, 3251), (2041, 3259)), ((2026, 3250), (65, 3261)),
    ((207, 1437), (1895, 1425)), ((207, 1642), (1895, 1632)),
    ((52, 2518), (2048, 2500)), ((52, 2728), (2048, 2705)), ((711, 2518), (1387, 2500)), ((711, 2728), (1387, 2705)),
    ((162, 92), (1930, 95)), ((162, 930), (1930, 921)),
]
frc = cv2.imread(FRONT); bkc = cv2.imread(BACK)
fr = cv2.cvtColor(frc, cv2.COLOR_BGR2GRAY); bk = cv2.cvtColor(bkc, cv2.COLOR_BGR2GRAY)
H, _ = cv2.findHomography(np.float32([p[1] for p in PTS]), np.float32([p[0] for p in PTS]), 0)

def holes(g):
    cl = cv2.createCLAHE(3.0, (16, 16)).apply(g)
    p = cv2.SimpleBlobDetector_Params()
    p.filterByColor = True; p.blobColor = 0
    p.minThreshold = 20; p.maxThreshold = 120; p.thresholdStep = 10
    p.filterByArea = True; p.minArea = 12; p.maxArea = 140
    p.filterByCircularity = True; p.minCircularity = 0.7
    p.filterByConvexity = True; p.minConvexity = 0.85
    p.filterByInertia = True; p.minInertiaRatio = 0.55
    return np.float32([k.pt for k in cv2.SimpleBlobDetector_create(p).detect(cl)])

def feats(P, deg=3):
    x, y = P[:, 0] / 1000, P[:, 1] / 1000
    cols = [np.ones_like(x)]
    for d in range(1, deg + 1):
        for i in range(d + 1):
            cols.append(x ** (d - i) * y ** i)
    return np.stack(cols, 1)

F = holes(fr); B = holes(bk); tf = cKDTree(F)
Pm = cv2.perspectiveTransform(B.reshape(-1, 1, 2), H).reshape(-1, 2)
coef = None
for rad in [20, 12, 8, 6, 5]:
    if coef is not None:
        Pm = feats(B) @ coef
    d, idx = tf.query(Pm, distance_upper_bound=rad); ok = np.isfinite(d)
    _, idx2 = cKDTree(Pm).query(F[idx[ok]])
    m = idx2 == np.where(ok)[0]
    bi = np.where(ok)[0][m]; fi = idx[ok][m]
    coef, *_ = np.linalg.lstsq(feats(B[bi]), F[fi], rcond=None)
    r = np.hypot(*((feats(B[bi]) @ coef) - F[fi]).T)
    k = r < max(3 * np.median(r), 3)
    bi, fi = bi[k], fi[k]
    coef, *_ = np.linalg.lstsq(feats(B[bi]), F[fi], rcond=None)
inv, *_ = np.linalg.lstsq(feats(F[fi]), B[bi], rcond=None)
r = np.hypot(*((feats(B[bi]) @ coef) - F[fi]).T)
print(f"비아 짝 {len(bi)}개, 잔차 평균 {r.mean():.2f}px, 중앙 {np.median(r):.2f}px, 90% {np.percentile(r, 90):.2f}px")

h, w = fr.shape
gy, gx = np.mgrid[0:h, 0:w].astype(np.float32)
M = (feats(np.stack([gx.ravel(), gy.ravel()], 1)) @ inv).astype(np.float32)
warped = cv2.remap(bkc, M[:, 0].reshape(h, w), M[:, 1].reshape(h, w), cv2.INTER_LINEAR)
cv2.imwrite(OUTD + "back_on_front.jpg", warped, [cv2.IMWRITE_JPEG_QUALITY, 92])
cv2.imwrite(OUTD + "front_back_overlay.jpg", cv2.addWeighted(frc, 0.5, warped, 0.5, 0), [cv2.IMWRITE_JPEG_QUALITY, 92])
json.dump(dict(
    front=FRONT, back=BACK,
    poly="3차 다항식. 입력 (x/1000, y/1000) 항 순서: 1, x, y, x², xy, y², x³, x²y, xy², y³",
    back_to_front=coef.tolist(), front_to_back=inv.tolist(),
    pairs=int(len(bi)), resid_mean_px=float(r.mean()), resid_p90_px=float(np.percentile(r, 90)),
    note="뒷면 기준 사진 픽셀 <-> 앞면 기준 사진 픽셀. 좌우 반전 포함. 비아 구멍 자동 짝맞춤으로 보정",
), open(OUTJ, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
