#!/usr/bin/env python3
"""用 yt-dlp 抓每支影片的真實中繼資料，寫進 course/data/video-meta.json。

策展 agent 抄下來的長度常有 ±30 秒誤差，觀看數更是隨時在變。建置時會用這個檔
覆寫長度、頻道與觀看數，課程總時長才會準；`make audit` 也靠它查長度區間與觀看數。

用法：
    python3 src/build/fetch_meta.py            # 只補還沒有的
    python3 src/build/fetch_meta.py --refresh  # 全部重抓
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / os.environ.get("COURSE", "course") / "data"
META = DATA / "video-meta.json"

VID = re.compile(r"(?:v=|youtu\.be/)([\w-]{11})")
FIELDS = (
    "%(id)s\t%(duration)s\t%(view_count)s\t%(channel)s\t%(title)s"
    "\t%(subtitles)j\t%(automatic_captions)j"
)

# 只在意學習者實際用得到的軌道：英文與中文。自動字幕動輒 150 種語言，全存沒有意義。
WANTED = ("en", "zh")


def subtitle_langs(blob: str) -> list[str]:
    """把 yt-dlp 的字幕 JSON 縮成排序後的 en/zh 語言碼清單。"""
    if not blob or blob in ("NA", "null"):
        return []
    try:
        tracks = json.loads(blob)
    except json.JSONDecodeError:
        return []
    return sorted(k for k in tracks if k.split("-")[0] in WANTED)


def collect_ids() -> list[str]:
    """掃過所有策展資料，收集去重後的 video id（保持出現順序）。"""
    ids: dict[str, None] = {}

    def walk(node) -> None:
        if isinstance(node, dict):
            url = node.get("url")
            if isinstance(url, str) and (m := VID.search(url)):
                ids.setdefault(m.group(1), None)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    for path in sorted(DATA.glob("*.json")):
        if path.name == "video-meta.json":
            continue
        try:
            walk(json.loads(path.read_text()))
        except json.JSONDecodeError as exc:
            print(f"✗ {path.name} 不是合法 JSON：{exc}", file=sys.stderr)
    return list(ids)


def fetch(vid: str) -> tuple[str, dict]:
    # 沒有 cookie 時 YouTube 會在數百次請求後回「Sign in to confirm you're not a bot」，
    # 那不是影片失效。COOKIES_BROWSER 指定要借用哪個瀏覽器的登入狀態。
    cookies = os.environ.get("COOKIES_BROWSER", "chrome")
    proc = subprocess.run(
        [
            "yt-dlp",
            "--no-update",
            "--no-warnings",
            "--skip-download",
            "--ignore-no-formats-error",
            *(["--cookies-from-browser", cookies] if cookies else []),
            "--print",
            FIELDS,
            f"https://www.youtube.com/watch?v={vid}",
        ],
        capture_output=True,
        text=True,
        timeout=90,
    )
    line = proc.stdout.strip().split("\n")[-1] if proc.stdout.strip() else ""
    parts = line.split("\t")
    if len(parts) < 5 or parts[0] != vid:
        err = (proc.stderr or "").strip().split("\n")[-1][:120]
        return vid, {"status": "ERROR", "note": err or "no output"}
    _, dur, views, channel, title = parts[:5]
    manual = subtitle_langs(parts[5] if len(parts) > 5 else "")
    auto = subtitle_langs(parts[6] if len(parts) > 6 else "")
    return vid, {
        "status": "OK",
        "seconds": int(float(dur)) if dur not in ("NA", "None", "") else 0,
        "views": int(views) if views.isdigit() else None,
        "channel": channel,
        "title": title,
        # 人工上字幕代表製作用心，自動字幕代表至少聽得懂——兩者價值不同，分開記
        "subs": manual,
        "auto_subs": auto,
    }


def main() -> int:
    refresh = "--refresh" in sys.argv
    meta = {} if refresh else (json.loads(META.read_text()) if META.exists() else {})

    ids = collect_ids()
    todo = [v for v in ids if v not in meta or meta[v].get("status") != "OK"]
    print(f"影片 {len(ids)} 支，需抓取 {len(todo)} 支")

    with ThreadPoolExecutor(max_workers=3) as pool:
        for i, (vid, info) in enumerate(pool.map(fetch, todo), 1):
            meta[vid] = info
            flag = "✓" if info["status"] == "OK" else "✗"
            print(f"  {flag} [{i}/{len(todo)}] {vid} {info.get('title', info.get('note', ''))[:60]}")

    # 只留還在用的，避免舊資料殘留
    meta = {v: meta[v] for v in ids if v in meta}
    META.write_text(json.dumps(meta, ensure_ascii=False, indent=2, sort_keys=True) + "\n")

    ok = sum(1 for v in meta.values() if v.get("status") == "OK")
    total_s = sum(v.get("seconds") or 0 for v in meta.values() if v.get("status") == "OK")
    print(f"→ {META.relative_to(ROOT)}  {ok}/{len(meta)} OK，合計 {total_s // 3600}h {total_s % 3600 // 60}m")
    return 0 if ok == len(meta) else 1


if __name__ == "__main__":
    raise SystemExit(main())
