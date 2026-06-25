"""
Тесты авторизации (Auth API).
"""
import allure


@allure.feature("Авторизация")
class TestAuth:
    """Тесты авторизации пользователей."""

    @allure.story("Успешная авторизация")
    @allure.title("POST /auth/login - успешная авторизация")
    def test_successful_login(self, api_client):
        """Проверка успешной авторизации с валидными данными."""
        response = api_client.login(username="emilys", password="emilyspass")

        assert response.status_code == 200, f"Ожидался 200, получен {response.status_code}"

        data = response.json()
        assert "accessToken" in data, "В ответе отсутствует accessToken"
        assert "refreshToken" in data, "В ответе отсутствует refreshToken"
        assert "id" in data, "В ответе отсутствует id"
        assert "username" in data, "В ответе отсутствует username"

        assert data["username"] == "emilys", "Неверный username"
        assert data["id"] == 1, "Неверный id пользователя"

        assert len(data["accessToken"]) > 0, "accessToken пустой"
        assert len(data["refreshToken"]) > 0, "refreshToken пустой"

    @allure.story("Неуспешная авторизация")
    @allure.title("POST /auth/login - неверный пароль")
    def test_failed_login_wrong_password(self, api_client, random_user_data):
        """Проверка авторизации с неверным паролем."""
        # Используем Faker для генерации случайного пароля
        wrong_password = f"wrong_{random_user_data['username']}_123"

        response = api_client.login(username="emilys", password=wrong_password)

        assert response.status_code == 401, f"Ожидался 401, получен {response.status_code}"

        data = response.json()
        assert "message" in data, "В ответе отсутствует message"
