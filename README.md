# Streamlit-LangGraph-Chatbot-Demo


## 專案簡介

這是一個基於 Streamlit 的聊天機器人專案，集成了 LangGraph 框架，用於快速構建多輪對話的聊天機器人。專案特性如下：

## 專案特色

1. **Streamlit 串接 LangGraph**：快速構建聊天機器人應用程式。
2. **流式輸出**：實現實時的流式回應顯示，提升用戶體驗。
3. **多輪問答**：支援多輪對話，實現智能上下文處理。

## 最近更新

- 2025.01.09: 新增無法查詢現在日期與時間的問題，現在可使用系統內建 datetime 或其他服務取得當前日期與時間，並回傳給使用者。

## 安裝與執行

請依以下步驟安裝並執行專案。

### 1. Clone 專案

使用 Git 將專案複製到本地：

```bash
git clone https://github.com/Gingoooo/streamlit-langgraph-chatbot.git
cd streamlit-langgraph-chatbot-Demo
```

### 2. 建立虛擬環境

為了保持依賴的獨立性，建議使用虛擬環境：

```bash
python -m venv venv
source venv/bin/activate  # Windows 用戶使用 `venv\Scripts\activate`
```

### 3. 配置環境變數

將範例檔案複製為 `.env`，並將 Gemini API 金鑰添加到 .env 檔案中：

建立 `.env` 檔案，並添加以下內容以設定必要的環境變數：

```bash
cp .env.example .env
```

編輯 .env 檔案，添加以下內容：

```
API_KEY=your_gemini_api_key
```

安裝套件以讀取 `.env` 檔案（已在 `requirements.txt` 中包含）。

### 4. 安裝依賴套件

使用 `requirements.txt` 安裝必要的依賴：

```bash
pip install -r requirements.txt
```

### 5. 執行應用程式

啟動 Streamlit 應用程式：

```bash
streamlit run app.py
```

## 使用 Docker 部署

可以使用 Docker 和 Docker Compose 部署此服務

### 1. 構建 Docker 映像

在項目根目錄下，執行以下命令構建 Docker 映像：

```bash
docker-compose build
```

### 2. 運行容器

構建完成後，執行以下命令啟動容器：

```bash
docker-compose up
```

應用將運行在 http://localhost:8501。



## 系統需求

建議使用 Python 3.12 或以上版本，以確保最佳相容性與性能。


## 資料夾結構

```
Streamlit-LangGraph-Chatbot-Demo/
├── app.py                # 主執行檔案
├── utils.py              # 工具函式
├── prompts.py            # 提示詞
├── logs/                 # 日誌目錄
├── .env                  # 環境變數配置檔案
├── requirements.txt      # 依賴套件清單
└── README.md             # 專案文檔
```
