import time
import csv
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

# 設置無頭模式
options = webdriver.ChromeOptions()
options.add_argument('--headless')  # 啟用無頭模式
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 原始 CSV 檔案路徑
original_csv_file_path = os.path.join('1220/base.csv')

# 讀取 CSV 中的使用者名單
def read_users_from_csv():
    users = []
    try:
        with open(original_csv_file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)  # Skip header row
            for row in reader:
                users.append(row[0])  # Get user from the first column
    except FileNotFoundError:
        print(f"CSV file {original_csv_file_path} not found.")
    return users

# 點擊登入按鈕並進行登入
def login_to_instagram():
    driver.get("https://www.threads.net/?hl=jp")
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.LINK_TEXT, "Log in"))).click()
    WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Username, phone or email"]')))

    driver.find_element(By.XPATH, '//input[@placeholder="Username, phone or email"]').send_keys("l31068474")
    driver.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys("2024irtm")
    driver.find_element(By.XPATH, '//input[@placeholder="Password"]').send_keys(Keys.RETURN)
    time.sleep(5)

# 處理每個使用者的資料
def process_user_profiles(users_to_process):
    for user in users_to_process:
        profile_url = f"https://www.threads.net/@{user}?hl=zh-tw"
        driver.get(profile_url)
        time.sleep(1)

        user_csv_file_path = f"1220/{user}_profile_data.csv"
        with open(user_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user', 'time', 'content'])  # 標題行
            seen_data = set()
            last_height = driver.execute_script("return document.body.scrollHeight")  # Get current page height
            no_new_content_counter = 0  # 計數器用來檢查是否有新內容

            while no_new_content_counter < 5:  # 重試 5 次
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(1)  # 延遲確保頁面有時間加載

                new_height = driver.execute_script("return document.body.scrollHeight")  # Get new page height
                if new_height == last_height:  # 如果新高度和舊高度相同，代表頁面沒有加載新內容
                    no_new_content_counter += 1  # 增加計數器
                    if no_new_content_counter >= 5:  # 如果重試 5 次仍無新內容，則跳出
                        break
                else:
                    no_new_content_counter = 0  # 重置計數器，如果加載了新內容
                last_height = new_height  # Update the last height for the next iteration

                # 抓取內容
                try:
                    author_elements = driver.find_elements(By.CLASS_NAME, 'xrvj5dj')
                    for element in author_elements:
                        try:
                            lines = element.text.split('\n')
                            if len(lines) > 3:
                                user = lines[0]
                                post_time = lines[1]
                                content = ' '.join(lines[3:])
                                if post_time.count('-') == 2:
                                    year = post_time.split('-')[0]
                                    if int(year) <= 2023:
                                        break  # 停止抓取更多資料
                                unique_key = lines[3][-10:]
                                if unique_key not in seen_data:
                                    writer.writerow([user, post_time, content])
                                seen_data.add(unique_key)
                        except StaleElementReferenceException:
                            continue
                except StaleElementReferenceException:
                    time.sleep(1)  # 增加短延遲後重試
                    continue

# 登入並開始處理
login_to_instagram()
users_to_process = read_users_from_csv()
process_user_profiles(users_to_process)

# 關閉瀏覽器
driver.quit()
