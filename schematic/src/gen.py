# -*- coding: utf-8 -*-
# Generates the Apple II clone board schematic page (placement map + block schematic + BOM)
import csv
import html
import os
import re
import sys

# block keys -> (Korean label, css var)
BLK = {
 'cpu':  ('메인 CPU / 버스', 'b-cpu'),
 'dec':  ('주소 디코드 / 소프트스위치', 'b-dec'),
 'ram':  ('DRAM 64KB + 주소 MUX', 'b-ram'),
 'rom':  ('시스템 ROM', 'b-rom'),
 'vid':  ('비디오 / 문자발생', 'b-vid'),
 'tim':  ('클럭 / 타이밍', 'b-tim'),
 'io':   ('I/O (게임·카세트·스피커)', 'b-io'),
 'z80':  ('Z80 서브시스템', 'b-z80'),
 'exp':  ('슬롯 / 확장 로직', 'b-exp'),
 'unk':  ('역할 미확인', 'b-unk'),
}

# ref, part, marking, x0,y0,x1,y1 (portrait, slots at top, 1000x1600 grid), block, conf, note
P = [
 ('U1','74LS373','8450D8',435,55,495,215,'z80','확인','Z80 주소/데이터 래치'),
 ('U2','Z80A CPU','SHARP LH0080A',505,100,840,215,'z80','확인','Z80A 4MHz급. CP/M 실행, 6502와 별도 동작 (2026-11-06 확인)'),
 ('U3','LM339','NS M8420',855,115,905,240,'io','확인','쿼드 컴퍼레이터: 카세트 입력 정형'),
 ('U4','74LS244','8448C5',440,225,495,355,'z80','확인','Z80 버스 버퍼'),
 ('U5','82S123','N82S123N',510,225,560,355,'z80','확인','32×8 바이폴라 PROM: Z80→6502 주소 변환 (덤프로 확인, SoftCard와 같은 매핑)'),
 ('U6','74LS367','8445E4',575,225,630,355,'z80','확인','Z80 주소 버퍼'),
 ('U7','74LS367','8445E4',645,225,700,355,'z80','확인','Z80 주소 버퍼'),
 ('U8','74LS163','8501D2',715,225,770,355,'z80','확인','동기 카운터 (Z80 클럭/웨이트 생성 추정)'),
 ('U9','74LS00','8501C2',780,225,830,355,'z80','확인','NAND 게이트'),
 ('U10','74LS05','8432D0',445,400,500,525,'z80','확인','오픈컬렉터 인버터 (DMA/RES 라인 구동 추정)'),
 ('U11','74LS04','5050C0',515,400,570,525,'z80','확인','인버터'),
 ('U12','74LS74','74LS74A',580,400,635,525,'z80','확인','D-FF'),
 ('U13','74LS32','8435D1',650,400,705,525,'z80','확인','OR 게이트'),
 ('U14','74LS74','74LS74A',715,400,770,525,'z80','확인','D-FF'),
 ('U15','74LS10','8438D0',780,400,835,525,'z80','확인','3입력 NAND'),
 ('U16','74LS323','8432B0',85,505,145,630,'exp','확인','8비트 3-state 시프트/저장 레지스터'),
 ('U17','82S129','N82S129N K8509 S (확인)',155,505,215,630,'exp','확인','Disk II 16-섹터 시퀀서(P6) 상위 4비트 제어신호 PROM (U18과 짝, 덤프 확인)'),
 ('U18','82S129','N82S129N · 라벨 "M"',225,505,280,630,'exp','확인','Disk II 16-섹터 시퀀서(P6) 하위 4비트 다음상태 PROM (U17과 짝, 덤프 확인)'),
 ('U19','74LS174','MB74LS174',290,505,345,630,'exp','확인','6비트 D-FF 래치'),
 ('U20','74LS259','5050C1',355,505,410,630,'exp','확인','8비트 어드레서블 래치 (뱅크/모드 스위치 추정)'),
 ('U21','74LS139','8502D0',445,560,500,690,'dec','확인','듀얼 2→4 디코더'),
 ('U22','74LS138','8450C5',510,560,565,690,'dec','확인','3→8 디코더. 입력 A·B·C = 메인 A8·A9·A10, /G2A = U76 /2Q(타이밍), /G2B = 메인 A11, G1 = U50 O4 → Y3 = $C3xx (U62 스위치 켜기) (측정 2026-11-25)'),
 ('U23','74LS138','8450C5',580,560,635,690,'dec','확인','3→8 디코더 (DEVICE SELECT 추정). Y0(핀 15) → U49 CLK (측정 2026-11-26)'),
 ('U24','74LS138','8450C5',645,560,700,690,'dec','확인','3→8 디코더 ($C0xx 내부 I/O 추정)'),
 ('U25','74LS259','5050C1',715,560,770,690,'dec','확인','소프트스위치 래치 (TEXT/MIXED/PAGE2/HIRES·AN0-3, Apple II F14 상당)'),
 ('U26','74LS74','74LS74A',785,560,835,690,'io','확인','D-FF (스피커/카세트 출력 토글 추정)'),
 ('U27','NE558','NE558N VV8441',845,560,905,690,'io','확인','쿼드 타이머: 패들 PDL0-3 (Apple II H13 상당)'),
 ('U28','74LS251','8444D0',915,560,970,690,'io','확인','8→1 MUX: 버튼/패들/카세트IN 읽기 (Apple II H14 상당)'),
 ('U29','74LS245','8502E3',20,680,80,835,'cpu','확인','메인 CPU 데이터 버스 트랜시버'),
 ('U30','UM6502','UM6502 8404',85,680,420,785,'cpu','확인','메인 CPU (1.023MHz)'),
 ('U31','74LS367','8445E4',445,710,500,835,'cpu','확인','주소 버스 버퍼 (Apple II 8T97 대체)'),
 ('U32','74LS367','8445E4',515,710,570,835,'cpu','확인','주소 버스 버퍼'),
 ('U33','74LS367','8445E4',580,710,635,835,'cpu','확인','주소 버스 버퍼'),
 ('U34','74LS00','8501C2',650,710,705,835,'dec','확인','NAND. 1Y = NAND(메인 A15, A14) → U50 핀 1. 2A·3B = 메인 Φ0(버퍼 전). 2Y(핀 6) = NAND(Φ0, 34-5) → U35 /2G. 34-5 = U49 2Q(핀 7), 같은 넷이 U50 핀 7·U36 핀 5 (측정 2026-11-24~26)'),
 ('U35','74LS139','8502D0',715,710,770,835,'dec','확인','듀얼 2→4 디코더. 1번: A = 메인 A10, B = 메인 A9, /1G = U62 /2Q, 1Y3 → U62 CLK(스위치 끄기). 2번: /2G = U34 2Y, 2A = U36 O2, 2B = U36 O1, 2Y0 → U45 /CE, 2Y1 → U46 /CE, 2Y2 → U51 핀 6 (측정 2026-11-25~26)'),
 ('U36','82S129','N82S129N · 라벨 "3"',780,710,835,835,'dec','확인','256×4 PROM (덤프 확인). 입력: 1(A6) = U51 O4, 6(A1) = 메인 A13, 2(A5) = NAND(A15, A14)(U34 1Y), 7(A2) = GND, /CE1·/CE2 = GND, 15(A7) = U49 3Q, 4(A3) = 메인 A12(U33 핀 11). O1(핀 12) → U35 2B, O2(핀 11) → U35 2A, O3(핀 10) → U45·U46 A12(핀 2). U35 2Y2 = U51 O4·$E000–$EFFF (U68 창), 2Y1(U46) = $E000–$FFFF(U51 O4 = 0, 3Q = 0), 2Y0(U45) = $D000 등 (측정 2026-11-26). 덤프는 주소 비트 보정본 (docs/11)'),
 ('U37','74LS174','MB74LS174 8424',845,710,905,835,'dec','확인','6비트 래치'),
 ('U38','82S129','N82S129N K8509',915,710,970,835,'dec','확인','256×4 PROM (디코드용)'),
 ('U39','MN4164','MN4164P-25',20,870,75,1000,'ram','확인','64K×1 DRAM, D0 추정'),
 ('U40','MN4164','MN4164P-25',85,870,140,1000,'ram','확인','64K×1 DRAM'),
 ('U41','MN4164','MN4164P-25',150,870,210,1000,'ram','확인','64K×1 DRAM'),
 ('U42','MN4164','MN4164P-25',220,870,280,1000,'ram','확인','64K×1 DRAM'),
 ('U43','74LS153','8449D0',285,870,340,1000,'ram','확인','DRAM 주소 MUX (CPU/비디오 × ROW/COL)'),
 ('U44','74LS153','8449D0',350,870,405,1000,'ram','확인','DRAM 주소 MUX'),
 ('U45','2764 EPROM','NEC D2764D · 라벨 "C/D8"',425,870,510,1110,'rom','확인','$C000–$DFFF 시스템 ROM ($C300·$C800 Videx 80컬럼, $C600 Disk II 부트, $D000–$DFFF BASIC 전반부)'),
 ('U46','2764 EPROM','NEC D2764D · 라벨 "EF5"',545,870,635,1110,'rom','확인','$E000–$FFFF 시스템 ROM ($E000–$F7FF BASIC 후반부, $F800–$FFFF Autostart Monitor, 슬롯 6 즉시 부팅)'),
 ('U47','74LS157','8450E1',650,870,705,1000,'vid','확인','2→1 MUX: U68 주소 A6–A9 (A = U64 쪽, B = 메인 쪽, SELECT = U51 O2) (측정 2026-11-24)'),
 ('U48','74LS02','8442D1',720,870,775,1000,'dec','확인','NOR. 3Y = NOR(U64 A12, Φ0) → U68 A8(U64 쪽). 1Y → U51 핀 2, 2Y = NOR(U62 /2Q, 48-6) → U51 핀 15 (측정 2026-11-24~25)'),
 ('U49','74LS175','5070D0',785,870,840,1000,'tim','확인','쿼드 D-FF. 2Q(핀 7) → U34 2B·U50 핀 7·U36 핀 5 (U35 2번 디코더 enable 조건), 3Q(핀 10) → U36 핀 15, CLK(핀 9) = U23 Y0(슬롯 0 DEVICE SELECT 추정) → 랭귀지 카드식 뱅크 전환 래치로 추정. /CLR(핀 1) = 1kΩ 풀업, 리셋과 직결 아님 (측정 2026-11-26). 핀 8 = GND'),
 ('U50','82S129','N82S…509 · 라벨 "1"',850,870,905,1000,'dec','확인','256×4 PROM (덤프 확인). 핀 1 = NAND(A15, A14)(U34), 핀 5 = 메인 A13, 핀 6 = GND, /CE = GND. O4(핀 9) → U22 G1 (측정 2026-11-25)'),
 ('U51','82S129','N82S…509 · 라벨 "2"',915,870,970,1000,'dec','확인','256×4 PROM (덤프 확인). O2(핀 11) = U68 주소 MUX SELECT. O4(핀 9) → U36 A6(핀 1). 입력: 1 = U64 R/W, 2 = U48 1Y, 4 = U77 1Y2, 6 = U35 2Y2, 7 = Φ0, 15 = U48 2Y. /CE = GND (측정 2026-11-24~25)'),
 ('U52','MN4164','MN4164P-25',20,1035,75,1170,'ram','확인','64K×1 DRAM'),
 ('U53','MN4164','MN4164P-25',85,1035,140,1170,'ram','확인','64K×1 DRAM'),
 ('U54','MN4164','MN4164P-25',150,1035,210,1170,'ram','확인','64K×1 DRAM'),
 ('U55','MN4164','MN4164P-25',220,1035,280,1170,'ram','확인','64K×1 DRAM, D7 추정'),
 ('U56','74LS153','8449D0',285,1035,340,1170,'ram','확인','DRAM 주소 MUX'),
 ('U57','74LS153','8449D0',350,1035,405,1170,'ram','확인','DRAM 주소 MUX'),
 ('U58','74LS157','8450E1',650,1035,705,1170,'vid','확인','2→1 MUX: U68 주소 A0·A5·A10 (A = U64 쪽, B = 메인 쪽) (측정 2026-11-24)'),
 ('U59','74LS157','8450E1',715,1035,770,1170,'vid','확인','2→1 MUX: U68 주소 A1–A4 (A = U64 쪽, B = 메인 쪽) (측정 2026-11-24)'),
 ('U60','74LS00','8501C2',785,1035,840,1170,'tim','확인','NAND'),
 ('U61','74LS74','74LS74A',850,1035,905,1170,'tim','확인','D-FF'),
 ('U62','74LS74','74LS74AP',915,1035,970,1170,'tim','확인','D-FF. 2번 FF = Videx식 스위치: /PRE = U22 Y3($C3xx), CLK = U35 1Y3, D = GND, /CLR = +5V, /Q → U35 /1G·U48-5 (측정 2026-11-25)'),
 ('U63','74LS245','8502E3',425,1120,580,1175,'rom','확인','ROM/내부 데이터 버스 트랜시버'),
 ('U64','UM6502','UM6502 8404',15,1185,350,1300,'vid','확인','두 번째 6502. 화면 하단 기능키 바, 80컬럼 비디오, 한글 디스플레이 총괄 보조 CPU, 독립 동작. 클럭(핀 37) = U76 /2Q(핀 9) (측정 2026-11-25)'),
 ('U65','2764 EPROM','NEC D2764D · 라벨 "VD5"',365,1185,460,1425,'vid','확인','U64 보조 CPU 펌웨어 (화면 초기화, Apple/CPM 기능키 바 라벨, 비디오 제어)'),
 ('U66','74LS374','8445DD',480,1205,535,1370,'vid','확인','비디오 데이터 래치'),
 ('U67','74LS245','8502E3',545,1205,600,1370,'vid','확인','6116 데이터 버스 트랜시버'),
 ('U68','HM6116LP-3','Hitachi 8505',610,1190,710,1420,'vid','확인','2K×8 SRAM: 80컬럼 화면 버퍼, 메인($E000–$E7FF)·U64($4000/$5000) 공유. 주소 = U47·U58·U59 출력 (측정 2026-11-24)'),
 ('U69','74LS273','8452D0 M74LS273P',725,1205,780,1370,'vid','확인','8비트 D-FF 래치 (클리어 포함). 비디오 데이터/속성 래치 추정'),
 ('U70','2764 EPROM','라벨 "CHR P4"',795,1155,890,1390,'vid','확인','문자 발생 ROM: 2KB×4 뱅크 (영문 Normal/Inverse, 세미그래픽, 한글 자모 조합 폰트)'),
 ('U71','74LS166','8502C3',910,1230,965,1375,'vid','확인','8비트 병렬→직렬 시프트 (도트 출력)'),
 ('U72','74LS04','5050C0',60,1320,185,1375,'tim','확인','X1·트리머·저항 2개와 붙어 있음 → 14.318MHz 발진 인버터 (배치로 확인)'),
 ('U73','74LS175','8451D2',200,1320,330,1375,'tim','확인','타이밍 래치'),
 ('U74','74LS08','8451C0',25,1400,80,1550,'tim','확인','AND. 1Y(핀 3) = AND(1A = U75 QA, 1B = U72 1Y(72-2) 넷, 76-5·84-4·19-9·16-12도 같은 넷) → U76 2번 FF J/K (U64 클럭 토글 조건, 측정 2026-11-25)'),
 ('U75','74LS195','8445C0',90,1400,150,1550,'tim','확인','4비트 시프트: 마스터 타이밍 (Apple II D2 상당)'),
 ('U76','74LS109','8449D1 M74LS109AP',160,1400,215,1550,'tim','확인','듀얼 JK 플립플롭. 2번 FF: J = U74 1Y, /K = 그 반전(U72 2Y), /PRE·/CLR = +5V → T 플립플롭, /2Q → U22 /G2A·U61 CLK·U64 클럭(핀 37) (측정 2026-11-25)'),
 ('U77','74LS139','8502D0',225,1400,285,1550,'dec','확인','듀얼 2→4 디코더. 1Y2 → U51 핀 4 (측정 2026-11-25)'),
 ('U78','74LS74','74LS74A',295,1400,350,1550,'tim','확인','D-FF'),
 ('U79','74LS157','8450E1',360,1400,415,1550,'vid','확인','2→1 MUX'),
 ('U80','74LS257','503000',420,1400,480,1550,'vid','확인','3-state 2→1 MUX'),
 ('U81','74LS257','503000',620,1400,680,1550,'vid','확인','3-state 2→1 MUX'),
 ('U82','74LS393','8451C1',690,1400,745,1550,'vid','확인','듀얼 4비트 카운터: 비디오 H/V 카운터 추정'),
 ('U83','74LS174','MB74LS174',760,1400,815,1550,'vid','확인','6비트 래치'),
 ('U84','74LS00','8501C2',825,1400,880,1550,'vid','확인','NAND'),
 ('U85','74S153','TI SN74S153N',890,1400,950,1550,'vid','확인','고속 4→1 MUX: 비디오 출력 선택'),
]
# connectors / misc
C = [
 ('SL1','슬롯 커넥터 50핀','Woo Young PBC22-50DA-2.54DS',60,0,120,480,'exp','확인','Apple II 확장 슬롯 (번호 미확인)'),
 ('SL2','슬롯 커넥터 50핀','Woo Young PBC22-50DA-2.54DS',160,0,215,480,'exp','확인',''),
 ('SL3','슬롯 커넥터 50핀','Woo Young PBC22-50DA-2.54DS',255,0,315,480,'exp','확인',''),
 ('SL4','슬롯 커넥터 50핀','Woo Young PBC22-50DA-2.54DS',360,0,420,480,'exp','확인',''),
 ('J1','전원 커넥터 5핀','',15,70,55,245,'tim','확인','외부 SMPS(한국산, 단자 FG·AC·+12V·+5V·GND·−5V·−12V)에서 5가닥(빨강·파랑·초록·주황·검정) 하네스로 입력. 레일 5개 확인, 핀 순서는 측정 필요'),
 ('J2','핀 헤더 2×10 (직립)','',25,260,60,440,'io','확인','20핀. 키보드 커넥터 추정'),
 ('J3','핀 헤더 2×10 (ㄱ자)','',25,470,60,630,'io','확인','20핀 라이트앵글. 용도 미확인 (프린터 등 외부 I/F 추정)'),
 ('J4','3.5mm 잭','',520,0,575,60,'io','확인','케이스 표기 "CASS\'T". 카세트 단자 (IN/OUT 구분은 측정 필요). 옆에 세라믹 콘덴서·저항'),
 ('J5','3.5mm 잭','',625,0,675,60,'io','확인','케이스 표기 "CASS\'T". 카세트 단자 (IN/OUT 구분은 측정 필요). 옆에 세라믹 콘덴서'),
 ('J6','RGB 출력 5핀 헤더','',720,0,800,35,'vid','확인','케이스 표기 "RGB". 3개 핀에 직렬 저항: 주황-주황-노랑(330k?) ×2, 갈색-빨강-주황(12k?) ×1, 측정 필요. 핀 배치 미확인'),
 ('J7','RCA 잭','',850,0,910,55,'vid','확인','케이스 표기 "VIDEO". 컴포지트 비디오 출력'),
 ('Q1','트랜지스터 TO-92','',930,65,965,105,'vid','추정','RCA 옆. 컴포지트 비디오 출력 버퍼(이미터 팔로워) 추정'),
 ('J8','2핀 커넥터','',940,175,980,215,'io','추정','스피커 추정 (옆에 트랜지스터 Q2와 저항 3개)'),
 ('Q2','트랜지스터 TO-92','',905,245,940,285,'io','추정','J8 옆. 스피커 구동 추정'),
 ('J9','16핀 DIP 소켓','',905,390,965,520,'io','확인','게임 I/O 포트 (Apple II J14 상당)'),
 ('J10','핀 헤더 2×8 (ㄱ자)','',555,1400,595,1540,'unk','확인','16핀 라이트앵글. 옆에 미실장 패드 7개. 용도 미확인'),
 ('X1','수정 발진자 + 트리머 콘덴서','',15,1305,58,1375,'tim','확인','소형 금속 캔 수정 + 세라믹 트리머 + 저항 2개(U64 아래 가로 배치) + U72 74LS04 = Apple II식 수정 발진 회로. 수정 표기 "14.31818 NISEM" (U64를 빼고 확인, 2026-11-25)'),
]

