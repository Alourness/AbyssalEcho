import math
import random

class Player:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = 450
        self.y = 375
        self.size = 16
        self.outer = canvas.create_polygon(0,0,0,0,0,0,0,0, fill="", outline="#e879f9", width=2)
        self.body = canvas.create_polygon(0,0,0,0,0,0,0,0, fill="#c084fc", outline="#f3e8ff", width=1.5)
        self.core = canvas.create_polygon(0,0,0,0,0,0,0,0, fill="#ffffff", outline="")

    def update_coords(self, anim_tick):
        ps = self.size
        pulse = math.sin(anim_tick * 0.15) * 3
        self.canvas.coords(self.outer, self.x, self.y-(ps+4+pulse), self.x+(ps+4+pulse), self.y, self.x, self.y+(ps+4+pulse), self.x-(ps+4+pulse), self.y)
        self.canvas.coords(self.body, self.x, self.y-ps, self.x+ps, self.y, self.x, self.y+ps, self.x-ps, self.y)
        self.canvas.coords(self.core, self.x, self.y-ps*0.4, self.x+ps*0.4, self.y, self.x, self.y+ps*0.4, self.x-ps*0.4, self.y)
        
        p_colors = ["#c084fc", "#e879f9", "#a855f7", "#d8b4fe"]
        self.canvas.itemconfig(self.body, fill=p_colors[(anim_tick // 4) % len(p_colors)])

class Enemy:
    def __init__(self, canvas, x, y):
        self.canvas = canvas
        self.outer = canvas.create_rectangle(x-2, y-2, x+20, y+20, fill="", outline="#ef4444", width=1.5)
        self.body = canvas.create_rectangle(x, y, x+18, y+18, fill="#dc2626", outline="#fca5a5", width=1)
        self.core = canvas.create_rectangle(x+5, y+5, x+13, y+13, fill="#fef08a", outline="")
        self.base_speed = random.uniform(1.0, 1.8)
        self.speed = 1.5
        self.offset = random.uniform(0, 6.28)
        self.timer = random.randint(40, 100)
        self.mode = "flank"

    def delete(self):
        self.canvas.delete(self.body)
        self.canvas.delete(self.outer)
        self.canvas.delete(self.core)