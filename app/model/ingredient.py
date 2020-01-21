import MySQLdb

from db import DBConnector
from model.project import project


class ingredient:
    """食材モデル"""

    def __init__(self):
        self.attr = {}
        self.attr["ingredient_id"] = None         # ingredient_id int
        self.attr["ingredient_name"] = None       # ingredient_name str notNull

    @staticmethod
    def migrate():

        # データベースへの接続とカーソルの生成
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            # データベース生成
            cursor.execute('CREATE DATABASE IF NOT EXISTS db_%s;' %
                           project.name())
            # 生成したデータベースに移動
            cursor.execute('USE db_%s;' % project.name())
            # テーブル初期化(DROP)
            cursor.execute('DROP TABLE IF EXISTS table_ingredients;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_ingredients` (
                    `ingredient_id` int(100) unsigned NOT NULL AUTO_INCREMENT,
                    `ingredient_name` varchar(255) NOT NULL DEFAULT '',
                    PRIMARY KEY (`ingredient_id`),
                    UNIQUE KEY (`ingredient_name`)
                ); """)
            # データの追加
            cursor.execute("""
                INSERT INTO table_ingredients (ingredient_name)
                    VALUES ('たまご'),('きのこ'),('ベーコン'),('パスタ麺'),('ほうれん草')
                           ,('牛肉'),('じゃがいも'),('人参'),('玉ねぎ'),('白滝')
                           ,('水'),('醤油'),('砂糖'),('みりん'),('ほんだし')
                           ,('鶏肉'),('にんにく'),('塩こしょう'),('オリーブオイル'),('キャベツ')
                           ,('トマト'),('薄力粉'),('ホットケーキミックス'),('ピーマン'),('ハム')
                           ,('ケチャップ'),('スライスチーズ'),('ひき肉'),('ご飯'),('生姜')
                           ,('オイスターソース'),('ソース'),('チリパウダー'),('カレールー'),('ウスターソース')
                           ,('ツナ'),('豆腐'),('豆板醤'),('料理酒'),('水溶き片栗粉')
                           ,('ごま油'),('ねぎ'),('ウインナー'),('サラダ油'),('マヨネーズ')
                           ,('バター'),('塩'),('しめじ')
                    """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find_ingredient(id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
             # 対応する名前を返す
            cursor.execute("""
                SELECT ingredient_name FROM table_ingredients
                WHERE ingredient_id = %s ;""",
                           (id,))
            con.commit()
            recode = cursor.fetchall()
        name = recode
        return name

    @staticmethod
    def find(ingredient_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_ingredients
                WHERE  ingredient_id = %s;
            """, (ingredient_id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        #import pdb; pdb.set_trace()
        data = results[0]
        ing = ingredient()
        ing.attr["ingredient_id"] = data["ingredient_id"]
        ing.attr["ingredient_name"] = data["ingredient_name"]
        return ing

    @staticmethod
    def find_nametoingredient_id(word):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT ingredient_id
                FROM   table_ingredients
                WHERE  ingredient_name = %s;
            """, (word,))
            results = cursor.fetchall()
        # import pdb
        # pdb.set_trace()
        if (len(results) == 0):
            return None
        recode = results[0]
        i_id = recode[0]
        return i_id
