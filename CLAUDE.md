# Claude 工作目錄

這是 pink_chara 的 Claude 主工作資料夾，用於存放 AI 協作專案、腳本與產出物。

## 目錄架構

```
claude/
├── CLAUDE.md           # 本檔案：工作目錄說明與慣例
├── projects/           # 各別專案子目錄
├── scripts/            # 可重複使用的工具腳本
├── prompts/            # 常用提示語模板
└── output/             # Claude 產出的草稿、報告、資料
```

## 工作慣例

- **專案**：每個專案放在 `projects/<project-name>/`，各自有獨立的 README
- **腳本**：工具腳本放 `scripts/`，依語言分子目錄（`scripts/python/`、`scripts/shell/`）
- **提示語**：可重複使用的 prompt 模板放 `prompts/`，以 `.md` 格式儲存
- **產出**：一次性的草稿與報告放 `output/`，依日期命名（`YYYY-MM-DD_主題`）

## 常用指令

```bash
# 進入工作目錄
cd ~/Documents/claude

# 建立新專案
mkdir -p projects/<name> && touch projects/<name>/README.md

# 列出所有專案
ls projects/
```

## 溝通語言

- 一律使用**繁體中文**回應
- 程式碼、指令、專有名詞保留英文原文

## 注意事項

- 敏感資訊（API 金鑰、密碼）不放在此目錄，統一使用環境變數或 `.env`（不納入版控）
- 大型二進位檔、資料集不放此目錄