base_dir = os.path.dirname(os.path.abspath(__file__))

# --- placement: positions come from data/bom.csv (front side, slots at top, 1000x1600 grid) ---
# The BOM boxes are hand-traced from the photo, so their sizes are rough.  Each IC is redrawn as
# a DIP body sized by pin count, centred on its BOM box and oriented like it, then nudged apart
# where neighbours would touch.  Connectors keep their BOM boxes.
with open(os.path.join(base_dir, '..', '..', 'data', 'bom.csv'), encoding='utf-8') as f:
    BOM_XY = {d['ref']: tuple(int(d[k]) for k in ('x0', 'y0', 'x1', 'y1')) for d in csv.DictReader(f)}

def _xy(r):
    ref = r[0]
    return r[:3] + BOM_XY.get(ref, r[3:7]) + r[7:]
P = [_xy(r) for r in P]
C = [_xy(r) for r in C]

PINS = {
 'Z80A CPU':40, 'UM6502':40, '2764 EPROM':28, 'HM6116LP-3':24,
 '74LS373':20, '74LS244':20, '74LS245':20, '74LS323':20, '74LS374':20, '74LS273':20,
 '74LS00':14, '74LS02':14, '74LS04':14, '74LS05':14, '74LS08':14, '74LS10':14,
 '74LS32':14, '74LS74':14, '74LS393':14, 'LM339':14,
}
UNIT = 165            # grid units per inch (40-pin DIP ≈ 2.05" ≈ 335 units in the BOM)
def dip_size(part):
    n = PINS.get(part, 16)
    length = (n/2*0.1 + 0.05) * UNIT
    width = (0.56 if n >= 24 else 0.29) * UNIT
    return n, length, width

