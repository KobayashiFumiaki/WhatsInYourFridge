import tornado.web
import re
import hashlib  # パスワード暗号化のためのライブラリ
from model.user import user

# 認証を必要とするページは、このクラスを継承する


class SigninBaseHandler(tornado.web.RequestHandler):
    def get_current_user(self):
        return self.get_secure_cookie("user")

# # サインイン後の画面サンプル


# class SignedinPageHandler(SigninBaseHandler):
#     # サインイン完了後のページ用サンプル(以下のimportが必須)
#     # from controller.SigninHandlers import SigninBaseHandler
#     # from model.user import user
#     def get(self):
#         if not self.current_user:
#             self.redirect("/signin")
#             return
#         # サインインユーザーの取得
#         _id = int(tornado.escgape.xhtml_escape(self.current_user))
#         _signedInUser = user.find(_id)

#         # その他必要な処理をここで

#         # ダッシュボードを表示
#         self.render("dashboard.html", user=_signedInUser)

# # サインイン


class SigninHandler(SigninBaseHandler):
    def get(self):
        # パラメータを取得(2つ目の引数は、取得できない場合の初期値を設定できます。)
        _message = self.get_argument("message", None)
        messages = []
        if _message is not None:
            messages.append(_message)
        _errors = []

        # サインイン画面の表示(パラメータにメッセージが設定されていればそれを渡す)
        self.render("signin.html", errors=_errors)

    def post(self):
        # パラメータの取得
        _name = self.get_argument("form-name", None)
        _raw_pass = self.get_argument("form-password", None)

        # エラーメッセージの初期化
        _errors = []

        # 入力項目の必須チェック
        if _name == None or _raw_pass == None:
            if _name == None:
                _errors.append("Nameを入力してください")
            if _raw_pass == None:
                _errors.append("Passwordを入力してください")
            self.render("signin.html", errors=_errors, messages=[])
            return

        # 入力されたパスワードをsha224で一方向の暗号化
        _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

        # nameでユーザー情報を取得
        u = user.find_by_name(_name)

        # 認証(ユーザーが存在する & パスワードが一致する で認証OK)
        if u == None or _pass != u.attr["password"]:
            # 認証失敗
            _errors.append(
                "Nameかパスワードが間違っています")
            self.render("signin.html", errors=_errors, messages=[])
            return

        # DBに保管されたユーザーIDを文字列化して暗号化Cookieに格納
        self.set_secure_cookie("user", str(u.attr["user_id"]))
        # 認証が必要なページへリダイレクト
        self.redirect("/")

# サインアウト


class SignoutHandler(SigninBaseHandler):
    def get(self):
        # 認証済みの暗号化Cookieを削除
        self.clear_cookie("user")
        # サインイン画面へリダイレクト(サインアウト完了の旨を添えて)
        self.redirect("/signin?message=%s" %
                      tornado.escape.url_escape("You are now signed out."))

# サインアップ(ユーザー登録)


class SignupHandler(SigninBaseHandler):
    def get(self):
        # サインイン画面の表示
        self.render("signup.html", errors=[])

    def post(self):
        # パラメータの取得
        _name = self.get_argument("form-name", None)
        _raw_pass = self.get_argument("form-password", None)
        # import pdb
        # pdb.set_trace()

        # 入力項目の必須チェック
        errors = []
        if not _name:
            self.render("signup.html",
                        errors="Nameを入力してください", messages=[])
        if not _raw_pass:
            self.render("signup.html",
                        errors="Passwordを入力してください", messages=[])
        if len(errors) > 0:  # エラーはサインイン画面に渡す
            self.render("signup.html")
            return
        if self.check_name(_name):
            if self.check_pass(_raw_pass):
                # 入力されたパスワードをsha224で一方向の暗号化
                _pass = hashlib.sha224(_raw_pass.encode()).hexdigest()

                # nameでユーザー情報を取得
                u = user.find_by_name(_name)

                # IDの重複を許可しない
                if u is not None:
                    self.render("signup.html", errors=[
                                "そのユーザIDはすでに使われています"], messages=[])
                    return

                # ユーザー情報を保存
                u = user.build()
                u.attr["user_name"] = _name
                u.attr["password"] = _pass
                u.save()

                # サインイン画面へリダイレクト(サインイン完了の旨を添えて)
                self.redirect("/signin?message=%s" % tornado.escape.url_escape(
                    "ユーザ登録成功しました"))
            else:
                self.render("signup.html",
                            errors="そのパスワードは登録できません", messages=[])
                return
        else:
            self.render("signup.html", errors="そのユーザーIDは登録できません", messages=[])
            return

    def check_name(self, name):
        m = re.search(r'\A[a-z\d]{8,100}\Z(?i)', name)
        return True if m else False

    def check_pass(self, _pass):
        m = re.search(
            r'\A(?=.*?[a-z])(?=.*?[A-Z])(?=.*?\d)[a-zA-Z\d]{8,100}\Z', _pass)
        return True if m else False
