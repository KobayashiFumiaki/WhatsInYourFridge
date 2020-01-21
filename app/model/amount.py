import MySQLdb

from db import DBConnector
from model.project import project


class amount:
    """分量モデル"""

    def __init__(self):
        self.attr = {}
        self.attr["amount_id"] = None            # amount_id int
        self.attr["ingredient_id"] = None          # ingredient_id int notNull
        self.attr["cookig_id"] = None       # cooking_img_url int notNull
        self.attr["ingredient_number"] = None  # cooking_img_url str notNull

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
            cursor.execute('DROP TABLE IF EXISTS table_amounts;')
            # テーブル初期化(CREATE)
            cursor.execute("""
                CREATE TABLE `table_amounts` (
                    `amount_id` int(100) unsigned NOT NULL AUTO_INCREMENT,
                    `ingredient_id` int(100) NOT NULL ,
                    `cooking_id` int(100) NOT NULL ,
                    `ingredient_number` varchar(255) NOT NULL DEFAULT '',
                    PRIMARY KEY (`amount_id`),
                    UNIQUE KEY (`ingredient_id`,`cooking_id`)
                ); """)
            # データの追加
            cursor.execute("""
                INSERT INTO table_amounts (ingredient_id, cooking_id, ingredient_number)
                    VALUES ('6','1','100g'),('7','1','1個'),('8','1','1/4本'),('9','1','1/4個'),('10','1','1/4袋'),('11','1','100cc'),('12','1','大1'),('13','1','大1'),('14','1','大1'),('15','1','大1/4')
                          ,('16','2','250g'),('17','2','1/2かけら'),('18','2','適量'),('19','2','小さじ1'),('20','2','適量'),('21','2','適量')
                          ,('5','3','一枚'),('9','3','少々'),('11','3','70cc'),('22','3','60g'),('23','3','大さじ2'),('24','3','半分'),('25','3','一枚'),('26','3','適量'),('27','3','一枚'),('47','3','ひとつまみ'),('48','3','一握り')
                          ,('9','4','1/4個'),('17','4','5mm'),('18','4','少々'),('21','4','1/2個'),('26','4','小さじ1'),('28','4','80g'),('29','4','一杯分'),('30','4','5mm'),('31','4','小さじ1'),('32','4','小さじ1'),('33','4','小さじ1/4')
                          ,('9','5','1個'),('11','5','150cc'),('26','5','大さじ1'),('34','5','1かけ'),('35','5','大さじ1'),('36','5','大さじ1'),('48','5','ひとつかみ')
                          ,('11','6','120cc'),('12','6','小さじ2'),('13','6','小さじ1'),('17','6','一片'),('28','6','50g'),('29','6','150g~200g'),('30','6','少々'),('37','6','1/2丁'),('38','6','小さじ1'),('39','6','大さじ1'),('40','6','少々'),('41','6','小さじ1'),('42','6','適量')
                          ,('1','7','M2個'),('9','7','1/2個'),('13','7','小さじ1/4'),('14','7','小さじ1'),('18','7','各少々'),('24','7','1個'),('26','7','大さじ5'),('29','7','300g'),('43','7','3本'),('44','7','適量'),('45','7','小さじ1/2'),('46','7','5g')
                    """)
            con.commit()

    @staticmethod
    def db_cleaner():
        with DBConnector(dbName=None) as con, con.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS db_%s;' % project.name())
            con.commit()

    @staticmethod
    def find(amount_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            cursor.execute("""
                SELECT *
                FROM   table_amounts
                WHERE  amount_id = %s;
            """, (amount_id,))
            results = cursor.fetchall()

        if (len(results) == 0):
            return None
        data = results[0]
        am = amount()
        am.attr["amount_id"] = data["amount_id"]
        am.attr["ingredient_id"] = data["ingredient_id"]
        am.attr["cooking_id"] = data["cooking_id"]
        am.attr["ingredient_number"] = data["ingredient_number"]
        #import pdb; pdb.set_trace()
        return am

    @staticmethod
    def select_by_cooking_id(cooking_id):
        # cooking_idから検索
        with DBConnector(dbName='db_%s' % project.name()) as con, \
                con.cursor(MySQLdb.cursors.DictCursor) as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT *
                FROM   table_amounts
                WHERE  cooking_id = %s;
            """, (cooking_id,))
            results = cursor.fetchall()

        records = []
        for data in results:
            am = amount()
            am.attr["amount_id"] = data["amount_id"]
            am.attr["ingredient_id"] = data["ingredient_id"]
            am.attr["cooking_id"] = data["cooking_id"]
            am.attr["ingredient_number"] = data["ingredient_number"]
            records.append(am)

        #import pdb; pdb.set_trace()
        return records

    @staticmethod
    def find_ingredient_id(cooking_id):
        # ingredient_idのみを返す
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            # 対応するidをリストで返す
            cursor.execute("""
                SELECT ingredient_id
                FROM table_amounts
                WHERE cooking_id = %s; """,
                           (cooking_id,))
            con.commit()
            recodes = cursor.fetchall()

        # import pdb
        # pdb.set_trace()
        i_id = [recode[0] for recode in recodes]
        return i_id

    @staticmethod
    def find_ingredient_idtocooking_id(i_id):
        with DBConnector(dbName='db_%s' % project.name()) as con, con.cursor() as cursor:
            cursor.execute("""
                SELECT cooking_id
                FROM table_amounts
                WHERE ingredient_id = %s; """,
                           (i_id,))
            con.commit()
            recodes = cursor.fetchall()
        return recodes
