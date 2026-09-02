#!/usr/bin/env python3
"""
news-update.py — Take a deep-research JSON output, ask 9router/bestmay to produce
fresh ICC-JAPAN news items, then inject them into a single flat date-sorted
list at ~/projects/iccjpn-site/news.html.

Invoked by scripts/news-update.sh (which runs deep-research first and passes
the JSON path as argv[1]).

Policy:
- Items must be recent (dates within MAX_AGE_MONTHS of today, default 3).
- Articles are maintained in one flat list, sorted newest-first by 年月.
- List pruned to MAX_ITEMS_TOTAL most recent items.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request
from datetime import datetime
from pathlib import Path

SITE_ROOT = Path(os.environ.get("ICC_SITE_ROOT", Path.home() / "projects/iccjpn-site"))
NEWS_HTML = SITE_ROOT / "news.html"
LLM_URL = os.environ.get("ICC_NEWS_LLM_URL", "http://127.0.0.1:20128/v1/chat/completions")
LLM_KEY = os.environ.get("ICC_NEWS_LLM_KEY", "not-needed")
MODEL = os.environ.get("ICC_NEWS_MODEL", "bestmay")
MAX_ITEMS_TOTAL = int(os.environ.get("ICC_NEWS_MAX_TOTAL_KEEP", "20"))
MAX_NEW_PER_RUN = int(os.environ.get("ICC_NEWS_MAX_NEW_PER_RUN", "3"))
# Max age a news item can have (months). Applied to NEW items only — historical
# entries in news.html are left untouched.
MAX_AGE_MONTHS = int(os.environ.get("ICC_NEWS_MAX_AGE_MONTHS", "3"))

LIST_OPEN = '<div class="news-list">'
LIST_CLOSE_MARKER = '<!-- news-list-end -->'

_JP_DATE_RE = re.compile(r"(\d{4})\s*年\s*(\d{1,2})\s*月")


def parse_jp_date(s: str) -> tuple[int, int] | None:
    if not s:
        return None
    m = _JP_DATE_RE.search(s)
    return (int(m.group(1)), int(m.group(2))) if m else None


def months_ago(ym: tuple[int, int], now: datetime | None = None) -> int:
    now = now or datetime.now()
    return (now.year - ym[0]) * 12 + (now.month - ym[1])


def call_llm(system: str, user: str, *, temperature: float = 0.3,
             max_tokens: int = 4000, retries: int = 3,
             timeout: int = 600) -> str:
    payload = {
        "model": MODEL,
        "temperature": temperature,
        "max_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": system},
            {"role": "user", "content": user},
        ],
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        LLM_URL, data=data,
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {LLM_KEY}",
        },
    )
    last_err = None
    for attempt in range(retries):
        try:
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8").strip()
            # Some 9router models always answer as an SSE stream even without
            # stream:true — reassemble the content deltas in that case.
            if body.startswith("data:"):
                parts: list[str] = []
                for line in body.splitlines():
                    line = line.strip()
                    if not line.startswith("data:"):
                        continue
                    chunk_raw = line[5:].strip()
                    if not chunk_raw or chunk_raw == "[DONE]":
                        continue
                    chunk = json.loads(chunk_raw)
                    choices = chunk.get("choices") or [{}]
                    delta = choices[0].get("delta") or {}
                    parts.append(delta.get("content") or "")
                content = "".join(parts).strip()
            else:
                parsed = json.loads(body)
                content = (parsed["choices"][0]["message"]["content"] or "").strip()
            if not content:
                raise ValueError("empty content in LLM response")
            return content
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"LLM call failed after {retries} attempts: {last_err}")


def parse_json_loose(text: str):
    """Extract a JSON array from an LLM response. Handles:
    - markdown fences  (```json ... ``` or ``` ... ```)
    - leading prose ("Here is the JSON: [...]")
    - trailing prose
    - the full-text `[...]` pattern
    Raises ValueError on unrecoverable failure.
    """
    if not text or not text.strip():
        raise ValueError("LLM returned empty response")
    text = text.strip()
    # Strip markdown fences
    if text.startswith("```"):
        text = re.sub(r"^```(?:json)?\s*", "", text)
        text = re.sub(r"\s*```\s*$", "", text)
    # Fast path
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    # Greedy match of outermost [...] — try progressively shorter slices if
    # the first attempt has an unterminated string somewhere inside.
    first_bracket = text.find("[")
    if first_bracket == -1:
        raise ValueError(
            f"no '[' found in LLM response; first 200 chars: {text[:200]!r}"
        )
    # Find matching closing bracket by counting, ignoring brackets inside strings.
    depth = 0
    in_str = False
    escape = False
    last_close = -1
    for i, ch in enumerate(text[first_bracket:], start=first_bracket):
        if escape:
            escape = False
            continue
        if ch == "\\" and in_str:
            escape = True
            continue
        if ch == '"':
            in_str = not in_str
            continue
        if in_str:
            continue
        if ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                last_close = i
                break
    if last_close == -1:
        raise ValueError(
            f"unclosed '[' in LLM response; first 200 chars: {text[:200]!r}"
        )
    return json.loads(text[first_bracket:last_close + 1])


def synthesise_news(research_raw: dict) -> list[dict]:
    """Ask the LLM for a flat list of recent news items."""
    trimmed = {}
    for src, items in (research_raw.get("sources") or {}).items():
        if not isinstance(items, list):
            continue
        trimmed[src] = items[:20]
    data_text = json.dumps(trimmed, ensure_ascii=False, indent=1)[:30000]

    now = datetime.now()
    cutoff_year = now.year
    cutoff_month = now.month - MAX_AGE_MONTHS
    while cutoff_month <= 0:
        cutoff_month += 12
        cutoff_year -= 1

    system = (
        "あなたはICC JAPANの広報担当者です。ICC JAPANはベトナム人エンジニアを"
        "日本企業へ紹介する人材紹介会社です。外国人労働者・育成就労・特定技能・"
        "関連法改正など、ICC JAPANの顧客（日本の中小企業）にとって有益な**最新**"
        "ニュースを、提供された調査データから抽出・要約してください。\n\n"
        f"本日は{now.year}年{now.month}月{now.day}日です。\n"
        f"**ニュースの日付は{cutoff_year}年{cutoff_month}月以降のもののみ採用してください。**\n"
        f"それより古いニュース（{MAX_AGE_MONTHS}ヶ月以上前）は絶対に含めないでください。\n\n"
        "各ニュースは以下のJSON配列の要素として出力してください。Markdownの"
        "コードフェンスは使わず、純粋なJSON配列のみを出力してください：\n\n"
        "[\n"
        "  {\n"
        '    "title": "日本語のニュース見出し（30-60文字）",\n'
        '    "date": "YYYY年M月",\n'
        '    "label": "重要|新着|注目|法改正|制度変更|調査結果|実績|市場分析|業界動向|試験情報|新サービス",\n'
        '    "summary": "<p>...</p>タグで始まる日本語のHTML要約（100-250文字、<strong>や<ul><li>を使ってよい）",\n'
        '    "source": "出典（例：厚生労働省／日経新聞／TechCrunch Japan）"\n'
        "  }\n"
        "]\n\n"
        "ルール：\n"
        "- 同じ出来事を複数項目にしない。\n"
        "- 出典が不明な内容は出さない。\n"
        f"- **合計で必ず{MAX_NEW_PER_RUN}件以内**に厳選する（最重要・最新のみ）。\n"
        "- 宣伝的すぎる表現・過度な誇張は避ける。"
    )
    user = (
        "以下は外国人労働者・日本の雇用関連ニュースの生データです。ここから"
        "上記ルールに従ってニュース項目を抽出してください。\n\n" + data_text
    )
    parsed = None
    last_err: Exception | None = None
    for attempt in range(3):
        try:
            raw = call_llm(system, user, temperature=0.3, max_tokens=4000)
            if not raw.strip():
                raise ValueError("empty LLM response")
            parsed = parse_json_loose(raw)
            if not isinstance(parsed, list):
                raise ValueError(
                    f"LLM returned non-list output: {type(parsed).__name__}"
                )
            break
        except Exception as exc:  # noqa: BLE001
            last_err = exc
            print(f"[news-update] LLM parse attempt {attempt + 1}/3 failed: "
                  f"{exc}", file=sys.stderr)
            time.sleep(2)
    if parsed is None:
        raise RuntimeError(f"LLM synthesis failed 3× — last error: {last_err}")

    cleaned: list[dict] = []
    dropped_old = 0
    for item in parsed:
        if not isinstance(item, dict):
            continue
        if not (item.get("title") and item.get("summary")):
            continue
        date_str = (item.get("date") or now.strftime("%Y年%-m月")).strip()
        ym = parse_jp_date(date_str)
        if ym is not None:
            age = months_ago(ym, now)
            if age > MAX_AGE_MONTHS or age < -1:
                dropped_old += 1
                print(f"  [drop] {date_str} — {item.get('title', '')[:60]} "
                      f"({age}mo, limit {MAX_AGE_MONTHS})", file=sys.stderr)
                continue
        cleaned.append({
            "title": item["title"].strip(),
            "date": date_str,
            "label": (item.get("label") or "新着").strip(),
            "summary": item["summary"].strip(),
            "source": (item.get("source") or "").strip(),
        })
        if len(cleaned) >= MAX_NEW_PER_RUN:
            break
    if dropped_old:
        print(f"[news-update] dropped {dropped_old} stale item(s) "
              f"(> {MAX_AGE_MONTHS}mo)", file=sys.stderr)
    return cleaned


def render_article(item: dict) -> str:
    """Render one news item as the site's news-card HTML."""
    label_class_map = {
        "重要": "news-label-important",
        "法改正": "news-label-law",
        "制度変更": "news-label-update",
        "新サービス": "news-label-update",
        "試験情報": "news-label-update",
        "職種追加": "news-label-update",
        "調査結果": "news-label-success",
        "実績": "news-label-success",
        "特集": "news-label-success",
        "市場分析": "news-label-trend",
        "業界動向": "news-label-trend",
        "注目": "news-label-highlight",
        "新着": "news-label-new",
    }
    label_class = label_class_map.get(item["label"], "news-label-new")

    source_html = ""
    if item["source"]:
        source_html = f'                        <p class="news-source">出典：{item["source"]}</p>\n'

    summary = item["summary"]
    if not summary.lstrip().startswith("<"):
        summary = f"<p>{summary}</p>"

    return (
        f'\n                <article class="news-card">\n'
        f'                    <div class="news-header">\n'
        f'                        <span class="news-label {label_class}">{item["label"]}</span>\n'
        f'                        <time class="news-date">{item["date"]}</time>\n'
        f'                    </div>\n'
        f'                    <h3 class="news-title">{item["title"]}</h3>\n'
        f'                    <div class="news-content">\n'
        f'                        {summary}\n'
        f'{source_html}'
        f'                    </div>\n'
        f'                </article>\n'
    )


