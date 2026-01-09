import pytest
import json
import logging
from unittest.mock import patch
from io import StringIO

from src.oop_work import Product, Category, load_data_from_json  # Замените your_module


def test_product_creation():
    product = Product("Test Product", "Description", 10.0, 5)
    assert product.name == "Test Product"
    assert product.description == "Description"
    assert product.price == 10.0
    assert product.quantity == 5


def test_category_creation():
    category = Category("Test Category", "Description")
    assert category.name == "Test Category"
    assert category.description == "Description"
    assert len(category.products) == 0


def test_category_product_count():
    category = Category("Test Category", "Description")
    product1 = Product("Product 1", "Desc", 5.0, 2)
    product2 = Product("Product 2", "Desc", 10.0, 1)
    category.products = [product1, product2]
    assert category.product_count() == 2


def test_load_data_from_json_file_not_found():
    categories = load_data_from_json("nonexistent_file.json")
    assert len(categories) == 0


def test_load_data_from_json_invalid_json(tmp_path):
    file_path = tmp_path / "invalid.json"
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("invalid json")

    categories = load_data_from_json(str(file_path))
    assert len(categories) == 0


def test_load_data_from_json_missing_fields(tmp_path, caplog):
    test_data = {"categories": [{"description": "Description1", "products": []}]}  # Missing 'name'

    file_path = tmp_path / "test_products.json"
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(test_data, f)

    with caplog.at_level(logging.WARNING):
        categories = load_data_from_json(str(file_path))
        assert len(categories) == 0
        assert "Пропущена категория с отсутствующими полями." in caplog.text
