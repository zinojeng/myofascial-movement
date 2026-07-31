#!/usr/bin/env python3
"""身體區域的正規化與分組。

這門課的分面不是肌群而是**區域**——理由寫在 CH1：筋膜是連續的結締組織系統，
把一支影片標成「只練股二頭肌」會強化「一條一條分開處理」的錯誤心像。
標到區域這一層，剛好對應課程的實作流程（自我評估 → 低強度輸入 → 主動活動 →
負荷整合 → 再評估），也是讀者在找內容時真正會用的詞。

比對規則：關鍵字出現在傳入的任何一段文字裡即命中。關鍵字刻意寫長
（用「大腿後側」而不是「腿後」），因為「小腿後側肌群」會誤中短關鍵字。
"""

from __future__ import annotations

# 標準區域名 -> 觸發關鍵字。順序即輸出順序（由遠端到近端、由下到上）。
REGIONS: dict[str, list[str]] = {
    "足底與踝部": [
        "足底", "足弓", "腳底", "腳掌", "蹠", "拇趾", "腳趾", "足踝", "踝關節",
        "背屈", "蹠屈", "跟腱", "阿基里斯", "舟狀骨", "內外翻",
        "plantar", "foot", "ankle", "achilles", "toe", "arch",
    ],
    "小腿": [
        "小腿", "腓腸肌", "比目魚肌", "脛前肌", "脛後肌", "腓骨肌", "小腿三頭",
        "calf", "gastroc", "soleus", "tibialis", "shin",
    ],
    "膝與大腿": [
        "大腿", "膝關節", "膝蓋", "髕", "股四頭", "股直肌", "股外側", "股內側",
        "大腿後側", "腿後肌群", "膕旁", "膕窩", "內收肌", "髂脛束",
        "knee", "quad", "hamstring", "adductor", "it band", "itb", "thigh",
    ],
    "髖與骨盆": [
        "髖", "臀大肌", "臀中肌", "臀小肌", "臀部", "屁股", "骨盆", "梨狀肌",
        "髂腰肌", "腰大肌", "闊筋膜張肌", "鼠蹊", "腹股溝", "深層外旋",
        "hip", "glute", "pelvi", "piriformis", "psoas", "tfl", "groin",
    ],
    "腰背": [
        "腰椎", "下背", "腰部", "腰方肌", "胸腰筋膜", "豎脊肌", "多裂肌", "背部肌群",
        "脊椎伸展", "捲脊", "腰薦",
        "lumbar", "low back", "thoracolumbar", "erector", "multifidus", "quadratus",
    ],
    "胸廓": [
        "胸椎", "胸廓", "肋骨", "肋間", "橫膈", "呼吸", "吐氣", "吸氣", "胸大肌",
        "胸小肌", "前胸",
        "thoracic", "rib", "diaphragm", "breath", "pec ", "pectoral",
    ],
    "肩胛與肩部": [
        "肩胛", "肩關節", "肩膀", "肩袖", "旋轉肌", "背闊肌", "闊背肌", "三角肌",
        "斜方肌", "前鋸肌", "菱形肌", "上背", "手臂", "前臂", "肱二頭", "肱三頭",
        "shoulder", "scapul", "rotator cuff", "lat ", "latissimus", "deltoid",
        "trapezius", "serratus", "forearm",
    ],
    "頸部": [
        "頸椎", "頸部", "脖子", "枕下", "胸鎖乳突", "頸深屈", "肩頸",
        "neck", "cervical", "suboccipital", "scm",
    ],
    "全身整合": [
        "全身", "整合流程", "全身性", "後側鏈", "前側鏈", "動力鏈", "串聯",
        "full body", "whole body", "posterior chain", "anterior chain", "flow",
    ],
}

# 側欄的分組順序
GROUPS: list[str] = ["下肢", "軀幹", "上肢與頸部", "全身"]

GROUP_OF: dict[str, str] = {
    "足底與踝部": "下肢",
    "小腿": "下肢",
    "膝與大腿": "下肢",
    "髖與骨盆": "下肢",
    "腰背": "軀幹",
    "胸廓": "軀幹",
    "肩胛與肩部": "上肢與頸部",
    "頸部": "上肢與頸部",
    "全身整合": "全身",
}

_LOOKUP: list[tuple[str, str]] = [
    (kw.lower(), region) for region, kws in REGIONS.items() for kw in kws
]


def canonical(text: str | None) -> list[str]:
    """一段文字裡出現的所有區域（保持 REGIONS 的宣告順序）。"""
    if not text:
        return []
    hay = text.lower()
    hit = {region for kw, region in _LOOKUP if kw in hay}
    return [r for r in REGIONS if r in hit]


def extract(*texts: str | None) -> list[str]:
    """從任意數量的描述字串中抽出去重後的區域名（保持出現順序）。"""
    out: list[str] = []
    for text in texts:
        for region in canonical(text):
            if region not in out:
                out.append(region)
    return out
