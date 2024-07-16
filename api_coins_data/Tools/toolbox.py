from __future__ import annotations

import fnmatch
import json
import logging
import platform
import shutil
import types

import http.client

from datetime import datetime, timezone, timedelta
import os
import time
import asyncio
import pickle
import traceback
from contextlib import contextmanager
from urllib.parse import urlparse, parse_qs, urlencode

import aiohttp


def read_large_file(file_path, limit_lines: int):
    count_lines = 0
    data_list = []

    with open(file_path, 'r') as file:
        for line in file:
            if line:
                data_list.append(line.strip())
                count_lines += 1
                if count_lines == limit_lines:
                    yield data_list
                    data_list = []
                    count_lines = 0
    # Если последняя порция данных меньше limit_lines, вернуть оставшуюся часть
    if data_list:
        yield data_list


def deserialize_json(json_data):
    """ Сериализует JSON данные в объект Python."""
    try:
        if json_data.strip():  # Проверка, что строка не пустая
            python_object = json.loads(json_data)
            return python_object
        else:
            print("Пустая строка JSON.")
            return None
    except json.JSONDecodeError as e:
        print(f"Произошла ошибка при десериализации JSON: {e}")
        return None


def split_list(lst: list, n: int):
    """
    Функция разбивает список на указанное значение [n] и возвращает срезы.
        :param lst: Список объектов.
        :param n: Количество объектов в возвращаемом срезе списка
    """
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_root_path_project(abspath_file):
    """
    Функция возвращает абсолютный путь корня проекта по файлу маркеру, файл маркер должен быть в корне проекта.
    Returns: str
    abspath: абсолютный путь вызываемого файла проекта. (__file__)
    """
    current_directory = os.path.abspath(os.path.dirname(abspath_file))  # Получаем текущую директорию скрипта
    print(f"\n{current_directory=}")
    while True:
        if os.path.exists(os.path.join(current_directory, 'project_marker_file.txt')):
            return current_directory  # Нашли файл-маркер, это корень проекта
        parent_directory = os.path.dirname(current_directory)
        print(f"{parent_directory=}")
        if parent_directory == current_directory:
            break  # Дошли до корня файловой системы, не нашли файл-маркер
        current_directory = parent_directory
    return None  # Файл-маркер не найден


def remove_directory_contents(directory_path):
    """
    Удаляет все файлы и папки в указанной директории.

    Args: directory_path (str): Путь к целевой директории.
    Returns: None
    Raises: Exception: Возникает, если произошла ошибка при удалении файлов и папок.
    """
    try:
        # Используем os.walk для обхода всех файлов и папок в директории
        for root, dirs, files in os.walk(directory_path):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)  # Удаляем файл
            for dir_i in dirs:
                dir_path = os.path.join(root, dir_i)
                shutil.rmtree(dir_path)  # Удаляем папку и её содержимое
        print(f"\nВсе файлы и папки в {directory_path} были удалены.")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


class AiohttpSession:
    def __init__(self, limit=25, ssl=False, total=320, sock_connect=160, sock_read=160, trust_env=False, logger=None):
        """
        Конструктор класса AiohttpSession.

        :param limit: Максимальное количество одновременных соединений
        :param ssl: использовать ли SSL-шифрование для соединений
        :param total: общее время ожидания для HTTP-запросов
        :param sock_connect: время ожидания соединения с сервером
        :param sock_read: время ожидания ответа от сервера
        :param trust_env: использовать ли значения настроек из системных переменных окружения
        :param logger: объект логгера для записи сообщений
        ---------------------------------------------------------------------------------------
        Обработка ошибок: добавлен объект logger, который можно использовать для записи сообщений о возникших ошибках и
        проблемах. При возникновении исключений можно использовать методы
        logger.exception() или logger.error() для записи соответствующей информации в лог.
        """
        self.limit = limit
        self.ssl = ssl
        self.total = total
        self.sock_connect = sock_connect
        self.sock_read = sock_read
        self.trust_env = trust_env
        self.logger = logger or logging.getLogger(__name__)

    def create_session(self) -> aiohttp.client.ClientSession:
        """
        Создает объект сессии для выполнения HTTP-запросов.
        :return: Объект ClientSession
        """
        conn = aiohttp.TCPConnector(
            limit=self.limit,
            ssl=self.ssl,
            enable_cleanup_closed=True,  # включить очистку закрытых соединений
            # keepalive_timeout=120, # время жизни соединения в секундах
        )

        timeout = aiohttp.ClientTimeout(
            total=self.total,
            sock_connect=self.sock_connect,
            sock_read=self.sock_read
        )

        cookie_jar = aiohttp.CookieJar()  # инициализация объекта для хранения кук

        session = aiohttp.ClientSession(
            connector=conn,
            timeout=timeout,
            trust_env=self.trust_env,
            cookie_jar=cookie_jar
        )

        self.logger.debug("Создан новый объект ClientSession")

        return session


