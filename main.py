import tkinter as tk
import math
import random

class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Plasma Top-Down Game - Level 1")
        self.root.geometry("900x700")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, width=900, height=700, bg="#07070c", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.draw_background_debris()
        
        self.canvas.create_rectangle(0, 0, 900, 45, fill="#11111a", outline="#1c1c2e", width=2)
        self.ui_text = self.canvas.create_text(20, 22, anchor="w", fill="#d8b4fe", font=("Consolas", 11, "bold"), text="")
        
        self.player_x = 450
        self.player_y = 370
        self.player_size = 16
        self.player_id = self.canvas.create_polygon(self.player_x, self.player_y-self.player_size, self.player_x+self.player_size, self.player_y, self.player_x, self.player_y+self.player_size, self.player_x-self.player_size, self.player_y, fill="#c084fc", outline="#f3e8ff", width=2)
        
        self.max_speed = 5.0
        self.lives = 3
        self.stamina = 100.0
        self.space_pressed = False
        self.is_ramming = False
        self.ram_aura = self.canvas.create_oval(0, 0, 0, 0, outline="", width=2)
        
        self.enemies_remaining = 50
        self.spawn_counter = 0
        
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.trails = []
        
        self.mouse_x = 450
        self.mouse_y = 370
        
        self.aim_line = self.canvas.create_line(0, 0, 0, 0, fill="#a855f7", dash=(3, 3), width=1)
        self.crosshair = self.canvas.create_oval(0, 0, 0, 0, outline="#e879f9", width=1.5)
        
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-3>", self.on_right_click)
        self.root.bind("<KeyPress-space>", lambda e: setattr(self, "space_pressed", True))
        self.root.bind("<KeyRelease-space>", lambda e: setattr(self, "space_pressed", False))
        
        for _ in range(5): self.spawn_enemy()
        self.update_game()

    def draw_background_debris(self):
        for _ in range(35):
            x, y = random.randint(20, 880), random.randint(65, 680)
            sz = random.randint(2, 6)
            self.canvas.create_polygon(x, y-sz, x+sz, y, x, y+sz, x-sz, y, fill="#12121e", outline="#1e1e30", width=1)

    def on_mouse_move(self, event):
        self.mouse_x = max(0, min(900, event.x))
        self.mouse_y = max(45, min(700, event.y))

    def on_right_click(self, event):
        if self.mouse_y <= 45: return
        angle = math.atan2(self.mouse_y - self.player_y, self.mouse_x - self.player_x)
        spd = 24
        dx, dy = math.cos(angle) * spd, math.sin(angle) * spd
        p_id = self.canvas.create_line(self.player_x, self.player_y, self.player_x + dx*0.8, self.player_y + dy*0.8, fill="#e879f9", width=5)
        self.projectiles.append({"id": p_id, "dx": dx, "dy": dy, "x": self.player_x, "y": self.player_y, "life": 120})
        
        for _ in range(6):
            self.particles.append({"x": self.player_x, "y": self.player_y, "dx": random.uniform(-3, 3), "dy": random.uniform(-3, 3), "life": 10, "color": "#c084fc", "id": self.canvas.create_oval(self.player_x-2, self.player_y-2, self.player_x+2, self.player_y+2, fill="#f0abfc", outline="")})

    def spawn_enemy(self):
        if self.enemies_remaining <= 0: return
        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top": x, y = random.randint(0, 900), 55
        elif side == "bottom": x, y = random.randint(0, 900), 690
        elif side == "left": x, y = 0, random.randint(55, 700)
        else: x, y = 900, random.randint(55, 700)
        e_id = self.canvas.create_rectangle(x, y, x+18, y+18, fill="#ef4444", outline="#fca5a5", width=1)
        self.enemies.append({"id": e_id, "base_speed": random.uniform(1.0, 1.8), "speed": 1.5, "offset": random.uniform(0, 6.28), "timer": random.randint(40, 100), "mode": "flank", "x": x, "y": y})
        self.enemies_remaining -= 1

    def update_game(self):
        self.spawn_counter += 1
        if self.spawn_counter >= 420:
            self.spawn_counter = 0
            for _ in range(5): self.spawn_enemy()
            
        if self.space_pressed and self.stamina > 0:
            self.is_ramming = True
            self.stamina = max(0.0, self.stamina - 4.5)
        else:
            self.is_ramming = False
            self.stamina = min(100.0, self.stamina + 1.2)
            
        dist_to_mouse = math.hypot(self.mouse_x - self.player_x, self.mouse_y - self.player_y)
        if dist_to_mouse > 5:
            angle = math.atan2(self.mouse_y - self.player_y, self.mouse_x - self.player_x)
            current_speed = min(self.max_speed * (1.4 if self.is_ramming else 1.0), dist_to_mouse * 0.08)
            move_x = math.cos(angle) * current_speed
            move_y = math.sin(angle) * current_speed
            self.player_x += move_x
            self.player_y += move_y
            
            if current_speed > 1.5:
                p_id = self.canvas.create_oval(self.player_x-3, self.player_y-3, self.player_x+3, self.player_y+3, fill="#d8b4fe", outline="")
                self.particles.append({"x": self.player_x, "y": self.player_y, "dx": random.uniform(-1.5, 1.5), "dy": random.uniform(-1.5, 1.5), "life": 14, "color": "#c084fc", "id": p_id})
        
        self.player_x = max(self.player_size+15, min(900-self.player_size-15, self.player_x))
        self.player_y = max(45+self.player_size+15, min(700-self.player_size-15, self.player_y))
        
        self.canvas.coords(self.player_id, self.player_x, self.player_y-self.player_size, self.player_x+self.player_size, self.player_y, self.player_x, self.player_y+self.player_size, self.player_x-self.player_size, self.player_y)
        
        if self.is_ramming:
            aura_col = "#ff007f" if (self.spawn_counter // 3) % 2 == 0 else "#ff69b4"
            self.canvas.coords(self.ram_aura, self.player_x-28, self.player_y-28, self.player_x+28, self.player_y+28)
            self.canvas.itemconfig(self.ram_aura, outline=aura_col, width=3)
        else:
            self.canvas.coords(self.ram_aura, 0, 0, 0, 0)
        
        p_trail = self.canvas.create_polygon(self.player_x, self.player_y-self.player_size, self.player_x+self.player_size, self.player_y, self.player_x, self.player_y+self.player_size, self.player_x-self.player_size, self.player_y, fill="", outline="#581c87", width=1)
        self.trails.append({"id": p_trail, "life": 4})

        self.canvas.coords(self.aim_line, self.player_x, self.player_y, self.mouse_x, self.mouse_y)
        self.canvas.coords(self.crosshair, self.mouse_x-8, self.mouse_y-8, self.mouse_x+8, self.mouse_y+8)

        for p in self.projectiles[:]:
            p["life"] -= 1
            if p["life"] <= 0:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)
                continue

            closest_enemy = None
            min_dist = float('inf')
            for e in self.enemies:
                e_coords = self.canvas.coords(e["id"])
                if not e_coords: continue
                ex, ey = (e_coords[0]+e_coords[2])/2, (e_coords[1]+e_coords[3])/2
                d = math.hypot(ex - p["x"], ey - p["y"])
                if d < min_dist:
                    min_dist = d
                    closest_enemy = (ex, ey)
            
            if closest_enemy and min_dist < 220:
                target_angle = math.atan2(closest_enemy[1] - p["y"], closest_enemy[0] - p["x"])
                speed = math.hypot(p["dx"], p["dy"])
                target_dx = math.cos(target_angle) * speed
                target_dy = math.sin(target_angle) * speed
                p["dx"] = p["dx"] * 0.94 + target_dx * 0.06
                p["dy"] = p["dy"] * 0.94 + target_dy * 0.06

            self.canvas.move(p["id"], p["dx"], p["dy"])
            p["x"] += p["dx"]
            p["y"] += p["dy"]
            
            p_trail = self.canvas.create_line(p["x"]-p["dx"]*0.5, p["y"]-p["dy"]*0.5, p["x"], p["y"], fill="#a855f7", width=3)
            self.trails.append({"id": p_trail, "life": 3})

            if p["x"] > 900 or p["x"] < 0 or p["y"] > 700 or p["y"] < 45:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)
                continue

            hit = False
            for enemy in self.enemies[:]:
                e_coords = self.canvas.coords(enemy["id"])
                if not e_coords: continue
                if e_coords[0] <= p["x"] <= e_coords[2] and e_coords[1] <= p["y"] <= e_coords[3]:
                    self.canvas.delete(enemy["id"])
                    self.enemies.remove(enemy)
                    hit = True
                    for _ in range(10):
                        self.particles.append({"x": p["x"], "y": p["y"], "dx": random.uniform(-5, 5), "dy": random.uniform(-5, 5), "life": 12, "color": "#f43f5e", "id": self.canvas.create_rectangle(p["x"]-2, p["y"]-2, p["x"]+2, p["y"]+2, fill="#fca5a5", outline="")})
                    break

            if hit:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)

        for enemy in self.enemies[:]:
            e_coords = self.canvas.coords(enemy["id"])
            if not e_coords: continue
            ex, ey = (e_coords[0]+e_coords[2])/2, (e_coords[1]+e_coords[3])/2
            
            if self.is_ramming and math.hypot(self.player_x-ex, self.player_y-ey) < (self.player_size + 24):
                self.canvas.delete(enemy["id"])
                self.enemies.remove(enemy)
                for _ in range(12):
                    self.particles.append({"x": ex, "y": ey, "dx": random.uniform(-6, 6), "dy": random.uniform(-6, 6), "life": 15, "color": "#ff007f", "id": self.canvas.create_rectangle(ex-2, ey-2, ex+2, ey+2, fill="#ff69b4", outline="")})
                continue

            enemy["timer"] -= 1
            if enemy["timer"] <= 0:
                enemy["timer"] = random.randint(40, 100)
                enemy["mode"] = random.choice(["flank", "rush", "retreat", "circle"])
                enemy["base_speed"] = random.uniform(0.9, 2.0)
                
            dist = math.hypot(self.player_x-ex, self.player_y-ey)
            base_angle = math.atan2(self.player_y-ey, self.player_x-ex)
            
            if enemy["mode"] == "flank": angle = base_angle + math.sin(self.spawn_counter*0.06 + enemy["offset"])*1.4
            elif enemy["mode"] == "rush": angle = base_angle
            elif enemy["mode"] == "retreat" and dist < 150: angle = base_angle + math.pi
            elif enemy["mode"] == "circle": angle = base_angle + math.pi/2
            else: angle = base_angle
            
            spd = enemy["base_speed"] * (1.5 if enemy["mode"] == "rush" else 1.0)
            edx, edy = math.cos(angle)*spd, math.sin(angle)*spd
            self.canvas.move(enemy["id"], edx, edy)
            
            e_trail = self.canvas.create_rectangle(ex-9, ey-9, ex+9, ey+9, fill="", outline="#991b1b", width=1)
            self.trails.append({"id": e_trail, "life": 3})

            if dist < (self.player_size + 9):
                self.lives -= 1
                self.canvas.delete(enemy["id"])
                self.enemies.remove(enemy)
                flash = self.canvas.create_rectangle(0, 45, 900, 700, fill="#ef4444", outline="")
                self.root.after(40, lambda: self.canvas.delete(flash))
                if self.lives <= 0:
                    self.canvas.create_text(450, 370, text="GAME OVER", fill="#ef4444", font=("Consolas", 36, "bold"), anchor="center")
                    return
                break

        for t in self.trails[:]:
            t["life"] -= 1
            if t["life"] <= 0:
                self.canvas.delete(t["id"])
                self.trails.remove(t)

        for part in self.particles[:]:
            self.canvas.move(part["id"], part["dx"], part["dy"])
            part["life"] -= 1
            if part["life"] <= 0:
                self.canvas.delete(part["id"])
                self.particles.remove(part)

        if not self.enemies and self.enemies_remaining <= 0:
            self.canvas.create_text(450, 370, text="VICTORY!", fill="#4ade80", font=("Consolas", 36, "bold"), anchor="center")
            return

        stamina_bar = "|" * int(self.stamina / 5)
        self.canvas.itemconfig(self.ui_text, text=f"LIVES: {self.lives} | STAMINA: [{stamina_bar:<20}] {int(self.stamina)}% | ENEMIES: {len(self.enemies)+self.enemies_remaining}")
        self.root.after(16, self.update_game)

if __name__ == "__main__":
    root = tk.Tk()
    game = Game(root)
    root.mainloop()