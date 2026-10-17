"""Юнит-тесты для модуля fridge."""

import datetime
from decimal import Decimal
from fridge import add, add_by_note, find, get_amount, get_expired


def test_add_basic():
    """Тестирование добавления партии с датой и без нее."""
    goods = {}
    add(goods, 'Яйца', Decimal('10'), '2023-09-30')
    assert 'Яйца' in goods
    assert len(goods['Яйца']) == 1
    assert goods['Яйца'][0]['amount'] == Decimal('10')
    assert goods['Яйца'][0]['expiration_date'] == datetime.date(2023, 9, 30)

    # Добавляем еще одну партию того же товара
    add(goods, 'Яйца', Decimal('3'), '2023-10-15')
    assert len(goods['Яйца']) == 2

    # Товар без срока годности
    add(goods, 'Вода', Decimal('2.5'))
    assert goods['Вода'][0]['expiration_date'] is None


def test_add_by_note():
    """Тестирование добавления продуктов через парсинг строки заметки."""
    goods = {}
    add_by_note(goods, 'Яйца гусиные 4 2023-07-15')
    assert 'Яйца гусиные' in goods
    assert goods['Яйца гусиные'][0]['amount'] == Decimal('4')
    assert goods['Яйца гусиные'][0]['expiration_date'] == datetime.date(2023, 7, 15)

    # Заметка без даты
    add_by_note(goods, 'Масло сливочное крестьянское 0.4')
    assert 'Масло сливочное крестьянское' in goods
    assert goods['Масло сливочное крестьянское'][0]['amount'] == Decimal('0.4')
    assert goods['Масло сливочное крестьянское'][0]['expiration_date'] is None


def test_find():
    """Тестирование регистронезависимого поиска продуктов."""
    goods = {
        'Яйца': [
            {'amount': Decimal('1'), 'expiration_date': datetime.date(2023, 6, 24)}
        ],
        'Яйца гусиные': [
            {'amount': Decimal('4'), 'expiration_date': datetime.date(2023, 7, 15)}
        ],
        'Морковь': [
            {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 6)}
        ],
    }

    assert find(goods, 'Яйц') == ['Яйца', 'Яйца гусиные']
    assert find(goods, 'яйц') == ['Яйца', 'Яйца гусиные']
    assert find(goods, 'морковь') == ['Морковь']
    assert find(goods, 'Молоко') == []


def test_get_amount():
    """Тестирование суммирования остатков продуктов."""
    goods = {
        'Яйца': [{'amount': Decimal('1'), 'expiration_date': None}],
        'Яйца перепелиные': [
            {'amount': Decimal('10'), 'expiration_date': None},
            {'amount': Decimal('5'), 'expiration_date': None},
        ],
        'Морковь': [
            {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 8, 1)},
            {'amount': Decimal('3'), 'expiration_date': datetime.date(2023, 8, 6)},
        ],
        'Вода': [{'amount': Decimal('2.5'), 'expiration_date': None}],
    }

    # Поиск по подстроке "яйца" должен учесть и 'Яйца', и 'Яйца перепелиные'
    assert get_amount(goods, 'яйца') == Decimal('16')
    assert get_amount(goods, 'морковь') == Decimal('5')
    assert get_amount(goods, 'сок') == Decimal('0')


def test_get_expired(monkeypatch):
    """Тестирование проверки просрочки относительно фиксированной даты."""
    # Зафиксируем сегодняшнюю дату как 10 декабря 2023 года (из примера ТЗ)
    fixed_date = datetime.date(2023, 12, 10)

    class MockDate(datetime.date):
        @classmethod
        def today(cls):
            return fixed_date

    monkeypatch.setattr(datetime, 'date', MockDate)

    goods = {
        'Хлеб': [
            {'amount': Decimal('1'), 'expiration_date': None},
            {'amount': Decimal('1'), 'expiration_date': datetime.date(2023, 12, 9)},
        ],
        'Яйца': [
            {'amount': Decimal('2'), 'expiration_date': datetime.date(2023, 12, 12)},
            {'amount': Decimal('3'), 'expiration_date': datetime.date(2023, 12, 11)},
        ],
        'Вода': [{'amount': Decimal('100'), 'expiration_date': None}],
    }

    # 10 декабря: Хлеб истек 9 декабря
    assert get_expired(goods, in_advance_days=0) == [('Хлеб', Decimal('1'))]

    # 1 день вперед (+1): до 11 декабря включительно (Хлеб 9 дек + Яйца 11 дек)
    res_1 = dict(get_expired(goods, in_advance_days=1))
    assert res_1 == {'Хлеб': Decimal('1'), 'Яйца': Decimal('3')}

    # 2 дня вперед (+2): до 12 декабря включительно (Хлеб 9 дек + все Яйца 11 и 12 дек)
    res_2 = dict(get_expired(goods, in_advance_days=2))
    assert res_2 == {'Хлеб': Decimal('1'), 'Яйца': Decimal('5')}
