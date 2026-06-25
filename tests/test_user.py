"""
Тесты получения данных пользователя (User API).
"""
import allure


@allure.feature("Пользователь")
class TestUser:
    """Тесты получения данных пользователя."""

    @allure.story("Получение текущего пользователя")
    @allure.title("GET /auth/me - с валидным токеном")
    def test_get_current_user_with_token(self, api_client, auth_token):
        """Проверка получения данных текущего пользователя с токеном."""
        response = api_client.get_current_user(token=auth_token)

        # Проверка статус-кода
        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        # Проверка структуры ответа
        data = response.json()
        assert "id" in data, "В ответе отсутствует id"
        assert "username" in data, "В ответе отсутствует username"
        assert "email" in data, "В ответе отсутствует email"
        assert "firstName" in data, "В ответе отсутствует firstName"
        assert "lastName" in data, "В ответе отсутствует lastName"

        # Проверка, что это тот же пользователь
        assert data["username"] == "emilys", "Неверный username"
        assert data["id"] == 1, "Неверный id пользователя"

    @allure.story("Получение пользователя без токена")
    @allure.title("GET /auth/me - без токена")
    def test_get_current_user_without_token(self, api_client):
        """Проверка получения данных пользователя без токена."""
        # Создаём новый клиент без токена
        response = api_client.session.get(f"{api_client.BASE_URL}/auth/me")

        # Проверка статус-кода
        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"
