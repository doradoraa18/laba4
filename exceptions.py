import os
import random
import requests


BASE_URL = "https://api.unsplash.com"


class ApiError(Exception):
    """Ошибка при работе с внешним API."""
    pass


def _get_headers() -> dict:
    """
    Заголовки для запросов к Unsplash.
    Читает UNSPLASH_ACCESS_KEY из переменных окружения.
    """
    access_key = os.getenv("UNSPLASH_ACCESS_KEY")
    if not access_key:
        raise ApiError("Отсутствует ключ UNSPLASH_ACCESS_KEY")
    return {"Authorization": f"Client-ID {access_key}"}


def search_image(keyword: str, per_page: int = 10, timeout: int = 15) -> bytes | None:
    """
    1-й режим: поиск картинок по ключевым словам.

    GET /search/photos?query=<keyword>&per_page=<per_page>
    """
    try:
        url = f"{BASE_URL}/search/photos"
        params = {
            "query": keyword,
            "per_page": per_page,
        }

        resp = requests.get(url, params=params, headers=_get_headers(), timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        if not results:
            return None

        photo = random.choice(results)
        image_url = photo["urls"]["regular"]

        img_resp = requests.get(image_url, timeout=timeout)
        img_resp.raise_for_status()
        return img_resp.content
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Ошибка поиска изображения: {e}") from e


def random_image(timeout: int = 15) -> bytes | None:
    """
    2-й режим: случайная картинка.

    GET /photos/random
    """
    try:
        url = f"{BASE_URL}/photos/random"
        resp = requests.get(url, headers=_get_headers(), timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        if isinstance(data, list):
            photo = random.choice(data)
        else:
            photo = data

        image_url = photo["urls"]["regular"]

        img_resp = requests.get(image_url, timeout=timeout)
        img_resp.raise_for_status()
        return img_resp.content
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Ошибка получения случайного изображения: {e}") from e


def popular_image(topic: str = "trending", per_page: int = 15, timeout: int = 15) -> bytes | None:
    """
    3-й режим: популярные изображения по теме.

    GET /search/photos?query=<topic>&order_by=popular&per_page=<per_page>
    """
    try:
        url = f"{BASE_URL}/search/photos"
        params = {
            "query": topic,
            "order_by": "popular",
            "per_page": per_page,
        }

        resp = requests.get(url, params=params, headers=_get_headers(), timeout=timeout)
        resp.raise_for_status()
        data = resp.json()

        results = data.get("results", [])
        if not results:
            return None

        photo = random.choice(results)
        image_url = photo["urls"]["regular"]

        img_resp = requests.get(image_url, timeout=timeout)
        img_resp.raise_for_status()
        return img_resp.content
    except ApiError:
        raise
    except Exception as e:
        raise ApiError(f"Ошибка получения популярного изображения: {e}") from e
