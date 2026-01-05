import json


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

    def __init__(self, name: str, description: str):
        """
        Инициализирует новый объект Category.

        Args:
            name (str): Название категории.
            description (str): Описание категории.
        """
        self.name = name
        self.description = description
        self.products: list[Product] = []  # Список товаров в категории


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
            data = json.load(f)
    except FileNotFoundError:
        print(f"Ошибка: Файл {filename} не найден.")
        return []  # Возвращаем пустой список в случае ошибки
    except json.JSONDecodeError:
        print(f"Ошибка: Некорректный формат JSON в файле {filename}.")
        return []  # Возвращаем пустой список в случае ошибки
    except Exception as e:
        print(f"Произошла неожиданная ошибка: {e}")
        return []

    for category_data in data["categories"]:  # Перебираем категории
        category = Category(
            category_data["name"], category_data["description"]
        )  # Создаем объект Category
        for product_data in category_data[
            "products"
        ]:  # Перебираем продукты в категории
            product = Product(
                product_data["name"],
                product_data["description"],
                product_data["price"],
                product_data["quantity"],
            )  # Создаем объект Product

            category.products.append(product)  # Добавляем продукт в категорию
        categories.append(category)  # Добавляем категорию в список категорий.
    return categories
