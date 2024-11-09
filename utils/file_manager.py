from logs.logs import p_log


def load_file_lines(file_path: str) -> list:
    """Чтение строк из файла."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        p_log(f"Ошибка: {file_path} не найден.", level='warning')
        return []


def save_file(lst: list, file_path: str) -> None:
    """Запись строк в файл."""
    with open(file_path, 'w', encoding='utf-8') as file:
        for pair in lst:
            file.write(f"{pair}\n")
        p_log(f"Данные успешно сохранены в {file_path}", level='debug')
