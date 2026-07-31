# 策展規格書：筋膜與動作整合

這份文件是所有策展與實證 agent 的共同依據。**開工前整份讀完。**

---

## 0. 鐵則（違反任何一條，整份產出作廢）

1. **策展不是生成。** video id 一律取自 `src/build/ytsearch.py` 的實際輸出，
   PMID 一律取自 `src/build/pubmed.py` 的實際輸出。憑印象拼出一個看起來合理的
   11 碼 id 或 8 碼 PMID，比留空糟一百倍——它會通過肉眼檢查，然後在讀者面前 404。
2. **留空要說明。** 找不到合格影片就 `"url": null` 並寫 `"note"`，說明你查了哪些關鍵字、
   為什麼那些結果不合格。留空但沒有 note 會被 `make audit` 擋下。
3. **不信任任何上游宣稱**，包括你自己三十秒前說「已驗證」的那一句。
4. **誠實比好看重要。** 查證結果對筋膜訓練不利就照實寫，標成 `contested` 或 `limited`。
   這門課的賣點就是它不賣承諾。

## 1. 課程立場（每一段文案都要守住）

這門課的核心不是「筋膜很神奇」，也不是「筋膜是騙局」，而是把每個主張拆成三層：

1. **做了之後可能有什麼效果？**（短期活動度、痠痛感受、主觀恢復、壓痛耐受）
2. **效果是不是筋膜本身造成的？**（機轉可能是疼痛耐受、神經調節、溫度血流、
   組織黏彈性、對伸展刺激的耐受度提高——**觀察到的效果不等於已證明的機轉**）
3. **它有沒有比其他方法更好？**（長期活動度上滾筒與靜態伸展效果相近，
   所以不能宣稱滾筒是唯一或必然較好的方法）

禁止出現的說法：「把沾黏壓開」「把筋膜拉開」「排出乳酸」「調整筋膜線」
——除非是在 CH2 的迷思查核裡當成被檢驗的對象引述。

寫「緊」的時候要留意：緊不一定代表組織縮短，壓痛不一定等於損傷。

## 2. 工具

```bash
# 找影片（唯一合法的 video id 來源）
uv run python src/build/ytsearch.py "<查詢字串>" 10 --min 0:40 --max 12:00
uv run python src/build/ytsearch.py "<查詢字串>" 10 --json

# 找文獻（唯一合法的 PMID 來源）
uv run python src/build/pubmed.py search "<query>" 12
uv run python src/build/pubmed.py abs <PMID> [<PMID> ...]
```

搜尋要點：

- 中文查詢用繁體，補打簡體與英文各一次，三種寫法的結果差很多。
- 好用的中文頻道：啾c物理治療師、物理治療師 Wilson、Hunter 物理治療所、
  生生優動、練健康 LKK Wellness、Coach Hank、一分鐘健身教室、CYFIT兆佑。
  好用的英文頻道：Physiotutors、E3 Rehab、Squat University、Precision Movement、
  Tom Merrick、GMB Fitness、Jeff Nippard、Bob & Brad、Upright Health。
- **先搜尋再決定單元要放什麼**，不要先想好動作再硬找影片。
- 觀看數低於 3,000 的會被稽核警告，盡量避開（但有品質的小頻道可以留，
  在 `why` 說明為什麼值得）。

## 3. 章節與配額（**數字必須完全相符，差一支建置就失敗**）

| 章節 | 檔案 | 單元 | 項目 | unit type |
|---|---|---:|---:|---|
| CH0 課程使用方式與安全界線 | `ch0.json` | 1 | 0 | `guide` |
| CH1 什麼是筋膜與筋膜系統 | `ch1-2.json` | 4 | 0 | `concept` |
| CH2 筋膜常見說法與科學爭議 | `ch1-2.json` | 4 | 0 | `myth` |
| CH3 自我筋膜放鬆與工具使用 | `ch3.json` | 4 | 24 | `practice` |
| CH4 活動度、伸展與主動控制 | `ch4.json` | 4 | 24 | `practice` |
| CH5 彈性回彈與負荷適應 | `ch5.json` | 3 | 15 | `practice` |
| CH6 足部、下肢與後側鏈 | `ch6.json` | 3 | 18 | `practice` |
| CH7 骨盆、軀幹、胸廓與肩頸 | `ch7.json` | 3 | 18 | `practice` |
| CH8 日常與運動課表整合 | `ch8.json` | 1 | 6 | `program` |

合計 27 個單元、105 支示範影片、132 個影片欄位。
**每個實作單元的項目數固定 6 支**（CH5 為 5 支），稽核允許區間是 5–8。

### 單元清單（id 與主題已定，不要自己改）

**CH0** — `ch0-u1` 這門課怎麼用，以及什麼時候該停下來就醫

