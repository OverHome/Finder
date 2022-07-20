import re
import requests
from yandex_music import Client
from bs4 import BeautifulSoup


class Api:
    def __init__(self):
        self.yandex = YandexMusicApi()
        self.soundcloud = SoundCloudApi()
        self.youtube = YouTubeApi()

    def get_name(self, trek):
        a = self.yandex.client_ym.search(trek).tracks
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


class YandexMusicApi:
    def __init__(self):
        self.client_ym = Client("AQAAAAA0oQ1iAAfjTKCdkamLJEdlnd68qhGcy50")
        self.client_ym.init()

    def find_url(self, trek):
        a = self.client_ym.search(trek).best
        if a is None:
            return "https://music.yandex.ru/search?text=" + trek
        trek = a.result.trackId.split(":")
        return f"https://music.yandex.ru/album/{trek[1]}/track/{trek[0]}"

    def track_name(self, url):
        url = url.split("/")
        a = self.client_ym.tracks([url[6] + ":" + url[4]])
        trek = a[0].title
        artist = ""
        artists = a[0].artists
        artists.reverse()
        for i in artists:
            artist += i["name"] + " "
        return trek + " - " + artist


class SoundCloudApi:

    def __init__(self):
        self.client_id = "a8eOWIooPyKf3C0dApsQTVCopqEMNgDH"

    def find_url(self, trek):
        while True:
            a = requests.get(
                f"https://api-v2.soundcloud.com/search?q={trek}&client_id={self.client_id}")
            mas = a.json()
            if a.status_code == 200:
                break
        if len(mas['collection']) > 0:
            trek = mas['collection'][0]['permalink_url']
        else:
            trek = "https://soundcloud.com/search/sounds?q=" + trek
        return trek

    def track_name(self, url):
        a = requests.get(url)
        a.encoding = 'utf-8'
        soup = BeautifulSoup(a.text, "lxml")
        t = soup.find("h1")
        t = t.text.split("\n")
        return t[0]


class YouTubeApi:
    def find_url(self, trak):
        a = requests.get("https://www.youtube.com/results?search_query=" + trak)
        v = re.findall(r"watch\?v=(\S{11})", a.text)
        if len(v) == 0:
            return "https://www.youtube.com/results?search_query=" + trak
        return "https://www.youtube.com/watch?v=" + v[0]

    def track_name(self, url):
        a = requests.get(url)
        a.encoding = "utf-8"
        t = a.text.split("<title>")[1].split("</title>")[0]
        return t[:-10]
