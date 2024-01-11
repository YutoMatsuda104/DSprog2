import numpy as np
import sqlite3

path = '/Users/yutomatsuda/Lecture/DSProg2/database/'

# DBファイル名
db_name = 'Keiba_local.sqlite'

# DBに接続する（指定したDBファイル存在しない場合は，新規に作成される）
con = sqlite3.connect(path + db_name)

# 2．SQLを実行するためのオブジェクトを取得
cur = con.cursor()

# 3．実行したいSQLを用意する
# テーブルを作成するSQL
# CREATE TABLE テーブル名（カラム名 型，...）;
sql_create_table_DSprogHW = 'CREATE TABLE Keiba_local(house_name text, first_pred real, second_pred real, third_pred real);'

# 4．SQLを実行する
cur.execute(sql_create_table_DSprogHW)

# データを挿入するSQL文を作成
sql_insert_data = '''
INSERT INTO Keiba_local (house_name, first_pred, second_pred, third_pred)
VALUES (?, ?, ?, ?);
'''

# 挿入したいデータ
data_to_insert = [
    ("ソールオリエンス", 1, 5, 4),
    ("シャフリヤール", 0, 2, 2),
    ("ホウホウエミーズ", 1, 0, 0),
    ("タイトルホルダー", 4, 4, 10),
    ("ドウドゥース", 3, 3, 7),
    ("ディープポンド", 4, 4, 4),
    ("アイアンバローズ", 0, 2, 1),
    ("ライラック", 1, 1, 1),
    ("ヒートオンビート", 0, 0, 1),
    ("ジャスティンパレス", 9, 7, 6),
    ("ハーパー", 0, 2, 0),
    ("ウインマリリン", 1, 1, 3),
    ("タスティエーラ", 3, 6, 9),
    ("プラダリア", 1, 1, 2),
    ("スルーセブンシーズ", 2, 3, 4),
    ("スターズオンアース", 6, 12, 6),
]

# 各データ行をデータベースに挿入
for data in data_to_insert:
    cur.execute(sql_insert_data, data)

# 変更をコミット
con.commit()

# テーブルからすべてのデータを選択するSQL文を作成
sql_select_all = 'SELECT * FROM Keiba_local;'

# SQLクエリを実行
cur.execute(sql_select_all)

# 結果を取得
all_data = cur.fetchall()

# 結果を表示
for row in all_data:
    print(row)

# データベース接続を閉じる
con.close()