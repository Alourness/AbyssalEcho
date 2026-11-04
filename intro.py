import math
from config import WINDOW_WIDTH, WINDOW_HEIGHT

class LevelIntro:
    def __init__(self, canvas, player, on_finish):
        self.canvas = canvas
        self.player = player
        self.on_finish = on_finish
        
        self.progress = 0.0  # от 0.0 до 1.0
        self.duration = 60   # кадров (~1 секунда)
        
        
        self.center_x = WINDOW_WIDTH / 2
        self.center_y = (WINDOW_HEIGHT + 50) / 2
        
        
        self.flash = self.canvas.create_rectangle(0, 50, WINDOW_WIDTH, WINDOW_HEIGHT, fill="#050508", outline="")

    def update(self):
        self.progress += 1.0 / self.duration
        t = min(1.0, self.progress)
        
        
        ease_t = 1 - (1 - t) ** 3
        
        
        alpha_val = int((1.0 - t) * 255)
        if alpha_val > 0:
         
            pass
        else:
            self.canvas.delete(self.flash)

        if t >= 1.0:
            self.canvas.delete(self.flash)
            self.on_finish()
            return True
            
        return False