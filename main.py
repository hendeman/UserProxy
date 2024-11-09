from time import sleep

from logs.logs import setup_logging, p_log
from setting import PROXIES, USERS, EMAIL_PROXY_LIST
from utils.all_function import format_proxy_url, format_email, is_valid
from utils.file_manager import load_file_lines, save_file


def get_email_ip():
    while True:
        proxies_dict = format_proxy_url(load_file_lines(PROXIES))
        email_list = format_email(load_file_lines(USERS))
        if not email_list:
            p_log(f"Список {USERS} пуст", level='warning')
            return
        if not proxies_dict:
            p_log(f"Список {USERS} пуст", level='warning')
            return
        proxies_valid = is_valid(proxies_dict)
        if proxies_valid:
            email_ip_list = []
            for email in email_list:
                email_ip = (email, next(iter(proxies_valid)))
                p_log(f'{email_ip[0]}:{email_ip[1]}')
                email_ip_list.append(f'{email_ip[0]}:{email_ip[1]}')
            save_file(email_ip_list, EMAIL_PROXY_LIST)
        else:
            p_log("Нет валидных прокси", level='warning')
        sleep(60)


if __name__ == "__main__":
    setup_logging()
    get_email_ip()
