#!/usr/bin/env bash
# HART 자동 commit/push 감시 스크립트 (MSYS2에서 실행, 창을 열어 둔 채로 사용)
#
#   bash ~/clone/HART/tools/hart_autopush.sh
#
# 동작:
#   Claude가 HART/.push/request 파일을 만들면 이 스크립트가 감지해서
#   정해진 git 명령만 실행하고, 결과를 HART/.push/result.log 에 남깁니다.
#   - request 첫 줄: 동작 (push | organize+push)
#   - 둘째 줄부터: 커밋 메시지 (명령으로 실행되지 않고 메시지로만 쓰임)
#   다른 명령은 실행하지 않습니다. 종료는 Ctrl+C.
set -u
HART="$(cd "$(dirname "$0")/.." && pwd)"
Q="$HART/.push"
REMOTE=git@github.com:mildstorm/HART.git
mkdir -p "$Q"
cd "$HART"

grep -qx '.push/' .gitignore 2>/dev/null || echo '.push/' >> .gitignore
[ -d .git ] || git init -q
git branch -M main 2>/dev/null || true
if git remote get-url origin >/dev/null 2>&1; then git remote set-url origin "$REMOTE"; else git remote add origin "$REMOTE"; fi

echo "[$(date '+%F %T')] 감시 시작: $Q/request (Ctrl+C로 종료)"
echo "ready $(date '+%F %T')" > "$Q/status"

while true; do
  if [ -f "$Q/request" ]; then
    mv "$Q/request" "$Q/processing"
    action="$(head -n1 "$Q/processing" | tr -d '\r ')"
    tail -n +2 "$Q/processing" | tr -d '\r' > "$Q/commit_msg.txt"
    [ -s "$Q/commit_msg.txt" ] || echo "update" > "$Q/commit_msg.txt"
    {
      echo "=== $(date '+%F %T') action=$action ==="
      case "$action" in
        organize+push)
          echo "--- organize_photos.sh ---"
          yes y | bash "$HART/organize_photos.sh" ;;
        push) ;;
        *) echo "알 수 없는 동작: $action (push 또는 organize+push만 허용)"; action=invalid ;;
      esac
      if [ "$action" != invalid ]; then
        echo "--- git add/commit ---"
        git add -A
        git -c core.autocrlf=false commit -F "$Q/commit_msg.txt" || echo "(커밋할 변경 없음)"
        echo "--- git push ---"
        GIT_TERMINAL_PROMPT=0 git push -u origin main
        echo "push_exit=$?"
        echo "--- 최근 커밋 ---"
        git log --oneline -3
      fi
    } > "$Q/result.log" 2>&1
    rm -f "$Q/processing"
    echo "done $(date '+%F %T')" > "$Q/status"
    echo "[$(date '+%F %T')] 처리 완료 ($action). 결과: $Q/result.log"
    tail -n 5 "$Q/result.log"
  fi
  sleep 3
done