**CH1**
- `ch1-u1` Fascia 與 fascial system：為什麼定義到現在還在吵
- `ch1-u2` 淺筋膜、深筋膜、肌內結締組織與肌腱：層次與連續性
- `ch1-u3` 筋膜的三個功能：感覺、力量傳遞與滑動
- `ch1-u4` 為什麼筋膜、肌肉、神經與關節不能分開討論

**CH2**（這一章是網站的「立場」頁）
- `ch2-u1` 滾筒真的能把沾黏「壓開」嗎？
- `ch2-u2` 肌肉結與 trigger point 到底是什麼？
- `ch2-u3` 筋膜鏈是不是確定存在？
- `ch2-u4` 姿勢不良、代償與疼痛之間有直接因果嗎？

**CH3**
- `ch3-u1` Foam roller：壓力、時間與節奏怎麼抓
- `ch3-u2` 按摩球：局部加壓與壓痛點處理
- `ch3-u3` 按摩槍與震動滾筒：強度與禁區
- `ch3-u4` 訓練前、訓練後與休息日該怎麼安排

**CH4**
- `ch4-u1` 靜態伸展：劑量、時機與它真正改變的東西
- `ch4-u2` 動態活動度與暖身
- `ch4-u3` 主動活動度與末端控制
- `ch4-u4` 負重活動度：把「拉得開」變成「用得到」

**CH5**
- `ch5-u1` 伸展－收縮循環：彈性回彈是怎麼回事
- `ch5-u2` 跳躍與落地：從雙腳到單腳
- `ch5-u3` 漸進負荷與結締組織的適應時間

**CH6**
- `ch6-u1` 足底與小腿
- `ch6-u2` 大腿後側與後側鏈
- `ch6-u3` 臀部與髖部

**CH7**
- `ch7-u1` 胸腰筋膜與軀幹
- `ch7-u2` 胸廓、呼吸與肩胛
- `ch7-u3` 頸肩區域

**CH8**
- `ch8-u1` 四種入口：久坐 10 分鐘、運動前 8 分鐘、運動後 10 分鐘、每週兩次 30 分鐘

## 4. 資料格式

一章一檔放在 `course/data/`。單章檔：

```jsonc
{
  "chapter": "CH3",
  "title": "自我筋膜放鬆與工具使用",
  "units": [ /* ... */ ]
}
```

一檔多章（只有 `ch1-2.json` 是這種）：

```jsonc
{ "chapters": [ { "chapter": "CH1", "title": "…", "units": [...] },
                { "chapter": "CH2", "title": "…", "units": [...] } ] }
```

單元：

```jsonc
{
  "id": "ch3-u1",
  "name": "Foam roller：壓力、時間與節奏怎麼抓",
  "type": "practice",
  "assessment": "至少 80 字的**可操作**自我檢核……",
  "tight": ["常見主訴部位1", "常見主訴部位2"],
  "weak": ["需要一起練的動作能力1", "…"],
  "lesson": {
    "title": "搜尋結果裡的實際標題",
    "channel": "實際頻道名",
    "url": "https://www.youtube.com/watch?v=<實際11碼id>",
    "duration": "10:20",
    "why": "為什麼選這支，以及它哪一段說法需要保留或修正"
  },
  "drills": [
    {
      "name": "小腿滾筒基礎操作",
      "en": "Calf Foam Rolling",
      "kind": "release",
      "target": "小腿三頭肌、跟腱",
      "dose": "每區 30–60 秒，壓力控制在可以正常呼吸、疼痛不超過 6/10；停止條件：出現麻、刺、放射痛立即停",
      "title": "搜尋結果裡的實際標題",
      "channel": "實際頻道名",
      "url": "https://www.youtube.com/watch?v=<實際11碼id>",
      "duration": "3:57"
    }
  ]
}
```

### 欄位規則

- `type` — 照第 3 節的表格填，只能是 `guide` / `concept` / `myth` / `practice` / `program`。
- `assessment` — **必填且至少 80 字**。要寫成讀者今天就能做的動作：量什麼、
  怎麼判讀、什麼數字算通過。觀念與迷思單元則寫成「看完後你應該能回答……」的自我提問。
- `tight` / `weak` — 各 2–6 個詞。`tight` 寫**常見主訴部位**（「小腿後側緊繃」），
  `weak` 寫**需要一起練的動作能力**（「踝背屈範圍」「單腳負重控制」）。
  這兩欄餵給區域分面，所以用得到部位詞（足底、小腿、髖、胸廓、頸部……）。
  概念與迷思單元填 `[]`。
- `kind` — 只能是 `assess`（自我評估）/ `release`（放鬆、自我按摩）/
  `move`（主動活動）/ `load`（負荷整合）。
