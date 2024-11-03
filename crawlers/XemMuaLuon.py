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

url = 'https://genk.vn/xem-mua-luon.chn'

# Mở trang bằng Selenium
driver.get(url)

# Đợi một chút để trang tải hoàn toàn nội dung
# time.sleep(3)

# Lấy danh sách các bài viết
watch_buy_immediately_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.knsw-list li.knswli')

data = []
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    # Lấy danh sách các bài viết
    watch_buy_immediately_elements = driver.find_elements(By.CSS_SELECTOR, 'ul.knsw-list li.knswli')

    for watch_buy_immediately_element in watch_buy_immediately_elements:
        watch_buy_immediately_data = {}
        div_left = watch_buy_immediately_element.find_element(By.CSS_SELECTOR, 'div.knswli-left.fl')
        link_tag = div_left.find_element(By.TAG_NAME, 'a')
        title = link_tag.get_attribute('title') or 'N/A'
        link = link_tag.get_attribute('href') or 'N/A'
        image_tag = div_left.find_element(By.TAG_NAME, 'img')
        image = image_tag.get_attribute('src') if image_tag else 'N/A'

        div_right = watch_buy_immediately_element.find_element(By.CSS_SELECTOR, 'div.knswli-right')
        try:
            afnews_type = div_right.find_element(By.CSS_SELECTOR, 'div.afnews-type a')
            category = afnews_type.text
        except:
            category = 'Xem - Mua - Luôn'  # Nếu không có category thì mặc định là 'Thủ Thuật'

        description = div_right.find_element(By.CSS_SELECTOR, 'span.knswli-sapo').text
        created_at = div_right.find_element(By.CSS_SELECTOR, 'div.knswli-meta span.knswli-time').text

        watch_buy_immediately_data['title'] = title
        watch_buy_immediately_data['link'] = link
        watch_buy_immediately_data['image'] = image
        watch_buy_immediately_data['description'] = description
        watch_buy_immediately_data['createdAt'] = created_at
        watch_buy_immediately_data['category'] = category

        # Kiểm tra trùng lặp trước khi thêm vào data
        if not any(existing['link'] == watch_buy_immediately_data['link'] for existing in data):
            data.append(watch_buy_immediately_data)
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
df['category'] = df['category'].fillna('Xem - Mua - Luôn')
df['category'] = df['category'].replace('', 'Xem - Mua - Luôn')
# df['category'] = df['category'].replace('Trà đá công nghệ', np.nan)
df['category'].value_counts()

df.to_csv('xemmualuon_selenium.csv', index=False, encoding='utf-8-sig')
print("Dữ liệu đã được xuất ra file 'xemmualuon_selenium.csv'.")
