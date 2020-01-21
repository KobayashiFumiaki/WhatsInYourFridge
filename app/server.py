#!/bin/env python
# -*- coding: utf-8 -*-
import tornado.ioloop
import tornado.web
import datetime
import os
import sys
from model.user import user
from model.cooking import cooking
from model.ingredient import ingredient
from model.amount import amount
from model.recipe import recipe
from model.recipes_number import recipes_number
from model.favorites import favorites
from model.logs import logs
from controller.CookingHandlers import CookingMenuHandler, ProfileHandler, SearchHandler
from controller.AuthenticationHandlers import SigninBaseHandler, SigninHandler, SignupHandler, SignoutHandler


class MainHandler(SigninBaseHandler):

    def get(self):
        if not self.current_user:
            self.redirect("/signin")
            return

        # サインインユーザーの取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))
        # htmlから入力されたwordを取得
        _word = self.get_argument("form-word", None)
        # 取得したwordからデータベースに検索し料理名を取得する
        word = cooking.find_cooking_name(_word)

        _menu = []
        _error = []
        # user_idからlog_idを取得
        _logMenuId = logs.findMenuLog(_id)

        if _logMenuId == 'null':
            _cooking_names = 'null'
            self.render("home.html", user=_signedInUser,
                        cooking_name=word, error=_error, menulog=_cooking_names[:5])
        else:
            # listでlog_idを取得
            _menuLog = list(dict.fromkeys(_logMenuId))
            # log_idで料理名を取得
            _cooking_names = [cooking.find_idtoname(log) for log in _menuLog]
            # 日
            # _day = datetime.date.today().day
            # データベースに登録されている日を取得
            # _rday = cooking.find_day()
            # if _day
            # homeを表示
            self.render("home.html", user=_signedInUser,
                        cooking_name=word, error=_error, menulog=_cooking_names[:5])


application = tornado.web.Application([
    (r"/", MainHandler),
    (r"/menu", CookingMenuHandler),
    (r"/signin", SigninHandler),
    (r"/signup", SignupHandler),
    (r"/signout", SignoutHandler),
    (r"/profile", ProfileHandler),
    (r"/search", SearchHandler),
],
    template_path=os.path.join(os.getcwd(),  "templates"),
    static_path=os.path.join(os.getcwd(), "static"),
    cookie_secret="x-D-#i&0S?R6w9qEsZB8Vpxw@&t+B._$",
)

if __name__ == "__main__":
    args = sys.argv
    if len(args) > 1:
        if args[1] == "migrate":
            cooking.migrate()
            ingredient.migrate()
            amount.migrate()
            recipe.migrate()
            recipes_number.migrate()
            user.migrate()
            favorites.migrate()
            logs.migrate()

        if args[1] == "db_cleaner":
            cooking.db_cleaner()
            ingredient.db_cleaner()
            amount.db_cleaner()
            recipe.db_cleaner()
            recipes_number.db_cleaner()
            user.db_cleaner()
            favorites.db_cleaner()
            logs.db_cleaner()

        if args[1] == "help":
            print("usage: python server.py migrate # prepare DB")
            print("usage: python server.py db_cleaner # remove DB")
            print("usage: python server.py # run web server")
    else:
        application.listen(3000, "0.0.0.0")
        tornado.ioloop.IOLoop.instance().start()
