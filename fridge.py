"""Модуль управления содержимым холодильника."""

import datetime
from decimal import Decimal
from typing import Dict, List, Optional, Tuple, Any

DATE_FORMAT = '%Y-%m-%d'


def add(
    items: Dict[str, List[Dict[str, Any]]],
    title: str,
    amount: Any,
    expiration_date: Optional[Any] = None
) -> None:
    """Добавляет партию продукта в словарь холодильника.

    :param items: словарь goods со всеми продуктами
    :param title: название продукта (может содержать пробелы)
    :param amount: количество продукта (целое или дробное)
    :param expiration_date: дата истечения срока годности в формате 'YYYY-MM-DD'
    """
    # Преобразуем строку даты в объект datetime.date при наличии
    if expiration_date is not None:
        if isinstance(expiration_date, str):
            exp_date = datetime.datetime.strptime(expiration_date, DATE_FORMAT).date()
        elif isinstance(expiration_date, datetime.date):
            exp_date = expiration_date
        else:
            exp_date = None
    else:
        exp_date = None

    # Приводим количество к Decimal для точных финансовых/весовых операций
    if not isinstance(amount, Decimal):
        amount = Decimal(str(amount))

    batch = {
        'amount': amount,
        'expiration_date': exp_date
    }

    # Если продукта еще нет в холодильнике, инициализируем пустой список партий
    if title not in items:
        items[title] = []

    items[title].append(batch)


def add_by_note(items: Dict[str, List[Dict[str, Any]]], note: str) -> None:
    """Парсит текстовую заметку о покупке и добавляет запись в холодильник.

    Форматы заметки:
    - "<название> <количество> <срок_годности>" (например, "Яйца гусиные 4 2023-07-15")
    - "<название> <количество>" (например, "Вода 2.5")
    """
    parts = note.strip().split()
    if not parts:
        return

    # Проверяем, является ли последнее слово датой
    try:
        datetime.datetime.strptime(parts[-1], DATE_FORMAT)
        # Успешно распарсили дату
        exp_date_str: Optional[str] = parts[-1]
        amount_str = parts[-2]
        title = ' '.join(parts[:-2])
    except (ValueError, IndexError):
        # Даты нет, последнее слово — количество
        exp_date_str = None
        amount_str = parts[-1]
        title = ' '.join(parts[:-1])

    amount = Decimal(amount_str)
    add(items, title, amount, exp_date_str)


def find(items: Dict[str, List[Dict[str, Any]]], needle: str) -> List[str]:
    """Ищет продукты в холодильнике по подстроке без учета регистра."""
    query = needle.lower()
    return [title for title in items.keys() if query in title.lower()]


def get_amount(items: Dict[str, List[Dict[str, Any]]], needle: str) -> Decimal:
    """Возвращает общее количество продукта (число типа Decimal) по запросу."""
    query = needle.lower()
    total_amount = Decimal('0')

    # Ищем во всех совпавших наименованиях и суммируем все партии
    for title, batches in items.items():
        if query in title.lower():
            for batch in batches:
                total_amount += batch['amount']

    return total_amount


def get_expired(
    items: Dict[str, List[Dict[str, Any]]],
    in_advance_days: int = 0
) -> List[Tuple[str, Decimal]]:
    """Возвращает список просроченных продуктов с их количеством."""
    pass
