import MySQLdb
import datetime
from decimal import Decimal

from db import DBConnector
from model.project import project


class logs:
    """ログモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["access_log_id"] = None       # access_log_id_id int
        self.attr["user_id"] = None             # user_id int notNull
        self.attr["cooking_id"] = None          # cooking_id int notNull
        self.attr["ymd"] = None                 # ymd_id str notNull

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
            cursor.execute('DROP TABLE IF EXISTS table_logs;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_logs` (
                    `access_log_id` int(100) unsigned NOT NULL AUTO_INCREMENT,
                    `user_id` int(100) NOT NULL ,
                    `cooking_id` int(100) NOT NULL ,
                    `ymd` varchar(255) NOT NULL,
                    PRIMARY KEY (`access_log_id`)
                ); """)

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def post_cooking(uid, cid):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの追加
            now = datetime.datetime.now()
            ymd = now.year*100 + now.month + now.day
            cursor.execute("""
                INSERT INTO table_logs (user_id,cooking_id,ymd) VALUES (%s,%s,%s); """, (uid, cid, ymd,))
            con.commit()

    @staticmethod
    def findMenuLog(uid):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT cooking_id FROM table_logs
                WHERE user_id = %s ORDER BY access_log_id DESC;""",
                           (uid,))
            results = cursor.fetchall()
        if(len(results) == 0):
            return 'null'
        # import pdb
        # pdb.set_trace()
        return results
