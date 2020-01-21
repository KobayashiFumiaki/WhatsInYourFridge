import MySQLdb

from db import DBConnector
from model.project import project
from model.recipe import recipe


class recipes_number:
    """レシピの順番モデル"""

    def __init__(self):
        self.attr = {}
        self.attr["recipe_number_id"] = None         # recipe_number_id int
        self.attr["cooking_id"] = None               # cooking_id int notNull
        # recipe_number str notNull
        self.attr["recipe_number"] = None
        # recipe_description str notNull
        self.attr["recipe_description"] = None

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
            cursor.execute('DROP TABLE IF EXISTS table_recipes_number;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_recipes_number` (
                    `recipe_number_id` int(100) unsigned NOT NULL AUTO_INCREMENT,
                    `recipe_id` int(100) NOT NULL ,
                    `cooking_id` int(100) NOT NULL  ,
                    `recipe_number` int(100) NOT NULL ,
                    PRIMARY KEY (`recipe_number_id`),
                    UNIQUE KEY (`recipe_id`,`cooking_id`)
                ); """)
            # データの追加
            cursor.execute("""
                INSERT INTO table_recipes_number (recipe_id,cooking_id,recipe_number)
                    VALUES ('25','1','1'),('26','1','2'),('27','1','3'),('28','1','4'),('29','1','5'),('30','1','6')
                          ,('31','2','1'),('32','2','2'),('33','2','3'),('34','2','4'),('35','2','5'),('36','2','6'),('37','2','7')
                          ,('38','3','1'),('39','3','2'),('40','3','3'),('41','3','4'),('42','3','5')
                          ,('43','4','1'),('44','4','2'),('45','4','3')
                          ,('46','5','1'),('47','5','2'),('48','5','3')
                          ,('49','6','1'),('50','6','2'),('51','6','3'),('52','6','4'),('53','6','5'),('54','6','6'),('55','6','7'),('56','6','8')
                          ,('57','7','1'),('58','7','2'),('59','7','3'),('60','7','4'),('61','7','5'),('62','7','6'),('63','7','7')
                    """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find_recipe_id(cid):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT recipe_id FROM table_recipes_number
                WHERE cooking_id = %s;
                """, (cid,))
            con.commit()
            results = cursor.fetchall()

        r_id = [result["recipe_id"] for result in results]
        # import pdb
        # pdb.set_trace()
        return r_id

    @staticmethod
    def find_recipe_number(cid):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT recipe_number FROM table_recipes_number
                WHERE cooking_id = %s;
                """, (cid,))
            con.commit()
            results = cursor.fetchall()

        r_number = [result["recipe_number"] for result in results]
        # import pdb
        # pdb.set_trace()
        return r_number