def dedupe_titles_against_html(items: list[dict], html: str) -> list[dict]:
    return [it for it in items if it["title"] not in html]


def _find_list_region(html: str) -> tuple[int, int]:
    """Return (insert_start, insert_end) byte offsets for the news-list region.
    insert_start = byte just after <div class="news-list">
    insert_end   = byte just before <!-- news-list-end -->"""
    start = html.find(LIST_OPEN)
    if start == -1:
        raise RuntimeError(
            f"news.html does not contain {LIST_OPEN!r} — run the flat-list migration first."
        )
    insert_start = start + len(LIST_OPEN)
    end = html.find(LIST_CLOSE_MARKER, insert_start)
    if end == -1:
        raise RuntimeError(
            f"news.html does not contain {LIST_CLOSE_MARKER!r} — structure broken?"
        )
    return insert_start, end


def sort_and_prune_list(html: str, *, keep: int = MAX_ITEMS_TOTAL) -> str:
    """Extract all articles inside news-list, sort by date desc (stable),
    keep the newest `keep` items, and re-emit."""
    insert_start, insert_end = _find_list_region(html)
    region = html[insert_start:insert_end]

    article_re = re.compile(r'(\s*<article class="news-card">.*?</article>)', re.DOTALL)
    articles = article_re.findall(region)
    if not articles:
        return html

    date_re = re.compile(r'<time class="news-date">([^<]+)</time>')

    def sort_key(article_html: str) -> tuple[int, int, int]:
        # (bucket, -year, -month)  — unparseable dates fall to the bottom
        m = date_re.search(article_html)
        if not m:
            return (1, 0, 0)
        ym = parse_jp_date(m.group(1))
        if ym is None:
            return (1, 0, 0)
        return (0, -ym[0], -ym[1])

    sorted_articles = sorted(articles, key=sort_key)
    kept = sorted_articles[:keep]

    new_region = "".join(kept) + "\n            "
    return html[:insert_start] + new_region + html[insert_end:]


