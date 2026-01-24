import json
import logging
from typing import List, Optional

logging.basicConfig(level=logging.INFO)


class Product:
    """
    Представляет товар в магазине.
    """

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        """
        Инициализирует новый объект Product.

        Args:
            name (str): Название товара.
            description (str): Описание товара.
            price (float): Цена товара (должна быть > 0).
            quantity (int): Количество товара в наличии.
        """
        self.name = name
        self.description = description
        self.price = price  # Используем сеттер
        self.quantity = quantity

    @property
    def price(self) -> float:
        """
        Геттер для атрибута price.

        Returns:
            float: Текущая цена товара.
        """
        if self._price is None:
            raise ValueError("Цена не установлена")
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        """
        Сеттер для атрибута price с проверкой на положительность.

        Args:
            value (float): Новая цена товара.

        Если цена ≤ 0, выводится сообщение:
            "Цена не должна быть нулевая или отрицательная"
        и значение НЕ обновляется.
        """
        if not isinstance(value, (int, float)):
            raise TypeError("Цена должна быть числом (int или float)")
        if value < 0:
            raise ValueError("Цена не должна быть отрицательная")
        self._price = value

    @classmethod
    def new_product(cls, product_data: dict) -> None:
        """
        Создаёт объект Product из словаря с данными.

        Args:
            product_data (dict): Словарь с ключами:
                - 'name' (str)
                - 'description' (str)
                - 'price' (float или str)
                - 'quantity' (int или str)

        Returns:
            Product: Новый экземпляр класса Product.

        Raises:
            ValueError: Если отсутствует обязательный ключ или данные некорректны.
        """
        try:
            # Проверка обязательных ключей
            if "name" not in product_data:
                raise KeyError("name")
            if "description" not in product_data:
                raise KeyError("description")
            if "price" not in product_data:
                raise KeyError("price")
            if "quantity" not in product_data:
                raise KeyError("quantity")

            name = product_data["name"]
            description = product_data["description"]
            price = float(product_data["price"])
            quantity = int(product_data["quantity"])

            return cls(name, description, price, quantity)

        except KeyError as e:
            raise ValueError(f"Отсутствует обязательный ключ в данных продукта: {e}")
        except (ValueError, TypeError) as e:
            raise ValueError(f"Некорректный тип данных для продукта: {e}")


class Category:
    """
    Представляет категорию товаров.
    """

    category_count = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        """
        Инициализирует новый объект Category.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
            products (Optional[List[Product]]): Список товаров (по умолчанию — пустой).
        """
        if not name:
            raise ValueError("Название категории не может быть пустым")
        if not description:
            raise ValueError("Описание категории не может быть пустым")

        self.name = name
        self.description = description
        self.__products = products or []
        Category.category_count += 1

    @property
    def products(self) -> List[str]:
        """Публичный доступ к списку товаров."""
        product_strings = []  # Инициализируем пустой список для хранения строковых представлений товаров
        for product in self.__products:  # Перебираем товары в категории
            # Формируем строку по заданному шаблону и добавляем её в список
            product_strings.append(f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n")
        return product_strings  # Возвращаем сформированный список строк

    @products.setter
    def products(self, value: List["Product"]) -> None:
        """Валидация при изменении списка товаров."""
        if not all(isinstance(p, Product) for p in value):
            raise TypeError("Все элементы должны быть типа Product")
        self.__products = value

    def add_product(self, product: Product) -> None:
        """
        Добавляет товар в категорию.

        Args:
            product (Product): Товар для добавления.

        Raises:
            TypeError: Если аргумент не является экземпляром Product.
        """
        if not isinstance(product, Product):
            raise TypeError("В категорию можно добавлять только объекты типа Product")
        self.__products.append(product)

    def product_count(self) -> int:
        """
        Возвращает количество товаров в категории.

        Returns:
            int: Число товаров.
        """
        return len(self.__products)

    def get_products(self) -> List[str]:
        """
        Возвращает список товаров в формате строк.

        Returns:
            List[str]: Список строк вида "Название, Цена руб. Остаток: X шт."
        """
        return [
            f"{p.name}, {p.price} руб. Остаток: {p.quantity} шт."
            for p in self.__products
        ]


def load_data_from_json(filename: str = "data/products.json") -> List[Category]:
    """
    Загружает данные о категориях и товарах из JSON-файла.

    Args:
        filename (str): Путь к JSON-файлу (по умолчанию "data/products.json").

    Returns:
        List[Category]: Список категорий с товарами.

    Notes:
        - Если файл не найден, возвращается пустой список.
        - Пропускаются категории без имени или описания.
        - Пропускаются товары с некорректными данными.
    """
    categories = []

    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logging.error(f"Файл {filename} не найден.")
        return []
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка формата JSON в файле {filename}: {e}")
        return []
    except Exception as e:
        logging.error(f"Неожиданная ошибка при чтении файла {filename}: {e}")
        return []

    for category_data in data.get("categories", []):
        # Проверка обязательных полей категории
        if not category_data.get("name"):
            logging.warning("Пропущена категория без имени.")
            continue
        if not category_data.get("description"):
            logging.warning("Пропущена категория без описания.")
            continue

        category = Category(
            name=category_data["name"], description=category_data["description"]
        )

        # Добавление товаров
        for product_data in category_data.get("products", []):
            try:
                product = Product.new_product(product_data)
                category.add_product(product)
            except (KeyError, ValueError) as e:
                logging.warning(f"Пропущен товар из-за ошибки: {e}")

        categories.append(category)

    return categories
