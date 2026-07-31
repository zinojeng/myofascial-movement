#!/usr/bin/env python3
"""介入方法的分類。

上百支示範影片其實只有十一種介入原型。單一動作（例如「小腿滾筒」）沒有專屬文獻，
但它所屬的方法（「滾筒與自我筋膜放鬆」）有一整批系統性回顧。文獻掛在方法上
才站得住腳——這也是這門課刻意不用「肌群」當分類軸的原因：文獻是按介入分的，
不是按肌肉分的。

比對規則：
1. 先只看策展者自己寫的欄位（name / en / target），再退而求其次看 YouTube 標題。
   標題是別人寫的，常塞滿與該動作無關的關鍵字（「…改善駝背和肩頸痠痛！」），
   拿它當第一順位會把分類帶偏。
2. 每一輪都先在同 kind 內比對，再跨 kind——避免「伸展」類關鍵字誤抓負荷整合動作。
3. CATEGORIES 由特異到通用排序，先命中者勝。所以 `static-stretch` 的通用關鍵字
   「伸展」放在最後，讓 `active-control`、`dynamic-mobility` 有機會先認領。
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
            "檢測", "測試", "自我評估", "自我測量", "量測", "再評估", "基準值", "測你的",
            "Knee to Wall", "Knee-to-Wall", "膝碰牆", "貼牆", "牆壁測試",
            "品質", "十項", "Qualitative", "Screen", "判讀",
            "Sit and Reach", "坐姿體前彎", "指地", "抬腿", "Straight Leg Raise",
            "Thomas Test", "湯瑪士", "FABER", "90/90", "背後互扣", "有沒有用",
            "Test", "Screen", "Assessment", "Measure", "FMS",
        ],
    ),
    # ---------------- 放鬆／自我按摩（工具施加壓力）----------------
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
            "缺血性加壓", "定點加壓", "按壓", "加壓", "指壓", "要不要壓",
            "自我按摩", "低強度處理", "Self-Massage", "Self Massage",
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
    # ---------------- 主動活動 ----------------
    (
        "breathing",
        "呼吸與胸廓活動",
        "move",
        [
            "呼吸", "吐氣", "吸氣", "橫膈", "肋廓擴張", "腹式",
            "breath", "diaphragm", "rib expansion",
        ],
    ),
    (
        "active-control",
        "主動活動度與動作控制",
        "move",
        [
            "主動", "控制", "末端", "離心控制", "分節", "分離", "穩定", "啟動",
            "鳥狗", "Bird Dog", "Bird-Dog", "死蟲", "Dead Bug",
            "active range", "motor control", "isometric hold", "end range",
            "segmental", "activation", "PAILs", "RAILs", "CARs",
            "滑動", "神經滑動", "Glide", "爬", "Crawl", "側走", "Side Step",
            "抵牆", "Wall-Braced",
        ],
    ),
    (
        "assisted-stretch",
        "輔助與被動伸展",
        "move",
        [
            "門框", "門邊", "牆面伸展", "毛巾伸展", "彈力帶伸展", "夥伴", "他人協助",
            "被動伸展", "收縮放鬆", "contract-relax", "hold-relax", "PNF",
            "passive stretch", "assisted stretch", "strap stretch", "partner stretch",
        ],
    ),
    (
        "dynamic-mobility",
        "動態活動度",
        "move",
        [
            "動態伸展", "動態活動", "動態暖身", "擺盪", "繞環", "翻書", "貓牛",
            "活動度流程", "活動度課表", "活動度組合", "暖身流程",
            "Open Book", "Cat Cow", "World's Greatest", "Leg Swing", "Arm Circle",
            "dynamic stretch", "dynamic warm", "mobility flow", "mobility routine",
            "Mobility", "Warm Up",
        ],
    ),
    (
        "static-stretch",
        "靜態伸展",
        "move",
        [
            "靜態伸展", "靜態拉筋", "持續伸展", "伸展", "拉筋", "牽張",
            "static stretch", "hold stretch", "stretch",
        ],
    ),
    # ---------------- 負荷整合 ----------------
    (
        "plyometric",
        "彈跳與伸展－收縮循環",
        "load",
        [
            "彈跳", "落地", "彈振", "反彈", "跳繩", "單腳跳", "跨步跳", "跳躍", "起跳",
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
            "負重", "負荷", "離心", "加重", "等長", "壺鈴", "啞鈴", "槓鈴", "彈力帶阻力",
            "深蹲", "硬舉", "分腿蹲", "臀橋", "橋式", "提踵", "羅馬尼亞", "彎舉", "推舉",
            "肌力訓練", "阻力訓練", "抬舉", "投擲", "收膝", "側棒", "landmine", "肌訓練",
            "Strengthening", "Raise", "Throw", "Plank", "Press",
            "Loaded", "eccentric", "isometric", "Squat", "Deadlift", "Lunge", "Bridge",
            "Calf Raise", "Nordic", "Copenhagen", "Jefferson", "Pallof",
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
    kind = drill.get("kind")
    curated = " ".join(str(drill.get(k) or "") for k in ("name", "en", "target"))
    title = str(drill.get("title") or "")

    # 策展欄位優先，YouTube 標題只當退路——標題常塞無關關鍵字
    for hay in (curated, title):
        for cid, _, ck, pats in CATEGORIES:
            if ck == kind and _match(pats, hay):
                return cid
        for cid, _, ck, pats in CATEGORIES:
            if ck != kind and _match(pats, hay):
                return cid
    return None


NAMES = {cid: name for cid, name, _, _ in CATEGORIES}
KINDS = {cid: kind for cid, _, kind, _ in CATEGORIES}
