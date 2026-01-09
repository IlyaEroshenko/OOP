import json
import logging
from typing import Optional


class Product:
    """
    Представляет товар в магазине.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализирует новый объект Product.

        Args:
            name (str): Название товара.
            description (str): Описание товара.
            price (float): Цена товара.
            quantity (int): Количество товара в наличии.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Представляет категорию товаров.
    """

    def __init__(
        self, name: str, description: str, products: Optional[list[Product]] = None
    ):
        """
        Инициализирует новый объект Category.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
        """
        self.name = name
        self.description = description
        self.products = (
            products if products is not None else []
        )  # Список товаров в категории
        Category.category_count += 1  # Увеличиваем счетчик категорий
        # Используем переданный список products, иначе создаем пустой.

    category_count = 0

    def product_count(self) -> int:
        return len(self.products)


def load_data_from_json(filename: str = "data/products.json") -> list[Category]:
    """
    Функция для загрузки данных о категориях и товарах из JSON-файла,
    обрабатывая возможные ошибки.

    Args:
        filename: Имя файла JSON (по умолчанию "products.json").

    Returns:
        list: Список объектов Category.
    """
    categories = []
    try:
        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)  # Загружаем JSON данные из файла
    except FileNotFoundError:
        logging.error(f"Файл {filename} не найден.")
        return []  # Возвращаем пустой список в случае ошибки
    except json.JSONDecodeError as e:
        logging.error(f"Ошибка: Некорректный формат JSON в файле {filename}: {e}")
        return []  # Возвращаем пустой список в случае ошибки
    except Exception as e:
        logging.error(f"Произошла неожиданная ошибка: {e}")
        return []

    for category_data in data.get("categories", []):  # Перебираем категории
        if "name" not in category_data or category_data.get(
            "products", []
        ):  # Перебираем продукты в категории
            logging.warning("Пропущена категория с отсутствующими полями.")
            continue

        category = Category(
            category_data["name"], category_data["description"]
        )  # Создаем объект Category
        for product_data in category_data.get(
            "products", []
        ):  # Перебираем продукты в категории
            try:
                product = Product(
                    product_data["name"],
                    product_data["description"],
                    float(product_data["price"]),
                    int(product_data["quantity"]),
                )

                category.products.append(product)  # Добавляем продукт в категорию
            except (KeyError, ValueError) as e:
                logging.warning(f"Пропущен товар из-за ошибки: {e}")
        categories.append(category)  # Добавляем категорию в список категорий.
    return categories
