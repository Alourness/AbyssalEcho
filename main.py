import tkinter as tk
from config import WINDOW_WIDTH, WINDOW_HEIGHT, BG_COLOR
from ui import MainMenu
from game import GameLevel

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("2D Plasma Top-Down Game")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.resizable(False, False)
        
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg=BG_COLOR, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        
        self.current_game = None
        self.menu = MainMenu(self.canvas, self.start_level)
        
        self.canvas.bind("<Motion>", self.on_mouse_move)
        self.canvas.bind("<Button-1>", self.on_left_click)
        self.canvas.bind("<ButtonPress-3>", self.on_right_press)
        self.canvas.bind("<ButtonRelease-3>", self.on_right_release)
        self.root.bind("<KeyPress-space>", self.on_space_press)
        self.root.bind("<KeyRelease-space>", self.on_space_release)
        self.root.bind("<Escape>", self.on_escape)

    def start_level(self, level):
        if self.current_game:
            self.current_game.stop()
        self.current_game = GameLevel(self.root, self.canvas, level, self.return_to_menu)

    def return_to_menu(self):
        if self.current_game:
            self.current_game.stop()
            self.current_game = None
        self.menu.create_menu()

    def on_mouse_move(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.mouse_x = event.x
            self.current_game.mouse_y = event.y
        else:
            self.menu.handle_motion(event.x, event.y)

    def on_left_click(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.handle_click(event.x, event.y)
        else:
            self.menu.handle_click(event.x, event.y)

    def on_right_press(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.on_right_press(event)

    def on_right_release(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.on_right_release(event)

    def on_space_press(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.space_pressed = True

    def on_space_release(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.space_pressed = False

    def on_escape(self, event):
        if self.current_game and self.current_game.is_running:
            self.current_game.toggle_pause(event)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()