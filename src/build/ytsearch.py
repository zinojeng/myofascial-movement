#!/usr/bin/env python3
"""YouTube 搜尋小工具——策展時取得**真實** video id 的唯一合法來源。

`pubmed.py` 之於 PMID，就是這支之於 video id：一律從實際搜尋結果取，
不可憑記憶拼湊。回傳的長度與觀看數直接來自 YouTube，可以先拿來過濾
不合課程門檻的影片，省得策展完才被 `make audit` 打回票。

用法：
  python3 src/build/ytsearch.py "<query>" [n] [--min 0:30] [--max 14:00]
  python3 src/build/ytsearch.py "<query>" 10 --json
  python3 src/build/ytsearch.py subs <id> [<id> ...]    # 查字幕（人工／自動）

需要 yt-dlp（`uv tool install yt-dlp`）。
"""

from __future__ import annotations

import json
import subprocess
import sys

FIELDS = "%(id)s\t%(duration)s\t%(view_count)s\t%(channel)s\t%(title)s"


def clock(secs: int) -> str:
    h, rem = divmod(int(secs), 3600)
    m, s = divmod(rem, 60)
    return f"{h}:{m:02}:{s:02}" if h else f"{m}:{s:02}"


def parse_clock(text: str) -> int:
    secs = 0
    for part in str(text).split(":"):
        secs = secs * 60 + int(part)
    return secs


def search(query: str, n: int) -> list[dict]:
    proc = subprocess.run(
        [
            "yt-dlp",
            "--no-update",
            "--no-warnings",
            "--flat-playlist",
            "--print",
            FIELDS,
            f"ytsearch{n}:{query}",
        ],
        capture_output=True,
        text=True,
        timeout=180,
    )
    out = []
    for line in proc.stdout.strip().splitlines():
        parts = line.split("\t")
        if len(parts) < 5:
            continue
        vid, dur, views, channel, title = parts[:5]
        if len(vid) != 11:
            continue
        out.append(
            {
                "id": vid,
                "url": f"https://www.youtube.com/watch?v={vid}",
                "seconds": int(float(dur)) if dur not in ("NA", "None", "") else 0,
                "views": int(views) if views.isdigit() else None,
                "channel": channel,
                "title": title,
            }
        )
    if not out and proc.stderr.strip():
        print(proc.stderr.strip().splitlines()[-1][:200], file=sys.stderr)
    return out


def subs_of(vid: str) -> tuple[list[str], list[str]]:
    """回傳 (人工字幕語言, 自動字幕語言)，只留 en/zh。"""
    proc = subprocess.run(
        [
            "yt-dlp",
            "--no-update",
            "--no-warnings",
            "--skip-download",
            "--print",
            "%(subtitles)j\t%(automatic_captions)j",
            f"https://www.youtube.com/watch?v={vid}",
        ],
        capture_output=True,
        text=True,
        timeout=120,
    )
    line = proc.stdout.strip().split("\n")[-1] if proc.stdout.strip() else ""
    parts = line.split("\t")

    def langs(blob: str) -> list[str]:
        if not blob or blob in ("NA", "null"):
            return []
        try:
            return sorted(k for k in json.loads(blob) if k.split("-")[0] in ("en", "zh"))
        except json.JSONDecodeError:
            return []

    return langs(parts[0] if parts else ""), langs(parts[1] if len(parts) > 1 else "")


def report_subs(ids: list[str]) -> int:
    """策展英文影片時的守門員：沒有 en 字幕的片對聽力吃力的學習者幾乎沒用。"""
    for vid in ids:
        manual, auto = subs_of(vid)
        mark = "✓" if any(x.startswith("en") for x in manual) else ("~" if manual or auto else "✗")
        print(f"{mark} {vid}  人工={manual or '無'}  自動={auto or '無'}")
    print("\n✓ 有人工英文字幕　~ 只有自動字幕　✗ 完全沒有字幕")
    return 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    if args[0] == "subs":
        return report_subs(args[1:])

    as_json = "--json" in args
    args = [a for a in args if a != "--json"]

    lo, hi = 0, 10**9
    for flag, setter in (("--min", "lo"), ("--max", "hi")):
        if flag in args:
            i = args.index(flag)
            bound = parse_clock(args[i + 1])
            if setter == "lo":
                lo = bound
            else:
                hi = bound
            del args[i : i + 2]

    query = args[0]
    n = int(args[1]) if len(args) > 1 else 10

    rows = [r for r in search(query, n) if lo <= r["seconds"] <= hi]

    if as_json:
        print(json.dumps(rows, ensure_ascii=False, indent=1))
        return 0

    if not rows:
        print("(no hits)")
        return 0
    for r in rows:
        views = f"{r['views']:,}" if r["views"] is not None else "?"
        print(f"{r['id']}  {clock(r['seconds']):>7}  {views:>12}  {r['channel']}  {r['title']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
