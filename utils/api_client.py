"""
HTTP-клиент для работы с DummyJSON API.
"""
import time
import requests


class DummyJSONClient:
    """Клиент для работы с API DummyJSON."""

    BASE_URL = "https://dummyjson.com"

    def __init__(self):

        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json"
        })

    def _make_request(self, method: str, url: str, **kwargs) -> requests.Response:
        """Выполняет запрос с задержкой для предотвращения rate limiting."""
        # Небольшая задержка перед запросом
        time.sleep(0.5)

        try:
            response = self.session.request(method, url, **kwargs)
            return response
        except requests.exceptions.ConnectionError as e:
            # Если соединение разорвано, ждём и пробуем снова
            time.sleep(2)
            response = self.session.request(method, url, **kwargs)
            return response

    # === Auth endpoints ===

    def login(self, username: str, password: str) -> requests.Response:
        """Авторизация пользователя."""
        payload = {
            "username": username,
            "password": password
        }
        return self._make_request("POST", f"{self.BASE_URL}/auth/login", json=payload)

    def get_current_user(self, token: str) -> requests.Response:
        """Получение данных текущего пользователя."""
        headers = {"Authorization": f"Bearer {token}"}
        return self._make_request("GET", f"{self.BASE_URL}/auth/me", headers=headers)

    # === Carts endpoints ===

    def get_all_carts(self) -> requests.Response:
        """Получение всех корзин."""
        return self._make_request("GET", f"{self.BASE_URL}/carts")

    def get_cart_by_id(self, cart_id: int) -> requests.Response:
        """Получение корзины по ID."""
        return self._make_request("GET", f"{self.BASE_URL}/carts/{cart_id}")

    def get_carts_by_user(self, user_id: int) -> requests.Response:
        """Получение корзин пользователя."""
        return self._make_request("GET", f"{self.BASE_URL}/carts/user/{user_id}")

    def create_cart(self, user_id: int, products: list) -> requests.Response:
        """Создание новой корзины."""
        payload = {
            "userId": user_id,
            "products": products
        }
        return self._make_request("POST", f"{self.BASE_URL}/carts/add", json=payload)

    def update_cart(self, cart_id: int, products: list, merge: bool = False) -> requests.Response:
        """Обновление корзины."""
        payload = {
            "products": products,
            "merge": merge
        }
        return self._make_request("PUT", f"{self.BASE_URL}/carts/{cart_id}", json=payload)

    def delete_cart(self, cart_id: int) -> requests.Response:
        """Удаление корзины."""
        return self._make_request("DELETE", f"{self.BASE_URL}/carts/{cart_id}")
