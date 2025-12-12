"""
Основная игровая логика
"""

from .board import Board
from .cells import Ship


class GameLogic:
    """Класс для управления игровой логикой"""

    def __init__(self):
        """Инициализация игры"""
        self.player_board = Board()
        self.computer_board = Board()
        self.placement_mode = True
        self.player_turn = True
        self.game_over = False
        self.computer_shots = []
        self.computer_ai = None

        # Корабли для размещения
        self.ships_to_place = [
            {"size": 4, "count": 1, "placed": 0, "name": "4-палубный (1 шт)"},
            {"size": 3, "count": 2, "placed": 0, "name": "3-палубный (2 шт)"},
            {"size": 2, "count": 3, "placed": 0, "name": "2-палубный (3 шт)"},
            {"size": 1, "count": 4, "placed": 0, "name": "1-палубный (4 шт)"}
        ]

        self.current_ship_size = None
        self.current_ship_horizontal = True

    def select_ship(self, size):
        """Выбор корабля для размещения"""
        for ship_info in self.ships_to_place:
            if ship_info["size"] == size:
                if ship_info["placed"] >= ship_info["count"]:
                    return False, f"Все {size}-палубные корабли уже размещены!"
                break

        self.current_ship_size = size
        orient = "горизонтально" if self.current_ship_horizontal else "вертикально"
        return True, f"Выбран {size}-палубный корабль ({orient})"

    def rotate_ship(self):
        """Поворот текущего корабля"""
        if self.current_ship_size:
            self.current_ship_horizontal = not self.current_ship_horizontal
            orient = "горизонтально" if self.current_ship_horizontal else "вертикально"
            return f"Корабль повёрнут: {orient}"
        return "Сначала выберите корабль!"

    def place_ship(self, x, y):
        """Размещение корабля на поле игрока"""
        if not self.current_ship_size or not self.placement_mode:
            return False, "Не выбран корабль или не режим размещения"

        # Проверка границ
        if self.current_ship_horizontal and x + self.current_ship_size > 10:
            x = 10 - self.current_ship_size
        elif not self.current_ship_horizontal and y + self.current_ship_size > 10:
            y = 10 - self.current_ship_size

        if x < 0 or y < 0:
            return False, "Нельзя разместить за границами поля!"

        ship = Ship(self.current_ship_size, x, y, self.current_ship_horizontal)

        # Проверка возможности размещения
        if not self.player_board.can_place_ship(ship):
            return False, "Нельзя разместить корабль здесь!"

        # Проверка лимита кораблей такого типа
        count_placed = 0
        for placed_ship in self.player_board.ships:
            if placed_ship.size == self.current_ship_size:
                count_placed += 1

        for ship_info in self.ships_to_place:
            if ship_info["size"] == self.current_ship_size:
                if count_placed >= ship_info["count"]:
                    return False, f"Максимум {ship_info['count']} шт. таких кораблей!"
                break

        # Размещение корабля
        if self.player_board.place_ship(ship):
            # Обновление счетчиков
            for ship_info in self.ships_to_place:
                if ship_info["size"] == self.current_ship_size:
                    ship_info["placed"] += 1
                    break

            placed_total = sum(s["placed"] for s in self.ships_to_place)

            if placed_total < 10:
                return True, f"Корабль размещен! Размещено: {placed_total}/10"
            else:
                return True, "Все корабли размещены! Нажмите 'НАЧАТЬ БИТВУ'"
        else:
            return False, "Ошибка при размещении корабля!"

    def remove_ship(self, x, y):
        """Удаление корабля по координатам"""
        for ship in self.player_board.ships[:]:
            if (x, y) in ship.cells:
                self.player_board.remove_ship(ship)

                # Обновление счетчиков
                for ship_info in self.ships_to_place:
                    if ship_info["size"] == ship.size:
                        ship_info["placed"] -= 1
                        break

                placed_total = sum(s["placed"] for s in self.ships_to_place)
                return True, f"Корабль удален. Размещено: {placed_total}/10"

        return False, "Корабль не найден"

    def auto_place_all_ships(self):
        """Автоматическая расстановка всех кораблей"""
        self.player_board = Board()

        # Сброс счетчиков
        for ship_info in self.ships_to_place:
            ship_info["placed"] = 0

        if self.player_board.auto_place_ships():
            # Обновление счетчиков
            for ship in self.player_board.ships:
                for ship_info in self.ships_to_place:
                    if ship_info["size"] == ship.size:
                        ship_info["placed"] += 1
                        break
            return True, "Все корабли автоматически размещены!"
        else:
            return False, "Не удалось разместить корабли!"

    def clear_all_ships(self):
        """Очистка всех кораблей"""
        self.player_board = Board()

        for ship_info in self.ships_to_place:
            ship_info["placed"] = 0

        return True, "Поле очищено. Выберите корабли."

    def start_battle(self):
        """Начало битвы"""
        placed_count = sum(s["placed"] for s in self.ships_to_place)
        if placed_count < 10:
            return False, "Разместите все 10 кораблей!"

        if not self.computer_board.auto_place_ships():
            return False, "Не удалось расставить корабли компьютера!"

        self.placement_mode = False
        self.player_turn = True
        self.game_over = False

        # Импорт здесь чтобы избежать циклических зависимостей
        from .board import SmartAI
        self.computer_ai = SmartAI(self.player_board)

        return True, "Битва началась!"

    def player_shoot(self, x, y):
        """Выстрел игрока по полю компьютера"""
        if not self.player_turn or self.game_over:
            return None, "Не ваш ход или игра окончена"

        result = self.computer_board.shoot(x, y)

        if result == "already_shot":
            return None, "Вы уже стреляли в эту клетку!"

        if result == "miss":
            self.player_turn = False
            return "miss", "Промах! Ход компьютера..."
        elif result == "hit":
            return "hit", "Попадание! Стреляйте ещё!"
        elif result == "destroyed":
            return "destroyed", "Корабль противника уничтожен! Стреляйте ещё!"

        return None, "Неизвестный результат"

    def computer_shoot(self):
        """Выстрел компьютера"""
        if self.player_turn or self.game_over:
            return None, "Ход игрока или игра окончена"

        # Получаем следующий выстрел от ИИ
        x, y = self.computer_ai.get_next_shot()

        result = self.player_board.shoot(x, y)

        # Регистрируем выстрел в ИИ
        self.computer_ai.register_shot(x, y, result)

        if result == "miss":
            self.player_turn = True
            return (x, y, "miss", f"Компьютер стрелял в ({x},{y}) - Промах!\nВАШ ХОД.")
        else:
            hit_text = "Попадание" if result == "hit" else "Корабль уничтожен"
            return (x, y, result, f"Компьютер стрелял в ({x},{y}) - {hit_text}!\nКомпьютер стреляет ещё...")

    def check_game_over(self):
        """Проверка окончания игры"""
        player_ships_alive = any(not ship.is_destroyed() for ship in self.player_board.ships)
        computer_ships_alive = any(not ship.is_destroyed() for ship in self.computer_board.ships)

        if not player_ships_alive or not computer_ships_alive:
            self.game_over = True
            winner = "КОМПЬЮТЕР" if not player_ships_alive else "ВЫ"
            player_score = sum(1 for s in self.computer_board.ships if s.is_destroyed())
            computer_score = sum(1 for s in self.player_board.ships if s.is_destroyed())

            return {
                "game_over": True,
                "winner": winner,
                "player_score": player_score,
                "computer_score": computer_score
            }

        return {"game_over": False}

    def get_ships_to_place(self):
        """Получить информацию о кораблях для размещения"""
        return self.ships_to_place

    def get_placed_total(self):
        """Получить общее количество размещенных кораблей"""
        return sum(s["placed"] for s in self.ships_to_place)