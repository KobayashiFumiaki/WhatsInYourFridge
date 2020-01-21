import MySQLdb

from db import DBConnector
from model.project import project


class user:
    """ユーザーモデル"""

    def __init__(self):
        self.attr = {}
        self.attr["user_id"] = None            # user_id int
        self.attr["user_name"] = None              # user_name str notNull
        self.attr["password"] = None           # password str notNull
        self.attr["token"] = None        # token str notNull

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
            cursor.execute('DROP TABLE IF EXISTS table_users;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_users` (
                    `user_id` int(11) unsigned NOT NULL AUTO_INCREMENT,
                    `user_name` varchar(255) NOT NULL DEFAULT '',
                    `password` varchar(255) NOT NULL DEFAULT '',
                    `token` varchar(255) DEFAULT NULL,
                    PRIMARY KEY (`user_id`),
                    UNIQUE KEY (`user_name`)
                ); """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(user_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_users
                WHERE  user_id = %s;
            """, (user_id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        u = user()
        u.attr["user_id"] = data["user_id"]
        u.attr["user_name"] = data["user_name"]
        u.attr["password"] = data["password"]
        return u

    def is_valid(self):
        return all([
            self.attr["user_id"] is None or type(
                self.attr["user_id"]) is int,
            self.attr["user_name"] is not None and type(
                self.attr["user_name"]) is str,
            self.attr["password"] is not None and type(
                self.attr["password"]) is str,
            self.attr["token"] is None and type(
                self.attr["token"]) is str
        ])

    @staticmethod
    def build():
        u = user()
        return u

    def save(self):
        if(self.is_valid):
            return self._db_save()
        return False

    def _db_save(self):
        if self.attr["user_id"] == None:
            return self._db_save_insert()
        return self._db_save_delete()

    def _db_save_insert(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:

            # データの保存(INSERT)
            cursor.execute("""
                INSERT INTO table_users
                    (user_name, password )
                VALUES
                    (%s, %s); """,
                           (self.attr["user_name"],
                               self.attr["password"],
                            ))

            cursor.execute("SELECT last_insert_id();")
            results = cursor.fetchone()
            self.attr["user_id"] = results[0]

            con.commit()

        return self.attr["user_id"]

    def _db_save_delete(self):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # データの削除(DELETE)
            cursor.execute("""
                DELETE FROM table_users
                WHERE user_id = %s; """,
                           (self.attr["user_id"],))
            con.commit()
        return True

    @staticmethod
    def find_by_name(user_name):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_users
                WHERE  user_name = %s;
            """, (user_name,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        u = user()
        u.attr["user_id"] = data["user_id"]
        u.attr["user_name"] = data["user_name"]
        u.attr["password"] = data["password"]
        return u
