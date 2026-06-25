"""
Тесты работы с корзинами (Carts API).
"""
import allure


@allure.feature("Корзины")
class TestCarts:
    """Тесты работы с корзинами."""

    @allure.story("Получение корзин пользователя")
    @allure.title("GET /carts/user/{userId} - получение корзин пользователя")
    def test_get_carts_by_user(self, api_client, user_id):
        """Проверка получения корзин пользователя."""
        response = api_client.get_carts_by_user(user_id=user_id)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert "carts" in data, "В ответе отсутствует carts"
        assert isinstance(data["carts"], list), "carts должен быть списком"

        for cart in data["carts"]:
            assert cart["userId"] == user_id, f"userId корзины {cart['id']} не совпадает"

    @allure.story("Получение корзины по ID")
    @allure.title("GET /carts/{cartId} - получение корзины по ID")
    def test_get_cart_by_id(self, api_client):
        """Проверка получения корзины по ID."""
        cart_id = 1
        response = api_client.get_cart_by_id(cart_id=cart_id)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert data["id"] == cart_id, "Неверный id корзины"
        assert "products" in data, "В ответе отсутствует products"
        assert "total" in data, "В ответе отсутствует total"
        assert "userId" in data, "В ответе отсутствует userId"

        assert isinstance(data["products"], list), "products должен быть списком"
        assert len(data["products"]) > 0, "products не должен быть пустым"

    @allure.story("Создание корзины")
    @allure.title("POST /carts/add - создание новой корзины")
    def test_create_cart(self, api_client, user_id, random_products, unique_test_id):
        """Проверка создания новой корзины с случайными товарами."""
        # Добавляем уникальный идентификатор в комментарий (если бы API поддерживал)
        # Для DummyJSON просто используем случайные товары

        response = api_client.create_cart(user_id=user_id, products=random_products)

        assert response.status_code == 201, f"Ожидался 201, получен {response.status_code}"

        data = response.json()
        assert "id" in data, "В ответе отсутствует id"
        assert data["userId"] == user_id, "Неверный userId"
        assert "products" in data, "В ответе отсутствует products"
        assert "total" in data, "В ответе отсутствует total"
        assert "totalQuantity" in data, "В ответе отсутствует totalQuantity"

        # Проверка расчёта totalQuantity
        expected_quantity = sum(p["quantity"] for p in random_products)
        assert data["totalQuantity"] == expected_quantity, \
            f"Ожидалось totalQuantity={expected_quantity}, получено {data['totalQuantity']}"

        assert data["total"] > 0, "total должен быть > 0"

    @allure.story("Обновление корзины")
    @allure.title("PUT /carts/{cartId} - обновление корзины")
    def test_update_cart(self, api_client, random_products):
        """Проверка обновления корзины со случайными товарами."""
        cart_id = 1

        # Берём первый товар из случайного набора
        products = [random_products[0]] if random_products else [{"id": 1, "quantity": 5}]
        products[0]["quantity"] = 5  # Фиксируем количество для проверки

        response = api_client.update_cart(cart_id=cart_id, products=products, merge=False)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert data["id"] == cart_id, "Неверный id корзины"
        assert "products" in data, "В ответе отсутствует products"
        assert "total" in data, "В ответе отсутствует total"

        # Проверка, что количество товара обновилось
        product = next((p for p in data["products"] if p["id"] == products[0]["id"]), None)
        assert product is not None, f"Товар с id={products[0]['id']} не найден"
        assert product["quantity"] == 5, f"Ожидалось quantity=5, получено {product['quantity']}"

    @allure.story("Удаление корзины")
    @allure.title("DELETE /carts/{cartId} - удаление корзины")
    def test_delete_cart(self, api_client):
        """Проверка удаления корзины."""
        cart_id = 1
        response = api_client.delete_cart(cart_id=cart_id)

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert data["id"] == cart_id, "Неверный id корзины"
        assert data["isDeleted"] is True, "isDeleted должен быть True"
        assert "deletedOn" in data, "В ответе отсутствует deletedOn"
