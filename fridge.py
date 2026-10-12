"""Модуль управления содержимым холодильника."""

import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Any

# Словарь goods имеет структуру:
# {
#     'Название продукта': [
#         {'amount': Decimal('1.0'), 'expiration_date': datetime.date(2023, 10, 15)},
#         ...
#     ]
# }


def add(items: dict, title: str, amount: Decimal, expiration_date: Optional[str] = None) -> None:
    """Добавляет партию продукта в словарь items."""
    pass


def add_by_note(items: dict, note: str) -> None:
    """Парсит текстовую заметку и добавляет продукт в словарь items."""
    pass


def find(items: dict, needle: str) -> List[str]:
    """Ищет продукты по подстроке без учета регистра."""
    pass


def get_amount(items: dict, needle: str) -> Decimal:
    """Возвращает суммарное количество продуктов, подходящих под запрос."""
    pass


def get_expired(items: dict, in_advance_days: int = 0) -> List[Tuple[str, Decimal]]:
    """Возвращает список просроченных продуктов с их количеством."""
    pass