GAP = 8               # minimum clearance between bodies
def place():
    boxes = []        # [ref, x0, y0, x1, y1, movable]
    for r in C:
        boxes.append([r[0], *r[3:7], False])
    for r in P:
        x0, y0, x1, y1 = r[3:7]
        _, L, W = dip_size(r[1])
        w, h = (W, L) if (y1-y0) >= (x1-x0) else (L, W)
        cx, cy = (x0+x1)/2, (y0+y1)/2
        boxes.append([r[0], cx-w/2, cy-h/2, cx+w/2, cy+h/2, True])
    for _ in range(400):
        moved = False
        for i in range(len(boxes)):
            for j in range(i+1, len(boxes)):
                a, b = boxes[i], boxes[j]
                if not (a[5] or b[5]):
                    continue
                ox = min(a[3], b[3]) - max(a[1], b[1]) + GAP
                oy = min(a[4], b[4]) - max(a[2], b[2]) + GAP
                if ox <= 0 or oy <= 0:
                    continue
                moved = True
                # push apart along the axis that needs the smaller move
                if ox < oy:
                    d = ox if (a[1]+a[3]) < (b[1]+b[3]) else -ox
                    k = (1, 3)
                else:
                    d = oy if (a[2]+a[4]) < (b[2]+b[4]) else -oy
                    k = (2, 4)
                sa = 0.5 if (a[5] and b[5]) else (1.0 if a[5] else 0.0)
                sb = 1.0 - sa
                for idx in k:
                    a[idx] -= d*sa
                    b[idx] += d*sb
        for bx in boxes:  # keep inside the board
            if bx[5]:
                dx = max(0, 4-bx[1]) - max(0, bx[3]-996)
                dy = max(0, 4-bx[2]) - max(0, bx[4]-1596)
                bx[1] += dx; bx[3] += dx; bx[2] += dy; bx[4] += dy
        if not moved:
            break
    return {bx[0]: tuple(round(v, 1) for v in bx[1:5]) for bx in boxes}

