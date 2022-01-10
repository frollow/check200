import csv
import time
import requests

from data import data
from random import random
from fake_useragent import UserAgent

ua = UserAgent()


# сохраняем запись в файл csv
def save_doc(url, status, platform):
    with open("names.csv", "a", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow((url, status, platform))


# проверяем статус запроса
def check_200(data):
    for url in data:
        # задаем User agent браузера (рандомный)
        headers = {"User-Agent": ua.random}
        status = requests.get(url, headers=headers, allow_redirects=False)
        # проверяем платформу или любые другие параметры запроса
        if status.status_code == 404:
            platform = "Page_404"
        elif "x-platform" in status.headers.keys():
            platform = status.headers["x-platform"]
        elif (
            "x-platform" not in status.headers.keys()
            and status.status_code == 200
        ):
            platform = "Custom_HTML"
        else:
            platform = "Other"
        # сохраняем запись в файл csv
        save_doc(url, status.status_code, platform)
        # выводим в консоль
        print("Запись добавлена в файл: ", status.status_code, url, platform)
        # ждем менее секунды и смотрим другую страницу
        sec = random() / 2
        time.sleep(sec)


check_200(data)
