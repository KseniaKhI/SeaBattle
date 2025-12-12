#!/usr/bin/env python3
"""
Точка входа в игру "Морской бой"
"""

from game.ui import SeaBattleStable


def main():
    """Основная функция запуска игры"""
    try:
        game = SeaBattleStable()
        game.run()
    except Exception as e:
        print(f"Ошибка: {e}")
        input("Нажмите Enter для выхода...")


if __name__ == "__main__":
    main()