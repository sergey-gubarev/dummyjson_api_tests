"""
Фикстуры для тестов DummyJSON API.
"""
import pytest
import time
from faker import Faker
from utils.api_client import DummyJSONClient

# Создаём экземпляр Faker с русской локалью
fake = Faker('ru_RU')


@pytest.fixture(scope="session")
def api_client():
    """Создание клиента API (одиночка на всю сессию тестов)."""
    return DummyJSONClient()


@pytest.fixture(scope="session")
def auth_token(api_client):
    """Получение токена авторизации."""
    response = api_client.login(username="emilys", password="emilyspass")
    assert response.status_code == 200, "Не удалось получить токен авторизации"
    return response.json()["accessToken"]


@pytest.fixture(scope="session")
def user_id(api_client):
    """Получение ID пользователя."""
    response = api_client.login(username="emilys", password="emilyspass")
    return response.json()["id"]


@pytest.fixture
def unique_test_id():
    """Генерация уникального идентификатора для теста."""
    return f"{fake.uuid4()[:8]}"


@pytest.fixture
def random_products():
    """Генерация случайного набора товаров."""
    # Используем реальные ID товаров из DummyJSON (1-194)
    import random
    num_products = random.randint(1, 3)
    products = []

    for _ in range(num_products):
        product_id = random.randint(1, 194)
        quantity = random.randint(1, 5)
        products.append({
            "id": product_id,
            "quantity": quantity
        })

    return products


@pytest.fixture
def random_user_data():
    """Генерация случайных данных пользователя (для негативных тестов)."""
    return {
        "username": fake.user_name(),
        "email": fake.email(),
        "first_name": fake.first_name(),
        "last_name": fake.last_name(),
        "phone": fake.phone_number()
    }


@pytest.fixture(autouse=True)
def delay_between_tests():
    """Задержка между тестами для предотвращения rate limiting."""
    yield
    time.sleep(1)
