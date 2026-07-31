# myofascial-movement — 筋膜與動作整合

**線上版**：<https://myofascial-movement.pages.dev> · 課程內容為**繁體中文**。

> **In English.** An evidence-graded course on fascia, self-myofascial release, mobility and
> load, curated entirely from public YouTube videos — 9 chapters, 27 units, 105 movement
> demos, 12 hours. Every claim is split into three layers: *what effect was observed*,
> *whether fascia is actually the mechanism*, and *whether it beats the alternatives*.
>
> The grading is deliberately unflattering: **not one of the 33 evidence verdicts reaches
> "strong"**. Foam rolling does increase range of motion acutely — but the effect crosses
> over to the limb you never touched, which is hard to reconcile with "breaking up
> adhesions". Findings that undercut the course's own premise are published as-is.
>
> Built on `curate-course` (from [htlin222/gym-course](https://github.com/htlin222/gym-course)),
> a topic-agnostic framework: replace `course/` and the same machinery produces a guitar
> course, a statistics course, a welding course.

---

把 YouTube 上散落的好內容，變成一門**結構完整、連結全數驗證、來源可查**的課程網站。

這個 repo 裝的是一門筋膜課：九個章節，從筋膜的解剖與功能定義、常見說法的科學爭議，
到自我筋膜放鬆、活動度與主動控制、彈性負荷適應，最後收在分區域實作與課表整合。

底層是 `curate-course` 框架，本身主題無關——`course/` 整組換掉就變成吉他課、統計課、電銲課。
框架取自 [htlin222/gym-course](https://github.com/htlin222/gym-course)，本課程只替換了 `course/`。

---

## 為什麼不是又一個滾筒影片清單

**一、它不賣承諾。** 筋膜是這幾年最好賣的兩個字，而這門課的每個主張都被拆成三層：

1. **做了之後可能有什麼效果？** 短期活動度、痠痛感受、主觀恢復、壓痛耐受
2. **效果是不是筋膜本身造成的？** 觀察到的效果 ≠ 已證明的機轉
3. **它有沒有比其他方法更好？** 長期活動度上，滾筒與靜態伸展的效果相當

所以你不會在這個網站上看到「把沾黏壓開」「排出乳酸」「調整筋膜線」——
除非是在 CH2 當成被檢驗的對象。

**二、但它不會因為「沒有論文」就丟掉好教練。** 筋膜訓練有大量知識本來就不是
研究論文能回答的：動作怎麼教、學員最常錯在哪、無感時怎麼退階、課表怎麼串。
所以每支影片標**兩個軸**——科學證據可信度與實務教學價值——外加內容角色徽章
（科學基礎／專家觀點／教練經驗／臨床經驗／動作示範／課表設計／爭議觀點／安全提醒）。

一支影片完全可以是「研究支持有限」而「教得非常好」。網站要回答的不是
「這個教練對不對」，而是 **這支影片哪一部分值得學、哪一部分需要保留**——
所以每支片各有 `coach_takeaway`（值得帶走的操作重點）與
`claim_boundary`（哪一句話要打折扣），兩者用不同顏色並排顯示。
判斷實務價值看的是八件事（是否說清楚適用對象、有無進階退階、是否解釋常見錯誤、
是否避免過度承諾、是否把感覺與結構改變分開、有無安全界線、是否解釋為什麼這樣安排、
是否允許個體差異），**不看訂閱數與觀看數**。細節見
[`docs/dual-axis-brief.md`](docs/dual-axis-brief.md)。

**三、連結真的活著。** 一百多個格子最大的風險是連結是捏造的，所以有兩層關卡：
`make audit` 離線把設定檔、配額、影片長度、實證欄位全查一遍（確定性，不打網路）；
`make verify` 再對每個 YouTube 連結重打 oEmbed、對每個 PMID 重打 PubMed API。
**不信任任何上游宣稱**，包括 AI agent 自稱驗證過的。

**四、每個動作都有停止條件。** 每一支示範影片的 `dose` 都寫了三件事：
時間或次數、壓力或強度、**什麼時候要立刻停**。禁區（膝窩、腋窩、鼠蹊、頸前三角、
腹部主動脈區、骨突）逐一寫進相關動作，深層靜脈栓塞風險標成「絕對不要滾壓」。

---

## 這門課的數字

| | |
|---|---|
| 章節 | 10（基礎與立場 3 + 方法與練習 3 + 部位與整合 3 + 筋膜線專題 1） |
| 單元 | 31（21 個實作主題、4 個觀念、4 個迷思查核、1 個課表、1 個說明） |
| 影片 | 129 支示範 + 31 堂主課 + 32 堂對照版＝192 個欄位、184 支不重複、110 個頻道 |
| 課程時長 | **15 小時 32 分**（所有語言版本全看過則為 22 小時） |
| 內容角色 | 192/192 已標註 · 科學與理論 18% · 教練／治療師實務 56% · 純示範 18% · 爭議觀點 1% |
| 來源分級 | 研究機構 7 · 臨床專業 30 · 專業教練 26 · 媒體 2 · 器材品牌 2 · 背景不明 8（使用中頻道 100% 已分級） |
| 字幕 | 184 支中 43 支有人工字幕、159 支至少有自動字幕、**25 支完全沒有**（14%） |
| 實證查核 | 26 個單元層級 + 11 個介入類別＝37 條判定 |
| 文獻 | 159 筆結構化引用，另有 152 個 PMID 直接寫在論述裡 |
| 科學證據 | 證據較充分 **0** · 中等 18 · 有限 14 · 專家共識 1 · 經驗性主張 1 · 存在爭議 3 |
| 驗證 | 稽核零錯誤、連結 184/184 有效、引用 159/159 標題相符、散文 PMID 152/152 存在 |

查證結果沒有很好看，而這正是重點：

- **37 條實證判定裡沒有任何一條拿到「證據較充分」**
- 滾筒能在當下增加關節活動度，但效果會**跨到沒滾到的對側肢體**——
  這比較像神經系統的疼痛耐受度改變，而不是局部組織被「壓開」
- 長期活動度上，**滾筒與靜態伸展的效果相當**，所以滾筒不是唯一或必然較好的方法
- 伸展改變的比較可能是**伸展耐受度**，而不是肌肉真的變長
- 筋膜鏈的解剖連續性只有部分被大體研究支持，且結論高度依賴解剖手法。
  62 篇人體解剖研究逐條驗證 Myers 六條經線的轉換點：後表線 3/3、後功能線 3/3、
  前功能線 2/2，但**螺旋線 5/9、側線 2/5、前表線 0/7，手臂線根本未被納入**——
  CH9 就是為這幾條而寫的
- 姿勢與疼痛的關聯在大型族群研究中一再落空

這些全部寫在網站上，`存在爭議` 標籤直接顯示在單元標題列。

字幕那一列也值得一看：**45 支影片完全沒有字幕，幾乎全部是中文頻道**
（全人物理治療所 8 支、啾c物理治療師 4 支、三個字SunGuts 3 支）。這是每個單元
另外配一支英文專業主課的原因——不是為了湊數量，是可及性。

---

## 快速開始

需要 [uv](https://docs.astral.sh/uv/)。建置腳本只用 Python 標準庫，沒有執行期相依。

```bash
git clone https://github.com/zinojeng/myofascial-movement.git
cd myofascial-movement

make build     # course/ → dist/
make serve     # http://localhost:8899
```

---

## 指令

```
make build     course/ → dist/，含配額驗證與 SEO 產出
make meta      用 yt-dlp 補齊 video-meta.json（真實長度、觀看數、頻道）
make audit     離線稽核設定檔、配額、影片長度與實證深度（不打網路，可放 CI）
make verify    重驗每個影片連結與每個 PMID（打真實 API）
make serve     本機預覽
make icons     重新下載 Lucide 圖示並打包成內嵌 sprite
make og        重新產生社群預覽圖（寫進 course/assets/og.png）
make lint      ruff 檢查
make check     lint + build + audit，提交前跑這個
make deploy    部署到 Cloudflare Pages
```

策展時另有兩支查詢工具，它們是 video id 與 PMID 的**唯一合法來源**：

```bash
uv run python src/build/ytsearch.py "滾筒 放鬆 教學" 10 --min 0:40 --max 12:00
uv run python src/build/pubmed.py  search "foam rolling range of motion" 12
uv run python src/build/pubmed.py  abs 38760635
```

---

## 換成你的主題

**你只需要動 `course/`**，其他都是框架。

```
course/
├── course.config.json   站台設定、章節、配額、所有 UI 文案
├── data/                策展資料（影片、實證、中繼資料）
├── taxonomy/            選用：主題專屬的詞彙模組
└── assets/              選用：og.png、favicon、樣式覆寫
```

這門課相對原框架換掉了兩個詞彙模組，理由值得說明：

- **`taxonomy/regions.py`** — 分面是**身體區域**而不是肌群。筋膜是連續的結締組織系統，
  把一支影片標成「只練股二頭肌」會強化「一條一條分開處理」的錯誤心像。
- **`taxonomy/methods.py`** — 類別是**介入方法**（滾筒、按摩球、靜態伸展、負重活動度……）
  而不是動作原型。因為**文獻是按介入分的，不是按肌肉分的**——
  「小腿滾筒」沒有專屬文獻，「滾筒與自我筋膜放鬆」有一整批系統性回顧。

`course/data/` 的格式與策展規則寫在 [`docs/curation-brief.md`](docs/curation-brief.md)。

---

## 部署到 Cloudflare Pages

### 方法 A：Git 整合（推薦，長期維護用）

Workers & Pages → Create application → Pages → Import an existing Git repository，
選這個 repo，建置設定填：

| 設定 | 內容 |
|---|---|
| Production branch | `main` |
| Framework preset | `None` |
| Build command | `python3 src/build/build.py` |
| Build output directory | `dist` |
| Root directory | `/` |

環境變數 `PYTHON_VERSION = 3.11`。這個專案沒有 Node 前端編譯，
`build.py` 會產生完整靜態網站到 `dist`，Cloudflare 部署那個目錄即可。

第一次部署完成後，把 `course/course.config.json` 的 `site.url` 更新成實際網址
（名稱被占用時 Cloudflare 會加後綴），再重新建置一次讓 SEO 標籤跟著更新。

> **不要用 Workers 的「Import a repository」。** 新版 dashboard 會把匯入引導到 Workers，
> 但那會建出一個 **Worker** 而不是 Pages 專案：Workers Builds 預設跑 `npx wrangler deploy`，
> 這個 repo 沒有 wrangler 設定檔，會直接失敗（`error occurred while running deploy command`）；
> 而且 `functions/` 只有 Pages 會載入，Worker 吃不到瀏覽計數器。
> Workers 與 Pages 共用同一個名稱空間，所以要先把同名的 Worker 服務刪掉，
> Pages 專案才能叫 `myofascial-movement`。

#### 選用：開啟瀏覽計數器

`functions/api/hits.js` 需要一個綁成 **`HITS`** 的 D1 資料庫。走 Git 整合時
**Pages 不會讀 `wrangler.jsonc`**（`make counter` 產生的那份只對本機 `wrangler pages deploy` 有效），
綁定要在 dashboard 設：

```bash
npx wrangler d1 create myofascial-movement-hits
npx wrangler d1 execute myofascial-movement-hits --file functions/schema.sql --remote
```

然後到 Pages 專案 → Settings → Functions → D1 database bindings，
新增 Variable name `HITS` → 選剛才那個資料庫 → 重新部署一次。

不做這一步也沒關係：API 回 503，前端會安靜地不顯示徽章，課程本身不受影響。
想連這個 fetch 都省掉，就把 `course.config.json` 的 `counter` 區塊整個刪除。

### 方法 B：本機 Wrangler 直接上傳

```bash
npx wrangler login
npx wrangler pages project create   # 專案名輸入 myofascial-movement
make deploy
```

`make deploy` 會先建置再上傳 `dist`，專案名取自 `course.config.json` 的 `site.project`。

---

## CI

`.github/workflows/check.yml` 在每次 push 與 PR 跑 `make check`（lint + build + audit）。
離線稽核是確定性的，同樣的 `course/` 永遠得到同樣的報告，所以擋得住 PR。
`make verify` 會打 YouTube 與 PubMed 的真實 API，只在手動 `workflow_dispatch` 時跑。

---

## 授權與免責

程式碼採 MIT，見 [LICENSE](LICENSE)。框架取自
[htlin222/gym-course](https://github.com/htlin222/gym-course)（同為 MIT）。

**影片著作權屬原 YouTube 頻道**，本專案只存連結與公開中繼資料，不重製也不代管。
Lucide 圖示為 ISC。

課程內容為運動指引與衛教，**不構成醫療診斷或治療建議**。緊繃不等於組織縮短，
壓痛不等於損傷。若出現新發生或進行性的肌力下降、麻木或感覺異常、急性外傷、
夜間或靜止時持續惡化的疼痛、關節明顯腫脹發熱、發燒等全身症狀、深層靜脈栓塞風險
或不明原因體重下降，請立即停止自行練習並就醫。
