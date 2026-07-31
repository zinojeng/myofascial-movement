#!/usr/bin/env python3
"""抓 YouTube 字幕全文，並用它查核策展宣稱。

## 為什麼需要這支

在這支工具出現之前，課程裡每一條 `claim_boundary`（這支片哪句話要打折扣）、
`coach_takeaway`（實務重點）與 `practical_value`（教學價值）都是從**標題與頻道**
推斷的——沒有人真的「聽過」影片內容。對一門主打「哪一部分值得學、哪一部分需要
保留」的課來說，這是最不該有的漏洞：我們等於在用封面評論一本書。

字幕全文直接來自 YouTube，不經任何第三方摘要服務。摘要會把我們最在意的細微
差別（「可能有幫助」vs「能把沾黏壓開」）洗掉，所以這裡刻意只取原文。

## 用法

    python3 src/build/transcript.py get <videoId> [--lang en]   # 印出純文字
    python3 src/build/transcript.py scan [--lang en]            # 全課掃描誇大宣稱
    python3 src/build/transcript.py scan --missing              # 只列「說了卻沒標」的

`scan` 會比對兩件事：影片**實際說了**哪些被課程列為不可接受的宣稱，
以及我們**有沒有**在 `claim_boundary` 標出來。兩者不一致就是策展缺口。

字幕快取在 .transcripts/（已 gitignore）——那是第三方影片的內容，不進版控。
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
COURSE = Path(os.environ.get("COURSE") or ROOT / "course").resolve()
DATA = COURSE / "data"
CACHE = ROOT / ".transcripts"

# 課程明確拒絕的說法。key 是中文標籤，值是中英文的比對樣式。
# 這份清單跟 docs/dual-axis-brief.md 第 6 節的「應避免的說法」對齊。
CLAIMS: dict[str, list[str]] = {
    "壓開沾黏": [
        r"break(?:ing)?\s+up\s+(?:the\s+)?(?:adhesion|scar tissue|knot)",
        r"break(?:ing)?\s+down\s+(?:the\s+)?(?:adhesion|scar tissue)",
        r"smooth out (?:the )?(?:fascia|adhesion)",
        "壓開沾黏", "打散沾黏", "把沾黏", "鬆開沾黏", "解除沾黏",
    ],
    "把筋膜拉長": [
        r"lengthen(?:ing)? (?:the )?(?:fascia|muscle)",
        r"stretch(?:ing)? out (?:the )?fascia",
        "把筋膜拉長", "筋膜變長", "延展筋膜", "拉長筋膜",
    ],
    "排乳酸／排毒": [
        r"flush(?:ing)? out (?:the )?(?:lactic acid|toxin)",
        r"release (?:the )?toxin", r"lactic acid build[- ]?up",
        "排出乳酸", "代謝乳酸", "排毒", "排除毒素",
    ],
    "永久矯正結構": [
        r"permanently (?:fix|correct|realign)",
        r"realign(?:ing)? (?:your )?(?:pelvis|spine)",
        "永久調正", "永久矯正", "把骨盆喬回", "矯正回正常位置",
    ],
    "越痛越有效": [
        r"no pain,? no gain", r"the more it hurts,? the better",
        "越痛越有效", "越痛效果越好", "要痛才有效",
    ],
    "單一原因論": [
        r"all (?:low )?back pain (?:is|comes from)",
        r"the (?:real )?cause of all",
        "所有下背痛都是", "都是筋膜造成", "只要按這個點就能治",
    ],
}

VTT_TAG = re.compile(r"<[^>]+>")
VTT_TS = re.compile(r"^\d{2}:\d{2}:\d{2}\.\d{3}\s+-->")


def vtt_to_text(vtt: str) -> str:
    """WEBVTT -> 去重後的純文字。自動字幕會逐行重複，必須去重才讀得下去。"""
    out: list[str] = []
    for raw in vtt.splitlines():
        line = VTT_TAG.sub("", raw).strip()
        if not line or line.startswith(("WEBVTT", "Kind:", "Language:")):
            continue
        if VTT_TS.match(line) or line.isdigit():
            continue
        if out and out[-1] == line:
            continue
        out.append(line)
    return "\n".join(out)


def fetch(vid: str, lang: str = "en") -> str | None:
    """回傳字幕全文；沒有字幕或被擋回 None。結果快取到 .transcripts/。"""
    CACHE.mkdir(exist_ok=True)
    cached = CACHE / f"{vid}.{lang}.txt"
    if cached.exists():
        return cached.read_text()

    tmp = CACHE / f".tmp-{vid}"
    # 只要一個語言變體，否則 YouTube 會因為連續請求回 429
    proc = subprocess.run(
        [
            "yt-dlp", "--no-update", "--no-warnings", "--skip-download",
            "--write-subs", "--write-auto-subs",
            "--sub-langs", lang, "--sub-format", "vtt",
            "-o", str(tmp) + ".%(ext)s",
            f"https://www.youtube.com/watch?v={vid}",
        ],
        capture_output=True, text=True, timeout=180,
    )
    files = sorted(CACHE.glob(f".tmp-{vid}*.vtt"))
    if not files:
        err = (proc.stderr or "").strip().split("\n")[-1][:100]
        print(f"  ✗ {vid} 沒有 {lang} 字幕（{err}）", file=sys.stderr)
        return None

    text = vtt_to_text(files[0].read_text())
    cached.write_text(text)
    for f in files:
        f.unlink()
    return text


def course_videos() -> list[dict]:
    """從建置產物取出所有影片節點，附帶它現有的 claim_boundary。"""
    built = ROOT / "dist" / "course.json"
    if not built.exists():
        print("✗ 先跑 make build", file=sys.stderr)
        sys.exit(1)
    c = json.loads(built.read_text())
    out = []
    for ch in c["chapters"]:
        for u in ch["units"]:
            for v in (u.get("lessons") or []) + (u.get("drills") or []):
                if v.get("url"):
                    out.append({**v, "unit": u["id"]})
    return out


def scan(lang: str, only_missing: bool) -> int:
    vids = course_videos()
    print(f"掃描 {len(vids)} 個影片欄位的 {lang} 字幕…\n")

    hits, no_subs, flagged_ok, gaps = 0, 0, 0, []
    seen: dict[str, str | None] = {}

    for v in vids:
        vid = re.search(r"(?:v=|youtu\.be/)([\w-]{11})", v["url"]).group(1)
        if vid not in seen:
            seen[vid] = fetch(vid, lang)
            time.sleep(0.6)  # 連續抓會撞 429
        text = seen[vid]
        if not text:
            no_subs += 1
            continue

        found = [
            label
            for label, pats in CLAIMS.items()
            if any(re.search(p, text, re.I) for p in pats)
        ]
        if not found:
            continue
        hits += 1
        if v.get("claim_boundary"):
            flagged_ok += 1
            if only_missing:
                continue
            mark = "✓ 已標註"
        else:
            gaps.append((v["unit"], v.get("channel"), found))
            mark = "✗ 未標註"
        print(f"{mark}  {v['unit']:9} {str(v.get('channel'))[:22]:24} {'、'.join(found)}")
        print(f"          {(v.get('name') or v.get('title') or '')[:70]}")

    print(f"\n{'=' * 60}")
    print(f"有字幕可查      {len(seen) - sum(1 for t in seen.values() if not t)}/{len(seen)} 支")
    print(f"沒有字幕        {sum(1 for t in seen.values() if not t)} 支（無從查核）")
    print(f"說了誇大宣稱    {hits} 個欄位")
    print(f"  已標 claim_boundary  {flagged_ok}")
    print(f"  ✗ 未標（策展缺口）    {len(gaps)}")
    return 1 if gaps else 0


def main() -> int:
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return 2

    lang = "en"
    if "--lang" in args:
        i = args.index("--lang")
        lang = args[i + 1]
        del args[i : i + 2]
    only_missing = "--missing" in args
    args = [a for a in args if a != "--missing"]

    if args[0] == "get":
        text = fetch(args[1], lang)
        if not text:
            return 1
        print(text)
        return 0
    if args[0] == "scan":
        return scan(lang, only_missing)

    print(__doc__)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
