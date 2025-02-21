# Threads Scraper

本項目用於爬取 Threads 用戶的貼文及個人資訊。

## 使用步骤

### 1. 克隆仓库
運行以下命令，clone 項目到本地：
```bash
git clone https://github.com/jjjjjjjoanna/threads_scrap.git
cd threads_scrap
```

### 2. pip install
```bash
pip install "scrapfly-sdk" loguru nested-lookup jmespath
```

### 3. .env
創建一個叫做 .env 的檔案，放上
```python
SCRAPFLY_KEY="scp-live-fc846e53b72d446f8a8a5a954269e853"
```
或其他你拿到的 KEY

### 4. 加入檔案
把 authors_data.csv 放到同一個目錄

### 5. 執行
```bash
python main.py
```
