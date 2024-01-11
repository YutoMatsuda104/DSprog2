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
sql_create_table_DSprogHW = 'CREATE TABLE Keiba(house_name text, win_score real, wintime real, last real, weight real, F real, FF real, FM real, M real, MF real, MM real);'

# 4．SQLを実行する
cur.execute(sql_create_table_DSprogHW)