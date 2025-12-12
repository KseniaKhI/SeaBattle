"""
Графический интерфейс игры
"""

import tkinter as tk
from tkinter import messagebox
from .game_logic import GameLogic
from .cells import Cell


class SeaBattleStable:
    """Основной класс для управления UI игры"""

    def __init__(self):
        """Инициализация игры"""
        self.root = tk.Tk()
        self.root.title("Морской бой")

        # Полноэкранный режим
        self.root.attributes('-fullscreen', True)

        # Получаем размеры экрана
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Фиксированные размеры
        self.font_sizes = {
            'title': 36,
            'button': 16,
            'label': 14,
            'small': 12,
            'canvas': 400
        }

        # Инициализация игровой логики
        self.game_logic = GameLogic()

        # Создание главного меню
        self.show_main_menu()

        # Привязка клавиши ESC
        self.root.bind('<Escape>', self.exit_fullscreen)

    def exit_fullscreen(self, event=None):
        """Выход из полноэкранного режима"""
        self.root.attributes('-fullscreen', False)
        self.root.geometry(f"{self.screen_width - 100}x{self.screen_height - 100}")

    def show_main_menu(self):
        """Показывает главное меню"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Фон
        bg_frame = tk.Frame(self.root, bg="#2C3E50")
        bg_frame.pack(fill=tk.BOTH, expand=True)

        # Центральный фрейм
        center_frame = tk.Frame(bg_frame, bg="#2C3E50")
        center_frame.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

        # Заголовок
        title_label = tk.Label(center_frame, text="МОРСКОЙ БОЙ",
                               font=("Arial", self.font_sizes['title'], "bold"),
                               fg="#ECF0F1", bg="#2C3E50")
        title_label.pack(pady=30)

        # Фрейм для кнопок
        buttons_frame = tk.Frame(center_frame, bg="#2C3E50")
        buttons_frame.pack(pady=20)

        # Кнопка начать игру
        start_button = tk.Button(buttons_frame, text="НАЧАТЬ ИГРУ",
                                 command=self.start_game_setup,
                                 font=("Arial", self.font_sizes['button'], "bold"),
                                 bg="#3498DB", fg="white",
                                 activebackground="#2980B9",
                                 width=18, height=2,
                                 relief=tk.RAISED, bd=3)
        start_button.pack(pady=10)

        # Кнопка выхода
        exit_button = tk.Button(buttons_frame, text="ВЫЙТИ",
                                command=self.root.quit,
                                font=("Arial", self.font_sizes['button'], "bold"),
                                bg="#E74C3C", fg="white",
                                activebackground="#C0392B",
                                width=18, height=2,
                                relief=tk.RAISED, bd=3)
        exit_button.pack(pady=10)

        # Правила
        rules_frame = tk.Frame(bg_frame, bg="#2C3E50")
        rules_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=20)

        rules = [
            "Правила игры:",
            "1. Расставьте 10 кораблей на своём поле",
            "2. Корабли не должны касаться друг друга",
            "3. По очереди стреляйте по полю противника",
            "4. Побеждает тот, кто первым уничтожит все корабли",
            "",
            "Управление: ESC - выйти из полноэкранного режима • ПКМ - удалить корабль"
        ]

        for rule in rules:
            label = tk.Label(rules_frame, text=rule,
                             font=("Arial", self.font_sizes['small']),
                             fg="#BDC3C7", bg="#2C3E50",
                             justify=tk.CENTER)
            label.pack()

    def start_game_setup(self):
        """Начинает расстановку кораблей"""
        for widget in self.root.winfo_children():
            widget.destroy()

        # Основной фрейм
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Заголовок
        title_frame = tk.Frame(main_frame, bg="#2C3E50", height=70)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        title_label = tk.Label(title_frame, text="РАССТАНОВКА КОРАБЛЕЙ",
                               font=("Arial", 28, "bold"),
                               fg="#ECF0F1", bg="#2C3E50")
        title_label.pack(expand=True)

        # Основной контент
        content_frame = tk.Frame(main_frame, bg="#ECF0F1")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Левая колонка - поле игрока
        left_column = tk.Frame(content_frame, bg="#ECF0F1")
        left_column.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        # Поле игрока
        field_frame = tk.Frame(left_column, bg="#ECF0F1")
        field_frame.pack(expand=True)

        field_label = tk.Label(field_frame, text="ВАШЕ ПОЛЕ",
                               font=("Arial", 18, "bold"), bg="#ECF0F1")
        field_label.pack(pady=5)

        # Фиксированный размер поля
        self.player_canvas = tk.Canvas(field_frame,
                                       width=self.font_sizes['canvas'],
                                       height=self.font_sizes['canvas'],
                                       bg="white", relief=tk.RAISED, bd=2)
        self.player_canvas.pack()

        # Правая колонка - управление
        right_column = tk.Frame(content_frame, bg="#ECF0F1", width=350)
        right_column.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        right_column.pack_propagate(False)

        # Статус
        status_frame = tk.Frame(right_column, bg="#ECF0F1", height=100)
        status_frame.pack(fill=tk.X, pady=5)
        status_frame.pack_propagate(False)

        self.status_label = tk.Label(status_frame,
                                     text="Разместите свои корабли\nна поле слева\n\nВыберите корабль:",
                                     font=("Arial", self.font_sizes['label']), bg="#ECF0F1",
                                     justify=tk.LEFT, wraplength=330,
                                     anchor=tk.W)
        self.status_label.pack(pady=10, padx=5)

        # Корабли для размещения
        self.ships_buttons = []
        ships_frame = tk.LabelFrame(right_column, text="КОРАБЛИ ДЛЯ РАЗМЕЩЕНИЯ",
                                    font=("Arial", self.font_sizes['label'], "bold"), bg="#ECF0F1")
        ships_frame.pack(fill=tk.X, pady=5)

        ships_to_place = self.game_logic.get_ships_to_place()
        for ship_info in ships_to_place:
            ship_btn = tk.Button(ships_frame, text=ship_info["name"],
                                 command=lambda s=ship_info["size"]: self.select_ship(s),
                                 font=("Arial", self.font_sizes['small']),
                                 bg="#3498DB", fg="white",
                                 width=25, height=1)
            ship_btn.pack(pady=3, padx=5)
            self.ships_buttons.append((ship_info["size"], ship_btn))

        # Кнопки управления
        control_frame = tk.LabelFrame(right_column, text="УПРАВЛЕНИЕ",
                                      font=("Arial", self.font_sizes['label'], "bold"), bg="#ECF0F1")
        control_frame.pack(fill=tk.X, pady=5)

        rotate_btn = tk.Button(control_frame, text="ПОВЕРНУТЬ КОРАБЛЬ",
                               command=self.rotate_ship,
                               font=("Arial", self.font_sizes['small']),
                               bg="#16A085", fg="white",
                               width=25, height=1)
        rotate_btn.pack(pady=3)

        auto_btn = tk.Button(control_frame, text="АВТОРАССТАНОВКА",
                             command=self.auto_place_ships,
                             font=("Arial", self.font_sizes['small']),
                             bg="#27AE60", fg="white",
                             width=25, height=1)
        auto_btn.pack(pady=3)

        clear_btn = tk.Button(control_frame, text="ОЧИСТИТЬ ПОЛЕ",
                              command=self.clear_ships,
                              font=("Arial", self.font_sizes['small']),
                              bg="#E74C3C", fg="white",
                              width=25, height=1)
        clear_btn.pack(pady=3)

        # Кнопка начала игры
        start_battle_frame = tk.Frame(right_column, bg="#ECF0F1", height=70)
        start_battle_frame.pack(fill=tk.X, pady=10)
        start_battle_frame.pack_propagate(False)

        self.start_game_btn = tk.Button(start_battle_frame, text="НАЧАТЬ БИТВУ",
                                        command=self.start_battle,
                                        font=("Arial", self.font_sizes['button'], "bold"),
                                        bg="#2C3E50", fg="white",
                                        state=tk.DISABLED,
                                        width=25, height=2)
        self.start_game_btn.pack(pady=10)

        # Легенда
        legend_frame = tk.LabelFrame(main_frame, text="ЛЕГЕНДА",
                                     font=("Arial", 14, "bold"), bg="#ECF0F1")
        legend_frame.pack(fill=tk.X, padx=10, pady=5)

        legend_items = [
            ("■", "Ваш корабль", "#3498DB"),
            ("✕", "Попадание", "#E74C3C"),
            ("○", "Промах", "#BDC3C7"),
            ("☠", "Уничтожен", "#2C3E50"),
            ("□", "Пустая клетка", "#FFFFFF")
        ]

        legend_row = tk.Frame(legend_frame, bg="#ECF0F1")
        legend_row.pack(fill=tk.X, padx=10, pady=5)

        for symbol, desc, color in legend_items:
            item_frame = tk.Frame(legend_row, bg="#ECF0F1")
            item_frame.pack(side=tk.LEFT, padx=15)

            color_frame = tk.Frame(item_frame, width=30, height=30, bg=color, relief=tk.RAISED, bd=1)
            color_frame.pack(side=tk.LEFT)
            color_frame.pack_propagate(False)

            color_label = tk.Label(color_frame, text=symbol,
                                   font=("Arial", 14),
                                   bg=color, fg="white" if color in ["#3498DB", "#2C3E50", "#E74C3C"] else "black")
            color_label.pack(expand=True)

            desc_label = tk.Label(item_frame, text=desc,
                                  font=("Arial", self.font_sizes['small']),
                                  bg="#ECF0F1", anchor=tk.W)
            desc_label.pack(side=tk.LEFT, padx=5)

        # Привязка событий
        self.player_canvas.bind("<Motion>", self.on_player_hover)
        self.player_canvas.bind("<Button-1>", self.on_player_click)
        self.player_canvas.bind("<Button-3>", self.on_player_right_click)

        # Отрисовка пустого поля
        self.draw_board_fixed(self.player_canvas, self.game_logic.player_board, hide_ships=False)

    def draw_board_fixed(self, canvas, board, hide_ships=True):
        """Фиксированная отрисовка игрового поля"""
        canvas.delete("all")

        # Фиксированный размер клетки
        cell_size = 32
        offset_x = 40
        offset_y = 40

        # Номера столбцов
        for x in range(10):
            x_center = offset_x + x * cell_size + cell_size // 2
            canvas.create_text(x_center, offset_y // 2,
                               text=str(x),
                               font=("Arial", 12, "bold"),
                               fill="black")

        # Номера строк
        for y in range(10):
            y_center = offset_y + y * cell_size + cell_size // 2
            canvas.create_text(offset_x // 2, y_center,
                               text=str(y),
                               font=("Arial", 12, "bold"),
                               fill="black")

        # Сетка и клетки
        for y in range(10):
            for x in range(10):
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                cell_state = board.grid[y][x]

                # Цвет и символ
                if cell_state == Cell.EMPTY:
                    fill_color = "white"
                    symbol = ""
                elif cell_state == Cell.SHIP:
                    if hide_ships:
                        fill_color = "white"
                        symbol = ""
                    else:
                        fill_color = "#3498DB"
                        symbol = "■"
                elif cell_state == Cell.MISS:
                    fill_color = "#BDC3C7"
                    symbol = "○"
                elif cell_state == Cell.HIT:
                    fill_color = "#E74C3C"
                    symbol = "✕"
                elif cell_state == Cell.DESTROYED:
                    fill_color = "#2C3E50"
                    symbol = "☠"

                # Рисуем клетку
                canvas.create_rectangle(x1, y1, x2, y2,
                                        fill=fill_color,
                                        outline="black",
                                        width=1)

                # Символ
                if symbol:
                    font_size = 16
                    if symbol == "☠":
                        font_size = 18

                    canvas.create_text(x1 + cell_size // 2, y1 + cell_size // 2,
                                       text=symbol,
                                       font=("Arial", font_size),
                                       fill="white" if cell_state in [Cell.SHIP, Cell.DESTROYED] else "black")

        # Внешняя рамка
        canvas.create_rectangle(offset_x, offset_y,
                                offset_x + 10 * cell_size, offset_y + 10 * cell_size,
                                outline="black", width=2)

    def update_ship_buttons(self):
        """Обновляет состояние кнопок кораблей"""
        ships_to_place = self.game_logic.get_ships_to_place()
        for ship_info in ships_to_place:
            for size, btn in self.ships_buttons:
                if size == ship_info["size"]:
                    if ship_info["placed"] >= ship_info["count"]:
                        btn.config(state=tk.DISABLED, bg="#95A5A6")
                    else:
                        btn.config(state=tk.NORMAL, bg="#3498DB")
                    break

    def select_ship(self, size):
        """Выбор корабля"""
        success, message = self.game_logic.select_ship(size)
        self.status_label.config(text=message)
        self.update_ship_buttons()

    def rotate_ship(self):
        """Поворот корабля"""
        message = self.game_logic.rotate_ship()
        self.status_label.config(text=message)

    def on_player_hover(self, event):
        """Предпросмотр размещения корабля"""
        if not self.game_logic.current_ship_size:
            return

        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            # Создаем временную доску для предпросмотра
            from .board import Board
            from .cells import Ship

            temp_board = Board()
            temp_board.grid = [row[:] for row in self.game_logic.player_board.grid]

            # Корректируем координаты если корабль выходит за границы
            current_ship_horizontal = self.game_logic.current_ship_horizontal
            current_ship_size = self.game_logic.current_ship_size

            if current_ship_horizontal and x + current_ship_size > 10:
                x = 10 - current_ship_size
            elif not current_ship_horizontal and y + current_ship_size > 10:
                y = 10 - current_ship_size

            if x >= 0 and y >= 0:
                temp_ship = Ship(current_ship_size, x, y, current_ship_horizontal)

                # Проверяем можно ли разместить
                can_place = temp_board.can_place_ship(temp_ship)

                # Проверяем лимит кораблей такого типа
                if can_place:
                    ships_to_place = self.game_logic.get_ships_to_place()
                    for ship_info in ships_to_place:
                        if ship_info["size"] == current_ship_size:
                            count_placed = 0
                            for placed_ship in self.game_logic.player_board.ships:
                                if placed_ship.size == current_ship_size:
                                    count_placed += 1
                            if count_placed >= ship_info["count"]:
                                can_place = False
                            break

                if can_place:
                    temp_board.place_ship(temp_ship, ignore_ships=True)

                self.draw_board_fixed(self.player_canvas, temp_board, hide_ships=False)

    def on_player_click(self, event):
        """Размещение корабля"""
        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            success, message = self.game_logic.place_ship(x, y)
            self.status_label.config(text=message)

            if success:
                self.update_ship_buttons()
                self.draw_board_fixed(self.player_canvas, self.game_logic.player_board, hide_ships=False)

                placed_total = self.game_logic.get_placed_total()
                if placed_total >= 10:
                    self.start_game_btn.config(state=tk.NORMAL, bg="#27AE60")

    def on_player_right_click(self, event):
        """Удаление корабля"""
        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            success, message = self.game_logic.remove_ship(x, y)
            if success:
                self.status_label.config(text=message)
                self.update_ship_buttons()
                self.draw_board_fixed(self.player_canvas, self.game_logic.player_board, hide_ships=False)
                self.start_game_btn.config(state=tk.DISABLED, bg="#2C3E50")

    def auto_place_ships(self):
        """Автоматическая расстановка кораблей"""
        success, message = self.game_logic.auto_place_all_ships()
        if success:
            self.status_label.config(text=message)
            self.update_ship_buttons()
            self.draw_board_fixed(self.player_canvas, self.game_logic.player_board, hide_ships=False)
            self.start_game_btn.config(state=tk.NORMAL, bg="#27AE60")
        else:
            messagebox.showerror("Ошибка", message)

    def clear_ships(self):
        """Очистка всех кораблей"""
        success, message = self.game_logic.clear_all_ships()
        self.status_label.config(text=message)
        self.update_ship_buttons()
        self.draw_board_fixed(self.player_canvas, self.game_logic.player_board, hide_ships=False)
        self.start_game_btn.config(state=tk.DISABLED, bg="#2C3E50")

    def start_battle(self):
        """Начало битвы"""
        success, message = self.game_logic.start_battle()
        if not success:
            messagebox.showwarning("Не все корабли", message)
            return

        for widget in self.root.winfo_children():
            widget.destroy()

        # Основной фрейм с фиксированной структурой
        main_frame = tk.Frame(self.root, bg="#ECF0F1")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        # Заголовок
        title_frame = tk.Frame(main_frame, bg="#2C3E50", height=70)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)

        self.battle_title = tk.Label(title_frame, text="МОРСКОЙ БОЙ - ИДЁТ БИТВА",
                                     font=("Arial", 28, "bold"),
                                     fg="#ECF0F1", bg="#2C3E50")
        self.battle_title.pack(expand=True)

        # Игровые поля
        fields_frame = tk.Frame(main_frame, bg="#ECF0F1")
        fields_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Левое поле (игрок)
        left_panel = tk.Frame(fields_frame, bg="#ECF0F1")
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)

        player_field_frame = tk.Frame(left_panel, bg="#ECF0F1")
        player_field_frame.pack(expand=True)

        player_label = tk.Label(player_field_frame, text="ВАШЕ ПОЛЕ",
                                font=("Arial", 18, "bold"), bg="#ECF0F1")
        player_label.pack(pady=5)

        self.player_canvas_battle = tk.Canvas(player_field_frame,
                                              width=self.font_sizes['canvas'],
                                              height=self.font_sizes['canvas'],
                                              bg="white", relief=tk.RAISED, bd=2)
        self.player_canvas_battle.pack()

        # Правое поле (компьютер)
        right_panel = tk.Frame(fields_frame, bg="#ECF0F1")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10)

        computer_field_frame = tk.Frame(right_panel, bg="#ECF0F1")
        computer_field_frame.pack(expand=True)

        computer_label = tk.Label(computer_field_frame, text="ПОЛЕ ПРОТИВНИКА",
                                  font=("Arial", 18, "bold"), bg="#ECF0F1")
        computer_label.pack(pady=5)

        self.computer_canvas = tk.Canvas(computer_field_frame,
                                         width=self.font_sizes['canvas'],
                                         height=self.font_sizes['canvas'],
                                         bg="white", relief=tk.RAISED, bd=2)
        self.computer_canvas.pack()
        self.computer_canvas.bind("<Button-1>", self.on_computer_click)

        # Статус
        status_frame = tk.Frame(main_frame, bg="#ECF0F1", height=80)
        status_frame.pack(fill=tk.X, padx=20, pady=10)
        status_frame.pack_propagate(False)

        self.battle_status = tk.Label(status_frame,
                                      text="ВАШ ХОД. Стреляйте по полю противника!",
                                      font=("Arial", 16, "bold"),
                                      bg="#ECF0F1", fg="#2C3E50",
                                      wraplength=800,
                                      justify=tk.CENTER)
        self.battle_status.pack(expand=True)

        # Кнопка сдаться
        surrender_frame = tk.Frame(main_frame, bg="#ECF0F1", height=60)
        surrender_frame.pack(fill=tk.X, padx=20, pady=5)
        surrender_frame.pack_propagate(False)

        surrender_btn = tk.Button(surrender_frame, text="СДАТЬСЯ",
                                  command=self.surrender,
                                  font=("Arial", self.font_sizes['button'], "bold"),
                                  bg="#E74C3C", fg="white",
                                  width=20, height=2)
        surrender_btn.pack(pady=10)

        # Легенда
        legend_frame = tk.LabelFrame(main_frame, text="ЛЕГЕНДА",
                                     font=("Arial", 14, "bold"), bg="#ECF0F1")
        legend_frame.pack(fill=tk.X, padx=10, pady=5)

        legend_items = [
            ("■", "Ваш корабль", "#3498DB"),
            ("✕", "Попадание", "#E74C3C"),
            ("○", "Промах", "#BDC3C7"),
            ("☠", "Уничтожен", "#2C3E50"),
            ("□", "Пустая клетка", "#FFFFFF")
        ]

        legend_row = tk.Frame(legend_frame, bg="#ECF0F1")
        legend_row.pack(fill=tk.X, padx=10, pady=5)

        for symbol, desc, color in legend_items:
            item_frame = tk.Frame(legend_row, bg="#ECF0F1")
            item_frame.pack(side=tk.LEFT, padx=15)

            color_frame = tk.Frame(item_frame, width=30, height=30, bg=color, relief=tk.RAISED, bd=1)
            color_frame.pack(side=tk.LEFT)
            color_frame.pack_propagate(False)

            color_label = tk.Label(color_frame, text=symbol,
                                   font=("Arial", 14),
                                   bg=color, fg="white" if color in ["#3498DB", "#2C3E50", "#E74C3C"] else "black")
            color_label.pack(expand=True)

            desc_label = tk.Label(item_frame, text=desc,
                                  font=("Arial", self.font_sizes['small']),
                                  bg="#ECF0F1", anchor=tk.W)
            desc_label.pack(side=tk.LEFT, padx=5)

        # Отрисовываем поля
        self.draw_board_fixed(self.player_canvas_battle, self.game_logic.player_board, hide_ships=False)
        self.draw_board_fixed(self.computer_canvas, self.game_logic.computer_board, hide_ships=True)

    def on_computer_click(self, event):
        """Выстрел по полю компьютера"""
        if not self.game_logic.player_turn or self.game_logic.game_over:
            return

        cell_size = 32
        offset_x = 40
        offset_y = 40

        x = (event.x - offset_x) // cell_size
        y = (event.y - offset_y) // cell_size

        if 0 <= x < 10 and 0 <= y < 10:
            self.player_shoot(x, y)

    def player_shoot(self, x, y):
        """Обработка выстрела игрока"""
        result, message = self.game_logic.player_shoot(x, y)

        if result is None:
            self.battle_status.config(text=message)
            return

        self.draw_board_fixed(self.computer_canvas, self.game_logic.computer_board, hide_ships=True)

        if result == "miss":
            self.battle_status.config(text=message)
            # Ход компьютера
            self.root.after(1000, self.computer_turn)
        else:
            self.battle_status.config(text=message)

            # Проверка окончания игры
            game_over_info = self.game_logic.check_game_over()
            if game_over_info["game_over"]:
                self.show_game_over(game_over_info)

    def computer_turn(self):
        """Ход компьютера"""
        if self.game_logic.game_over:
            return

        result = self.game_logic.computer_shoot()
        if result is None:
            return

        x, y, shot_result, message = result

        # Обновляем поле игрока
        self.draw_board_fixed(self.player_canvas_battle, self.game_logic.player_board, hide_ships=False)

        self.battle_status.config(text=message)

        # Проверка окончания игры
        game_over_info = self.game_logic.check_game_over()
        if game_over_info["game_over"]:
            self.show_game_over(game_over_info)
            return

        if shot_result == "miss":
            # Возвращаем ход игроку
            return
        else:
            # Компьютер стреляет еще раз
            self.root.after(1500, self.computer_turn)

    def show_game_over(self, game_over_info):
        """Показать окно окончания игры"""
        self.game_logic.game_over = True
        self.computer_canvas.unbind("<Button-1>")

        # Показываем все корабли компьютера
        self.draw_board_fixed(self.computer_canvas, self.game_logic.computer_board, hide_ships=False)

        result_window = tk.Toplevel(self.root)
        result_window.title("Игра окончена!")
        result_window.geometry("400x300")
        result_window.resizable(False, False)
        result_window.configure(bg="#2C3E50")
        result_window.transient(self.root)
        result_window.grab_set()

        result_window.update_idletasks()
        width = result_window.winfo_width()
        height = result_window.winfo_height()
        x = (self.screen_width // 2) - (width // 2)
        y = (self.screen_height // 2) - (height // 2)
        result_window.geometry(f'{width}x{height}+{x}+{y}')

        result_label = tk.Label(result_window,
                                text=f"ПОБЕДИЛ: {game_over_info['winner']}",
                                font=("Arial", 24, "bold"),
                                fg="#ECF0F1", bg="#2C3E50")
        result_label.pack(pady=30)

        stats_text = f"Уничтожено кораблей:\nВы: {game_over_info['player_score']}/10\nКомпьютер: {game_over_info['computer_score']}/10"

        stats_label = tk.Label(result_window, text=stats_text,
                               font=("Arial", 14),
                               fg="#BDC3C7", bg="#2C3E50")
        stats_label.pack(pady=20)

        new_game_btn = tk.Button(result_window, text="НОВАЯ ИГРА",
                                 command=self.new_game,
                                 font=("Arial", 14, "bold"),
                                 bg="#3498DB", fg="white",
                                 width=15, height=2)
        new_game_btn.pack(pady=20)

    def surrender(self):
        """Сдача"""
        if messagebox.askyesno("Сдаться", "Вы уверены, что хотите сдаться?"):
            self.game_logic.game_over = True
            self.computer_canvas.unbind("<Button-1>")

            result_window = tk.Toplevel(self.root)
            result_window.title("Игра окончена!")
            result_window.geometry("400x250")
            result_window.resizable(False, False)
            result_window.configure(bg="#2C3E50")
            result_window.transient(self.root)
            result_window.grab_set()

            result_window.update_idletasks()
            width = result_window.winfo_width()
            height = result_window.winfo_height()
            x = (self.screen_width // 2) - (width // 2)
            y = (self.screen_height // 2) - (height // 2)
            result_window.geometry(f'{width}x{height}+{x}+{y}')

            result_label = tk.Label(result_window,
                                    text="ВЫ СДАЛИСЬ\nПОБЕДИЛ: КОМПЬЮТЕР",
                                    font=("Arial", 20, "bold"),
                                    fg="#ECF0F1", bg="#2C3E50")
            result_label.pack(pady=30)

            new_game_btn = tk.Button(result_window, text="НОВАЯ ИГРА",
                                     command=self.new_game,
                                     font=("Arial", 14, "bold"),
                                     bg="#3498DB", fg="white",
                                     width=15, height=2)
            new_game_btn.pack(pady=30)

    def new_game(self):
        """Новая игра"""
        for widget in self.root.winfo_children():
            if isinstance(widget, tk.Toplevel):
                widget.destroy()

        # Переинициализируем игровую логику
        self.game_logic = GameLogic()
        self.show_main_menu()

    def run(self):
        """Запуск приложения"""
        self.root.mainloop()