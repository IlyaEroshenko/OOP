import pytest
from src.oop_work import Category, Product

# Тесты для класса Product
def test_product_creation():
    """Тест создания экземпляра класса Product."""
    product = Product("Test Product", "Test Description", 100.0, 10)
    assert product.name == "Test Product"
    assert product.description == "Test Description"
    assert product.price == 100.0
    assert product.quantity == 10

# Тесты для класса Category
def test_category_creation():
    """Тест создания экземпляра класса Category."""
    category = Category("Test Category", "Test Category Description")
    assert category.name == "Test Category"
    assert category.description == "Test Category Description"
    assert category.products == []
