# 強化學習題庫 Streamlit App

這個專案提供一個可直接練習強化學習題目的 Streamlit 測驗網站。

功能包含：

- 從 150 題題庫中隨機抽出 50 題
- 一次只顯示 1 題
- 可使用 `上一題` / `下一題` 回頭修改答案
- 每題 2 分
- 可開啟作弊模式立即查看答案與詳解，該題不計分
- 測驗結束後顯示完整題目預覽、你的答案、正確答案、紅綠對錯標示與詳解
- 支援大部分 LaTeX 數學公式顯示

## 專案結構

```text
.
├─ app.py
├─ normalize_qna.py
├─ QnA.md
├─ requirements.txt
├─ README.md
├─ .gitignore
├─ data/
│  └─ questions.json
└─ scripts/
   ├─ __init__.py
   └─ normalize_qna.py
```

說明：

- `app.py`：Streamlit 主程式
- `QnA.md`：整理後的人類可讀題庫
- `data/questions.json`：實際給 app 使用的結構化題庫
- `scripts/normalize_qna.py`：題庫正規化與同步輸出腳本
- `normalize_qna.py`：根目錄快捷入口，方便直接執行

## 環境安裝

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 啟動 app

```powershell
.\.venv\Scripts\Activate.ps1
streamlit run app.py
```

## 重新產生題庫

如果你修改了 `QnA.md` 或想重新套用正規化規則，可以執行：

```powershell
.\.venv\Scripts\Activate.ps1
python normalize_qna.py
```

執行後會同步更新：

- `QnA.md`
- `data/questions.json`

## 備註

- 題庫來源包含 ChatGPT、Gemini、Claude 三組題目。
- 若少數題目仍出現公式顯示不理想，優先修改 `data/questions.json` 或在 `scripts/normalize_qna.py` 的覆寫規則中修正。
