#舊的可以爬name&content的
import csv
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Set up Selenium WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get("https://www.threads.net/?hl=zh-tw")

# Wait for the page to load (adjust timeout if needed)
driver.implicitly_wait(10)

# Scroll and find elements
SCROLL_PAUSE_TIME = 2
SCROLL_TIME_LIMIT = 10 # Time limit for scrolling in seconds
start_time = time.time()

while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Check if time limit has been reached
    if time.time() - start_time > SCROLL_TIME_LIMIT:
        break

# Find elements (adjust selectors based on actual content)
author_elements = driver.find_elements(By.CLASS_NAME, 'xrvj5dj')

# Print out the number of elements found
print(f"Found {len(author_elements)} author elements")

# Specify the full path to the CSV file
csv_file_path = os.path.join(os.path.expanduser('~'), 'Desktop', 'authors_data.csv')
print(f"Saving CSV to: {csv_file_path}")

# Filter and save data to CSV
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['user'])

    for element in author_elements:
        lines = element.text.split('\n')
        if len(lines) > 3:
            # Write the user, time, time2, and content into the CSV file
            user = lines[0]  # First line: user
            # time = lines[1]  # Second line: time
            # time2 = lines[2]  # Third line: time2
            # content = ' '.join(lines[3:])  # Remaining lines: content
            
            print("Saving to CSV:", user)  # Debugging step
            writer.writerow([user])  # Write all data in one row
        else:
            print("Skipped (less than 4 lines):", element.text)  # Debugging step

print("CSV file created successfully.")

# Close the browser
driver.quit()

