import cv2, numpy as np, glob, json
from PIL import Image, ImageOps
import sys
# 사용법: python register_back_zoom.py <뒷면 기준 스캔.jpg> <확대 사진 폴더/> <출력.json>
REF,U,OUT=sys.argv[1],sys.argv[2],sys.argv[3]
ref=cv2.imread(REF,cv2.IMREAD_GRAYSCALE)
RS=0.6; refs=cv2.resize(ref,None,fx=RS,fy=RS)
cl=cv2.createCLAHE(3.0,(8,8)); refs=cl.apply(refs)
sift=cv2.SIFT_create(nfeatures=40000)
kr,dr=sift.detectAndCompute(refs,None)
bf=cv2.BFMatcher()
out={}
for f in sorted(glob.glob(U+'*.jpg')):
    im=np.array(ImageOps.exif_transpose(Image.open(f)).convert('L'))
    best=None
    for s in (0.15,0.2,0.25):
        ims=cl.apply(cv2.resize(im,None,fx=s,fy=s))
        k,d=sift.detectAndCompute(ims,None)
        m=bf.knnMatch(d,dr,k=2)
        good=[a for a,b in m if a.distance<0.8*b.distance]
        if len(good)<8: continue
        src=np.float32([k[g.queryIdx].pt for g in good]); dst=np.float32([kr[g.trainIdx].pt for g in good])
        A,mask=cv2.estimateAffinePartial2D(src,dst,method=cv2.RANSAC,ransacReprojThreshold=4,maxIters=20000,confidence=0.999)
        if A is None: continue
        sc=np.hypot(A[0,0],A[1,0]); inl=int(mask.sum())
        if 0.4<sc<2.5 and (best is None or inl>best[0]): best=(inl,A,s,sc,len(good))
    if not best: print(f[-19:],'FAIL'); continue
    inl,A,s,sc,ng=best
    Af=np.vstack([A,[0,0,1]]); Hf=np.diag([1/RS,1/RS,1])@Af@np.diag([s,s,1])
    h,w=im.shape
    c=cv2.perspectiveTransform(np.float32([[0,0],[w,0],[w,h],[0,h]]).reshape(-1,1,2),Hf).reshape(-1,2)
    ang=np.degrees(np.arctan2(Hf[1,0],Hf[0,0]))
    print(f[-19:],'inl',inl,'/',ng,'rot',round(ang),'scale',round(np.hypot(Hf[0,0],Hf[1,0]),3),'ctr',c.mean(0).astype(int))
    out[f[-19:]]=dict(H=Hf.tolist(),inl=inl,corners=c.tolist())
json.dump(out,open(OUT,'w'))
