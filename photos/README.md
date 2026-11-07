# 보드 사진

2026-11-05 촬영 사진 118장 중 회로 판독에 쓰는 86장만 남겼습니다. 파일명 앞 6자리는 촬영 시각(HHMMSS)이고, 뒤에는 찍힌 부품의 참조번호를 붙였습니다.
보드에는 실크 인쇄가 없어서 참조번호(U1–U85, J1–J10 등)는 분석용으로 붙인 것입니다. 커넥터 이름 VIDEO·RGB·CASSETTE는 케이스 인쇄를 따랐습니다.

## 방향 기준

모든 문서는 **앞면, 확장 슬롯이 위쪽**인 방향을 기준으로 합니다. 이 방향에서 Z80은 오른쪽 위, 메인 6502는 가운데 왼쪽, 시리얼 라벨은 오른쪽 아래에 있습니다.
뒷면 사진은 앞면과 좌우가 반전되어 있습니다.

## 폴더 구성

```
photos/
├── overview/front/   앞면 전체 3장
├── overview/back/    뒷면 전체 2장
├── zoom/front/       앞면 확대 18장
├── zoom/back/        뒷면 확대 19장
├── backlit/          역광 뒷면 4장 (U64·U30 접사)
├── backlit/sweep/    역광 뒷면 전체 훑기 12장
├── case/             케이스 표기·전원 공급기 3장
├── keyboard/         본체 키보드 단자 J10·키보드 분해 22장 (2026-11-07)
└── screen/           화면 사진
```

## overview/front — 앞면 전체

| 파일 | 해상도 | 용도 |
| --- | --- | --- |
| 202813_front-flat_layout-ref.jpg | 2089×3363 | 보드만 잘라 원근 보정. **배치도 좌표 기준** |
| 203539_front-landscape_best-labels.jpg | 3245×2448 | 가로. 전체 사진 중 칩 표기가 가장 잘 보임 |
| 202556_front-full.jpg | 2447×3258 | 세로 전체 |

## overview/back — 뒷면 전체

| 파일 | 해상도 | 용도 |
| --- | --- | --- |
| 203240_back-flat_registration-ref.jpg | 2121×3369 | 원근 보정. **뒷면 확대 사진 정합 기준** |
| 203514_back-flat.jpg | 2134×3518 | 원근 보정 |

## zoom/front — 앞면 확대

| 파일 | 찍힌 부품 |
| --- | --- |
| 210859_U30-main6502_U29_dram.jpg | 메인 6502, U29, DRAM 위쪽 열 |
| 210909_U31-U38_U47-U51.jpg | 주소 버퍼, 디코드, PROM 1·2·3 |
| 210919_U30-bottom_tantal-resistor.jpg | 메인 6502 아래 탄탈 콘덴서·저항 (원본이 새 사진으로 교체됨) |
| 210931_U16-U20_slots_U21-U24.jpg | 확장 로직, 슬롯, 디코더 |
| 210938_U21-U28_U10-U15_J9-gameport.jpg | 디코드, 게임 I/O, 게임 포트 소켓 |
| 210946_U2-Z80_U4-U15_U3-LM339_slot-part.jpg | Z80 주변, LM339, 슬롯 커넥터 형명 |
| 211032_J2-J3-headers_U16-U20.jpg | 왼쪽 가장자리 2×10 헤더 2개 |
| 211036_U17-closeup.jpg | U17 표기 판독용 접사 |
| 212252_dram_U43-U57_rom-CD8-EF5_VD5.jpg | DRAM 2열, 74LS153, 시스템 ROM |
| 212258_U64-notch_X1-trimmer_U72-U80_VD5.jpg | 두 번째 6502 노치, 수정·트리머, 타이밍 |
| 212301_U69-LS273_U68-6116_CHRP4_J10.jpg | 비디오 영역, 아래쪽 줄, J10 |
| 212315_CHRP4_U71_U81-U85_J10.jpg | 오른쪽 아래 모서리 (상하 반전) |
| 212336_rom_U31-U38_U21-U28.jpg | ROM 오른쪽 디코드 영역 |
| 212342_U30-main6502_U16-U20.jpg | 메인 6502와 확장 로직 |
| 212346_rom-CD8-EF5_U43-U44_U47-U51.jpg | 시스템 ROM 정면 |
| 222530_U3-LM339-resistors_J8_Q1_Q2_J9.jpg | LM339 주변 저항 배열, 스피커 커넥터, 트랜지스터 |
| 223147_VIDEO-RGB-CASSETTE_top.jpg | 케이스 표기 VIDEO·RGB·CASSETTE 커넥터 (위에서) |
| 223156_RGB-CASSETTE_side.jpg | RGB 5핀과 CASSETTE 잭 (측면) |

