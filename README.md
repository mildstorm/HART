# HART: Apple II 클론 보드 리버스 엔지니어링

S/N 506267 Apple II 호환 메인보드의 사진, 부품 분석, 회로도를 정리한 저장소입니다.
이 보드는 6502 메인 CPU에 **Z80 서브시스템**과 **두 번째 6502**가 함께 실장된 형태로, 일반 Apple II와 구성이 다릅니다.

## 현재 상태

| 항목 | 상태 |
| --- | --- |
| 부품 식별 (IC 85개, 커넥터·트랜지스터 등 17개) | 완료. 일부 지워진 표기는 추정 |
| 기능 블록 회로도 | 완료 (Apple II 표준 설계 기반 추정 포함) |
| 부품 배치도 | 완료 |
| 앞면 확대 사진 | 18장 (중복 제거 후, 보드 전체·커넥터 주변) |
| 뒷면 확대 사진 | 14장, 13장은 뒷면 기준 사진에 정합 완료 |
| 핀 단위 결선 (넷리스트) | 진행 중. `data/netlist.csv` 시작 (U64 버스·클럭 분리 확인) |
| ROM / PROM 덤프 | 미완료 |
| 수리 (화면 안 나옴) | 진행 중. 메인 CPU 클럭(Φ0) 멈춤 의심. 다음 측정 순서는 [`docs/08-repair-log.md`](docs/08-repair-log.md) "다음에 할 일" |

## 보드 요약

| 항목 | 내용 |
| --- | --- |
| 메인 CPU | UM6502 (UMC, 8404) |
| 보조 CPU | Sharp LH0080A (Z80A). CP/M 카드 내장형 추정 |
| 두 번째 6502 | UM6502. 한글 폰트 처리 전용, 독립 동작 (2026-11-06 확인) |
| DRAM | MN4164P-25 ×8 = 64KB |
| SRAM | HM6116LP-3 2KB |
| ROM | 2764 ×4: "C/D8", "EF5"(시스템), "VD5", "CHR P4"(문자) |
| 확장 슬롯 | 50핀 ×4 (Woo Young) |
| 내장 I/O | 게임 포트, 카세트 IN/OUT, 스피커, 컴포지트 비디오(RCA), RGB 출력(5핀) |
| IC 날짜 코드 | 8404 – 8509 (1984 – 1985년) |

## 디렉터리 구성

```
HART/
├── README.md                     이 문서
├── photos/
│   ├── README.md                 사진 목록과 설명
│   ├── overview/front/, back/    보드 전체 사진 (앞 3, 뒤 2)
│   └── zoom/front/, back/        확대 사진 (앞 18, 뒤 14)
├── docs/
│   ├── 01-overview.md            분석 개요와 판독 범위
│   ├── 02-system-architecture.md 시스템 구성과 기능 블록
│   ├── 03-bom.md                 부품표 전체
│   ├── 04-open-questions.md      미확인 사항
│   ├── 05-interface-pinouts.md   슬롯·게임 포트 핀 배치, 소프트스위치 주소
│   ├── 06-next-steps.md          결선 확정 절차, 추가 촬영 가이드
│   ├── 07-back-trace-notes.md    뒷면 확대 사진 정합과 U64 핀맵
│   └── 08-repair-log.md          화면 안 나옴 증상 수리 점검 기록
├── schematic/
│   ├── apple2-clone-schematic.html  인터랙티브 블록 회로도 + 배치도 + 부품표
│   └── src/                      HTML 생성 스크립트 (gen.py + 템플릿)
├── analysis/                     정합 범위도, U64 뒷면 핀맵 등 분석 이미지
├── tools/                        확대 사진 정합/변환 스크립트 (Python, OpenCV)
└── data/
    ├── bom.csv                   부품 데이터 (배치 좌표 포함)
    └── back_zoom_registration.json  뒷면 확대 사진 → 스캔 좌표 변환 행렬
```

## 회로도 보기

`schematic/apple2-clone-schematic.html`을 브라우저로 열면 됩니다. 부품을 누르면 정보가 나오고, 범례를 누르면 블록별로 강조됩니다.

부품 데이터를 고친 뒤 HTML을 다시 만들려면:

```sh
cd schematic/src
python3 gen.py   # 같은 폴더의 page.tpl.html을 읽어 HTML 생성
```

> `gen.py`의 입출력 경로가 작성 환경 기준(`/home/claude/...`)으로 되어 있으니 실행 전 경로를 고쳐 주세요.
