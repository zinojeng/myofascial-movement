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

`scan` 把「影片逐字稿裡出現過禁用說法」的片子挑出來，**附上前後文**，
讓人判讀那句話是在**主張**還是在**反駁**。

**它不會告訴你哪裡有缺口，只會把要看的東西從一百多支縮到幾支。**
實測過：第一版直接把命中當成缺口，結果六個命中全是假陽性——
Physiotutors 那支片名就叫 *The (Non)Sense of Foam Rolling and Breaking Up
Adhesions*，講的正是這說法不成立。純字串比對永遠分不出引述與背書，
所以最後那一步必須是人。

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
        # 只比對筋膜。「lengthen the muscle」是離心收縮的正確描述，
        # 把它列為誇大宣稱會把講對的人一起抓進來。
        r"lengthen(?:ing)? (?:the )?fascia",
        r"stretch(?:ing)? out (?:the )?fascia",
        r"make (?:the |your )?fascia longer",
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

        lines = text.splitlines()
        found: list[tuple[str, str]] = []
        for label, pats in CLAIMS.items():
            for pat in pats:
                for i, ln in enumerate(lines):
                    if re.search(pat, ln, re.I):
                        ctx = " ".join(lines[max(0, i - 1) : i + 3])
                        found.append((label, ctx[:200]))
                        break
                else:
                    continue
                break
        if not found:
            continue
        hits += 1
        has_note = bool(v.get("claim_boundary"))
        flagged_ok += has_note
        if only_missing and has_note:
            continue
        mark = "已標 claim_boundary" if has_note else "未標 claim_boundary"
        print(f"● {v['unit']:9} {str(v.get('channel'))[:22]:24} [{mark}]")
        print(f"  {(v.get('name') or v.get('title') or '')[:74]}")
        for label, ctx in found:
            print(f"    ⟨{label}⟩ …{ctx}…")
        print()
        if not has_note:
            gaps.append((v["unit"], v.get("channel"), [f for f, _ in found]))

    print("=" * 66)
    print(f"有 {lang} 字幕可查   {len(seen) - sum(1 for t in seen.values() if not t)}/{len(seen)} 支")
    print(f"沒有字幕         {sum(1 for t in seen.values() if not t)} 支（這個語言無從查核）")
    print(f"逐字稿出現禁用說法  {hits} 支（已標 {flagged_ok} / 未標 {len(gaps)}）")
    print()
    print("↑ 這是**待人工判讀**的清單，不是缺口清單。")
    print("  純字串比對分不出「主張」與「反駁」——反駁這些說法的影片同樣會命中，")
    print("  而那正是這門課最想收的內容。請看上面的前後文自行判斷。")
    return 0


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
