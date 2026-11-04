import math
import random
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class Boss:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.x = x
        self.y = y
        self.hp = 25
        self.max_hp = 25
        self.size = 35
        
        self.outer = canvas.create_rectangle(x-38, y-38, x+38, y+38, fill="", outline="#ef4444", width=3)
        self.body = canvas.create_rectangle(x-30, y-30, x+30, y+30, fill="#7f1d1d", outline="#fca5a5", width=2)
        self.core = canvas.create_rectangle(x-12, y-12, x+12, y+12, fill="#ef4444", outline="#fee2e2", width=1.5)
        
        self.hp_bg = canvas.create_rectangle(WINDOW_WIDTH/2 - 150, 60, WINDOW_WIDTH/2 + 150, 70, fill="#181824", outline="#7f1d1d")
        self.hp_fill = canvas.create_rectangle(WINDOW_WIDTH/2 - 148, 62, WINDOW_WIDTH/2 + 148, 68, fill="#ef4444", outline="")
        
        self.speed = 0.8
        self.attack_cooldown = 150
        self.attack_timer = 70
        self.is_warning = False
        self.warning_ticks = 0
        self.current_aim_angle = 0.0
        self.warning_line = None

    def update(self, player_x, player_y, canvas, particles):
        # Движение босса с ограничением в пределах стен арены
        angle = math.atan2(player_y - self.y, player_x - self.x)
        self.x += math.cos(angle) * self.speed
        self.y += math.sin(angle) * self.speed
        
        self.x = max(50, min(WINDOW_WIDTH - 50, self.x))
        self.y = max(100, min(WINDOW_HEIGHT - 50, self.y))
        
        canvas.coords(self.outer, self.x-38, self.y-38, self.x+38, self.y+38)
        canvas.coords(self.body, self.x-30, self.y-30, self.x+30, self.y+30)
        canvas.coords(self.core, self.x-12, self.y-12, self.x+12, self.y+12)
        
        res_laser = None
        if not self.is_warning:
            self.attack_timer -= 1
            if self.attack_timer <= 0:
                self.is_warning = True
                self.warning_ticks = 65  # Время подготовки предупреждения
                
                # Сначала босс целится точно в центр игрока в момент старта
                self.current_aim_angle = math.atan2(player_y - self.y, player_x - self.x)
                
                length = 1500
                lx2 = self.x + math.cos(self.current_aim_angle) * length
                ly2 = self.y + math.sin(self.current_aim_angle) * length
                self.warning_line = canvas.create_line(self.x, self.y, lx2, ly2, fill="#ef4444", dash=(4, 4), width=2)
        else:
            self.warning_ticks -= 1
            
            # Желаемый угол на игрока в данный момент
            desired_angle = math.atan2(player_y - self.y, player_x - self.x)
            diff = (desired_angle - self.current_aim_angle + math.pi) % (2 * math.pi) - math.pi
            
            # Делаем скорость доворота прицела значительно ниже (в два раза медленнее скорости игрока / плавное отставание)
            max_turn_speed = 0.012 
            if abs(diff) > max_turn_speed:
                self.current_aim_angle += max_turn_speed if diff > 0 else -max_turn_speed
            else:
                self.current_aim_angle = desired_angle
            
            length = 1500
            lx2 = self.x + math.cos(self.current_aim_angle) * length
            ly2 = self.y + math.sin(self.current_aim_angle) * length
            canvas.coords(self.warning_line, self.x, self.y, lx2, ly2)
            
            if self.warning_ticks <= 0:
                canvas.delete(self.warning_line)
                self.is_warning = False
                self.attack_timer = self.attack_cooldown
                
                outer_id = canvas.create_line(0, 0, 0, 0, fill="#f87171", width=22)
                glow_id = canvas.create_line(0, 0, 0, 0, fill="#ef4444", width=12)
                core_id = canvas.create_line(0, 0, 0, 0, fill="#ffffff", width=5)
                res_laser = {"core": core_id, "glow": glow_id, "outer": outer_id, "x": self.x, "y": self.y, "angle": self.current_aim_angle, "life": 40, "is_boss": True}

        hp_width = 296 * (max(0, self.hp) / self.max_hp)
        canvas.coords(self.hp_fill, WINDOW_WIDTH/2 - 148, 62, WINDOW_WIDTH/2 - 148 + hp_width, 68)
        
        return res_laser

    def take_damage(self, amount, canvas, particles):
        self.hp -= amount
        for _ in range(3):
            particles.append({"x": self.x, "y": self.y, "dx": random.uniform(-3, 3), "dy": random.uniform(-3, 3), "life": 10, "color": "#ef4444", "id": canvas.create_rectangle(self.x-2, self.y-2, self.x+2, self.y+2, fill="#fca5a5", outline="")})
        if self.hp <= 0:
            self.delete(canvas)
            return True
        return False

    def delete(self, canvas):
        canvas.delete(self.body)
        canvas.delete(self.outer)
        canvas.delete(self.core)
        canvas.delete(self.hp_bg)
        canvas.delete(self.hp_fill)
        if self.warning_line:
            canvas.delete(self.warning_line)