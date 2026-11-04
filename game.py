import tkinter as tk
import math
import random
from config import *
from entities import Player, Enemy
from boss import Boss

class GameLevel:
    def __init__(self, root, canvas, level, on_return_menu):
        self.root = root
        self.canvas = canvas
        self.level = level
        self.on_return_menu = on_return_menu
        self.loop_id = None
        self.is_running = True
        
        self.setup_level()

    def setup_level(self):
        self.canvas.delete("all")
        self.draw_stone_arena()
        
        self.canvas.create_rectangle(0, 0, WINDOW_WIDTH, 50, fill=UI_BG_COLOR, outline="#2a2a38", width=2)
        self.ui_level = self.canvas.create_text(20, 25, anchor="w", fill="#f3e8ff", font=("Consolas", 12, "bold"), text=f"LEVEL: {self.level}")
        self.ui_lives = self.canvas.create_text(130, 25, anchor="w", fill="#d8b4fe", font=("Consolas", 10, "bold"), text="LIVES: 3")
        
        self.canvas.create_text(240, 25, anchor="w", fill="#ff69b4", font=("Consolas", 9, "bold"), text="🛡️")
        self.ram_bar_bg = self.canvas.create_rectangle(265, 18, 385, 24, fill="#1c1c28", outline="#3a3a4f")
        self.ram_bar_fill = self.canvas.create_rectangle(266, 19, 384, 23, fill="#ff007f", outline="")
        
        self.canvas.create_text(410, 25, anchor="w", fill="#a855f7", font=("Consolas", 9, "bold"), text="⚡")
        self.laser_bar_bg = self.canvas.create_rectangle(435, 18, 555, 24, fill="#1c1c28", outline="#3a3a4f")
        self.laser_bar_fill = self.canvas.create_rectangle(436, 19, 554, 23, fill="#a855f7", outline="")
        
        self.player = Player(self.canvas)
        self.player.x = WINDOW_WIDTH / 2
        self.player.y = (WINDOW_HEIGHT + 50) / 2
        
        self.lives = 3
        self.ram_stamina = 100.0
        self.space_pressed = False
        self.is_ramming = False
        self.ram_exhausted = False
        self.ram_aura = self.canvas.create_oval(0, 0, 0, 0, outline="", width=2)
        
        self.laser_stamina = 100.0
        self.right_clicked = False
        self.laser_exhausted = False
        self.active_laser = None
        self.laser_angle = 0.0
        
        # Настройка врагов в зависимости от уровня
        if self.level == 2:
            self.max_enemies = 40
        else:
            self.max_enemies = 15
            
        self.enemies_remaining = self.max_enemies
        self.spawn_counter = 0
        self.anim_tick = 0
        
        self.is_paused = False
        self.is_game_over = False
        self.is_victory = False
        self.boss = None
        
        self.enemies = []
        self.flying_lasers = []
        self.particles = []
        self.trails = []
        
        self.mouse_x = WINDOW_WIDTH / 2
        self.mouse_y = (WINDOW_HEIGHT + 50) / 2
        
        self.aim_line = self.canvas.create_line(0, 0, 0, 0, fill="#a855f7", dash=(3, 3), width=1)
        self.crosshair = self.canvas.create_oval(0, 0, 0, 0, outline="#e879f9", width=1.5)
        
        self.pause_text = self.canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2, text="PAUSED", fill="#ffffff", font=("Consolas", 40, "bold"), anchor="center", state="hidden")
        
        self.victory_shadow = self.canvas.create_text(WINDOW_WIDTH/2 + 3, WINDOW_HEIGHT/2 - 47, text="VICTORY", fill="#022c22", font=("Consolas", 52, "bold"), anchor="center", state="hidden")
        self.victory_text = self.canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, text="VICTORY", fill="#4ade80", font=("Consolas", 52, "bold"), anchor="center", state="hidden")
        
        self.gameover_shadow = self.canvas.create_text(WINDOW_WIDTH/2 + 3, WINDOW_HEIGHT/2 - 47, text="GAME OVER", fill="#450a0a", font=("Consolas", 52, "bold"), anchor="center", state="hidden")
        self.gameover_text = self.canvas.create_text(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 50, text="GAME OVER", fill="#ef4444", font=("Consolas", 52, "bold"), anchor="center", state="hidden")

        self.restart_btn = self.canvas.create_rectangle(WINDOW_WIDTH/2 - 110, WINDOW_HEIGHT/2 + 20, WINDOW_WIDTH/2 - 10, WINDOW_HEIGHT/2 + 70, fill="#1e1b4b", outline="#c084fc", width=2, state="hidden")
        self.restart_text = self.canvas.create_text(WINDOW_WIDTH/2 - 60, WINDOW_HEIGHT/2 + 45, text="RESTART", fill="#f3e8ff", font=("Consolas", 12, "bold"), anchor="center", state="hidden")
        
        self.next_btn = self.canvas.create_rectangle(WINDOW_WIDTH/2 + 10, WINDOW_HEIGHT/2 + 20, WINDOW_WIDTH/2 + 110, WINDOW_HEIGHT/2 + 70, fill="#1e1b4b", outline="#c084fc", width=2, state="hidden")
        self.next_text = self.canvas.create_text(WINDOW_WIDTH/2 + 60, WINDOW_HEIGHT/2 + 45, text="NEXT" if self.level < 3 else "MENU", fill="#f3e8ff", font=("Consolas", 12, "bold"), anchor="center", state="hidden")

        # Сразу спавним первых врагов при старте уровня
        for _ in range(5): 
            self.spawn_enemy()

        if self.loop_id:
            self.root.after_cancel(self.loop_id)
        self.update_game()

    def draw_stone_arena(self):
        for x in range(0, WINDOW_WIDTH, 50):
            for y in range(50, WINDOW_HEIGHT, 50):
                c = random.choice(["#07070a", "#09090f", "#0b0b12"])
                self.canvas.create_rectangle(x, y, x+50, y+50, fill=c, outline="#12121a", width=1)
                
        for _ in range(50):
            x, y = random.randint(30, WINDOW_WIDTH-30), random.randint(75, WINDOW_HEIGHT-25)
            sz = random.randint(3, 8)
            self.canvas.create_polygon(x, y-sz, x+sz*0.8, y+sz, x-sz*0.8, y+sz*0.6, fill="#181824", outline="#252538", width=1)

        for x in range(0, WINDOW_WIDTH, 30):
            self.canvas.create_rectangle(x, 50, x+30, 65, fill="#242430", outline="#111118", width=2)
            self.canvas.create_rectangle(x, WINDOW_HEIGHT-15, x+30, WINDOW_HEIGHT, fill="#242430", outline="#111118", width=2)
        for y in range(50, WINDOW_HEIGHT, 30):
            self.canvas.create_rectangle(0, y, 15, y+30, fill="#242430", outline="#111118", width=2)
            self.canvas.create_rectangle(WINDOW_WIDTH-15, y, WINDOW_WIDTH, y+30, fill="#242430", outline="#111118", width=2)

    def stop(self):
        self.is_running = False
        if self.loop_id:
            try:
                self.root.after_cancel(self.loop_id)
            except:
                pass

    def spawn_enemy(self):
        if self.enemies_remaining <= 0: return
        
        # На 2 уровне последний враг — это босс
        if self.level == 2 and self.enemies_remaining == 1 and not self.boss:
            self.boss = Boss(self.canvas, WINDOW_WIDTH / 2, 120)
            self.enemies_remaining -= 1
            return

        side = random.choice(["top", "bottom", "left", "right"])
        if side == "top": x, y = random.randint(30, WINDOW_WIDTH-30), 80
        elif side == "bottom": x, y = random.randint(30, WINDOW_WIDTH-30), WINDOW_HEIGHT-30
        elif side == "left": x, y = 30, random.randint(80, WINDOW_HEIGHT-30)
        else: x, y = WINDOW_WIDTH-30, random.randint(80, WINDOW_HEIGHT-30)
        
        en = Enemy(self.canvas, x, y)
        self.enemies.append(en)
        self.enemies_remaining -= 1

    def handle_click(self, x, y):
        if self.is_victory:
            if WINDOW_WIDTH/2 - 110 <= x <= WINDOW_WIDTH/2 - 10 and WINDOW_HEIGHT/2 + 20 <= y <= WINDOW_HEIGHT/2 + 70:
                self.setup_level()
            elif WINDOW_WIDTH/2 + 10 <= x <= WINDOW_WIDTH/2 + 110 and WINDOW_HEIGHT/2 + 20 <= y <= WINDOW_HEIGHT/2 + 70:
                self.stop()
                if self.level < 3:
                    from game import GameLevel
                    GameLevel(self.root, self.canvas, self.level + 1, self.on_return_menu)
                else:
                    self.on_return_menu()
        elif self.is_game_over:
            if WINDOW_WIDTH/2 - 60 <= x <= WINDOW_WIDTH/2 + 60 and WINDOW_HEIGHT/2 + 20 <= y <= WINDOW_HEIGHT/2 + 70:
                self.setup_level()

    def on_right_press(self, event):
        if not self.is_running or self.is_paused or self.is_game_over or self.is_victory: return
        if self.mouse_y <= 65 or self.laser_stamina <= 0 or self.laser_exhausted or self.active_laser: return
        self.right_clicked = True
        target_angle = math.atan2(self.mouse_y - self.player.y, self.mouse_x - self.player.x)
        self.laser_angle = target_angle
        
        outer_id = self.canvas.create_line(0, 0, 0, 0, fill="#e879f9", width=18)
        glow_id = self.canvas.create_line(0, 0, 0, 0, fill="#c084fc", width=10)
        core_id = self.canvas.create_line(0, 0, 0, 0, fill="#ffffff", width=4)
        self.active_laser = {"core": core_id, "glow": glow_id, "outer": outer_id}

    def on_right_release(self, event):
        if not self.right_clicked: return
        self.right_clicked = False
        if self.active_laser:
            core_id = self.active_laser["core"]
            glow_id = self.active_laser["glow"]
            outer_id = self.active_laser["outer"]
            
            dx = math.cos(self.laser_angle) * 22
            dy = math.sin(self.laser_angle) * 22
            self.flying_lasers.append({"core": core_id, "glow": glow_id, "outer": outer_id, "x": self.player.x, "y": self.player.y, "dx": dx, "dy": dy, "life": 90})
            self.active_laser = None

    def update_game(self):
        if not self.is_running: return

        if not self.is_paused and not self.is_game_over and not self.is_victory:
            self.anim_tick += 1
            
            if len(self.enemies) == 0 and not self.boss and self.enemies_remaining > 0:
                for _ in range(min(5, self.enemies_remaining)):
                    self.spawn_enemy()
                self.spawn_counter = 0

            self.spawn_counter += 1
            if self.spawn_counter >= 420:
                self.spawn_counter = 0
                for _ in range(5): self.spawn_enemy()
                
            if self.right_clicked:
                self.laser_stamina = max(0.0, self.laser_stamina - 2.4)
                if self.laser_stamina <= 5.0:
                    self.laser_exhausted = True
                    self.right_clicked = False
                    if self.active_laser:
                        self.canvas.delete(self.active_laser["core"])
                        self.canvas.delete(self.active_laser["glow"])
                        self.canvas.delete(self.active_laser["outer"])
                        self.active_laser = None
                    
            if self.space_pressed and self.ram_stamina > 0 and not self.ram_exhausted:
                self.is_ramming = True
                self.ram_stamina = max(0.0, self.ram_stamina - 4.5)
                if self.ram_stamina <= 5.0:
                    self.ram_exhausted = True
            else:
                self.is_ramming = False
                regen = 0.6 if self.ram_exhausted else 1.2
                self.ram_stamina = min(100.0, self.ram_stamina + regen)
                if self.ram_stamina >= 100.0:
                    self.ram_exhausted = False
                
            if not self.right_clicked:
                regen = 0.75 if self.laser_exhausted else 1.5
                self.laser_stamina = min(100.0, self.laser_stamina + regen)
                if self.laser_stamina >= 100.0:
                    self.laser_exhausted = False
                
            dist_to_mouse = math.hypot(self.mouse_x - self.player.x, self.mouse_y - self.player.y)
            if dist_to_mouse > 5:
                angle = math.atan2(self.mouse_y - self.player.y, self.mouse_x - self.player.x)
                current_speed = min(PLAYER_SPEED * (1.4 if self.is_ramming else 1.0), dist_to_mouse * 0.08)
                move_x = math.cos(angle) * current_speed
                move_y = math.sin(angle) * current_speed
                self.player.x += move_x
                self.player.y += move_y
                
                if current_speed > 1.5:
                    p_id = self.canvas.create_oval(self.player.x-3, self.player.y-3, self.player.x+3, self.player.y+3, fill="#d8b4fe", outline="")
                    self.particles.append({"x": self.player.x, "y": self.player.y, "dx": random.uniform(-1.5, 1.5), "dy": random.uniform(-1.5, 1.5), "life": 14, "color": "#c084fc", "id": p_id})
            
            self.player.x = max(self.player.size+15, min(WINDOW_WIDTH-self.player.size-15, self.player.x))
            self.player.y = max(65+self.player.size+15, min(WINDOW_HEIGHT-self.player.size-15, self.player.y))
            
            self.player.update_coords(self.anim_tick)
            
            if self.is_ramming:
                aura_col = "#ff007f" if (self.spawn_counter // 3) % 2 == 0 else "#ff69b4"
                self.canvas.coords(self.ram_aura, self.player.x-28, self.player.y-28, self.player.x+28, self.player.y+28)
                self.canvas.itemconfig(self.ram_aura, outline=aura_col, width=3)
            else:
                self.canvas.coords(self.ram_aura, 0, 0, 0, 0)
            
            ps = self.player.size
            p_trail = self.canvas.create_polygon(self.player.x, self.player.y-ps, self.player.x+ps, self.player.y, self.player.x, self.player.y+ps, self.player.x-ps, self.player.y, fill="", outline="#581c87", width=1)
            self.trails.append({"id": p_trail, "life": 4})

            if self.right_clicked and self.active_laser:
                target_angle = math.atan2(self.mouse_y - self.player.y, self.mouse_x - self.player.x)
                diff = (target_angle - self.laser_angle + math.pi) % (2 * math.pi) - math.pi
                self.laser_angle += diff * 0.04
                
                length = 1500
                lx2 = self.player.x + math.cos(self.laser_angle) * length
                ly2 = self.player.y + math.sin(self.laser_angle) * length
                
                self.canvas.coords(self.active_laser["outer"], self.player.x, self.player.y, lx2, ly2)
                self.canvas.coords(self.active_laser["glow"], self.player.x, self.player.y, lx2, ly2)
                self.canvas.coords(self.active_laser["core"], self.player.x, self.player.y, lx2, ly2)
                
                if self.boss:
                    bx, by = self.boss.x, self.boss.y
                    v1x, v1y = bx - self.player.x, by - self.player.y
                    dirx, diry = math.cos(self.laser_angle), math.sin(self.laser_angle)
                    proj = v1x * dirx + v1y * diry
                    if 0 <= proj <= length:
                        cx = self.player.x + dirx * proj
                        cy = self.player.y + diry * proj
                        if math.hypot(bx - cx, by - cy) < 35:
                            if self.boss.take_damage(0.4, self.canvas, self.particles):
                                self.boss = None

                for enemy in self.enemies[:]:
                    e_coords = self.canvas.coords(enemy.body)
                    if not e_coords: continue
                    ex, ey = (e_coords[0]+e_coords[2])/2, (e_coords[1]+e_coords[3])/2
                    v1x, v1y = ex - self.player.x, ey - self.player.y
                    dirx, diry = math.cos(self.laser_angle), math.sin(self.laser_angle)
                    proj = v1x * dirx + v1y * diry
                    if 0 <= proj <= length:
                        cx = self.player.x + dirx * proj
                        cy = self.player.y + diry * proj
                        if math.hypot(ex - cx, ey - cy) < 16:
                            enemy.delete()
                            self.enemies.remove(enemy)
                            for _ in range(10):
                                self.particles.append({"x": ex, "y": ey, "dx": random.uniform(-5, 5), "dy": random.uniform(-5, 5), "life": 12, "color": "#ff00ff", "id": self.canvas.create_rectangle(ex-2, ey-2, ex+2, ey+2, fill="#ffa07a", outline="")})

            if self.boss:
                new_boss_laser = self.boss.update(self.player.x, self.player.y, self.canvas, self.particles)
                if new_boss_laser:
                    self.flying_lasers.append(new_boss_laser)
                
                if math.hypot(self.player.x - self.boss.x, self.player.y - self.boss.y) < (self.player.size + 30):
                    self.lives -= 1
                    flash = self.canvas.create_rectangle(0, 50, WINDOW_WIDTH, WINDOW_HEIGHT, fill="#ef4444", outline="")
                    self.root.after(40, lambda: self.canvas.delete(flash))
                    if self.lives <= 0:
                        self.is_game_over = True
                        self.canvas.tag_raise(self.gameover_shadow)
                        self.canvas.tag_raise(self.gameover_text)
                        self.canvas.tag_raise(self.restart_btn)
                        self.canvas.tag_raise(self.restart_text)
                        self.canvas.itemconfig(self.gameover_shadow, state="normal")
                        self.canvas.itemconfig(self.gameover_text, state="normal")
                        self.canvas.itemconfig(self.restart_btn, state="normal")
                        self.canvas.itemconfig(self.restart_text, state="normal")
                        return

            for fl in self.flying_lasers[:]:
                fl["life"] -= 1
                if fl["life"] <= 0:
                    self.canvas.delete(fl["core"])
                    self.canvas.delete(fl["glow"])
                    self.canvas.delete(fl["outer"])
                    self.flying_lasers.remove(fl)
                    continue
                
                if fl.get("is_boss"):
                    length = 1500
                    angle = fl["angle"]
                    lx2 = fl["x"] + math.cos(angle) * length
                    ly2 = fl["y"] + math.sin(angle) * length
                    self.canvas.coords(fl["outer"], fl["x"], fl["y"], lx2, ly2)
                    self.canvas.coords(fl["glow"], fl["x"], fl["y"], lx2, ly2)
                    self.canvas.coords(fl["core"], fl["x"], fl["y"], lx2, ly2)
                    
                    v1x, v1y = self.player.x - fl["x"], self.player.y - fl["y"]
                    dirx, diry = math.cos(angle), math.sin(angle)
                    proj = v1x * dirx + v1y * diry
                    if 0 <= proj <= length:
                        cx = fl["x"] + dirx * proj
                        cy = fl["y"] + diry * proj
                        if math.hypot(self.player.x - cx, self.player.y - cy) < (self.player.size + 8):
                            self.lives -= 1
                            self.flying_lasers.remove(fl)
                            self.canvas.delete(fl["core"])
                            self.canvas.delete(fl["glow"])
                            self.canvas.delete(fl["outer"])
                            flash = self.canvas.create_rectangle(0, 50, WINDOW_WIDTH, WINDOW_HEIGHT, fill="#ef4444", outline="")
                            self.root.after(40, lambda: self.canvas.delete(flash))
                            if self.lives <= 0:
                                self.is_game_over = True
                                self.canvas.tag_raise(self.gameover_shadow)
                                self.canvas.tag_raise(self.gameover_text)
                                self.canvas.tag_raise(self.restart_btn)
                                self.canvas.tag_raise(self.restart_text)
                                self.canvas.itemconfig(self.gameover_shadow, state="normal")
                                self.canvas.itemconfig(self.gameover_text, state="normal")
                                self.canvas.itemconfig(self.restart_btn, state="normal")
                                self.canvas.itemconfig(self.restart_text, state="normal")
                                return
                            break
                else:
                    fl["x"] += fl["dx"]
                    fl["y"] += fl["dy"]
                    length = 1500
                    angle = math.atan2(fl["dy"], fl["dx"])
                    lx2 = fl["x"] + math.cos(angle) * length
                    ly2 = fl["y"] + math.sin(angle) * length
                    self.canvas.coords(fl["outer"], fl["x"], fl["y"], lx2, ly2)
                    self.canvas.coords(fl["glow"], fl["x"], fl["y"], lx2, ly2)
                    self.canvas.coords(fl["core"], fl["x"], fl["y"], lx2, ly2)

            self.canvas.coords(self.aim_line, self.player.x, self.player.y, self.mouse_x, self.mouse_y)
            self.canvas.coords(self.crosshair, self.mouse_x-8, self.mouse_y-8, self.mouse_x+8, self.mouse_y+8)

            for enemy in self.enemies[:]:
                e_coords = self.canvas.coords(enemy.body)
                if not e_coords: continue
                ex, ey = (e_coords[0]+e_coords[2])/2, (e_coords[1]+e_coords[3])/2
                
                e_pulse = math.sin(self.anim_tick * 0.2 + enemy.offset) * 2
                self.canvas.coords(enemy.outer, ex-11-e_pulse, ey-11-e_pulse, ex+11+e_pulse, ey+11+e_pulse)
                
                e_cols = ["#ef4444", "#f97316", "#dc2626", "#b91c1c"]
                self.canvas.itemconfig(enemy.body, fill=e_cols[(self.anim_tick // 3) % len(e_cols)])
                
                if self.is_ramming and math.hypot(self.player.x-ex, self.player.y-ey) < (self.player.size + 24):
                    enemy.delete()
                    self.enemies.remove(enemy)
                    for _ in range(12):
                        self.particles.append({"x": ex, "y": ey, "dx": random.uniform(-6, 6), "dy": random.uniform(-6, 6), "life": 15, "color": "#ff007f", "id": self.canvas.create_rectangle(ex-2, ey-2, ex+2, ey+2, fill="#ff69b4", outline="")})
                    continue

                enemy.timer -= 1
                if enemy.timer <= 0:
                    enemy.timer = random.randint(40, 100)
                    enemy.mode = random.choice(["flank", "rush", "retreat", "circle"])
                    enemy.base_speed = random.uniform(0.9, 2.0)
                    
                dist = math.hypot(self.player.x-ex, self.player.y-ey)
                base_angle = math.atan2(self.player.y-ey, self.player.x-ex)
                
                if enemy.mode == "flank": angle = base_angle + math.sin(self.spawn_counter*0.06 + enemy.offset)*1.4
                elif enemy.mode == "rush": angle = base_angle
                elif enemy.mode == "retreat" and dist < 150: angle = base_angle + math.pi
                elif enemy.mode == "circle": angle = base_angle + math.pi/2
                else: angle = base_angle
                
                spd = enemy.base_speed * (1.5 if enemy.mode == "rush" else 1.0)
                edx, edy = math.cos(angle)*spd, math.sin(angle)*spd
                
                self.canvas.move(enemy.body, edx, edy)
                self.canvas.move(enemy.outer, edx, edy)
                self.canvas.move(enemy.core, edx, edy)
                
                e_trail = self.canvas.create_rectangle(ex-9, ey-9, ex+9, ey+9, fill="", outline="#991b1b", width=1)
                self.trails.append({"id": e_trail, "life": 3})

                if dist < (self.player.size + 9):
                    self.lives -= 1
                    enemy.delete()
                    self.enemies.remove(enemy)
                    flash = self.canvas.create_rectangle(0, 50, WINDOW_WIDTH, WINDOW_HEIGHT, fill="#ef4444", outline="")
                    self.root.after(40, lambda: self.canvas.delete(flash))
                    if self.lives <= 0:
                        self.is_game_over = True
                        self.canvas.tag_raise(self.gameover_shadow)
                        self.canvas.tag_raise(self.gameover_text)
                        self.canvas.tag_raise(self.restart_btn)
                        self.canvas.tag_raise(self.restart_text)
                        
                        self.canvas.itemconfig(self.gameover_shadow, state="normal")
                        self.canvas.itemconfig(self.gameover_text, state="normal")
                        self.canvas.itemconfig(self.restart_btn, state="normal")
                        self.canvas.itemconfig(self.restart_text, state="normal")
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

            if not self.enemies and self.enemies_remaining <= 0 and not self.boss:
                self.is_victory = True
                self.canvas.tag_raise(self.victory_shadow)
                self.canvas.tag_raise(self.victory_text)
                self.canvas.tag_raise(self.restart_btn)
                self.canvas.tag_raise(self.restart_text)
                self.canvas.tag_raise(self.next_btn)
                self.canvas.tag_raise(self.next_text)
                
                self.canvas.itemconfig(self.victory_shadow, state="normal")
                self.canvas.itemconfig(self.victory_text, state="normal")
                self.canvas.itemconfig(self.restart_btn, state="normal")
                self.canvas.itemconfig(self.restart_text, state="normal")
                self.canvas.itemconfig(self.next_btn, state="normal")
                self.canvas.itemconfig(self.next_text, state="normal")
                return

            self.canvas.coords(self.ram_bar_fill, 266, 19, 266 + int(118 * (self.ram_stamina / 100.0)), 23)
            self.canvas.coords(self.laser_bar_fill, 436, 19, 436 + int(118 * (self.laser_stamina / 100.0)), 23)
            self.canvas.itemconfig(self.ui_lives, text=f"LIVES: {self.lives}")

        if self.is_running:
            self.loop_id = self.root.after(16, self.update_game)