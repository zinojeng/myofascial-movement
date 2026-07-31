#!/usr/bin/env python3
"""介入方法的分類。

上百支示範影片其實只有十種介入原型。單一動作（例如「小腿滾筒」）沒有專屬文獻，
但它所屬的方法（「滾筒／自我筋膜放鬆」）有一整批系統性回顧。文獻掛在方法上
才站得住腳——這也是這門課刻意不用「肌群」當分類軸的原因：文獻是按介入分的，
不是按肌肉分的。

比對規則：patterns 內任一關鍵字出現在 動作中文名 / 英文名 / target / 影片標題 即命中。
先在同 kind 內比對，避免「伸展」類關鍵字誤抓負荷整合動作。
"""

from __future__ import annotations

import re

# (id, 顯示名稱, kind, 比對關鍵字)
CATEGORIES: list[tuple[str, str, str, list[str]]] = [
    # ---------------- 自我評估 ----------------
    (
        "rom-self-test",
        "關節活動度自我檢測",
        "assess",
        [
            "檢測", "測試", "自我評估", "量測", "再評估", "基準值",
            "Knee to Wall", "貼牆", "Sit and Reach", "坐姿體前彎", "指地",
            "Thomas Test", "湯瑪士", "FABER", "90/90", "背後互扣",
            "Test", "Screen", "Assessment", "Measure",
        ],
    ),
    # ---------------- 放鬆／自我按摩 ----------------
    (
        "massage-gun",
        "按摩槍與局部震動",
        "release",
        [
            "按摩槍", "筋膜槍", "震動", "振動", "vibration", "percussive",
            "massage gun", "theragun", "hypervolt",
        ],
    ),
    (
        "massage-ball",
        "按摩球與局部加壓",
        "release",
        [
            "按摩球", "花生球", "筋膜球", "網球", "壓痛點", "激痛點", "trigger point",
            "massage ball", "lacrosse ball", "peanut", "ischemic compression",
            "缺血性加壓", "定點加壓",
        ],
    ),
    (
        "foam-roll",
        "滾筒與自我筋膜放鬆",
        "release",
        [
            "滾筒", "滾桶", "泡棉軸", "泡沫軸", "自我筋膜放鬆", "SMR",
            "foam roll", "foam roller", "self-myofascial", "rolling",
        ],
    ),
    (
        "assisted-stretch",
        "輔助與被動伸展",
        "release",
        [
            "被動伸展", "彈力帶伸展", "毛巾伸展", "牆面伸展", "夥伴伸展",
            "passive stretch", "assisted stretch", "strap stretch",
        ],
    ),
    # ---------------- 主動活動 ----------------
    (
        "static-stretch",
        "靜態伸展",
        "move",
        [
            "靜態伸展", "靜態拉筋", "持續伸展", "維持 30", "維持30",
            "static stretch", "hold stretch", "PNF", "本體感覺神經肌肉promotion",
            "收縮放鬆", "contract-relax",
        ],
    ),
    (
        "dynamic-mobility",
        "動態活動度",
        "move",
        [
            "動態伸展", "動態活動", "動態暖身", "擺盪", "繞環", "翻書", "貓牛",
            "Open Book", "Cat Cow", "World's Greatest", "Leg Swing", "Arm Circle",
            "dynamic stretch", "dynamic warm", "mobility flow", "CARs",
        ],
    ),
    (
        "active-control",
        "主動活動度與動作控制",
        "move",
        [
            "主動活動度", "主動控制", "末端control", "末端控制", "離心控制",
            "動作控制", "分節", "分離", "穩定", "啟動",
            "active range", "motor control", "isometric hold", "end range",
            "segmental", "activation", "PAILs", "RAILs",
        ],
    ),
    (
        "breathing",
        "呼吸與胸廓活動",
        "move",
        [
            "呼吸", "吐氣", "吸氣", "橫膈", "肋廓擴張", "腹式", "90/90 呼吸",
            "breath", "diaphragm", "rib expansion", "belly breathing",
        ],
    ),
    # ---------------- 負荷整合 ----------------
    (
        "plyometric",
        "彈跳與伸展－收縮循環",
        "load",
        [
            "跳", "彈跳", "落地", "彈振", "反彈", "跳繩", "單腳跳", "跨步跳",
            "增強式", "牽張收縮", "伸展收縮",
            "plyometric", "jump", "hop", "bound", "landing", "SSC",
            "stretch-shortening", "pogo",
        ],
    ),
    (
        "loaded-mobility",
        "負重活動度與離心負荷",
        "load",
        [
            "負重", "負荷", "離心", "加重", "壺鈴", "啞鈴", "槓鈴", "彈力帶阻力",
            "深蹲", "硬舉", "分腿蹲", "臀橋", "橋式", "提踵", "羅馬尼亞",
            "Loaded", "eccentric", "Squat", "Deadlift", "Lunge", "Bridge",
            "Calf Raise", "Nordic", "Copenhagen", "Jefferson",
        ],
    ),
]


def _match(patterns: list[str], haystack: str) -> bool:
    for p in patterns:
        if (
            re.search(p, haystack, re.I)
            if any(c in p for c in ".*+?[]")
            else p.lower() in haystack.lower()
        ):
            return True
    return False


def classify(drill: dict) -> str | None:
    """回傳這個項目所屬的介入方法 id。"""
    hay = " ".join(str(drill.get(k) or "") for k in ("name", "en", "target", "title"))
    kind = drill.get("kind")
    # 先在同 kind 內找，避免「伸展」類關鍵字誤抓負荷整合動作
    for cid, _, ck, pats in CATEGORIES:
        if ck == kind and _match(pats, hay):
            return cid
    for cid, _, ck, pats in CATEGORIES:
        if ck != kind and _match(pats, hay):
            return cid
    return None


NAMES = {cid: name for cid, name, _, _ in CATEGORIES}
KINDS = {cid: kind for cid, _, kind, _ in CATEGORIES}
