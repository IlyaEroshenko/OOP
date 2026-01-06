import pytest
import json
import os
from src.main import Product
from src.oop_work import load_data_from_json

TEST_DATA_FILE = "test_data.json"


@pytest.fixture  # fixture для создания тестового файла
def setup_test_data():
    test_data = {
        "categories": [
            {
                "name": "Category1",
                "description": "Description1",
                "products": [
                    {"name": "Product1", "description": "Desc1", "price": 10.0, "quantity": 5},
                    {"name": "Product2", "description": "Desc2", "price": 20.0, "quantity": 10}
                ]
            }
        ]
    }
    with open(TEST_DATA_FILE, "w", encoding="utf-8") as f:  # encoding
        json.dump(test_data, f, ensure_ascii=False, indent=4)  # indent для удобства чтения
    yield
    os.remove(TEST_DATA_FILE)  # удаление тестового файла


def test_product_creation():  # Тест для создания объекта Product
    product = Product("Test Product", "Description", 19.99, 10)
    assert product.name == "Test Product"
    assert product.description == "Description"
    assert product.price == 19.99
    assert product.quantity == 10


def test_load_data_success(setup_test_data):  # Тест для успешной загрузки данных из JSON
    categories = load_data_from_json(TEST_DATA_FILE)
    assert isinstance(categories, list)
    assert len(categories) == 1
    assert categories[0].name == "Category1"


def test_load_data_file_not_found():  # Тест для случая, когда файл не найден
    categories = load_data_from_json("non_existent_file.json")
    assert categories == []


def test_load_data_invalid_json():  # Тест для случая, когда JSON файл некорректен
    with open("invalid.json", "w", encoding="utf-8") as f:
        f.write("invalid json")
    categories = load_data_from_json("invalid.json")
    assert categories == []
    os.remove("invalid.json")
