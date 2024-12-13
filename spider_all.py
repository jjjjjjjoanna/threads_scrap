from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import time
import csv
import os

# 原始 CSV 檔案路徑
original_csv_file_path = os.path.join('authors_data.csv')

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



# 設置 Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.threads.net/?hl=jp")  # Threads 網頁版首頁

# 等待頁面加載
driver.implicitly_wait(10)

# 點擊登入按鈕
reply_button = driver.find_element(By.LINK_TEXT, "Log in")
reply_button.click()

# 等待 Instagram 登入頁面加載
time.sleep(5)

# 輸入 Instagram 用戶名
username_box = driver.find_element(By.XPATH, '//input[@placeholder="Username, phone or email"]')
username_box.send_keys("l31068474")

# 輸入 Instagram 密碼
password_box = driver.find_element(By.XPATH, '//input[@placeholder="Password"]')
password_box.send_keys("2024irtm")

# 提交登入表單
password_box.send_keys(Keys.RETURN)

# 等待登入完成
time.sleep(10)

# 從 CSV 中讀取使用者
users_to_process = read_users_from_csv()



def process_user_profiles(users_to_process):
    # 設置滾動時間
    SCROLL_PAUSE_TIME = 1

    # 循環處理每個使用者
    for user in users_to_process:
        profile_url = f"https://www.threads.net/@{user}?hl=zh-tw"
        
        # 打開使用者的頁面
        driver.get(profile_url)
        time.sleep(3)

        # 創建每個用戶的 CSV 檔案
        user_csv_file_path = f"{user}_profile_data.csv"
        with open(user_csv_file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['user', 'time', 'content'])  # 標題行

            # 滾動頁面以加載更多資料
            while True:
                # 滾動到頁面底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(SCROLL_PAUSE_TIME)

                # 抓取所有作者元素
                author_elements = driver.find_elements(By.CLASS_NAME, 'xrvj5dj')
                print(f"Found {len(author_elements)} author elements for {user}")

                # 檢查每一個元素的時間
                for element in author_elements:
                    lines = element.text.split('\n')
                    if len(lines) > 3:
                        post_time = lines[1]
                        if post_time.count('-') == 2:  # 如果有兩個 '-'
                            year = post_time.split('-')[0]
                            print(year)

                            # 如果年份是 2023 或更早，則寫入資料並停止抓取
                            if int(year) <= 2023:
                                print(f"Post time {post_time} is before or in 2023, stopping further posts for {user}")
                                author_elements = driver.find_elements(By.CLASS_NAME, 'xrvj5dj')
                                for element in author_elements:
                                    lines = element.text.split('\n')
                                    if len(lines) > 3:
                                        user = lines[0]
                                        post_time = lines[1]
                                        content = ' '.join(lines[3:])
                                        writer.writerow([user, post_time, content])

                                # 跳到下一位使用者
                                break
                else:
                    # 如果沒有觸發 break (即處理完所有元素)，繼續滾動頁面
                    continue

                # 如果跳出內部的 for 循環，則跳出外部的 while 循環
                break
process_user_profiles(users_to_process)
# 關閉瀏覽器
driver.quit()
