from config import WINDOW_WIDTH

class MainMenu:
    def __init__(self, canvas, on_select_level):
        self.canvas = canvas
        self.on_select_level = on_select_level
        self.menu_buttons = []
        self.create_menu()

    def create_menu(self):
        self.canvas.delete("all")
        self.draw_bg_grid()
        
        self.canvas.create_text(WINDOW_WIDTH/2, 120, text="ABYSSAL ECHO", fill="#f3e8ff", font=("Consolas", 36, "bold"), anchor="center", tags="menu")
        
        for i in range(1, 4):
            btn_y = 220 + (i - 1) * 90
            is_unlocked = (i <= 2)  # Уровни 1 и 2 доступны для выбора
            
            fill_col = "#12121c" if is_unlocked else "#0a0a0f"
            outline_col = "#a855f7" if is_unlocked else "#2a1b38"
            text_col = "#d8b4fe" if is_unlocked else "#443355"
            
            rect = self.canvas.create_rectangle(WINDOW_WIDTH/2 - 140, btn_y, WINDOW_WIDTH/2 + 140, btn_y + 70, fill=fill_col, outline=outline_col, width=2, tags="menu")
            txt = self.canvas.create_text(WINDOW_WIDTH/2, btn_y + 35, text=f"LEVEL {i}" if is_unlocked else f"LEVEL {i} (LOCKED)", fill=text_col, font=("Consolas", 12, "bold" if is_unlocked else "normal"), anchor="center", tags="menu")
            
            self.menu_buttons.append({
                "rect": rect, "text": txt, "level": i, 
                "x1": WINDOW_WIDTH/2 - 140, "y1": btn_y, "x2": WINDOW_WIDTH/2 + 140, "y2": btn_y + 70,
                "unlocked": is_unlocked
            })

    def draw_bg_grid(self):
        import random
        for x in range(0, WINDOW_WIDTH, 50):
            for y in range(0, 700, 50):
                c = random.choice(["#07070a", "#09090f", "#0b0b12"])
                self.canvas.create_rectangle(x, y, x+50, y+50, fill=c, outline="#12121a", width=1, tags="bg_grid")

    def handle_click(self, x, y):
        for btn in self.menu_buttons:
            if btn["unlocked"] and btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]:
                self.on_select_level(btn["level"])
                return True
        return False

    def handle_motion(self, x, y):
        for btn in self.menu_buttons:
            if btn["unlocked"]:
                if btn["x1"] <= x <= btn["x2"] and btn["y1"] <= y <= btn["y2"]:
                    self.canvas.itemconfig(btn["rect"], fill="#1e1b4b", outline="#e879f9")
                else:
                    self.canvas.itemconfig(btn["rect"], fill="#12121c", outline="#a855f7")