- `target` — 部位或肌群，用「、」分隔。這欄跟 `name` 一起餵給區域分面，**必填**。
- `dose` — **必填**，而且必須包含：時間或次數、壓力或強度、**停止條件**。
  這是這門課的安全承諾，寫「放鬆 1 分鐘」不合格。
- `duration` — 抄 `ytsearch.py` 輸出的長度。誤差超過 30 秒會被稽核抓到
  （之後 `make meta` 會用真實值覆寫，但先抄對）。
- `why` — 每堂主課必填，寫選片理由；如果那支影片有講錯的地方（例如講「壓開沾黏」），
  在這裡直接指出來，不要粉飾。
- 同一單元內不可出現重複的 url，也不可出現重複的 `name`。

### 項目編排：每個實作單元都走同一套流程

單元裡的 6 支影片依序大致對應：

> 自我評估（`assess`）→ 低強度輸入（`release`）→ 主動活動（`move`）→ 負荷整合（`load`）→ 再評估

不必每個單元都四種都有——CH3 以 `release` 為主、CH4 以 `move` 為主、
CH5 以 `load` 為主，CH6/CH7 每個區域則盡量四種都出現。

## 5. 實證資料（實證 agent 專用）

### 單元層級 `course/data/oe-<x>.json`

```jsonc
{
  "conditions": [
    {
      "unit": "ch3-u1",              // 或 concept-1 / concept-2 / concept-3
      "name": "滾筒與自我筋膜放鬆",
      "evidence_grade": "moderate",   // strong / moderate / limited / contested
      "summary": "300–600 字，先講觀察到的效果，再講機轉的不確定性，最後講跟其他方法比。",
      "mechanism": "可能的機轉有哪些，以及每個機轉各自的證據強度。",
      "certainty": "機轉的確定程度——這欄要誠實，多數情況答案是「低」。",
      "acute_rom": "對短期（單次介入後數分鐘至一小時）活動度的效果，附效果量。",
      "chronic_rom": "對長期（數週訓練後）活動度的效果，並與靜態伸展比較。",
      "pain_effect": "對疼痛、延遲性痠痛與壓痛耐受的效果。",
      "performance": "對最大肌力、爆發力與運動表現的效果（多數是「沒有明顯損害」）。",
      "red_flags": ["……", "……"],     // 陣列，3–6 條，寫成讀者能自我判斷的句子
      "caveats": "這個主題必須對讀者誠實告知的限制。"
    }
  ]
}
```

### 類別層級 `course/data/drill-evidence-<n>.json`

```jsonc
{
  "categories": [
    {
      "id": "foam-roll",                    // 必須是 taxonomy/methods.py 裡的 id
      "name": "滾筒與自我筋膜放鬆",
      "evidence_grade": "moderate",
      "summary": "200–400 字。",
      "citations": [                        // **至少 2 篇**，目標 3 篇
        {
          "pmid": "35616852",
          "title": "抄 pubmed.py 回傳的完整標題",
          "journal": "Sports Med",
          "year": 2022,
          "design": "systematic-review",     // 或 meta-analysis / rct / crossover / cadaveric / narrative-review
          "takeaway": "這篇實際上發現了什麼，含數字。不要寫成摘要的中文版。"
        }
      ]
    }
  ]
}
```

`taxonomy/methods.py` 目前定義的類別 id：
`rom-self-test` `massage-gun` `massage-ball` `foam-roll` `assisted-stretch`
`static-stretch` `dynamic-mobility` `active-control` `breathing`
`plyometric` `loaded-mobility`

### red_flags 的共同底線（每個單元至少涵蓋其中相關的幾條）

- 新發生或進行性的肌力下降
- 麻木、刺痛或其他感覺異常
- 急性外傷後的腫脹、變形或無法承重
- 夜間或休息時仍持續惡化的疼痛
- 關節明顯腫脹、發熱、發紅
- 發燒或不明原因體重下降等全身性症狀
- 深層靜脈栓塞風險（單側小腿腫脹、發熱、壓痛）——**絕對不要滾壓**
- 抗凝血劑使用、骨質疏鬆、皮膚傷口或感染部位

## 6. 交付前自我檢查

- [ ] 每個 video id 都能在你自己跑過的 `ytsearch.py` 輸出裡找到
- [ ] 每個 PMID 都能在你自己跑過的 `pubmed.py` 輸出裡找到
- [ ] 單元數與項目數跟第 3 節的表格完全相符
- [ ] 每個 `dose` 都有時間／強度／停止條件三件事
- [ ] 每個 `assessment` 都超過 80 字且可操作
- [ ] 同一單元內沒有重複的 url 或 name
- [ ] 檔案是合法 JSON（存檔後用 `python3 -m json.tool` 確認一次）
