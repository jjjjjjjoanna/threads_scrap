#新的可以爬name
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
script_directory = os.path.dirname(os.path.realpath(__file__))

# Wait for the page to load (adjust timeout if needed)
driver.implicitly_wait(10)

# Scroll and find elements
SCROLL_PAUSE_TIME = 2
SCROLL_TIME_LIMIT = 100  # Time limit for scrolling in seconds
WRITE_INTERVAL = 10  # Write to CSV every 10 seconds
start_time = time.time()
last_write_time = start_time  # Store the time of last write

# Specify the full path to the CSV file
csv_file_path = os.path.join(script_directory, 'authors_data.csv')
print(f"Saving CSV to: {csv_file_path}")

# Open CSV file for writing with UTF-8 encoding
with open(csv_file_path, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    
    # Write the header
    writer.writerow(['user'])

    # Set to store unique users
    users_to_write = set()  # Using set to avoid duplicates

    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Check if time limit has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time > SCROLL_TIME_LIMIT:
            break

        # Find elements (adjust selectors based on actual content)
        author_elements = driver.find_elements(By.CLASS_NAME, 'x1pha0wt')

        # Print out the number of elements found
        print(f"Found {len(author_elements)} author elements")

        # Iterate over each element and collect user data
        for element in author_elements:
            user = element.text.split('\n')[0].strip()  # Extract user text (first line)

            # Debugging step: print user
            print("Found user:", user)

            # Collect user data in the set (avoids duplicates)
            users_to_write.add(user)

        # Write to CSV every 10 seconds
        if time.time() - last_write_time >= WRITE_INTERVAL:
            # Write all collected unique users to CSV
            for user in users_to_write:
                writer.writerow([user])  # Write user data to CSV
            print(f"Written {len(users_to_write)} unique users to CSV.")
            
            # Reset the set of users and update last write time
            users_to_write.clear()
            last_write_time = time.time()

        # Delay before next scroll
        time.sleep(1)  # Small delay to ensure smooth scrolling

    print("CSV file created successfully.")

# Close the browser
driver.quit()
