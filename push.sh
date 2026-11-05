#!/usr/bin/env bash
# HART 저장소 초기 업로드 스크립트 (MSYS2에서 실행)
#   최초:   cd /home/milds/clone/HART && bash push.sh
#   이후:   bash push.sh "커밋 메시지"
set -e
cd "$(dirname "$0")"
REMOTE=git@github.com:mildstorm/HART.git

if [ ! -d .git ]; then
  git init
fi
git add -A
MSG="${1:-}"
if [ -n "$MSG" ]; then git -c core.autocrlf=false commit -m "$MSG" || echo "(커밋할 변경 없음)"; else
git -c core.autocrlf=false commit -m "Apple II 클론 보드(S/N 506267) 사진과 분석 자료 추가

- photos: 앞면 7장, 뒷면 4장
- docs: 개요, 시스템 구성, 부품표, 미확인 사항, 핀 배치, 다음 단계
- schematic: 인터랙티브 블록 회로도/배치도 HTML과 생성 스크립트
- data: 부품 데이터 CSV (배치 좌표 포함)

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
Claude-Session: https://claude.ai/code/session_01HyxGAzAGfyWGbqjMQU7sfC" || echo "(커밋할 변경 없음)"
fi
git branch -M main
if git remote get-url origin >/dev/null 2>&1; then
  git remote set-url origin "$REMOTE"
else
  git remote add origin "$REMOTE"
fi
git push -u origin main
