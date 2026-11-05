# 02. 시스템 구성

일반 Apple II와 달리 CPU가 세 개입니다. 6502 하나가 메인이고, Z80은 CP/M 카드를 내장한 구조로 보이며, 두 번째 6502는 역할이 미확인입니다.

## 블록 다이어그램

```mermaid
flowchart LR
  CLK["클럭/타이밍<br/>X1 14.318MHz, U72-U75, U49"] -->|Φ0/Φ1, 7M, Q3| CPU
  CLK -->|RAS/CAS/AX| RAM
  CPU["메인 CPU U30 UM6502<br/>버퍼 U29, U31-U33"] --> AB(("A0-A15"))
  CPU <--> DB(("D0-D7"))
  Z80["Z80 서브시스템 U2<br/>U1, U4-U15"] -.DMA/RDY.-> CPU
  Z80 -.-> AB
  Z80 <-.-> DB
  AB --> DEC["주소 디코드<br/>74LS138×3, 139×3, 82S129×4"]
  DEC --> ROM["시스템 ROM<br/>2764 C/D8, EF5"]
  DEC --> IO["내장 I/O<br/>게임 포트, 카세트, 스피커"]
  DEC --> SLOT["확장 슬롯 ×4"]
  AB --> RAM["DRAM 64KB<br/>MN4164×8, MUX 74LS153×4"]
  RAM <--> DB
  ROM --> DB
  RAM -->|비디오 데이터| VID["비디오<br/>VD5, CHR P4, 6116, 74LS166/273"]
  VID --> OUT["Q1 → J7 컴포지트(RCA)<br/>J6 RGB 5핀"]
  U64["U64 두 번째 6502<br/>역할 미확인"] -.-> VID
  SLOT <--> DB
```

점선은 결선 확인이 필요한 연결입니다. 인터랙티브 버전은 [`schematic/apple2-clone-schematic.html`](../schematic/apple2-clone-schematic.html)에 있습니다.

## 블록별 구성

| 블록 | 부품 | 내용 |
| --- | --- | --- |
| 메인 CPU | U30 UM6502, U29 74LS245, U31–U33 74LS367 | 1.023MHz. 74LS367은 Apple II의 8T97 대체 |
| Z80 서브시스템 | U2 LH0080A, U1 74LS373, U4 74LS244, U5 82S123, U6–U7 74LS367, U8 74LS163, U9–U15 | SoftCard 방식(DMA로 6502 정지 후 버스 점유) 추정. U5가 Z80→6502 주소 변환 |
| 두 번째 6502 | U64 UM6502 | 역할 미확인. 80컬럼/한글 표시 전용 CPU 또는 예비 소켓 가능성 |
| DRAM | U39–U42, U52–U55 MN4164, U43/44/56/57 74LS153 | 64KB. CPU/비디오 주소와 ROW/COL을 멀티플렉싱 |
| 시스템 ROM | U45 "C/D8", U46 "EF5", U63 74LS245 | C000–FFFF 16KB (라벨 기준 추정) |
| 비디오 | U65 "VD5", U70 "CHR P4", U68 HM6116, U66 74LS374, U67 74LS245, U69 74LS273, U71 74LS166, U82 74LS393, U85 74S153, 74LS157/257 다수 | VD5 = 40컬럼 문자 ROM, CHR P4 = 한글/80컬럼 추정. 6116은 화면 버퍼 또는 폰트 RAM 추정. 출력은 컴포지트(J7, 케이스 표기 VIDEO, Q1 버퍼)와 **RGB 5핀(J6, 케이스 표기 RGB)** 두 가지 |
| 클럭/타이밍 | X1 + 트리머 콘덴서, U72 74LS04, U73/U49 74LS175, U75 74LS195, U76 74LS109, U74 74LS08, U60/U61/U62/U78 | 14.31818MHz(추정)에서 7M, 3.58M, Q3, Φ0/Φ1, RAS/CAS 생성 |
| 주소 디코드 | U21/U35/U77 74LS139, U22–U24 74LS138, U34 74LS00, U48 74LS02, U36/U38/U50/U51 82S129, U25 74LS259 | ROM CS, C0xx 내부 I/O, I/O SELECT, DEVICE SELECT |
| 내장 I/O | U27 NE558, U28 74LS251, U3 LM339, U26 74LS74, Q2, J4/J5/J8/J9 | 게임 포트(Apple II H13/H14 상당), 카세트(3.5mm 잭 ×2, 케이스 표기 CASSETTE), 스피커(J8, Q2 구동) |
| 확장 | SL1–SL4, U16 74LS323, U17/U18 PROM, U19 74LS174, U20 74LS259 | 보조 로직 역할 미확인 (언어카드 또는 프린터 I/F 추정) |
| 전원 | J1 5핀 | +5V, GND, ±12V, −5V 추정 |

## Apple II 레퍼런스와의 대응

| 기능 | Apple II 원본 | 이 보드 |
| --- | --- | --- |
| 주소 버퍼 | 8T97 ×3 | 74LS367 ×3 |
| 비디오 카운터 | 74LS161 ×4 | 74LS393 |
| 소프트스위치 | F14 74LS259 | U25 74LS259 |
| 패들 타이머 | H13 558 | U27 NE558 |
| 게임 입력 MUX | H14 74LS251 | U28 74LS251 |
| 카세트 입력 | K13 741 | U3 LM339 |
| DRAM | 4116 ×24 (48KB, +12V/−5V 필요) | 4164 ×8 (64KB, +5V 단일) |
| ROM | 2316 ×6 | 2764 ×2 |