POS = place()

# short labels for connectors and small parts (full names stay in the BOM table / tooltip)
SHORT = {'J1':'전원', 'J2':'2×10', 'J3':'2×10 ㄱ', 'J4':'CASS', 'J5':'CASS', 'J6':'RGB',
         'J7':'VIDEO', 'J8':'SPK', 'J9':'GAME I/O', 'J10':'2×8 ㄱ', 'X1':'', 'Q1':'', 'Q2':''}

def label_of(mark):
    m = re.search(r'라벨 "([^"]+)"', mark)
    return m.group(1) if m else ''

def chip_svg(r):
    ref,part,mark,_x0,_y0,_x1,_y1,b,conf,note = r
    x0, y0, x1, y1 = POS[ref]
    w,h = x1-x0, y1-y0
    cls = BLK[b][1]
    vertical = h > w
    cx, cy = round(x0+w/2, 1), round(y0+h/2, 1)
    dash = ' stroke-dasharray="6 4"' if conf=='추정' else ''
    is_ic = ref.startswith('U')
    t = f'<g class="chip {cls}{" ic" if is_ic else " conn"}" data-ref="{ref}" tabindex="0"><title>{ref} {html.escape(part)} — {html.escape(note)}</title>'
    t += f'<rect x="{x0}" y="{y0}" width="{round(w,1)}" height="{round(h,1)}" rx="{3 if is_ic else 2}"{dash}/>'
    rot = f' transform="rotate(-90 {cx} {cy})"' if vertical else ''
    if ref.startswith('SL'):
        lines = [(ref, 'ref'), ('50-pin slot', '')]
    elif is_ic:
        short = part.replace(' EPROM','').replace(' CPU','').replace('LP-3','')
        lines = [(ref, 'ref'), (short, '')]
        lab = label_of(mark)
        if lab:
            lines.append((f'"{lab}"', 'tag'))
    else:
        s = SHORT.get(ref, '')
        lines = [(ref, 'ref')] + ([(s, 'tag')] if s else [])
    # lines run along the long side; stack them across the short side
    across = w if vertical else h
    step = min(16, (across-4)/len(lines))
    fs = f' style="font-size:{round(step*0.8,1)}px"' if step*0.8 < 14 else ''
    top = -step*(len(lines)-1)/2
    t += f'<text class="lbl"{fs}{rot}>'
    for i,(s,c) in enumerate(lines):
        t += f'<tspan x="{cx}" y="{round(cy+top+i*step,1)}"{f" class={chr(34)}{c}{chr(34)}" if c else ""}>{html.escape(s)}</tspan>'
    t += '</text></g>'
    return t