class Style:
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'
    END_SC = '\033[0m'


def find_files_with_extension(extension, folder_path):  # extension = 'txt'; folder_path = '/data_dir'
    # Функция возвращаем список найденных файлов с указанным расширением
    found_files = []
    # Обход файловой системы, начиная с указанной папки
    for root, dirs, files in os.walk(folder_path):
        # root - текущая директория, dirs - список поддиректорий, files - список файлов в текущей директории
        for filename in fnmatch.filter(files, f'*.{extension}'):
            # Фильтруем файлы по расширению, добавляем пути к найденным файлам в список found_files
            found_files.append(os.path.join(root, filename))

    return found_files


def save_txt_data(data_txt, path_file):
    """Сохраняет текстовые данные в файл.
    Args:
        data_txt (str): текстовые данные для сохранения.
        path_file (str): путь к файлу для сохранения данных.
    """
    with open(path_file, 'w', encoding='utf-8') as f:
        f.write(str(data_txt))


def save_txt_data_complementing(data_txt, path_file):
    """Дописывает текстовые данные в конец файла.
    Args:
        data_txt (str): текстовые данные для записи.
        path_file (str): путь к файлу для записи данных.
    """
    with open(path_file, 'a', encoding='utf-8') as f:
        f.write(f"{str(data_txt)}\n")


def download_txt_data(path_file) -> str:
    """Загружает текстовые данные из файла.
    Args:
        path_file (str): путь к файлу для загрузки данных.
    Returns:
        str: загруженные текстовые данные.
    """
    with open(path_file, encoding='utf-8') as f:
        return f.read()


def save_json_complementing(json_data, path_file, ind=False):
    """Дописывает данные в формате JSON в конец файла.
    Args:
        json_data (list[dict] | dict): данные в формате JSON для записи.
        path_file (str): путь к файлу для записи данных.
        ind (bool): Флаг, указывающий на необходимость форматирования записываемых данных.
                    По умолчанию форматирование отключено.
    """
    indent = None
    if ind:
        indent = 4
    if os.path.isfile(path_file):
        # File exists
        with open(path_file, 'a', encoding='utf-8') as outfile:
            outfile.seek(outfile.tell() - 1, os.SEEK_SET)
            outfile.truncate()
            outfile.write(',\n')
            json.dump(json_data, outfile, ensure_ascii=False, indent=indent)
            outfile.write(']')
    else:
        # Create file
        with open(path_file, 'w', encoding='utf-8') as outfile:
            array = [json_data]
            json.dump(array, outfile, ensure_ascii=False, indent=indent)


def save_json_data(json_data, path_file):
    """Сохраняет данные в формате JSON в файл.
    Args:
        json_data (list[dict] | dict): данные в формате JSON для сохранения.
        path_file (str): путь к файлу для сохранения данных.
    """
    with open(path_file, 'w', encoding="utf-8") as file:
        json.dump(json_data, file, indent=4, ensure_ascii=False)


def download_json_data(path_file) -> list[dict] | dict:
    """Загружает данные в формате JSON из файла.
    Args:
        path_file (str): путь к файлу для загрузки данных.
    Returns:
        list[dict] | dict: загруженные данные в формате
    """
    with open(path_file, encoding="utf-8") as f:
        return json.load(f)


def save_pickle_data(data_pickle, path_file):
    """Сохраняет данные в файл в формате pickle"""
    with open(path_file, 'wb') as f:
        pickle.dump(data_pickle, f)


def save_complementing_pickle_data(data_pickle, path_file):
    """Дописывает данные в конец файла в формате pickle"""
    with open(path_file, 'ab') as f:
        pickle.dump(data_pickle, f)


def download_pickle_data(path_file):
    """Генератор, который поочередно возвращает объекты из файла в формате pickle"""
    with open(path_file, 'rb') as f:
        while True:
            try:
                yield pickle.load(f)
            except EOFError:
                break


