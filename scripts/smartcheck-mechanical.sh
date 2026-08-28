#!/usr/bin/env bash
set -u

FAIL_COUNT=0
FAILURES=()

CMD=""
EXPECT=""
ALLOW=()

while [ $# -gt 0 ]; do
  case "$1" in
    --cmd)
      CMD="$2"
      shift 2
      ;;
    --expect)
      EXPECT="$2"
      shift 2
      ;;
    --allow)
      ALLOW+=("$2")
      shift 2
      ;;
    *)
      echo "SMARTCHECK FAIL:"
      echo "  unrecognized flag: $1"
      exit 1
      ;;
  esac
done

if [ -z "$CMD" ]; then
  echo "SMARTCHECK FAIL:"
  echo "  --cmd not supplied"
  exit 1
fi

if [ -z "$EXPECT" ]; then
  echo "SMARTCHECK FAIL:"
  echo "  --expect not supplied"
  exit 1
fi

ACTUAL="$(bash -c "$CMD")" && CMD_RC=0 || CMD_RC=$?

if [ "${CMD_RC:-0}" -ne 0 ]; then
  FAILURES+=("command exited nonzero: rc=$CMD_RC")
fi

if [ "$ACTUAL" != "$EXPECT" ]; then
  FAILURES+=("output mismatch: expected [$EXPECT] got [$ACTUAL]")
fi

STATUS="$(git status --porcelain --untracked-files=all 2>&1)"
GIT_RC=$?

if [ $GIT_RC -ne 0 ]; then
  FAILURES+=("git status failed: $STATUS")
else
  while IFS= read -r line; do
    if [ -z "$line" ]; then
      continue
    fi
    
    XY="${line:0:2}"
    path="${line:3}"
    
    [[ "$path" == \"* && "$path" == *\" ]] && path="${path:1:${#path}-2}"
    
    if [ "$XY" != "??" ]; then
      FAILURES+=("tracked change: $path ($XY)")
    else
      ALLOWED=0
      for allow_entry in "${ALLOW[@]}"; do
        if [ "$path" = "$allow_entry" ] || [[ "$path" == "$allow_entry"/* ]]; then
          ALLOWED=1
          break
        fi
      done
      
      if [ $ALLOWED -eq 0 ]; then
        FAILURES+=("untracked path not allowed: $path")
      fi
    fi
  done <<< "$STATUS"
fi

if [ ${#FAILURES[@]} -gt 0 ]; then
  echo "SMARTCHECK FAIL:"
  for failure in "${FAILURES[@]}"; do
    echo "  $failure"
  done
  exit 1
else
  echo "SMARTCHECK PASS"
  exit 0
fi
