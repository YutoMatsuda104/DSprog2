from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
import numpy as np
import time
import re
import sqlite3

# WebDriverのインスタンスを一度だけ生成
driver = webdriver.Chrome()
driver.implicitly_wait(10)

# URLを開く
url = "https://race.netkeiba.com/race/shutuba.html?race_id=202306050811"
driver.get(url)
time.sleep(0.1)

# 全ての馬のデータを格納するリスト
all_data = []

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

# 各馬の詳細ページで情報を取得
for house_name, house_link in houselink_list:
    driver.get(house_link)
    time.sleep(0.1)

    # 新しいdatum辞書を作成
    datum = {'馬名': house_name}
    winscore_list = []
    wintime_list = []
    last_list = []
    weight_change_list = []

    # ここから情報を取得
    b = 1
    while True:
        try:
            # 勝率の取得
            winscore = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{b}]/td[12]').text
            if winscore and winscore.isdigit():  # 数字のみを確認
                winscore_list.append(float(winscore))

            # 着差の取得（空白や**を回避）
            wintime = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{b}]/td[19]').text
            if wintime and wintime.replace('.', '', 1).isdigit():  # 数字または小数点を含む文字列のみを確認
                wintime_list.append(float(wintime))

            # 上りの取得（空白や**を回避）
            last = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{b}]/td[23]').text
            if last and last.replace('.', '', 1).isdigit():  # 数字または小数点を含む文字列のみを確認
                last_list.append(float(last))

            # 体重の増減の取得（空白を回避）
            weight = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[5]/div/table/tbody/tr[{b}]/td[24]').text
            match = re.search(r'\((\+|-)?(\d+)\)', weight)
            if match:  # マッチするものがあった場合
                weight_change = int(match.group(2)) * (-1 if match.group(1) == '-' else 1)
                weight_change_list.append(weight_change)


            b += 1
        except NoSuchElementException:
            break

    # 各データの平均値を計算して辞書に追加
    datum['勝率平均'] = np.mean(winscore_list) if winscore_list else None
    datum['着差平均'] = np.mean(wintime_list) if wintime_list else None
    datum['上り平均'] = np.mean(last_list) if last_list else None
    datum['馬体重増減平均'] = np.mean(weight_change_list) if weight_change_list else None

    # 血統情報のリンクを取得して、その勝率を計算
    bloodline_links = []
    try:
        bloodline_elements = {
            '父': '//*[@id="db_main_box"]/div[2]/div/div[2]/div/dl/dd/table/tbody/tr[1]/td[1]/a',
            '父の父': '//*[@id="db_main_box"]/div[2]/div/div[2]/div/dl/dd/table/tbody/tr[1]/td[2]/a',
            '父の母': '//*[@id="db_main_box"]/div[2]/div/div[2]/div/dl/dd/table/tbody/tr[2]/td/a',
            '母': '//*[@id="db_main_box"]/div[2]/div/div[2]/div/dl/dd/table/tbody/tr[3]/td[1]/a',
            '母の父': '//*[@id="db_main_box"]/div[2]/div/div[2]/div/dl/dd/table/tbody/tr[3]/td[2]/a',
            '母の母': '//*[@id="db_main_box"]/div[2]/div/div[2]/div/dl/dd/table/tbody/tr[4]/td/a'
        }
        for key, xpath in bloodline_elements.items():
            element = driver.find_element(By.XPATH, xpath)
            link = element.get_attribute("href").replace("ped", "result")
            bloodline_links.append((key, link))
    except NoSuchElementException:
        continue

    # 血統リンクから勝率を取得
    for key, link in bloodline_links:
        driver.get(link)
        time.sleep(0.1)
        winscore_list = []
        c = 1
        while True:
            try:
                winscore = driver.find_element(By.XPATH, f'//*[@id="contents"]/div[2]/div[1]/table/tbody/tr[{c}]/td[12]').text
                if winscore and winscore.isdigit():
                    winscore_list.append(float(winscore))
                c += 1
            except NoSuchElementException:
                break

        datum[f'{key}の勝率平均'] = np.mean(winscore_list) if winscore_list else None

    # 全体のデータリストに個々の馬のデータを追加
    all_data.append(datum)

# ドライバーを閉じる
driver.quit()

# Google Colab
path = '/Users/yutomatsuda/Lecture/DSProg2/'

# DBファイル名
db_name = 'Keiba_2.sqlite'

# DBに接続する（指定したDBファイル存在しない場合は，新規に作成される）
con = sqlite3.connect(path + db_name)

# 2．SQLを実行するためのオブジェクトを取得
cur = con.cursor()

# 3．実行したいSQLを用意する
# テーブルを作成するSQL
# CREATE TABLE テーブル名（カラム名 型，...）;
sql_create_table_DSprogHW = 'CREATE TABLE Keiba(house_name text, win_score real, wintime real, last real, weight real, F real, FF real, FM real, M real, MF real, MM real);'

# 4．SQLを実行する
cur.execute(sql_create_table_DSprogHW)

# データを挿入するSQLコマンド
sql_insert_data = 'INSERT INTO Keiba (house_name, win_score, wintime, last, weight, F, FF, FM, M, MF, MM) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);'

# データリストからデータをテーブルに挿入
for data in all_data:
    try:
        # 辞書からデータを取り出し、データベースに挿入
        cur.execute(sql_insert_data, (
            data['馬名'],
            data['勝率平均'],
            data['着差平均'],
            data['上り平均'],
            data['馬体重増減平均'],
            data.get('父の勝率平均', 'N/A'),
            data.get('父の父の勝率平均', 'N/A'),
            data.get('父の母の勝率平均', 'N/A'),
            data.get('母の勝率平均', 'N/A'),
            data.get('母の父の勝率平均', 'N/A'),
            data.get('母の母の勝率平均', 'N/A')  
        ))
    except KeyError as e:
        print(f"データにキーが欠けています: {e}")

# 変更をコミット
con.commit()

# データを選択するSQLコマンド
sql_select_data = 'SELECT * FROM Keiba;'
cur.execute(sql_select_data)

# すべての結果を取得
all_results = cur.fetchall()

# 結果を表示
for result in all_results:
    print(result)

# データベース接続を閉じる
con.close()