def add_work_days(current_date):
    """Если текущая дата выпадает на выходной, возвращает ближайшую рабочую дату."""

    # Преобразовываем переданную дату в объект datetime
    current_datetime = datetime.fromtimestamp(current_date)
    # Определяем, является ли текущий день выходным
    is_weekend = current_datetime.weekday() >= 5
    if is_weekend:
        # Определяем количество дней, которое нужно добавить к текущей дате
        days_to_add = 7 - current_datetime.weekday()
        # Добавляем нужное количество дней к текущей дате
        current_datetime += timedelta(days=days_to_add)
    # Возвращаем результат в формате timestamp
    return current_datetime.timestamp()


def date_str(time_int, utc=False, seconds=False, standart=False):
    """Возвращает строку с датой в формате '%d/%m/%y %H:%M' или '%H:%M:%S' (если seconds=True).
            Если standart=True - '%y-%m-%d'
           Если utc=True, то время будет возвращено в UTC"""
    if time_int > 1670000000000:
        time_int = time_int // 1000
    if standart:
        form_str = '%Y-%m-%d'
    else:
        form_str = '%H:%M:%S' if seconds else '%d/%m/%y %H:%M'
    return datetime.fromtimestamp(time_int, tz=timezone.utc).strftime(form_str) if utc else datetime.fromtimestamp(
        time_int).strftime(form_str)


def get_time_from_time(_time: float):
    """ Возвращает строку с временем в формате '%H:%M:%S' """
    if _time > 1670000000000:
        _time = _time // 1000
    form_str = 'T %H:%M:%S'
    # return datetime.fromtimestamp(_time, tz=timezone.utc).strftime(form_str)
    return datetime.fromtimestamp(_time).strftime(form_str)


def date_file(time_int):
    """Возвращает строку с датой и временем в формате '%d-%m-%Y_%H-%M-%S' для имени файла"""
    if time_int > 1670000000000:
        time_int = time_int // 1000
    # form_str = '%d-%m-%Y_%H-%M-%S'
    form_str = '<br>D %d-%m-%Y <br>T %H-%M-%S'
    # form_str = '%Y-%m-%d %H:%M:%S.%f'
    return datetime.fromtimestamp(time_int).strftime(form_str)


