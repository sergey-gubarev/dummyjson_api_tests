"""
Pydantic модели для валидации ответов API.
"""
from typing import List, Optional
from pydantic import BaseModel


class Product(BaseModel):
    """Модель товара в корзине."""
    id: int
    title: str
    price: float
    quantity: int
    total: float
    discountPercentage: float
    discountedTotal: Optional[float] = None
    thumbnail: str


class Cart(BaseModel):
    """Модель корзины."""
    id: int
    products: List[Product]
    total: float
    discountedTotal: float
    userId: int
    totalProducts: int
    totalQuantity: int


class CartsResponse(BaseModel):
    """Модель ответа со списком корзин."""
    carts: List[Cart]
    total: int
    skip: int
    limit: int


class AuthResponse(BaseModel):
    """Модель ответа авторизации."""
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
    accessToken: str
    refreshToken: str


class UserResponse(BaseModel):
    """Модель ответа данных пользователя."""
    id: int
    username: str
    email: str
    firstName: str
    lastName: str
    gender: str
    image: str
