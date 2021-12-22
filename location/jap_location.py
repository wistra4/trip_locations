import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import csv

# Chromeを起動
chrome_service = fs.Service(executable_path="driver/chromedriver")
driver = webdriver.Chrome(service=chrome_service)

# 明示的な待機
driver.implicitly_wait(10)

jap_id = '38'
# 指定したURLに遷移
driver.get("https://rtrp.jp/locations/" + jap_id + "/")

next_button = driver.find_element(by=By.CLASS_NAME, value='currentLocationName')
next_button.click()

# 接続を確認
for _ in range(2):
    try:
        # 失敗しそうな処理
        selector = 'div#locationSelectionDialog > section > dl > dt > a'
        locations = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
    except TimeoutException as e:
        # エラーメッセージを格納する
        error = e
    else:
        # 失敗しなかった場合はループを抜ける
        break
else:
    # リトライが失敗した時の処理
    print(error)

time.sleep(2)

# 階層構造を指定する数字
tree_num = 2

time.sleep(1)

# タイトルとURLを紐付ける空の辞書を作成
title_dict = {'1_1':'日本'}
id_dict = {'1_1':jap_id}
# 親子関係を保存する辞書を作成
parent_dict = {'1_1':'nothing'}

location_num = 1
locations = driver.find_elements(by=By.CSS_SELECTOR, value=selector)
for location in locations:
    # locationを特定するkeyを発行
    location_key = str(tree_num) + "_" + str(location_num)
    # titleを取得
    title = location.get_attribute("title")
    title_dict[location_key] = title
    # idを取得
    location_url = location.get_attribute("href")
    location_id = location_url.split("/")[4]
    id_dict[location_key] = location_id
    # 親idを保存
    parent_id = id_dict['1_1']
    parent_dict[location_key] = parent_id
    # 追加する情報を表示
    print(location_key, location_id, title, parent_id)
    # location_numをupdate
    location_num += 1
    # 時間をおく
    time.sleep(2)
pre_dict_length = location_num-1
print(pre_dict_length)

time.sleep(2)

status = 0

while status < 7:

    # 階層構造をupdate
    tree_num += 1
    location_num = 1

    for pre_location_num in range(pre_dict_length):
        pre_location_key = str(tree_num - 1) + "_" + str(pre_location_num + 1)
        driver.get("https://rtrp.jp/locations/" + id_dict[pre_location_key] + "/")

        # 明示的な待機
        driver.implicitly_wait(10)

        next_button = driver.find_element(by=By.CLASS_NAME, value='currentLocationName')
        next_button.click()

        # 接続を確認
        for _ in range(2):
            try:
                # 失敗しそうな処理
                selector = 'ul.subLocations > li > a'
                locations = WebDriverWait(driver, 10).until(
                        EC.visibility_of_element_located((By.CSS_SELECTOR, selector)))
            except TimeoutException as e:
                # エラーメッセージを格納する
                error = e
            else:
                # 失敗しなかった場合はループを抜ける
                break
        else:
            # リトライが失敗した時の処理
            print(error)

        time.sleep(2)

        locations = driver.find_elements(by=By.CSS_SELECTOR, value=selector)
        for location in locations:
            # locationを特定するkeyを発行
            location_key = str(tree_num) + "_" + str(location_num)
            # titleを取得
            title = location.get_attribute("title")
            title_dict[location_key] = title
            # idを取得
            location_url = location.get_attribute("href")
            location_id = location_url.split("/")[4]
            id_dict[location_key] = location_id
            # 親idを保存
            parent_id = id_dict[pre_location_key]
            parent_dict[location_key] = parent_id
            # 追加する情報を表示
            print(location_key, location_id, title, parent_id)
            # location_numをupdate
            location_num += 1
            # 時間をおく
            time.sleep(2)
        
        time.sleep(2)

        
        dict_length = location_num-1
        print(dict_length)

    print(title_dict)
    print(id_dict)
    print(parent_dict)

    pre_dict_length = location_num-1
    print(pre_dict_length)

    status += 1


# csvの書き出し
base_dir = os.getcwd()
meta_dir = base_dir + '/meta'
location_file = meta_dir + '/location.csv'
if not os.path.exists(meta_dir):
    os.mkdir(meta_dir)
with open(location_file, 'w') as f:
    writer = csv.writer(f)
    writer.writerow(['key', 'title', 'id', 'parent_id'])
with open(location_file, 'a') as f:
    writer = csv.writer(f)
    for key in title_dict:
        print(key)
        l_title = title_dict[key]
        print(l_title)
        l_id = id_dict[key]
        print(l_id)
        l_parent = parent_dict[key]
        print(l_parent)
        writer.writerow([key, l_title, l_id, l_parent])