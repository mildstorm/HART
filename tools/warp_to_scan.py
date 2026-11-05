import json,cv2,numpy as np,sys
from PIL import Image, ImageOps
# 사용법: python warp_to_scan.py <registration.json> <사진폴더/> <사진파일명> x0 y0 x1 y1 [배율] [출력.jpg]
H=json.load(open(sys.argv[1]))
PH=H.get('photos',H)
DIR=sys.argv[2]; sys.argv=sys.argv[2:]
name=sys.argv[1]; x0,y0,x1,y1=map(int,sys.argv[2:6]); K=float(sys.argv[6]) if len(sys.argv)>6 else 3
im=cv2.cvtColor(np.array(ImageOps.exif_transpose(Image.open(DIR+name))),cv2.COLOR_RGB2BGR)
e=PH[name]; Hf=np.array(e.get('H_photo_to_scan',e.get('H')))
T=np.array([[K,0,-K*x0],[0,K,-K*y0],[0,0,1]])
out=cv2.warpPerspective(im,T@Hf,(int(K*(x1-x0)),int(K*(y1-y0))),flags=cv2.INTER_CUBIC)
# grid every 50 ref px
for gx in range((x0//50+1)*50,x1,50):
    X=int(K*(gx-x0)); cv2.line(out,(X,0),(X,8),(0,255,255),2); cv2.putText(out,str(gx),(X+2,22),0,0.6,(0,255,255),2)
for gy in range((y0//50+1)*50,y1,50):
    Y=int(K*(gy-y0)); cv2.line(out,(0,Y),(8,Y),(0,255,255),2); cv2.putText(out,str(gy),(2,Y-3),0,0.6,(0,255,255),2)
cv2.imwrite(sys.argv[7] if len(sys.argv)>7 else 'warped.jpg',out,[cv2.IMWRITE_JPEG_QUALITY,90])
print(out.shape)
