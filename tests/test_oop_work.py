import pytest
from src.oop_work import Product



class TestProduct:
    def test_init_valid_price(self):
        """Тест: создание Product с положительной ценой."""
        product = Product("Ноутбук", "Игровой", 75000.0, 5)
        assert product.name == "Ноутбук"
        assert product.description == "Игровой"
        assert product.price == 75000.0
        assert product.quantity == 5

    def test_init_zero_price(self, capsys):
        """Тест: инициализация с ценой = 0 → сообщение, цена не устанавливается."""
        product = Product("Мышь", "Беспроводная", 0.0, 10)
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price is None  # _price осталось None

    def test_init_negative_price(self, capsys):
        """Тест: инициализация с отрицательной ценой → сообщение, цена не устанавливается."""
        product = Product("Клавиатура", "Механическая", -3000.0, 3)
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price is None

    def test_set_valid_price(self):
        """Тест: установка допустимой цены через сеттер."""
        product = Product("Смартфон", "Флагман", 50000.0, 8)
        product.price = 55000.0
        assert product.price == 55000.0

    def test_set_zero_price(self, capsys):
        """Тест: попытка установить цену = 0 через сеттер → сообщение, значение не меняется."""
        product = Product("Наушники", "Bluetooth", 2000.0, 15)
        product.price = 0
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 2000.0  # старое значение сохранилось

    def test_set_negative_price(self, capsys):
        """Тест: попытка установить отрицательную цену через сеттер → сообщение, значение не меняется."""
        product = Product("Колонка", "Портативная", 3500.0, 7)
        product.price = -500
        captured = capsys.readouterr()
        assert "Цена не должна быть нулевая или отрицательная" in captured.out
        assert product.price == 3500.0  # старое значение сохранилось

    def test_price_getter(self):
        """Тест: геттер возвращает текущее значение _price."""
        product = Product("Планшет", "10 дюймов", 40000.0, 4)
        assert product.price == 40000.0

    def test_new_product_valid_data(self):
        """Тест: Product.new_product() с корректными данными."""
        data = {
            "name": "Монитор",
            "description": "4K, 27 дюймов",
            "price": "25000",
            "quantity": "2"
        }
        product = Product.new_product(data)
        assert product.name == "Монитор"
        assert product.description == "4K, 27 дюймов"
        assert product.price == 25000.0
        assert product.quantity == 2

    def test_new_product_missing_key(self):
        """Тест: Product.new_product() без обязательного ключа → ValueError."""
        data = {
            "name": "Мышь",
            "description": "Оптическая",
            # "price" отсутствует
            "quantity": "5"
        }
        with pytest.raises(ValueError) as excinfo:
            Product.new_product(data)
        assert "Отсутствует обязательный ключ в данных продукта: 'price'" in str(excinfo.value)

    def test_new_product_invalid_price_type(self):
        """Тест: Product.new_product() с некорректным типом цены → ValueError."""
        data = {
            "name": "Клавиатура",
            "description": "RGB",
            "price": "нечисло",
            "quantity": "3"
        }
        with pytest.raises(ValueError) as excinfo:
            Product.new_product(data)
        assert "Некорректный тип данных для продукта" in str(excinfo.value)

    def test_new_product_invalid_quantity_type(self):
        """Тест: Product.new_product() с некорректным типом количества → ValueError."""
        data = {
            "name": "Веб‑камера",
            "description": "1080p",
            "price": "4000",
            "quantity": "десять"
        }
        with pytest.raises(ValueError) as excinfo:
            Product.new_product(data)
        assert "Некорректный тип данных для продукта" in str(excinfo.value)
