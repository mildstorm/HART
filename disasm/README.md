# 정원 HART 롬 덤프 디스어셈블리 및 분석 (ROM Disassembly)

본 디렉터리는 `rom/` 디렉터리에 위치한 정원 HART 11개 롬/PROM 덤프 이미지의 완전한 역어셈블리 소스 및 분석 데이터입니다.

## 파일 목록

| 파일명 | 종류 | 크기 | 주소 / 매핑 | 내용 요약 |
| :--- | :--- | :--- | :--- | :--- |
| [`U45_CD8.asm`](U45_CD8.asm) | 6502 어셈블리 | 8KB | `$C000–$DFFF` | 메인 CPU 시스템 ROM. $C300·$C800 Videx 80컬럼, $C600 내장 Disk II 부트, $D000 Applesoft BASIC 전반부 |
| [`U46_EF5.asm`](U46_EF5.asm) | 6502 어셈블리 | 8KB | `$E000–$FFFF` | 메인 CPU 시스템 ROM. $E000 BASIC 후반부, $F800 Autostart Monitor, $FAA6 슬롯 6 즉시 부팅 |
| [`U65_VD5.asm`](U65_VD5.asm) | 6502 어셈블리 | 8KB | U64 로컬 버스 | 보조 6502 실행 펌웨어. 화면 초기화, 비디오 제어, 화면 하단 기능키(F1–F12) 라벨 테이블(Apple/CPM) |
| [`U70_CHRP4_font.txt`](U70_CHRP4_font.txt) | 폰트 분석 덤프 | 8KB | 비디오 시프터 | 문자 발생기 ROM. 4개 뱅크(영문 Normal/Inverse, 세미그래픽, 한글 자모 조합형) 아스키 아트 덤프 |
| [`U17_U18_p6_sequencer.txt`](U17_U18_p6_sequencer.txt) | 상태머신 분석 | 256B | 내장 FDC | U17(상위 4비트 제어명령) + U18(하위 4비트 다음상태) = Disk II 16-섹터 시퀀서(P6, 341-0028) 전이표 |
| [`U5_82S123_z80_map.txt`](U5_82S123_z80_map.txt) | 주소변환 분석 | 32B | Z80 버스 변환 | Microsoft SoftCard 호환 Z80 -> 6502 하드웨어 실시간 주소 변환표 및 설명 |
| [`U50_U51_U36_U38_address_decode.txt`](U50_U51_U36_U38_address_decode.txt) | 진리표 분석 | 각 256B | 주소 디코더 | U50, U51, U36, U38 82S129 주소 디코드 PROM 4개의 전체 256 주소 진리표 |

## 디스어셈블리 주요 발견 사항

1. **U45 / U46**: 표준 Apple II+ ROM(Applesoft BASIC + Autostart Monitor)을 기본으로 하되, $C300/$C800에 Videx 80컬럼 펌웨어가 통합되고, $FAA6 리셋 루틴에서 슬롯 검색을 건너뛰고 내장 FDD($C600)로 직접 점프하도록 개조되었습니다.
2. **U65**: 화면 하단에 표시되는 기능키 바 문자열(Apple 모드 3세트 + CP/M 모드 1세트: DIR, ERA, REN 등)이 포함된 완전한 6502 프로그램으로, 두 번째 6502(U64)가 비디오와 키보드 확장을 전담했음을 보여줍니다.
3. **U17 + U18**: 두 칩을 상/하위 4비트로 결합하면 정확히 Apple Disk II 16-섹터 시퀀서(P6, 341-0028 호환) 256바이트 상태 머신이 완성됩니다.