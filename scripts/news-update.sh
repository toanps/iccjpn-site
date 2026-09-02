#!/usr/bin/env bash
# news-update.sh — Weekly ICC JAPAN news refresh.
#
# Pipeline:
#   1. deep-research raw data collection across multiple foreigner-in-Japan queries
#   2. LLM (9router/bestmay) synthesises into news-card items (Japanese)
#   3. Inject into ~/projects/iccjpn-site/news.html (backup + dedupe + prune)
#   4. git add/commit/push → Cloudflare Pages auto-deploys
#
# Flags:
#   --dry-run     Skip write + git (preview at /tmp/icc-news-update.diff.html)
#   --no-push     Commit locally but don't push
#   --discord     Also send the research summary to Discord
#
# Scheduled weekly via `openclaw cron` (crow agent, Saturday 08:00 JST).

set -euo pipefail

SITE_ROOT="${ICC_SITE_ROOT:-$HOME/projects/iccjpn-site}"
SCRIPT_DIR="$SITE_ROOT/scripts"
RESEARCH_SH="$HOME/.openclaw/skills/deep-research/scripts/research-cli.sh"
OUTPUT_DIR="/tmp/icc-news-research"
DISCORD_FLAG=""
DRY_RUN=""
DO_PUSH="yes"

for arg in "$@"; do
  case "$arg" in
    --dry-run)  DRY_RUN="--dry-run" ;;
    --no-push)  DO_PUSH="no" ;;
    --discord)  DISCORD_FLAG="--discord" ;;
    -h|--help)
      sed -n '2,20p' "$0"; exit 0 ;;
    *)
      echo "unknown arg: $arg" >&2; exit 2 ;;
  esac
done

mkdir -p "$OUTPUT_DIR"

# Angles tuned for ICC JAPAN's audience: Japanese SMEs hiring foreign workers.
# Mix of Japanese (targets domestic news sources) and English (broader context).
ANGLES="外国人労働者 日本 法改正 最新|育成就労制度 2026|特定技能 制度変更|\
外国人雇用 助成金 最新|外国人材 中小企業 導入事例|\
ベトナム人 労働者 日本 ニュース|\
immigration law Japan 2026 foreign workers|\
technical intern training Japan policy update"

TS="$(date -u +%Y%m%d_%H%M%S)"
JSON_OUT="$OUTPUT_DIR/research_${TS}.json"

echo "[icc-news] $(date '+%F %T') starting weekly update" >&2
echo "[icc-news] angles: $(echo "$ANGLES" | tr '|' '\n' | wc -l | tr -d ' ') queries" >&2

RESEARCH_COUNT="${ICC_NEWS_RESEARCH_COUNT:-6}"
RESEARCH_TIMEOUT_SECONDS="${ICC_NEWS_RESEARCH_TIMEOUT_SECONDS:-420}"

set +e
python3 - "$RESEARCH_TIMEOUT_SECONDS" "$RESEARCH_SH" "$ANGLES" "$RESEARCH_COUNT" "$OUTPUT_DIR" "$DISCORD_FLAG" <<'PY'
import subprocess
import sys

timeout_s = int(sys.argv[1])
research_sh, angles, count, output_dir, discord_flag = sys.argv[2:7]
cmd = [
    "bash", research_sh, "外国人労働者 日本 最新ニュース",
    "--angles", angles,
    "--sources", "brave,bird",
    "--count", count,
    "--output", output_dir,
]
if discord_flag:
    cmd.append(discord_flag)
try:
    raise SystemExit(subprocess.run(cmd, timeout=timeout_s).returncode)
except subprocess.TimeoutExpired:
    print(f"[icc-news] ERROR: research collection timed out after {timeout_s}s", file=sys.stderr)
    raise SystemExit(124)
PY
rc=$?
set -e
if [[ $rc -ne 0 ]]; then
  echo "[icc-news] ERROR: research collection failed or timed out (rc=$rc, timeout=${RESEARCH_TIMEOUT_SECONDS}s)" >&2
  exit "$rc"
fi

# research-cli.sh writes research_YYYYMMDD_HHMMSS.json — find the newest one.
LATEST="$(ls -1t "$OUTPUT_DIR"/research_*.json 2>/dev/null | head -1)"
if [[ -z "$LATEST" ]]; then
  echo "[icc-news] ERROR: deep-research produced no JSON output" >&2
  exit 1
fi
echo "[icc-news] research output: $LATEST" >&2

# Run the synthesizer + injector
PY="$SITE_ROOT/venv/bin/python3"
[[ -x "$PY" ]] || PY="$(command -v python3)"

OUT="$(
  "$PY" "$SCRIPT_DIR/news-update.py" "$LATEST" $DRY_RUN
)"
echo "$OUT"

# SUMMARY line printed by news-update.py on success (skipped if nothing added)
if ! echo "$OUT" | grep -q '^SUMMARY '; then
  echo "[icc-news] no new items — skipping git commit" >&2
  exit 0
fi

if [[ -n "$DRY_RUN" ]]; then
  echo "[icc-news] dry run — skipping git commit" >&2
  exit 0
fi

# Commit + push
cd "$SITE_ROOT"
if git diff --quiet news.html; then
  echo "[icc-news] news.html unchanged after injection — skipping commit" >&2
  exit 0
fi

SUMMARY_LINE="$(echo "$OUT" | grep '^SUMMARY ' | head -1 | sed 's/^SUMMARY //')"
DATE_STAMP="$(date '+%Y-%m-%d')"
git add news.html
git commit -m "chore(news): weekly refresh $DATE_STAMP ($SUMMARY_LINE)" >&2

if [[ "$DO_PUSH" == "yes" ]]; then
  git push >&2
  echo "[icc-news] pushed — Cloudflare Pages will auto-deploy" >&2
else
  echo "[icc-news] --no-push set; commit made locally only" >&2
fi

echo "[icc-news] done."
