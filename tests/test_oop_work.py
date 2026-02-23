import pytest
from unittest.mock import mock_open, patch
from src.oop_work import Product, Category, load_data_from_json  # замените 'shop' на имя вашего модуля


def test_product_creation_valid():
    """Тест: создание продукта с корректными данными."""
    product = Product("Гравер", "Аккумуляторный", 1500.50, 10)
    assert product.name == "Гравер"
    assert product.description == "Аккумуляторный"
    assert product.price == 1500.50
    assert product.quantity == 10


def test_product_price_setter_valid():
    """Тест: установка корректной цены через сеттер."""
    product = Product("Тест", "Описание", 100, 5)
    product.price = 200.0
    assert product.price == 200.0


def test_product_price_setter_negative():
    """Тест: попытка установить отрицательную цену."""
    product = Product("Тест", "Описание", 100, 5)
    with pytest.raises(ValueError, match="Цена не должна быть отрицательная"):
        product.price = -50


def test_product_price_setter_zero():
    """Тест: попытка установить цену = 0."""
    product = Product("Тест", "Описание", 100, 5)
    with pytest.raises(ValueError, match="Цена не должна быть отрицательная"):
        product.price = 0


def test_product_price_setter_non_number():
    """Тест: передача не числа в price."""
    product = Product("Тест", "Описание", 100, 5)
    with pytest.raises(TypeError, match="Цена должна быть числом \\(int или float\\)"):
        product.price = "не число"


def test_product_price_getter_unset():
    """Тест: обращение к price, если она не установлена (через сеттер)."""
    product = Product("Тест", "Описание", 100, 5)
    # Вручную обнуляем _price (для теста)
    product._price = None
    with pytest.raises(ValueError, match="Цена не установлена"):
        _ = product.price


def test_new_product_valid():
    """Тест: создание Product из словаря (корректные данные)."""
    data = {
        "name": "Гравер",
        "description": "Аккумуляторный",
        "price": "1500.50",
        "quantity": "10"
    }
    product = Product.new_product(data)
    assert product.name == "Гравер"
    assert product.price == 1500.50
    assert product.quantity == 10


def test_new_product_missing_key():
    """Тест: отсутствие обязательного ключа в словаре."""
    data = {"name": "Гравер", "description": "Описание"}
    with pytest.raises(ValueError, match="Отсутствует обязательный ключ"):
        Product.new_product(data)


def test_new_product_invalid_type():
    """Тест: некорректный тип данных в словаре."""
    data = {"name": "Гравер", "description": "Описание", "price": "abc", "quantity": "10"}
    with pytest.raises(ValueError, match="Некорректный тип данных для продукта"):
        Product.new_product(data)


# --- Тесты для класса Category ---

def test_category_creation_valid():
    """Тест: создание категории с корректными данными."""
    category = Category("Инструменты", "Все для ремонта")
    assert category.name == "Инструменты"
    assert category.description == "Все для ремонта"
    assert len(category.products) == 0  # Если __products не сделан truly private


def test_category_creation_empty_name():
    """Тест: попытка создать категорию с пустым именем."""
    with pytest.raises(ValueError, match="Название категории не может быть пустым"):
        Category("", "Описание")


def test_category_creation_empty_description():
    """Тест: попытка создать категорию с пустым описанием."""
    with pytest.raises(ValueError, match="Описание категории не может быть пустым"):
        Category("Имя", "")


def test_add_product_invalid_type():
    """Тест: попытка добавить не-Product в категорию."""
    category = Category("Инструменты", "Описание")
    with pytest.raises(TypeError, match="В категорию можно добавлять только объекты типа Product"):
        category.add_product("не продукт")


def test_product_count():
    """Тест: метод product_count."""
    category = Category("Инструменты", "Описание")
    product1 = Product("Гравер", "Описание", 1500, 10)
    product2 = Product("Дрель", "Описание", 2000, 5)
    category.add_product(product1)
    category.add_product(product2)
    assert category.product_count() == 2


def test_get_products():
    """Тест: метод get_products (формат строк)."""
    category = Category("Инструменты", "Описание")
    product = Product("Гравер", "Описание", 1500.50, 10)
    category.add_product(product)
    result = category.get_products()
    assert result == ["Гравер, 1500.5 руб. Остаток: 10 шт."]


# --- Тесты для функции load_data_from_json ---

def test_load_data_from_json_file_not_found():
    """Тест: файл не найден."""
    with patch("builtins.open", mock_open(), create=True) as m:
        m.side_effect = FileNotFoundError
        result = load_data_from_json("nonexistent.json")
        assert result == []


def test_load_data_from_json_invalid_json():
    """Тест: неверный JSON в файле."""
    mock_json = '{"categories": [{"name": "Инструменты", "description": "Описание", "products": [}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        result = load_data_from_json("invalid.json")
        assert result == []
