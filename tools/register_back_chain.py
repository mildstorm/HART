import cv2, numpy as np, glob, json, os, sys
from PIL import Image, ImageOps
# 새 사진을 이미 정합된 사진(앵커)에 직접 맞춘 뒤, 앵커의 H를 이어 붙여 기준 좌표로 변환
# 사용법: python register_back_chain.py <앵커 정합.json> <앵커 사진 폴더> <새 사진 폴더> <출력.json>
# 기준 스캔과 직접 맞추는 register_back_zoom.py가 실패할 때(근접·조명 차이) 사용. 잘 맞은 새 사진(inl>=100)은 다음 사진의 앵커가 됨
ANCH_JSON, ANCH_DIR, NEW_DIR, OUT = sys.argv[1:5]
S = 0.3
sift = cv2.SIFT_create(nfeatures=8000)
cl = cv2.createCLAHE(3.0, (8, 8))
def load(f):
    im = np.array(ImageOps.exif_transpose(Image.open(f)).convert('L'))
    ims = cl.apply(cv2.resize(im, None, fx=S, fy=S))
    k, d = sift.detectAndCompute(ims, None)
    return im.shape, k, d
anc = {k: v for k, v in json.load(open(ANCH_JSON)).items() if v['inl'] >= 10}
A = {}
for name in anc:
    A[name] = load(os.path.join(ANCH_DIR, name))
fl = cv2.FlannBasedMatcher(dict(algorithm=1, trees=5), dict(checks=64))
out = {}
files = sorted(glob.glob(os.path.join(NEW_DIR, '*.jpg')))
for rnd in range(3):
 for f in files:
  if os.path.basename(f) in out: continue
  if True:
    shp, k, d = load(f)
    best = None
    for name, (ashp, ak, ad) in A.items():
        m = fl.knnMatch(d, ad, k=2)
        good = [a for a, b in m if a.distance < 0.7 * b.distance]
        if len(good) < 15: continue
        src = np.float32([k[g.queryIdx].pt for g in good]); dst = np.float32([ak[g.trainIdx].pt for g in good])
        Hm, mask = cv2.findHomography(src, dst, cv2.RANSAC, 4.0)
        if Hm is None: continue
        inl = int(mask.sum())
        if best is None or inl > best[0]: best = (inl, name, Hm)
    nm = os.path.basename(f)
    if not best or best[0] < 40:
        print(nm, 'FAIL', best[0] if best else 0); continue
    inl, name, Hm = best
    Sm = np.diag([S, S, 1]); Hfull = np.linalg.inv(Sm) @ Hm @ Sm  # new full px -> anchor full px
    Href = np.array(anc[name]['H']) @ Hfull
    h, w = shp
    c = cv2.perspectiveTransform(np.float32([[0, 0], [w, 0], [w, h], [0, h]]).reshape(-1, 1, 2), Href).reshape(-1, 2)
    print(nm, 'via', name[9:15], 'inl', inl, 'ctr', c.mean(0).astype(int))
    out[nm] = dict(H=Href.tolist(), inl=inl, via=name, corners=c.tolist())
    if inl >= 100:
        A[nm] = (shp, k, d); anc[nm] = dict(H=Href.tolist())
json.dump(out, open(OUT, 'w'))

