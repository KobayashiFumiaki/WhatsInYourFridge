import MySQLdb

from db import DBConnector
from model.project import project


class favorites:
    """お気に入りモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["favorites_id"] = None         # favorites_id int
        self.attr["user_id"] = None  # user_id int notNull
        self.attr["cooking_id"] = None  # cooking_id int notNull

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
            cursor.execute('DROP TABLE IF EXISTS table_favorites;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_favorites` (
                    `favorites_id` int(100) unsigned NOT NULL AUTO_INCREMENT,
                    `user_id` int(255) NOT NULL ,
                    `cooking_id` int(255) NOT NULL ,
                    PRIMARY KEY (`favorites_id`)
                ); """)

            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    def is_valid(self):
        return all([
            self.attr["favorites_id"] is None or type(
                self.attr["favorites_id"]) is int,
            self.attr["user_id"] is not None and type(
                self.attr["user_id"]) is int,
            self.attr["cooking_id"] is not None and type(
                self.attr["cooking_id"]) is int
        ])

    @staticmethod
    def build():
        f = favorites()
        return f

    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    def _db_save(self):
        if self.attr["favorites_id"] == None:
            return self._db_save_insert()
        return self._db_save_delete()

    def _db_save_insert(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_favorites
                    (user_id, cooking_id )
                VALUES(%s, %s); """, (self.attr["user_id"], self.attr["cooking_id"]))
            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["favorites_id"] = results[0]

            con.commit()
        #     import pdb
        # pdb.set_trace()

        return self.attr["favorites_id"]

    def _db_save_delete(self):

        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(UPDATE)
            cursor.execute("""
                DELETE FROM table_favorites
                WHERE favorites_id = %s; """,
                           (self.attr["favorites_id"],))
            con.commit()

        return True

    @staticmethod
    def favorite(user_id, cooking_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT favorites_id
                FROM table_favorites
                WHERE user_id = %s
                    and cooking_id = %s; """,
                           (user_id, cooking_id,))
            recode = cursor.fetchall()

        f_id = recode
        return f_id

    @staticmethod
    def find_favorite(uid):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
                # 対応するidをリストで返す
            cursor.execute("""
                SELECT *
                FROM table_favorites
                WHERE user_id = %s; """,
                           (uid, ))
            recode = cursor.fetchall()

        results = recode
        # for data in results:
        #     fa = favorites()
        #     fa.attr["favorites_id"] = int(data["favorites_id"])
        #     fa.attr["user_id"] = int(data["user_id"])
        #     fa.attr["cooking_id"] = int(data["cooking_id"])
        return results
