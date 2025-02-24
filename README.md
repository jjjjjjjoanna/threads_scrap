# 揭密 threads 2024 年底流量密碼

## 關於 scrape_threads

### 1. clone
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

## 資料前處理

### 清洗文本
移除標點符號、數字、分享網址等等雜訊

### 移除停用詞
使用 nltk 英文停用字以及線上提供的中文停用字集
舉例：「還是、還有、換句話說、或」

### 詞幹提取
使用 SnowballStemmer 以及 jieba 將句子拆分成單詞

### 建立向量
將處理後的文字轉換維度為 5000 的 TF-IDF 向量

## 分群方法

### K-means
按照前面膝蓋法的結果，分成 8 個 cluster

### HAC
使用 AgglomerativeClustering 函式嘗試四種方法
single、complete、average、ward

### HAC + K-means
對子集合先進行 HAC 分群，再將分群後的中心當作 Kmeans 的初始中心

## 特徵篩選方法

### TF-IDF

### Word Frequency

### Chi-square

### Pointwise Mutual Information

## 最終報告

[口頭報告](https://www.canva.com/design/DAGZz-HT4H4/cB6tV64tPA3SF95u1znRoA/edit?utm_content=DAGZz-HT4H4&utm_campaign=designshare&utm_medium=link2&utm_source=sharebutton)

書面報告如附檔 資訊檢索與文字探勘導論第九組期末報告.pdf
