import tkinter as tk
import math
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Top-Down Game - Level 1")
        self.root.geometry("800x600")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, width=800, height=600, bg="#1a1a1a")
        self.canvas.pack(fill="both", expand=True)
        
        # Создаем игрока в центре в виде фиолетового ромбика (полигон)
        # Координаты ромба относительно центра (400, 300): верх, право, низ, лево
        self.player_x = 400
        self.player_y = 300
        self.player_size = 18 # Радиус ромба
        self.player_id = self.canvas.create_polygon(
            self.player_x, self.player_y - self.player_size,  # Верх
            self.player_x + self.player_size, self.player_y,  # Право
            self.player_x, self.player_y + self.player_size,  # Низ
            self.player_x - self.player_size, self.player_y,  # Лево
            fill="#9b59b6", outline="#8e44ad", width=2
        )
        
        self.player_speed = 4.5
        self.hp = 100
        
        # Списки врагов
        self.enemies = []
        
        # Управление
        self.keys_pressed = {}
        self.root.bind("<KeyPress>", self.on_key_press)
        self.root.bind("<KeyRelease>", self.on_key_release)
        
        # UI (Интерфейс 1 уровня)
        self.ui_text = self.canvas.create_text(20, 20, anchor="nw", fill="white", font=("Arial", 12, "bold"), 
                                               text="Level: 1 / 1 | HP: 100/100 | Survive & Fight!")
        
        # Спавн начальных врагов
        for _ in range(3):
            self.spawn_enemy()
            
        # Запуск быстрого игрового цикла (~60 FPS: 16 мс)
        self.update_game()

    def on_key_press(self, event):
        self.keys_pressed[event.keysym] = True
        self.keys_pressed[event.char] = True

    def on_key_release(self, event):
        self.keys_pressed.pop(event.keysym, None)
        self.keys_pressed.pop(event.char, None)

    def spawn_enemy(self):
        x = random.choice([-30, 830])
        y = random.randint(50, 550)
        e_id = self.canvas.create_rectangle(x, y, x + 20, y + 20, fill="#e74c3c", outline="")
        self.enemies.append({"id": e_id, "speed": 2.0})

    def update_game(self):
        # 1. Плавное движение игрока
        dx, dy = 0, 0
        if self.keys_pressed.get("w") or self.keys_pressed.get("Up"):    dy -= self.player_speed
        if self.keys_pressed.get("s") or self.keys_pressed.get("Down"):  dy += self.player_speed
        if self.keys_pressed.get("a") or self.keys_pressed.get("Left"):  dx -= self.player_speed
        if self.keys_pressed.get("d") or self.keys_pressed.get("Right"): dx += self.player_speed
        
        # Строгие границы уровня (учитываем размер ромба, чтобы не вылезал за экран)
        self.player_x = max(self.player_size, min(800 - self.player_size, self.player_x + dx))
        self.player_y = max(self.player_size, min(600 - self.player_size, self.player_y + dy))
        
        # Пересчитываем координаты вершин ромба для плавного перемещения
        self.canvas.coords(
            self.player_id,
            self.player_x, self.player_y - self.player_size,
            self.player_x + self.player_size, self.player_y,
            self.player_x, self.player_y + self.player_size,
            self.player_x - self.player_size, self.player_y
        )

        # 2. Логика врагов
        for enemy in self.enemies:
            e_coords = self.canvas.coords(enemy["id"])
            if not e_coords: continue
            ex, ey = (e_coords[0] + e_coords[2]) / 2, (e_coords[1] + e_coords[3]) / 2
            
            angle = math.atan2(self.player_y - ey, self.player_x - ex)
            edx = math.cos(angle) * enemy["speed"]
            edy = math.sin(angle) * enemy["speed"]
            
            self.canvas.move(enemy["id"], edx, edy)
            
            # Столкновение с игроком
            if math.hypot(self.player_x - ex, self.player_y - ey) < 20:
                self.hp -= 1
                if self.hp <= 0:
                    self.canvas.create_text(400, 300, text="GAME OVER", fill="#e74c3c", font=("Arial", 36, "bold"), anchor="center")
                    return # Стоп цикл

        # Периодический спавн новых врагов (поддерживаем популяцию)
        if len(self.enemies) < 6 and random.random() < 0.04:
            self.spawn_enemy()

        # 3. Обновление UI
        self.canvas.itemconfig(self.ui_text, text=f"Level: 1 / 1 | HP: {max(0, self.hp)}/100 | Enemies: {len(self.enemies)}")
        
        # ~60 FPS (16 миллисекунд) для идеальной плавности
        self.root.after(16, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()