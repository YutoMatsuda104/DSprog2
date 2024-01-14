from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import time

# WebDriverの設定
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# 有馬記念の出走馬リストページにアクセス
url = "https://race.netkeiba.com/race/shutuba.html?race_id=202306050811"  # 有馬記念のURLを指定
driver.get(url)
time.sleep(1)

# 馬のリンクを取得
houselink_list = []
for a in range(1, 21):
    try:
        # 馬名とリンクの取得
        house_name_element = driver.find_element(By.XPATH, f'//*[@id="tr_{a}"]/td[4]/div/div/span/a')
        house_name = house_name_element.text
        house_link = house_name_element.get_attribute("href")
        houselink_list.append((house_name, house_link))
    except NoSuchElementException:
        continue

# 各馬のリンクをループし、各馬の過去10レースのデータを取得
for house_name, house_link in houselink_list:
    # 各馬の詳細ページにアクセス
    driver.get(house_link)
    time.sleep(1)  # ページが完全にロードされるのを待つ

    # 過去のレース結果を取得するためのデータ構造を初期化
    horse_races = []
    
    # 過去10レースの情報を取得
    for i in range(1, 11):
        try:
            race_data = {}
            # 日付、レース名、頭数、枠番、馬番、人気、着順、距離、着差を取得
            race_data['date'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[1]/a').text
            race_data['race_name'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[5]/a').text
            race_data['head'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[7]').text
            race_data['frame'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[8]').text
            race_data['house_num'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[9]').text
            race_data['pop'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[11]').text
            race_data['rank'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[12]').text
            race_data['distance'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[15]').text
            race_data['rank_dis'] = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{i}]/td[19]').text

            # 取得したレースのデータをリストに追加
            horse_races.append(race_data)
        except NoSuchElementException as e:
            print(f"馬 {house_name} の {i} 番目のレースデータが見つかりません。エラー: {e}")
            break  # 10レース分のデータがない場合、ループを抜ける

    # 取得した馬のレース結果を表示または保存
    print(f"馬 {house_name} の過去10レースのデータ:")
    for race in horse_races:
        print(race)

# WebDriverを閉じる
driver.quit()


