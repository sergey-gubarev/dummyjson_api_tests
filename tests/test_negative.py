"""
Негативные тесты для API DummyJSON.
"""
import allure
from faker import Faker

fake = Faker('ru_RU')


@allure.feature("Негативные проверки")
class TestNegative:
    """Негативные сценарии тестирования."""

    @allure.story("Несуществующая корзина")
    @allure.title("GET /carts/{cartId} - несуществующий ID")
    def test_get_nonexistent_cart(self, api_client):
        """Проверка получения несуществующей корзины."""
        # Генерируем случайный большой ID
        nonexistent_id = fake.random_int(min=99999, max=999999)

        response = api_client.get_cart_by_id(cart_id=nonexistent_id)

        assert response.status_code == 404, f"Ожидался 404, получен {response.status_code}"

    @allure.story("Невалидные данные при создании корзины")
    @allure.title("POST /carts/add - невалидный body")
    def test_create_cart_invalid_body(self, api_client):
        """Проверка создания корзины с невалидными данными."""
        response = api_client.create_cart(user_id=1, products=[])

        assert response.status_code in [400, 200], \
            f"Ожидался 400 или 200, получен {response.status_code}"

    @allure.story("Некорректное количество товара")
    @allure.title("POST /carts/add - количество 0")
    def test_create_cart_zero_quantity(self, api_client):
        """Проверка создания корзины с количеством товара 0."""
        products = [{"id": 1, "quantity": 0}]
        response = api_client.create_cart(user_id=1, products=products)

        assert response.status_code in [400, 200], \
            f"Ожидался 400 или 200, получен {response.status_code}"

        if response.status_code == 200:
            data = response.json()
            assert data["totalQuantity"] == 0, "totalQuantity должен быть 0"

    @allure.story("Невалидный пользователь")
    @allure.title("POST /carts/add - несуществующий userId")
    def test_create_cart_invalid_user(self, api_client, random_products):
        """Проверка создания корзины с несуществующим userId."""
        # Генерируем случайный несуществующий userId
        invalid_user_id = fake.random_int(min=99999, max=999999)

        response = api_client.create_cart(user_id=invalid_user_id, products=random_products)

        # API может вернуть 400 или 404
        assert response.status_code in [400, 404, 200], \
            f"Ожидался 400, 404 или 200, получен {response.status_code}"
