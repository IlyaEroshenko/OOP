import pytest
import json

from src.oop_work import Product, Category, load_data_from_json


def test_load_data_success():
    """Проверяет успешную загрузку данных."""
    categories = load_data_from_json("data/products.json")
    assert isinstance(categories, list)
    assert len(categories) > 0  # Предполагаем, что в файле есть категории
    assert isinstance(categories[0], Category)
    assert isinstance(categories[0].products[0], Product) # Проверяем, что в категории есть продукты

def test_load_data_file_not_found():
    """Проверяет обработку FileNotFoundError."""
    categories = load_data_from_json("nonexistent_file.json")
    assert categories == [] # В случае ошибки должен возвращаться пустой список

def test_load_data_json_decode_error():
    """Проверяет обработку JSONDecodeError."""
    # Создаем файл с некорректным JSON
    with open("invalid.json", "w") as f:
        f.write("This is not JSON")
    categories = load_data_from_json("invalid.json")
    assert categories == [] # В случае ошибки должен возвращаться пустой список