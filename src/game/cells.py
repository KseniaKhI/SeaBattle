"""
Определение классов Cell и Ship
"""

import random


class Cell:
    """Класс для представления состояния клетки"""
    EMPTY = 0
    SHIP = 1
    MISS = 2
    HIT = 3
    DESTROYED = 4


class Ship:
    """Класс для представления корабля"""

    def __init__(self, size, x, y, horizontal):
        """
        Инициализация корабля

        Args:
            size (int): Размер корабля (1-4)
            x (int): X координата начала
            y (int): Y координата начала
            horizontal (bool): True если горизонтальный
        """
        self.size = size
        self.x = x
        self.y = y
        self.horizontal = horizontal
        self.health = size
        self.cells = []
        self.update_cells()

    def update_cells(self):
        """Обновление списка клеток, занимаемых кораблем"""
        self.cells = []
        for i in range(self.size):
            if self.horizontal:
                self.cells.append((self.x + i, self.y))
            else:
                self.cells.append((self.x, self.y + i))

    def is_destroyed(self):
        """Проверка, уничтожен ли корабль"""
        return self.health <= 0