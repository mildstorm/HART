#!/usr/bin/env bash
# 사진 정리 스크립트 (MSYS2에서 실행):  bash /home/milds/clone/HART/organize_photos.sh
# 1) clone 폴더에 흩어진 원본 사진 중 회로 판독에 쓰는 37장을 clone/photos/ 로 이동
# 2) 중복·불필요 15장 삭제 (실행 전 확인)
# 3) HART/photos 를 새 구조(overview/, zoom/)로 다시 구성 (옛 front/, back/ 폴더 제거)
set -e
CLONE=/home/milds/clone
HART="$CLONE/HART"
RAW="$CLONE/photos"
cd "$CLONE"

REMOVE=("20261105_211007.jpg" "20261105_211014.jpg" "20261105_212202.jpg" "20261105_212232.jpg" "20261105_212238.jpg" "20261105_212246.jpg" "20261105_212325.jpg" "20261105_222454.jpg" "20261105_222526.jpg" "20261105_225236.jpg" "20261105_225245.jpg" "20261105_230636.jpg" "20261105_230731.jpg" "20261105_230737.jpg" "20261105_230744.jpg" "20261105_230749.jpg" "20261105_230812.jpg" "20261105_230841.jpg" "20261105_230845.jpg" "20261105_232344.jpg" "20261105_232348.jpg" "20261105_232354.jpg" "20261105_232403.jpg" "20261105_232410.jpg" "20261105_232414.jpg" "20261105_232505.jpg" "Scan_20261105_202618.jpg" "Scan_20261105_202655.jpg" "Scan_20261105_202917.jpg" "Scan_20261105_202936.jpg" "Scan_20261105_203305.jpg" "Scan_20261105_203456.jpg")
declare -A KEEP=(
  ["20261105_210859.jpg"]="zoom/front/210859_U30-main6502_U29_dram.jpg"
  ["20261105_210909.jpg"]="zoom/front/210909_U31-U38_U47-U51.jpg"
  ["20261105_210919.jpg"]="zoom/front/210919_U30-bottom_tantal-resistor.jpg"
  ["20261105_210931.jpg"]="zoom/front/210931_U16-U20_slots_U21-U24.jpg"
  ["20261105_210938.jpg"]="zoom/front/210938_U21-U28_U10-U15_J9-gameport.jpg"
  ["20261105_210946.jpg"]="zoom/front/210946_U2-Z80_U4-U15_U3-LM339_slot-part.jpg"
  ["20261105_211032.jpg"]="zoom/front/211032_J2-J3-headers_U16-U20.jpg"
  ["20261105_211036.jpg"]="zoom/front/211036_U17-closeup.jpg"
  ["20261105_212252.jpg"]="zoom/front/212252_dram_U43-U57_rom-CD8-EF5_VD5.jpg"
  ["20261105_212258.jpg"]="zoom/front/212258_U64-notch_X1-trimmer_U72-U80_VD5.jpg"
  ["20261105_212301.jpg"]="zoom/front/212301_U69-LS273_U68-6116_CHRP4_J10.jpg"
  ["20261105_212315.jpg"]="zoom/front/212315_CHRP4_U71_U81-U85_J10.jpg"
  ["20261105_212336.jpg"]="zoom/front/212336_rom_U31-U38_U21-U28.jpg"
  ["20261105_212342.jpg"]="zoom/front/212342_U30-main6502_U16-U20.jpg"
  ["20261105_212346.jpg"]="zoom/front/212346_rom-CD8-EF5_U43-U44_U47-U51.jpg"
  ["20261105_212430.jpg"]="zoom/back/20261105_212430.jpg"
  ["20261105_212435.jpg"]="zoom/back/20261105_212435.jpg"
  ["20261105_212438.jpg"]="zoom/back/20261105_212438.jpg"
  ["20261105_212441.jpg"]="zoom/back/20261105_212441.jpg"
  ["20261105_212444.jpg"]="zoom/back/20261105_212444.jpg"
  ["20261105_212452.jpg"]="zoom/back/20261105_212452.jpg"
  ["20261105_212455.jpg"]="zoom/back/20261105_212455.jpg"
  ["20261105_212457.jpg"]="zoom/back/20261105_212457.jpg"
  ["20261105_212501.jpg"]="zoom/back/20261105_212501.jpg"
  ["20261105_212504.jpg"]="zoom/back/20261105_212504.jpg"
  ["20261105_212507.jpg"]="zoom/back/20261105_212507.jpg"
  ["20261105_212510.jpg"]="zoom/back/20261105_212510.jpg"
  ["20261105_212512.jpg"]="zoom/back/20261105_212512.jpg"
  ["20261105_222530.jpg"]="zoom/front/222530_U3-LM339-resistors_J8_Q1_Q2_J9.jpg"
  ["20261105_222546.jpg"]="zoom/back/20261105_222546_edge-connectors.jpg"
  ["20261105_223147.jpg"]="zoom/front/223147_VIDEO-RGB-CASSETTE_top.jpg"
  ["20261105_223156.jpg"]="zoom/front/223156_RGB-CASSETTE_side.jpg"
  ["20261105_224231.jpg"]="zoom/front/sweep/224231_U72-U76_U64.jpg"
  ["20261105_224237.jpg"]="zoom/front/sweep/224237_dram-left_U30.jpg"
  ["20261105_224246.jpg"]="zoom/front/sweep/224246_rom-CD8-EF5_dram-right.jpg"
  ["20261105_224301.jpg"]="zoom/front/sweep/224301_rom-EF5_U47-U51_CHRP4.jpg"
  ["20261105_224306.jpg"]="zoom/front/sweep/224306_U47-U51_PROM-1-2-3.jpg"
  ["20261105_224311.jpg"]="zoom/front/sweep/224311_U21-U28_gameport-resistors.jpg"
  ["20261105_224317.jpg"]="zoom/front/sweep/224317_U21-U24_U10-U15.jpg"
  ["20261105_224321.jpg"]="zoom/front/sweep/224321_U30_U16-U20_slots.jpg"
  ["20261105_224326.jpg"]="zoom/front/sweep/224326_J2-J3-J1_slots.jpg"
  ["20261105_224331.jpg"]="zoom/front/sweep/224331_slots_J1-power.jpg"
  ["20261105_224334.jpg"]="zoom/front/sweep/224334_slots_U1-U4.jpg"
  ["20261105_224339.jpg"]="zoom/front/sweep/224339_Z80_cassette-jacks_RGB.jpg"
  ["20261105_224342.jpg"]="zoom/front/sweep/224342_LM339_VIDEO_J8_J9.jpg"
  ["20261105_225226.jpg"]="zoom/front/225226_U64-front_VD5_X1.jpg"
  ["20261105_225255.jpg"]="zoom/front/225255_U30-front_U16-U20.jpg"
  ["20261105_225321.jpg"]="zoom/back/225321_back-U30-area_left-edge.jpg"
  ["20261105_225326.jpg"]="zoom/back/225326_back-U64-area.jpg"
  ["20261105_225351.jpg"]="zoom/back/225351_back-connector-corner.jpg"
  ["20261105_225408.jpg"]="zoom/back/225408_back-U64-area_2.jpg"
  ["20261105_225412.jpg"]="zoom/back/225412_back-bottom-left.jpg"
  ["20261105_225440.jpg"]="case/225440_case-VIDEO-RGB-CASST.jpg"
  ["20261105_225522.jpg"]="case/225522_PSU-terminals.jpg"
  ["20261105_225533.jpg"]="case/225533_PSU-harness.jpg"
  ["20261105_230434.jpg"]="case/230434_PSU-wire-colors.jpg"
  ["20261105_230643.jpg"]="zoom/front/230643_U64_oscillator_X1-trimmer.jpg"
  ["20261105_230741.jpg"]="zoom/front/230741_U30-top_dram-row.jpg"
  ["20261105_230752.jpg"]="zoom/front/230752_oscillator_R-pair_U72-LS04.jpg"
  ["20261105_230758.jpg"]="zoom/front/230758_U30-pin1-side_traces.jpg"
  ["20261105_230803.jpg"]="zoom/front/230803_U30-bottom_traces.jpg"
  ["20261105_230807.jpg"]="zoom/front/230807_U16-U20_to_U30-traces.jpg"
  ["20261105_230829.jpg"]="zoom/front/230829_U64_U72_U73.jpg"
  ["20261105_232340.jpg"]="zoom/front/232340_oscillator_X1_R-pair_U72.jpg"
  ["20261105_232417.jpg"]="zoom/front/232417_U30_dram-row.jpg"
  ["20261105_232515.jpg"]="backlit/232515_backlit_U64.jpg"
  ["20261105_232518.jpg"]="backlit/232518_backlit_U64-left_U72-row.jpg"
  ["20261105_232548.jpg"]="backlit/232548_backlit_dram-area.jpg"
  ["20261105_232551.jpg"]="backlit/232551_backlit_U30.jpg"
  ["20261105_233927.jpg"]="backlit/sweep/20261105_233927.jpg"
  ["20261105_233940.jpg"]="backlit/sweep/20261105_233940.jpg"
  ["20261105_233943.jpg"]="backlit/sweep/20261105_233943.jpg"
  ["20261105_233952.jpg"]="backlit/sweep/20261105_233952.jpg"
  ["20261105_234009.jpg"]="backlit/sweep/20261105_234009.jpg"
  ["20261105_234012.jpg"]="backlit/sweep/20261105_234012.jpg"
  ["20261105_234015.jpg"]="backlit/sweep/20261105_234015.jpg"
  ["20261105_234019.jpg"]="backlit/sweep/20261105_234019.jpg"
  ["20261105_234030.jpg"]="backlit/sweep/20261105_234030.jpg"
  ["20261105_234032.jpg"]="backlit/sweep/20261105_234032.jpg"
  ["20261105_234045.jpg"]="backlit/sweep/20261105_234045_U64-crystal-corner.jpg"
  ["20261105_234054.jpg"]="backlit/sweep/20261105_234054.jpg"
  ["Scan_20261105_202556.jpg"]="overview/front/202556_front-full.jpg"
  ["Scan_20261105_202813.jpg"]="overview/front/202813_front-flat_layout-ref.jpg"
  ["Scan_20261105_203240.jpg"]="overview/back/203240_back-flat_registration-ref.jpg"
  ["Scan_20261105_203514.jpg"]="overview/back/203514_back-flat.jpg"
  ["Scan_20261105_203539.jpg"]="overview/front/203539_front-landscape_best-labels.jpg"
)

