# CH9 規格書：筋膜線的臨床觀察與訓練應用

這一章處理一個尷尬但真實的情況：**手臂線、螺旋線、側線、前線的解剖驗證最弱，
但它們在教學現場最常被拿來組織課表。** 這門課的立場不是「沒證據就不談」，
而是把它放在正確的位置上談。

---

## 1. 先看我們自己查證出來的數字

`oe-a.json` 的 `concept-2`（對應 CH2-u3）已經逐線列出解剖驗證結果，
新內容**必須與它一致，不可互相矛盾**。62 篇人體解剖研究的系統性回顧
（PMID 26281953）逐一驗證 Myers 六條經線的轉換點：

| 線 | 轉換點驗證 | 力傳遞證據 |
|---|---|---|
| 後表線 | **3/3**（14 篇） | 三個轉換點有中等證據 |
| 後功能線 | **3/3**（8 篇） | 兩個中的一個有中等證據 |
| 前功能線 | **2/2**（6 篇） | 只有一篇，輕微且未達顯著 |
| **螺旋線** | **5/9**（21 篇） | 未被單獨檢驗 |
| **側線** | **2/5**（10 篇） | 未被單獨檢驗 |
| **前表線** | **0/7** | 無 |
| **手臂線** | 未納入該回顧 | 無 |

**這一章負責的四條，正好是表格下半部那些。** 這不是巧合，也不該被淡化——
它應該是這一章的開場白。

另一個必須帶到的反證：94 人的 RCT 把後表線切成五段各滾 10 分鐘，
**每一段都能改善大腿後側柔軟度與踝背屈，連滾頭皮都可以**（PMID 34886078）。
如果按頭皮也有效，效果就不像沿著特定的線傳遞。

## 2. 這一章的核心命題

> **旋轉、側向、前側鏈的訓練值得做——但它們值得做的理由，
> 不是「那條線被證實存在」。**

多平面動作、抗旋轉、額狀面控制、前側鏈離心負荷，這些本來就是有價值的訓練內容。
筋膜線是一個**方便的教學組織方式**（coaching heuristic），讓教練把散落的動作
串成有邏輯的順序，不是一個已被證實的解剖機轉。

所以每個單元都要能同時說出這兩句話而不打架：

1. 「這條線的解剖驗證是 X/Y，力傳遞證據 Z」——誠實的科學狀態
2. 「但這組動作值得練，因為它們訓練的是 ○○○」——不依賴那條線成立的理由

**禁止**出現的說法：調整螺旋線、把側線打開、釋放手臂線、沿著筋膜線放鬆、
「因為它們連在一起所以要一起練」。

## 3. 四個單元

| id | 主題 | 對應的訓練內容 |
|---|---|---|
| `ch9-u1` | 手臂線：上肢負荷傳遞與肩帶連結 | 肩帶穩定、闊背與胸腰筋膜的負荷、懸吊與推拉、握力與前臂 |
| `ch9-u2` | 螺旋線：旋轉、反旋轉與交叉步態 | 抗旋轉、投擲與揮擊、對側手腳協調、胸椎旋轉與髖分離 |
| `ch9-u3` | 側線：額狀面穩定與側向負荷 | 單腳站立、側棒、側向位移、髖外展控制、負重行走 |
| `ch9-u4` | 前線：淺前線與深前線 | 前側鏈離心、髖屈肌與腹部、橫膈與腰肌、骨盆底與呼吸連動 |

`ch9-u4` 刻意同時涵蓋**淺前線**（解剖驗證 0/7，最弱）與**深前線**
（臨床上最常被討論，橫膈、腰大肌、骨盆底），因為兩者常被混為一談。

每個單元 **1 堂主課 + 6 支示範**，型別 `practice`。

## 4. 示範影片的編排

沿用全課的流程，每單元 6 支大致依序：

> 自我評估（`assess`）→ 低強度輸入（`release`）→ 主動活動（`move`）→ 負荷整合（`load`）

但這一章的重心要**明顯偏向 `load` 與 `move`**（建議 assess 1 / release 1 /
move 2 / load 2）。理由：這四條線的價值主張在「訓練」不在「放鬆」——
如果一章講螺旋線卻塞滿滾筒，等於用行動承認我們相信「沿線放鬆」那套。

這也順帶修正全課的內容配比：目前 `demo` 只佔 14%（目標 30%），
這一章的示範影片會把它拉回來。

## 5. 實證欄位（`oe-e.json`）

四個 condition：`ch9-u1` `ch9-u2` `ch9-u3` `ch9-u4`，欄位定義同
[`dual-axis-brief.md`](dual-axis-brief.md) 第 5 節。

**`evidence_grade` 這一章要用到目前為止全課沒用過的兩級**，這正是它們存在的理由：

- `expert-consensus` **專家共識** — 沒有直接試驗，但專業社群做法高度一致。
  例如「訓練旋轉能力要同時練抗旋轉」在教練與治療圈幾乎沒有爭議。
- `experience` **經驗性主張** — 來自長期教學觀察，尚無研究檢驗。
  例如「側線緊繃的人單腳站立時骨盆會掉」這類觀察。

把它們標成 `limited` 是錯的——那會讓讀者以為有人做過研究但結果不好。
真實情況是**根本沒人做過那個研究**，而臨床上仍有一致做法。

`certainty` 欄位要特別誠實：這一章多數條目的機轉確定程度是「低」。

`caveats` 必須寫出這一章最重要的那句話：**這些動作的訓練效益不依賴筋膜線假說成立。**

引用方向：myofascial chains anatomical continuity、anatomy trains systematic review、
myofascial force transmission in vivo、latissimus dorsi thoracolumbar fascia load、
anti-rotation core training、rotational power training transfer、
frontal plane control single leg、hip abductor strength、
anterior chain eccentric training、diaphragm psoas pelvic floor coordination、
serape effect、gait contralateral arm swing。

## 6. 找影片的方向

**優先高分級頻道**（見 `channels.json` 的 `tier`）：Physiotutors、E3 Rehab、
[P]rehab、Squat University、Sports Injury Physio、Clinical Physio、
Institute of Human Anatomy、Precision Movement、The Movement System。

搜尋詞建議用**訓練功能**而不是線的名字——因為用線名搜到的多半是
Tom Myers 體系的推廣內容，那正是我們不該讓它自己作證的一方：

- 手臂線 → shoulder load transfer、latissimus thoracolumbar fascia、
  scapular control pulling、carry variations grip
- 螺旋線 → anti-rotation core、Pallof press progression、rotational power medicine ball、
  thoracic rotation hip dissociation、contralateral gait
- 側線 → frontal plane stability、side plank progression、lateral lunge、
  hip abductor control single leg、suitcase carry
- 前線 → anterior chain eccentric、hip flexor strength、dead bug progression、
  diaphragm 90/90 breathing、psoas function

如果真的要收一支持正方立場的影片來對照，可以，但要標 `contested-view`
並在 `claim_boundary` 寫清楚哪一句超出證據。

## 7. 交付檢查

- [ ] 4 個單元、每單元剛好 6 支示範，型別 `practice`
- [ ] 每個單元都同時說出「解剖驗證到哪裡」與「為什麼仍值得練」
- [ ] 沒有任何一句話寫成「調整／打開／釋放某條線」
- [ ] `evidence_grade` 有用到 `expert-consensus` 或 `experience`
- [ ] 每支影片有 `source_type` / `practical_value` / `coach_takeaway`
- [ ] 每個 `dose` 有時間或次數、強度、停止條件
- [ ] 與 `oe-a.json` 的 `concept-2` 不矛盾
