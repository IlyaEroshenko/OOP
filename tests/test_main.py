import pytest
from src.oop_work import Product, Category


def test_product_creation():
    """Тест проверяет создание объекта Product."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_category_creation():
    """Тест проверяет создание объекта Category."""
    category = Category("Test Category", "Test Description")
    assert category.name == "Test Category"
    assert category.description == "Test Description"
    assert category.product_count() == 0


def test_add_product_to_category():
    """Тест добавления продукта в категорию."""
    category = Category("Test Category", "Test Description")
    product = Product("Test Product", "Test Description", 100.0, 10)
    category.add_product(product)
    assert category.product_count() == 1


def test_product_new_product():
    """Тест метода new_product класса Product."""
    product_data = {
        "name": "Test Product",
        "description": "Test Description",
        "price": 100.0,
        "quantity": 10,
    }
    product = Product.new_product(product_data)
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10


def test_product_invalid_data():
    """Тест обработки неверных данных в new_product."""
    with pytest.raises(ValueError):
        Product.new_product(
            {"name": "Test", "description": "Test", "price": "invalid", "quantity": 1}
        )
    with pytest.raises(ValueError):
        Product.new_product(
            {"name": "Test", "description": "Test", "price": 100, "quantity": "invalid"}
        )
    with pytest.raises(ValueError):
        Product.new_product(
            {"description": "Test", "price": 100, "quantity": 1}
        )
