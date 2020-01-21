import tornado.web
from model.cooking import cooking
from model.amount import amount
from model.ingredient import ingredient
from model.user import user
from model.logs import logs
from model.recipe import recipe
from model.recipes_number import recipes_number
from model.favorites import favorites
from controller.AuthenticationHandlers import SigninBaseHandler


class CookingMenuHandler(SigninBaseHandler):
    def get(self):
        # ユーザーのIDを取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))
        # htmlから入力された言葉を取得
        _word = self.get_argument("form-word", None)
        # 入力された料理のidを取得
        _cid = cooking.find_nametoid(_word)
        word = cooking.find_cooking_name(_word)

        # import pdb
        # pdb.set_trace()
        # 検索できる文字
        # 肉じゃが、ピザ、タコライス、カレー、麻婆豆腐、オムライス

        # 食材検索をするための処理
        if not word:
            # ingredient.pyからingredient_idを取得
            ingredient_id = ingredient.find_nametoingredient_id(_word)

            # 検索できない文字を検索した時の処理
            if not ingredient_id:
                _logMenuId = logs.findMenuLog(_id)

                _error = "その文字では検索できません"

                if _logMenuId == 'null':
                    _cooking_names = 'null'
                    self.render("home.html", user=_signedInUser,
                                error=_error, menulog=_cooking_names[:5])
                else:
                    # listでlog_idを取得
                    _menuLog = list(dict.fromkeys(_logMenuId))
                    # log_idで料理名を取得
                    _cooking_names = [cooking.find_idtoname(
                        log) for log in _menuLog]
                    # 日
                    # _day = datetime.date.today().day
                    # データベースに登録されている日を取得
                    # _rday = cooking.find_day()
                    # if _day
                    # homeを表示
                    self.render("home.html", user=_signedInUser,
                                error=_error, menulog=_cooking_names[:5])

            # amount.pyからingredient_idを使いcooking_idを取得
            cooking_ids = amount.find_ingredient_idtocooking_id(ingredient_id)
            _cooking_names = [cooking.find_idtoname(
                coo) for coo in cooking_ids]

            _favorites = favorites.find_favorite(_uid)

            self.render("search.html", user=_signedInUser,
                        cooking_names=_cooking_names, favorites=_favorites)

        # 料理名で検索した時の処理
        else:
            # wordがあればlogに登録する処理
            if word is not None:
                logs.post_cooking(_uid, _cid)
            # 料理の画像のurlを取得
            cooking_img_url = cooking.find_cooking_url(_word)

            # 料理IDからレシピのIDを取得
            _recipes = recipes_number.find_recipe_id(_cid)
            _recipe = [recipe.find(rec) for rec in _recipes]
            # print(_recipes.__class__)
            # print(hash['recipe_id'])

            # 料理IDからレシピのナンバーを取得
            _recipes_number = recipes_number.find_recipe_number(_cid)

            # 料理idから分量リストを取得
            _amount = amount.select_by_cooking_id(_cid)
            _ing_id = amount.find_ingredient_id(_cid)

            # 分量idから食材リストを取得
            _ingredient = [ingredient.find(ing) for ing in _ing_id]

            # お気に入り情報の取得
            _favorite = favorites.favorite(_uid, _cid)

            if len(_favorite) == 0:
                _favorite = None
            else:
                _favorite = _favorite[0][0]

            self.render("menu.html", img=cooking_img_url,
                        cooking_name=word, user=_signedInUser, amount=_amount, ingredient=_ingredient, recipes=_recipe, recipe_numbers=_recipes_number, favorite=_favorite)

    def post(self):
        # パラメータの取得
        _fid = self.get_argument("fav", None)
        _word = self.get_argument("f-word", None)

        # ユーザーのIDを取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))

        # 入力された料理のidを取得
        _cid = cooking.find_nametoid(_word)

        f = favorites.build()
        if _fid == "None":
            f.attr["favorites_id"] = None
        else:
            f.attr["favorites_id"] = _fid
        f.attr["user_id"] = _uid
        f.attr["cooking_id"] = _cid
        # import pdb
        # pdb.set_trace()
        f.save()
        # ページへリダイレクト
        self.redirect("/menu?form-word=" + _word)


class ProfileHandler(SigninBaseHandler):
    def get(self):
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))

        # ユーザーIDによるお気に入り情報の取得
        _favorites = favorites.find_favorite(_uid)
        _cooking_names = [cooking.find_idtoname(
            fav["cooking_id"]) for fav in _favorites]

        # favorites_IDを取得
        # _favorite = [fav["favorites_id"] for fav in _favorites]

        # if len(_favorite) == 0:
        #     _favorite = None
        # else:
        #     _favorite = _favorite

        self.render("profile.html", user=_signedInUser,
                    favorites=_favorites, cooking_names=_cooking_names)

    def post(self):
        # パラメータの取得
        _fid = self.get_argument("fav", None)
        _word = self.get_argument("f-word", None)

        # ユーザーのIDを取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))

        # 入力された料理のidを取得
        _cid = cooking.find_nametoid(_word)

        f = favorites.build()
        if _fid == "None":
            f.attr["favorites_id"] = None
        else:
            f.attr["favorites_id"] = _fid
        f.attr["user_id"] = _uid
        f.attr["cooking_id"] = _cid
        # import pdb
        # pdb.set_trace()
        f.save()

        # ページへリダイレクト
        self.redirect("/profile")


class SearchHandler(SigninBaseHandler):
    def get(self):
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))

        _word = self.get_argument("form-word", None)

        # ingredient.pyからingredient_idを取得
        ingredient_id = ingredient.find_nametoingredient_id(_word)
        # amount.pyからingredient_idを使いcooking_idを取得
        cooking_ids = amount.find_ingredient_idtocooking_id(ingredient_id)
        _cooking_names = [cooking.find_idtoname(
            coo) for coo in cooking_ids]

        _favorites = favorites.find_favorite(_uid)

        self.render("search.html", user=_signedInUser)

    def post(self):
        # パラメータの取得
        _fid = self.get_argument("fav", None)
        _word = self.get_argument("f-word", None)

        # ユーザーのIDを取得
        _id = tornado.escape.xhtml_escape(self.current_user)
        _uid = int(_id)
        _signedInUser = user.find(int(_id))

        # 入力された料理のidを取得
        _cid = cooking.find_nametoid(_word)

        f = favorites.build()
        if _fid == "None":
            f.attr["favorites_id"] = None
        else:
            f.attr["favorites_id"] = _fid
        f.attr["user_id"] = _uid
        f.attr["cooking_id"] = _cid
        # import pdb
        # pdb.set_trace()
        f.save()

        # ページへリダイレクト
        self.redirect("/search?form-word=" + _word)
