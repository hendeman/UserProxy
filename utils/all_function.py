import threading
import requests

from logs.logs import p_log
from setting import API_URL


def format_proxy_url(load_proxies_list: list) -> dict:
    """Функция для преобразования строки вида
    185.162.130.86:10001:90b3f1baa62f85ee:RNW78Fm5
    в словарь с ключами
    '{ip}:{port}':{'link': 'http://{username}:{password}@{ip}:{port}', 'status': None} """

    proxies_dict = {}
    for proxi in load_proxies_list:
        parsed_proxy = proxi.split(":")
        if len(parsed_proxy) == 4:
            ip = parsed_proxy[0]
            port = parsed_proxy[1]
            username = parsed_proxy[2]
            password = parsed_proxy[3]
            proxy = f"http://{username}:{password}@{ip}:{port}"
            proxies_dict[f'{ip}:{port}'] = {'link': proxy, 'status': None}
    return proxies_dict


def format_email(load_email_list: list) -> list:
    """Функция для получения email из email:password"""

    email_list = []
    for user in load_email_list:
        parsed_user = user.split(":")
        if len(parsed_user) >= 2:
            email_list.append(parsed_user[0])
    return email_list


def check_proxy(proxy: str, dct: dict, key: str) -> None:
    """Функция для проверки прокси и получения статуса ответа."""

    url = API_URL
    try:
        response = requests.get(url, proxies={"http": proxy, "https": proxy}, timeout=5)
        if response.status_code == 200:
            dct[key]['status'] = 200
        else:
            dct[key]['status'] = None
            p_log(f"Неверный ответ для {key}:{response.status_code}", level='debug')
    except Exception as err:
        dct[key]['status'] = None
        p_log(f"Ошибка прокси {key} -- {err}", level='debug')


def is_valid(proxies_dict: dict) -> dict:
    threads = []

    for key, data in proxies_dict.items():
        thread = threading.Thread(target=check_proxy, args=(data['link'], proxies_dict, key))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    return {key: value for key, value in proxies_dict.items() if value['status'] == 200}