board = ''.join(chip_svg(r) for r in C+P)

legend = ''.join(f'<li><span class="sw {v[1]}"></span>{v[0]}</li>' for k,v in BLK.items())

rows = ''
for r in P+C:
    ref,part,mark,*_ ,b,conf,note = r
    rows += (f'<tr data-blk="{b}"><td class="mono">{ref}</td><td>{html.escape(part)}</td>'
             f'<td class="mono dim">{html.escape(mark)}</td><td><span class="sw {BLK[b][1]}"></span>{BLK[b][0]}</td>'
             f'<td><span class="conf {"c-ok" if conf=="확인" else "c-est"}">{conf}</span></td><td>{html.escape(note)}</td></tr>')

tpl_path = os.path.join(base_dir, 'page.tpl.html')
out_path = os.path.join(base_dir, '..', 'apple2-clone-schematic.html')

sys.path.insert(0, os.path.join(base_dir, '..', '..', 'tools'))
import netmodel
nets_html = netmodel.render_html()

tpl = open(tpl_path, encoding='utf-8').read()
out = tpl.replace('%%BOARD%%', board).replace('%%LEGEND%%', legend).replace('%%ROWS%%', rows).replace('%%NETS%%', nets_html)\
         .replace('%%NIC%%', str(len(P))).replace('%%NCONN%%', str(len(C)))
open(out_path,'w',encoding='utf-8').write(out)
print(f"Generated {out_path}: {len(out)} bytes, {len(P)} ICs, {len(C)} connectors")