## zoom/front/sweep — 앞면 정면 연속 촬영

22:42–22:43에 보드를 정면에서 구역별로 이어 찍은 13장입니다. 조명이 고르고 기울기가 작아 앞면 패턴을 뒷면 사진과 겹쳐 볼 때 쓰기 좋습니다. 파일명 뒤에 찍힌 구역을 붙였습니다.

## zoom/back — 뒷면 확대

13장(`20261105_2124xx`, `2125xx`)은 보드를 90° 돌린 상태로 찍혔고, 각각 뒷면 기준 사진에 위치를 맞춘 결과가 [`data/back_zoom_registration.json`](../data/back_zoom_registration.json)에 있습니다. 어디를 찍은 사진인지는 [`docs/07-back-trace-notes.md`](../docs/07-back-trace-notes.md)의 표와 [`analysis/back_zoom_coverage.jpg`](../analysis/back_zoom_coverage.jpg)를 보세요. 정합 데이터가 파일명을 키로 쓰므로 이 13장은 이름을 바꾸지 않았습니다.

`20261105_222546_edge-connectors.jpg`는 뒷면 위쪽 가장자리의 VIDEO·RGB·CASSETTE 납땜부입니다.

## 3차 추가 (22:52–22:55)

| 파일 | 내용 |
| --- | --- |
| zoom/front/225226_U64-front_VD5_X1.jpg | 두 번째 6502 정면 |
| zoom/front/225255_U30-front_U16-U20.jpg | 메인 6502 정면 |
| zoom/back/225321_back-U30-area_left-edge.jpg | 메인 6502 뒷면, 앞면 기준 왼쪽 가장자리 |
| zoom/back/225326 / 225408 | 두 번째 6502 뒷면 |
| zoom/back/225351_back-connector-corner.jpg | 잭·RCA 쪽 뒷면 모서리 |
| zoom/back/225412_back-bottom-left.jpg | 뒷면 아래쪽 |
| case/225440_case-VIDEO-RGB-CASST.jpg | 케이스 인쇄 VIDEO / RGB / CASS'T |
| case/225522_PSU-terminals.jpg | 전원 공급기 단자: FG, AC 90–130/180–260V, +12V, +5V, GND, −5V, −12V (MADE IN KOREA) |
| case/225533_PSU-harness.jpg | 보드 J1로 가는 5가닥 하네스 (빨강·파랑·초록·주황·검정) |

## 4차 추가 (23:06–23:08) — 두 6502 주변 접사

| 파일 | 내용 |
| --- | --- |
| 230643_U64_oscillator_X1-trimmer.jpg | 두 번째 6502와 발진 회로 |
| 230752_oscillator_R-pair_U72-LS04.jpg | 수정·트리머·저항 2개·74LS04: Apple II식 발진 회로 |
| 230829_U64_U72_U73.jpg | U64 아래 줄 전체 |
| 230741_U30-top_dram-row.jpg | 메인 6502 윗줄 핀과 DRAM |
| 230758_U30-pin1-side_traces.jpg | 메인 6502 1번 핀 쪽: 탄탈 콘덴서, 저항, 넓은 동박, 앞면 패턴 |
| 230803_U30-bottom_traces.jpg | 메인 6502 아래 앞면 패턴 (DRAM MUX 쪽으로 가는 주소선) |
| 230807_U16-U20_to_U30-traces.jpg | 확장 로직에서 메인 6502로 가는 앞면 패턴 |

## backlit — 역광 뒷면 (23:25)

앞쪽에서 빛을 비추고 뒷면을 찍은 사진입니다. 구리가 없는 곳은 밝게, 양면 어느 쪽이든 구리가 있는 곳은 어둡게 보여 칩 아래 앞면 배선을 볼 수 있습니다.

| 파일 | 내용 |
| --- | --- |
| backlit/232515_backlit_U64.jpg | 두 번째 6502 뒷면. 핀 번호 표시본: [`analysis/u64_backlit_pins.jpg`](../analysis/u64_backlit_pins.jpg) |
| backlit/232518_backlit_U64-left_U72-row.jpg | U64 왼쪽(뒷면 기준)과 아래 줄 |
| backlit/232548_backlit_dram-area.jpg | DRAM 구역 |
| backlit/232551_backlit_U30.jpg | 메인 6502 뒷면 (비교용) |

앞면 접사 2장 추가: `zoom/front/232340_oscillator_X1_R-pair_U72.jpg`, `zoom/front/232417_U30_dram-row.jpg`

### backlit/sweep — 역광 전체 훑기 (23:39–23:40), 12장

