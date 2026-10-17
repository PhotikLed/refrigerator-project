"""Интерактивная консольная демонстрация работы с холодильником."""

from decimal import Decimal
from fridge import add, add_by_note, find, get_amount, get_expired


def demo():
    goods = {}

    print('--- 1. Добавление продуктов через add() ---')
    add(goods, 'Яйца', Decimal('10'), '2023-09-30')
    add(goods, 'Яйца', Decimal('3'), '2023-10-15')
    add(goods, 'Вода', Decimal('2.5'))
    print('Содержимое холодильника:', goods)

    print('\n--- 2. Добавление продуктов через заметку add_by_note() ---')
    add_by_note(goods, 'Яйца гусиные 4 2023-07-15')
    add_by_note(goods, 'Морковь мытая 1.5 2023-08-01')
    add_by_note(goods, 'Сок яблочный 2')

    print('\n--- 3. Поиск продуктов (find) ---')
    matches = find(goods, 'яйц')
    print('Поиск "яйц":', matches)

    print('\n--- 4. Подсчет количества (get_amount) ---')
    total_eggs = get_amount(goods, 'яйца')
    print('Общее количество по запросу "яйца":', total_eggs)

    print('\n--- 5. Проверка просроченных продуктов (get_expired) ---')
    expired = get_expired(goods, in_advance_days=30)
    print('Просроченные партии:', expired)


if __name__ == '__main__':
    demo()