def inject_items(html: str, items: list[dict]) -> str:
    """Insert new items at the top of the news-list region. Sort + prune later."""
    if not items:
        return html
    insert_start, _ = _find_list_region(html)
    blob = "".join(render_article(it) for it in items)
    return html[:insert_start] + blob + html[insert_start:]


def main():
    if len(sys.argv) < 2:
        print("usage: news-update.py <research_json_path> [--dry-run]",
              file=sys.stderr)
        sys.exit(2)
    research_path = Path(sys.argv[1])
    dry_run = "--dry-run" in sys.argv[2:]

    research_raw = json.loads(research_path.read_text(encoding="utf-8"))
    print(f"[news-update] loaded {research_path}", file=sys.stderr)

    items = synthesise_news(research_raw)
    print(f"[news-update] LLM produced {len(items)} news items", file=sys.stderr)

    html = NEWS_HTML.read_text(encoding="utf-8")
    items = dedupe_titles_against_html(items, html)
    print(f"[news-update] {len(items)} new items after dedupe", file=sys.stderr)

    updated = inject_items(html, items)
    updated = sort_and_prune_list(updated, keep=MAX_ITEMS_TOTAL)

    if updated == html:
        print("[news-update] no changes (nothing new, list already sorted) — "
              "exiting cleanly", file=sys.stderr)
        return

    if dry_run:
        diff_path = Path("/tmp/icc-news-update.diff.html")
        diff_path.write_text(updated, encoding="utf-8")
        print(f"[news-update] dry run — preview at {diff_path}", file=sys.stderr)
        return

    backup = NEWS_HTML.with_suffix(
        f".bak.{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    )
    backup.write_text(html, encoding="utf-8")
    NEWS_HTML.write_text(updated, encoding="utf-8")
    print(f"[news-update] wrote {NEWS_HTML} (backup: {backup.name})", file=sys.stderr)

    print(f"SUMMARY added={len(items)}")


if __name__ == "__main__":
    main()
