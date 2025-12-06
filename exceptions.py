import requests


CAT_URL = "https://cataas.com/cat"  # случайный котик [web:251][web:264]


def get_cat_image(timeout: int = 15) -> bytes | None:
    """
    Делает запрос к API котиков и возвращает байты картинки.
    В случае ошибки возвращает None, чтобы бот не падал.
    """
    try:
        resp = requests.get(CAT_URL, timeout=timeout)
        resp.raise_for_status()
        return resp.content
    except Exception:
        # Здесь можно добавить логирование в файл, если понадобится
        return None