echo "삭제 대상 ${#REMOVE[@]}장:"; for f in "${REMOVE[@]}"; do [ -e "$f" ] && echo "  $f"; done
read -r -p "위 사진을 삭제하고 나머지를 정리할까요? [y/N] " ans
[ "$ans" = "y" ] || [ "$ans" = "Y" ] || { echo "취소했습니다."; exit 1; }

mkdir -p "$RAW"
for f in "${!KEEP[@]}"; do [ -e "$f" ] && mv -n "$f" "$RAW/"; done
for f in "${REMOVE[@]}"; do rm -f "$f" "$RAW/$f"; done
missing=0; for f in "${!KEEP[@]}"; do [ -e "$RAW/$f" ] || { echo "없음: $f"; missing=1; }; done
[ $missing = 0 ] || { echo "원본이 빠져 있어 HART 재구성을 중단합니다."; exit 1; }

rm -rf "$HART/photos/front" "$HART/photos/back" "$HART/photos/overview" "$HART/photos/zoom"
for f in "${!KEEP[@]}"; do d="$HART/photos/${KEEP[$f]}"; mkdir -p "$(dirname "$d")"; cp -p "$RAW/$f" "$d"; done
rm -f "$CLONE/apple2-clone-schematic.html"   # 옛 사본 (최신본은 HART/schematic/)
echo "완료: 원본 $(ls "$RAW" | wc -l)장 → $RAW, 저장소 사진 $(find "$HART/photos" -name "*.jpg" | wc -l)장"
echo "업로드: cd $HART && bash push.sh \"사진 폴더 재구성, 중복 사진 제거\""