def time_it(func):
    """
    Декоратор для замера времени выполнения функции в формате часы:минуты:секунды.
    Выводит время выполнения функции в консоль.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        total_time = end_time - start_time
        hours = int(total_time // 3600)
        minutes = int((total_time % 3600) // 60)
        seconds = round((total_time % 3600) % 60, 4)
        print(f"\nВремя выполнения функции {func.__name__}: {hours:02d}:{minutes:02d}:{seconds:.4f}")
        return result
    return wrapper


class TimeDelta:
    """
    Класс, представляющий временной интервал между двумя датами
        :param past_date: прошлая дата
        :param current_date: нынешняя или будущая
    """
    def __init__(self, past_date, current_date):
        if isinstance(past_date, datetime) and isinstance(current_date, datetime):
            self.timestamp1 = past_date.timestamp()
            self.timestamp2 = current_date.timestamp()
        elif isinstance(past_date, (int, float)) and isinstance(current_date, (int, float)):
            self.timestamp1 = past_date
            self.timestamp2 = current_date
        else:
            raise TypeError("Неподдерживаемый тип данных для past_date и current_date")

        self._calculate_diff()

    def _calculate_diff(self):
        """Вычисляет разницу между датами и записывает ее в атрибуты класса"""
        dt1 = datetime.fromtimestamp(self.timestamp1)
        dt2 = datetime.fromtimestamp(self.timestamp2)
        diff = dt2 - dt1
        self.days = diff.days
        self.hours = diff.seconds // 3600
        self.minutes = (diff.seconds // 60) % 60
        self.seconds = diff.seconds % 60

    def __str__(self):
        """Возвращает строку с описанием временного интервала"""
        return f"Разница между датами: " \
               f"{self.days} дней, {self.hours} часов, {self.minutes} минут, {self.seconds} секунд"


@contextmanager
def create_loop():
    loop_contex = None
    try:
        loop_contex = asyncio.get_event_loop()
        yield loop_contex
    finally:
        if loop_contex:
            if not loop_contex.is_closed():
                all_tasks = asyncio.all_tasks(loop_contex)
                if not all_tasks:
                    print("\nВсе задачи выполнены...")
                else:
                    for t, task in enumerate(all_tasks, start=1):
                        # print(f"[{t}] {task}\n{task.done()=}")
                        # print('--' * 40)
                        task.cancel()
                loop_contex.close()
                time.sleep(2)


class UrlParser:
    def __init__(self, url):
        # Разбиваем URL на составляющие и сохраняем в self.parsed_url
        self.parsed_url = urlparse(url)
        # Получаем параметры запроса и сохраняем в self.query_params
        self.query_params = parse_qs(self.parsed_url.query)

    def get_scheme(self):
        # Возвращает схему (http, https, ftp и т.д.)
        return self.parsed_url.scheme

    def get_domain(self):
        # Возвращает доменное имя
        return self.parsed_url.netloc

    def get_path(self):
        # Возвращает путь
        return self.parsed_url.path

    def get_query_params(self):
        # Возвращает параметры запроса в виде словаря
        return self.query_params

    def set_query_param(self, key, value):
        # Изменяет значение параметра запроса с заданным ключом на заданное значение
        self.query_params[key] = [value]

    def set_query_params(self, params: dict):
        # Задает новые параметры запроса
        # принимает словарь параметров запроса, а метод
        self.query_params = params

    def build_url(self):
        # Преобразует словарь параметров запроса в строку запроса и возвращает полный URL-адрес
        query_string = urlencode(self.query_params, doseq=True)
        return f"{self.get_scheme()}://{self.get_domain()}{self.get_path()}?{query_string}"


def get_system_information():
    # Получение информации о системе
    system_info = platform.uname()
    # Получение информации о версии Python
    python_version = platform.python_version()
    # Получение информации о процессоре
    processor = platform.processor()
    # Получение информации о системе (имя и версия)
    # system_name = platform.system()
    system_version = platform.version()
    # Получение информации о версии операционной системы
    os_release = platform.release()
    # Формирование упорядоченного текста
    computer_info = f"Система: {system_info.system}\n" \
                    f"Узел сети: {system_info.node}\n" \
                    f"Выпуск: {os_release}\n" \
                    f"Версия системы: {system_version}\n" \
                    f"Версия Python: {python_version}\n" \
                    f"Процессор: {processor}"
    return computer_info


class TgBot3000:
    try:
        conf = download_pickle_data('/home/pavelpc/conf3000.bin').__next__()
    except FileNotFoundError:
        conf = {}
    def __init__(self):
        self.token = self.conf['tb3000']
        print(f'Token: {self.token}')
        self.chat_id = self.conf['mci']
        self.base_url = f"https://api.telegram.org/bot{self.token}/"

    def send_message(self, text):
        method = "sendMessage"
        url = f"{self.base_url}{method}"
        data = {
            "chat_id": self.chat_id,
            "text": text
        }
        self._send_request(url, data)

    def send_photo(self, photo_bytes=b'', photo_path='', caption=None):
        """
        Отправляет изображение в чат.
            :photo_path (str): Путь к изображению на локальном компьютере.
            :caption (str, опционально): Подпись к изображению.

        Возвращает:
        dict: Ответ от Telegram API в виде словаря.
        """

        photo = photo_bytes
        if photo_path:
            photo = photo_path

        method = "sendPhoto"
        url = f"{self.base_url}{method}"
        data = {
            "chat_id": self.chat_id,
        }
        if caption:
            data["caption"] = caption
        self._send_multipart_request(url, data, photo)

    @staticmethod
    def _send_request(url, data):
        encoded_data = urlencode(data)
        encoded_data = encoded_data.encode("utf-8")
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Content-Length": len(encoded_data)
        }
        conn = http.client.HTTPSConnection("api.telegram.org")
        conn.request("POST", url, body=encoded_data, headers=headers)
        response = conn.getresponse()
        response_data = response.read()
        conn.close()
        return json.loads(response_data.decode("utf-8"))

    def _send_multipart_request(self, url, data, photo):
        boundary = "----Boundary"
        data["boundary"] = boundary
        body = self._create_multipart_body(data, photo, boundary)
        headers = {
            "Content-Type": f"multipart/form-data; boundary={boundary}"
        }
        conn = http.client.HTTPSConnection("api.telegram.org")
        conn.request("POST", url, body=body, headers=headers)
        response = conn.getresponse()
        response_data = response.read()
        conn.close()
        return json.loads(response_data.decode("utf-8"))

    @staticmethod
    def _create_multipart_body(data, photo, boundary):
        body = []
        if isinstance(photo, bytes):
            file_path = "error.png"
        else:
            file_path = photo
        for key, value in data.items():
            body.append(f"--{boundary}".encode("utf-8"))  # Преобразуйте в байты
            body.append(f'Content-Disposition: form-data; name="{key}"'.encode("utf-8"))  # Преобразуйте в байты
            body.append(b"")  # Пустая строка в байтах
            body.append(value.encode("utf-8"))  # Преобразуйте в байты
        body.append(f"--{boundary}".encode("utf-8"))  # Преобразуйте в байты
        body.append(f'Content-Disposition: form-data; name="photo"; filename="{file_path}"'.encode("utf-8"))
        body.append(b"Content-Type: application/octet-stream")  # Преобразуйте в байты
        body.append(b"")  # Пустая строка в байтах

        if isinstance(photo, bytes):
            body.append(photo)
        else:
            with open(photo, "rb") as file:
                body.append(file.read())
        body.append(f"--{boundary}--".encode("utf-8"))  # Преобразуйте в байты
        body.append(b"")  # Пустая строка в байтах
        return b"\r\n".join(body)  # Преобразуйте в байты


def format_error_from_handler(dict_error_handler, display_html=None):
    data_error = dict_error_handler['error']

    str_info_error = (f"{'==' * 60}\nDATETIME: {data_error['DATETIME']}\n"
                      f"FUNC_NAME: {data_error['FUNC_NAME']}\n"
                      f"PATH_MODULE: {data_error['PATH_MODULE']}\n"
                      f"ERROR_IN_LINE: {data_error['ERROR_IN_LINE']}\n"
                      f"ERROR_CODE_STR: {data_error['ERROR_CODE_STR']}\n"
                      f"ARGUMENTS: {data_error['ARGUMENTS']}\n"
                      f"ERROR: {data_error['ERROR']}\n\n"
                      f"input_data: {dict_error_handler['input_data']}\n\n"
                      f"sys_info: {dict_error_handler['sys_info']}\n").strip()
    if display_html:
        str_info_error = str_info_error.replace('\n', '<br>')
    return str_info_error


def error_handler(func: types.FunctionType):
    def wrapper(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
            return result
        except Exception as e:
            traceback_info = traceback.extract_tb(e.__traceback__)[-1]

            er = {
                "error": {
                    "DATETIME": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "FUNC_NAME": func.__name__,
                    "PATH_MODULE": func.__code__.co_filename,
                    "ERROR_IN_LINE": traceback_info.lineno,
                    "ERROR_CODE_STR": traceback_info.line,
                    "ARGUMENTS": f"positional: {args}, named: {kwargs}",
                    f"ERROR": traceback.format_exc()},

                "input_data": {"ARGS": str(list(args)), "KWARGS": str(kwargs)},
                "sys_info": get_system_information()
            }
            # print(f"{Style.RED}{er['error']}{Style.END_SC}")
            print({"error": format_error_from_handler(er, display_html=True)})

            path_error_data_file = os.path.join(os.path.dirname(__file__), f"error_{er['error']['FUNC_NAME']}.json")
            save_json_complementing(json_data=er, path_file=path_error_data_file, ind=True)
            return er
    return wrapper


def async_error_handler(func):
    async def wrapper(*args, **kwargs):
        try:
            result = await func(*args, **kwargs)
            return result
        except Exception as e:
            traceback_info = traceback.extract_tb(e.__traceback__)[-1]
            er = {
                "error": {
                    "DATETIME": datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'),
                    "FUNC_NAME": func.__name__,
                    "PATH_MODULE": func.__code__.co_filename,
                    "ERROR_IN_LINE": traceback_info.lineno,
                    "ERROR_CODE_STR": traceback_info.line,
                    "ARGUMENTS": f"positional: {args}, named: {kwargs}",
                    f"ERROR": traceback.format_exc()},

                "input_data": {"ARGS": list(args), "KWARGS": kwargs},
                "sys_info": get_system_information()
            }
            print(f"{Style.RED}{er['error']}{Style.END_SC}")
            return er
    return wrapper


# class OpenAITranscriber:
#     def __init__(self, api_key):
#         self.api_key = api_key
#         openai.api_key = self.api_key
#
#     def transcribe_audio(self, model, audio_path):
#         with open(audio_path, "rb") as audio_file:
#             transcript = openai.Audio.transcribe(model, audio_file)
#             return transcript


if __name__ == '__main__':
    bot = TgBot3000()

    # Отправка сообщения
    message_text = "SSSSSSSSS!"
    bot.send_message(message_text)

    # Отправка изображения
    # photo_path = "110600528.jpeg"  # Укажите путь к изображению
    # photo_caption = "Красивый пейзаж"
    # bot.send_photo(photo_path=photo_path, caption=photo_caption)
