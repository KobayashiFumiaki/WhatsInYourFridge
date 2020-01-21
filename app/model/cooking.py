import MySQLdb

from db import DBConnector
from model.project import project


class cooking:
    """クッキングモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["cooking_id"] = None            # cooking_id int
        self.attr["cooking_name"] = None          # cooking_name str notNull
        self.attr["cooking_img_url"] = None       # cooking_img_url str notNull

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
            cursor.execute('DROP TABLE IF EXISTS table_cookings;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_cookings` (
                    `cooking_id` int(100) unsigned NOT NULL AUTO_INCREMENT,
                    `cooking_name` varchar(255) NOT NULL DEFAULT '',
                    `cooking_img_url` varchar(255) NOT NULL DEFAULT '',
                    PRIMARY KEY (`cooking_id`),
                    UNIQUE KEY (`cooking_name`)
                ); """)
            # データの追加
            cursor.execute("""
                INSERT INTO table_cookings (cooking_name, cooking_img_url)
                    VALUES ('肉じゃが','../static/img/nikujyaga.jpg'),('チキンステーキ','../static/img/chickensteak.jpg')
                    ,('ピザ','../static/img/pizza.jpg'),('タコライス','../static/img/takoraisu.jpg')
                    ,('カレー','../static/img/curry.jpg'),('麻婆豆腐','../static/img/mabodofu.jpg')
                    ,('オムライス', '../static/img/omuraisu.jpg')
                    """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    def is_valid(self):
        return all([
            self.attr["cooking_id"] is None or type(
                self.attr["cooking_id"]) is int,
            self.attr["cooking_name"] is not None and type(
                self.attr["cooking_name"]) is str,
            self.attr["cooking_url"] is not None and type(
                self.attr["cooking_url"]) is str,
        ])

    @staticmethod
    def build():
        c = cooking()
        return c

    @staticmethod
    def find_nametoid(c_name):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
             # 対応するidをリストで返す
            cursor.execute("""
                SELECT cooking_id FROM table_cookings
                WHERE cooking_name = %s ;""",
                           (c_name,))
            con.commit()
            recode = cursor.fetchall()
        # cook = len(recode)
        # print(recode.__class__)
        # import pdb
        # pdb.set_trace()
        if len(recode) == 0:
            return recode
        else:
            cid = recode[0]
            cid2 = cid[0]
            return cid2

    @staticmethod
    def find_cooking_name(c_name):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
             # 対応するidをリストで返す
            cursor.execute("""
                SELECT cooking_name FROM table_cookings
                WHERE cooking_name = %s ;""",
                           (c_name,))
            con.commit()
            recode = cursor.fetchall()
        if len(recode) == 0:
            return recode
        else:
            cname = recode[0]
            cname2 = cname[0]
            return cname2

    @staticmethod
    def find_cooking_url(c_name):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
             # 対応するidをリストで返す
            cursor.execute("""
                SELECT cooking_img_url FROM table_cookings
                WHERE cooking_name = %s ;""",
                           (c_name,))
            con.commit()
            recode = cursor.fetchall()
        curl = recode[0]
        curl2 = curl[0]
        return curl2

    @staticmethod
    def find_idtoname(cid):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
             # 対応するidをリストで返す
            cursor.execute("""
                SELECT cooking_name FROM table_cookings
                WHERE cooking_id = %s ;""",
                           (cid,))
            con.commit()
            recode = cursor.fetchall()
            cooking_name = recode[0]
        return cooking_name
