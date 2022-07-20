import os
import sqlite3
from flask import *
from api import Api

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = os.urandom(20).hex()
api = Api()


@app.route("/find")
def find_all_trek():
    trek = request.args.get('trek')
    trek_full_name = get_full_name(trek)
    ym = api.yandex.find_url(trek_full_name)
    sc = api.soundcloud.find_url(trek_full_name)
    yt = api.youtube.find_url(trek_full_name)
    f = open("templates/result.html", encoding='utf-8')
    ht = f.read()
    ht = ht.replace("ymurl", ym).replace("scurl", sc).replace("yturl", yt).replace("res_name", trek_full_name)
    if "login" in session:
        ht = ht.replace("Войти", "Профиль").replace("/login", "/profile")
    return ht


@app.route("/")
def index():
    f = open("templates/index.html", encoding="utf-8")
    ret = f.read()
    if "login" in session:
        ret = ret.replace("Войти", "Профиль").replace("/login", "/profile")
    return ret


@app.route("/login")
def login():
    f = open("templates/login.html", encoding="utf-8")
    return f.read()


@app.route("/register")
def register():
    f = open("templates/login.html", encoding="utf-8")
    st = f.read().replace("register", "login").replace("login_chek", "register_chek").replace("Войти", "Рег").replace(
        "Регистрация", "Войти").replace("Рег", "Регистрация").replace("17", "37")
    return st


@app.route("/exit")
def exit():
    session.pop("login")
    return redirect("/")


@app.route("/login_chek")
def login_chek():
    login = request.args.get('login')
    password = request.args.get('password')
    db = sqlite3.connect("Database/finder.db")
    cur = db.cursor()
    req = f"SELECT * FROM users WHERE login = '{login}'"
    a = cur.execute(req)
    for i in a:
        if i[1] == password:
            session['login'] = login
    return redirect("/")


@app.route("/register_chek")
def register_chek():
    login = request.args.get('login')
    password = request.args.get('password')
    db = sqlite3.connect("Database/finder.db")
    cur = db.cursor()
    req = f"SELECT * FROM users WHERE login = '{login}'"
    a = cur.execute(req)
    inbase = False
    for i in a:
        inbase = True
        break
    if inbase:
        return redirect("/register")
    else:
        req = f"INSERT INTO users VALUES(?,?)"
        cur.execute(req, (login, password))
        db.commit()
        session['login'] = login
        return redirect("/")


@app.route("/like")
def like():
    trek = request.args.get('trek')
    if "login" not in session:
        return redirect("/login")
    login = session['login']
    db = sqlite3.connect("Database/finder.db")
    cur = db.cursor()
    req = f"INSERT INTO likes VALUES(?,?)"
    cur.execute(req, (login, trek))
    db.commit()
    return redirect("/profile")


@app.route("/profile")
def profile():
    f = open("templates/profile.html", encoding="utf-8")
    res = f.read()
    if "login" not in session:
        return redirect("/login")
    res = res.replace("login", "exit").replace("Войти", "Выйти")
    login = session['login']
    db = sqlite3.connect("Database/finder.db")
    cur = db.cursor()
    req = f"SELECT * FROM likes WHERE login = '{login}'"
    treks = cur.execute(req)
    for i in treks:
        res += f"""<p><form class="", action="/find", method="get">
                        <input type="hidden" name="trek" id="trek" value="{i[1]}">
                        <input class="btn btn-primary btn-block custom" type="submit", value="{i[1]}">
                    </form></p>"""
    res += """</div>
            </body>
        </html>"""
    return res


def get_full_name(trek):
    if "music.yandex.ru" in trek:
        return api.yandex.track_name(trek)
    elif "soundcloud.com" in trek:
        return api.soundcloud.track_name(trek)
    elif "youtu.be" in trek or "youtube.com" in trek:
        return api.youtube.track_name(trek)
    else:
        return api.get_name(trek)


# if __name__ == "__main__":
app.run()
