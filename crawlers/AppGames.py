from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np
import time

options = webdriver.ChromeOptions()
# options.add_argument("--verbose")
options.add_argument('--no-sandbox')
options.add_argument('--headless')
options.add_argument('--disable-gpu')
# options.add_argument("--window-size=1920, 1200")
options.add_argument('--disable-dev-shm-usage')
driver = webdriver.Chrome(options=options)

url = 'https://genk.vn/apps-games.chn'

# Mở trang bằng Selenium
driver.get(url)

# Đợi một chút để trang tải hoàn toàn nội dung
# time.sleep(3)

# Lấy danh sách các bài viết
appsgame_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.knsw-list li.knswli')

data = []
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Lấy danh sách các bài viết
    appsgame_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.knsw-list li.knswli')

    for appsgame_element in appsgame_elements:
        appsgame_data = {}
        div_left = appsgame_element.find_element(By.CSS_SELECTOR, 'div.knswli-left.fl')
        link_tag = div_left.find_element(By.TAG_NAME, 'a')
        title = link_tag.get_attribute('title') or 'N/A'
        link = link_tag.get_attribute('href') or 'N/A'
        image_tag = div_left.find_element(By.TAG_NAME, 'img')
        image = image_tag.get_attribute('src') if image_tag else 'N/A'

        div_right = appsgame_element.find_element(By.CSS_SELECTOR, 'div.knswli-right')
        try:
            afnews_type = div_right.find_element(By.CSS_SELECTOR, 'div.afnews-type a')
            category = afnews_type.text
        except:
            category = 'Apps/Games'  # Nếu không có category thì mặc định là 'Thủ Thuật'

        description = div_right.find_element(By.CSS_SELECTOR, 'span.knswli-sapo').text
        created_at = div_right.find_element(By.CSS_SELECTOR, 'div.knswli-meta span.knswli-time').text

        appsgame_data['title'] = title
        appsgame_data['link'] = link
        appsgame_data['image'] = image
        appsgame_data['description'] = description
        appsgame_data['createdAt'] = created_at
        appsgame_data['category'] = category

        # Kiểm tra trùng lặp trước khi thêm vào data
        if not any(existing['link'] == appsgame_data['link'] for existing in data):
            data.append(appsgame_data)
    if len(data) >= 1000:
        break
    # Cuộn xuống trang (if needed)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(5)  # Đợi một chút để tải thêm bài viết

    # Kiểm tra chiều cao trang
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:  # Nếu không còn chiều cao mới, thoát vòng lặp
      try:
        load_more_button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, 'a.btnviewmore'))
        )
        load_more_button.click()
        time.sleep(3)  # Wait for new content to load
      except Exception as e:
        print("No more 'Xem thêm' button or could not click:", e)
        break
    last_height = new_height  # Cập nhật chiều cao

for item in data:
    print(item)

# Đóng trình duyệt sau khi hoàn thành cào dữ liệu
driver.quit()

df = pd.DataFrame(data)
df['category'] = df['category'].fillna('Apps/Games')
df['category'] = df['category'].replace('', 'Apps/Games')
# df['category'] = df['category'].replace('Trà đá công nghệ', np.nan)
df['category'].value_counts()

df.to_csv('appsgame_selenium.csv', index=False, encoding='utf-8-sig')
print("Dữ liệu đã được xuất ra file 'appsgame_selenium.csv'.")
