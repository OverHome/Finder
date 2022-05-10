import os
import re
from flask import *
import requests
from yandex_music import Client
from bs4 import BeautifulSoup
import sqlite3

app = Flask(__name__, template_folder='.')
app.config['SECRET_KEY'] = os.urandom(20).hex()
client_ym = Client("AQAAAAA0oQ1iAAfjTKCdkamLJEdlnd68qhGcy50")
client_ym.init()


@app.route("/find")
def find_all_trek():
    trek = request.args.get('trek')
    trek_full_name = get_full_name(trek)
    ym = find_ym_url(trek_full_name)
    sc = find_sc_url(trek_full_name)
    yt = find_yt_url(trek_full_name)
    f = open("result.html", encoding='utf-8')
    ht = f.read()
    ht = ht.replace("ymurl", ym).replace("scurl", sc).replace("yturl", yt).replace("res_name", trek_full_name)
    if "login" in session:
        ht = ht.replace("Войти", "Профиль").replace("/login", "/profile")
    return ht


@app.route("/")
def index():
    f = open("index.html", encoding="utf-8")
    ret = f.read()
    if "login" in session:
        ret = ret.replace("Войти", "Профиль").replace("/login", "/profile")
    return ret


@app.route("/login")
def login():
    f = open("login.html", encoding="utf-8")
    return f.read()


@app.route("/register")
def register():
    f = open("login.html", encoding="utf-8")
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
    db = sqlite3.connect("finder.db")
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
    db = sqlite3.connect("finder.db")
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
    db = sqlite3.connect("finder.db")
    cur = db.cursor()
    req = f"INSERT INTO likes VALUES(?,?)"
    cur.execute(req, (login, trek))
    db.commit()
    return redirect("/profile")


@app.route("/profile")
def profile():
    f = open("profile.html", encoding="utf-8")
    res = f.read()
    if "login" not in session:
        return redirect("/login")
    res = res.replace("login", "exit").replace("Войти", "Выйти")
    login = session['login']
    db = sqlite3.connect("finder.db")
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


def find_ym_url(trek):
    a = client_ym.search(trek).best
    if a == None:
        return "https://music.yandex.ru/search?text=" + trek
    trek = a.result.trackId.split(":")
    return f"https://music.yandex.ru/album/{trek[1]}/track/{trek[0]}"


def find_sc_url(trek):
    while True:
        a = requests.get(
            f"https://api-v2.soundcloud.com/search/tracks?q={trek}&variant_ids=2487&facet=genre&user_id=838568-90079-173935-833873&client_id=W4qA1SKQWL7HBFdsmfsBzBAWHpbUmEht&limit=20&offset=0&linked_partitioning=1&app_version=1652085324&app_locale=en")
        mas = a.json()
        if a.status_code == 200:
            break
    if len(mas['collection']) > 0:
        trek = mas['collection'][0]['permalink_url']
    else:
        trek = "https://soundcloud.com/search/sounds?q=" + trek
    return trek


def find_yt_url(trak):
    a = requests.get("https://www.youtube.com/results?search_query=" + trak)
    v = re.findall(r"watch\?v=(\S{11})", a.text)
    if len(v) == 0:
        return "https://www.youtube.com/results?search_query=" + trak
    return "https://www.youtube.com/watch?v=" + v[0]


def get_ym_name(url):
    url = url.split("/")
    a = client_ym.tracks([url[6] + ":" + url[4]])
    trek = a[0].title
    artist = ""
    artists = a[0].artists
    artists.reverse()
    for i in artists:
        artist += i["name"] + " "
    return trek + " - " + artist


def get_sc_name(url):
    a = requests.get(url)
    a.encoding = 'utf-8'
    soup = BeautifulSoup(a.text, "lxml")
    t = soup.find("h1")
    t = t.text.split("\n")
    return t[0]


def get_yt_name(url):
    a = requests.get(url)
    a.encoding = "utf-8"
    t = a.text.split("<title>")[1].split("</title>")[0]
    return t[:-10]


def get_name(trek):
    a = client_ym.search(trek).tracks
    if a == None:
        return trek
    a = a.results
    trek = a[0].title
    artist = ""
    artists = a[0].artists
    artists.reverse()
    for i in artists:
        artist += i["name"] + " "
    return trek + " - " + artist


def get_full_name(trek):
    if "music.yandex.ru" in trek:
        return get_ym_name(trek)
    elif "soundcloud.com" in trek:
        return get_sc_name(trek)
    elif "youtu.be" in trek or "youtube.com" in trek:
        return get_yt_name(trek)
    else:
        return get_name(trek)


# if __name__ == "__main__":
app.run()