뒷면 전체를 역광으로 구역별로 찍은 사진입니다. 배율이 낮아 핀 하나하나보다는 앞면 배선이 어디로 이어지는지 큰 흐름을 보는 데 씁니다. 보드를 여러 각도로 돌려 찍어 자동 정합은 되지 않았습니다.
`20261105_234045_U64-crystal-corner.jpg`는 수정 발진자 쪽 모서리와 U64(세로 방향)를 담고 있습니다.

`case/230434_PSU-wire-colors.jpg`: 전원 공급기 단자별 선 색 (아래 05 문서 참고)

## 제거한 사진 (32장)

| 원본 파일 | 제거 이유 |
| --- | --- |
| 20261105_225236 | 225226과 같은 구도 |
| 20261105_225245 | 초점 흐림 |
| 20261105_230636 / 230731 / 230737 / 230744 / 230749 / 230812 / 230841 / 230845 | U64·U30 주변 중복 접사 |
| 20261105_232344 / 232348 / 232354 / 232403 / 232410 / 232414 / 232505 | 중복 (같은 구도/부분 확대) |
| Scan_20261105_202618 / 202655 / 202917 / 202936 | 앞면 전체 중복 |
| Scan_20261105_203305 / 203456 | 뒷면 전체 중복 |
| 20261105_211007 | U16–U20 중복 (210931, 211036이 더 선명) |
| 20261105_211014 | J1–J3 비스듬히 (211032가 정면) |
| 20261105_212202 | 디코드 영역 중복 |
| 20261105_212232 / 212238 | 비스듬한 전경, 판독용으로 부족 |
| 20261105_212246 | 메인 6502 영역 중복 |
| 20261105_212325 | U64 영역 중복 |
| 20261105_222454 / 222526 | 커넥터 중복 (223147이 더 선명) |

## 앞면 추가 사진 `zoom/front/add_20261107/` (2026-11-07)

보드를 90° 돌린 채 비스듬히 찍은 앞면 사진 10장. 슬롯·Z80(U1, U2)·U30 오른쪽 칩 줄 주변입니다. 각 사진을 앞면 기준 사진(202813)에 맞춘 변환이 [`data/front_add_20261107_registration.json`](../data/front_add_20261107_registration.json)에 있습니다 (일치점 17–54개, 대략적). 005000에서 U31–U34 노치가 아래쪽임을 확인했습니다.

## 화면 사진 `screen/`

| 파일 | 내용 |
| --- | --- |
| 20261107_015041_boot-logo_vertical-roll.jpg | 수리 후 첫 부팅 화면. "HART" 로고와 "Zung Won Co.,Ltd. 542-3675 SEOUL KOREA". 모니터 수직 동기가 안 맞아 위아래로 두 번 겹쳐 보임 |

## 키보드 `keyboard/` (2026-11-07)

| 파일 | 내용 |
| --- | --- |
| 20261107_131132_J10-header_connector-unplugged.jpg | 본체 J10(키보드 단자)과 뽑은 케이블 커넥터 |
| 20261107_133005 / 141505 | 본체쪽 케이블 커넥터 뒷면 배선, 전선 없는 칸의 핀 |
| 20261107_143208_keyboard-top_ZPC-40.jpg | 키보드 윗면. 명판 "PERSONAL COMPUTER ZPC-40" |
| 20261107_143736_kbd-pcb-component-side_LS145-LS03-JAE16P.jpg | 키보드 기판 부품면: SN74LS145N, 74LS03, 저항, JAE 16P 단자, 케이블 |
| 20261107_143815 / 143824 / 143828 / 144013 | 키보드 기판 납땜면 (143824가 칩·단자 부분 가장 선명) |
| Scan_20261107_144038 / 144116 / 144256 | 키보드 납땜면 평면 보정본 |
| Scan_20261107_144416_kbd-keys-and-pcb-top.jpg | 케이스에서 꺼낸 키 배열과 기판 부품면 |
| 20261107_145210 / 145216 / 145233 / 145236 / 145242 | 키보드 납땜면 구역별 (위·가운데·아래) |
| 20261107_145239_kbd-solder-side_connector-ICs.jpg | 키보드 납땜면 단자·칩 부분. **측정 번호 그림 기준** ([`analysis/kbd_measure_simple.jpg`](../analysis/kbd_measure_simple.jpg)) |
| 20261107_145358 / 145413 / 145419 | 키보드 부품면: 칩 표기·노치 방향, JAE 16P, 점퍼선, 케이스에 붙은 검정 선 중계 패드 |

## 추가로 필요한 사진

[`docs/06-next-steps.md`](../docs/06-next-steps.md)의 "추가 촬영 요청" 표를 보세요.
