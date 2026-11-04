import tkinter as tk

root = tk.Tk()
root.title("2D Top-Down Game (Tkinter)")
root.geometry("800x600")

canvas = tk.Canvas(root, width=800, height=600, bg="#1e1e1e")
canvas.pack(fill="both", expand=True)

# Создаем игрока (зеленый квадратик)
player = canvas.create_rectangle(385, 285, 415, 315, fill="#00ff96", outline="")

player_speed = 10
keys_pressed = {}

def update():
    dx, dy = 0, 0
    if keys_pressed.get("w") or keys_pressed.get("Up"):    dy -= player_speed
    if keys_pressed.get("s") or keys_pressed.get("Down"):  dy += player_speed
    if keys_pressed.get("a") or keys_pressed.get("Left"):  dx -= player_speed
    if keys_pressed.get("d") or keys_pressed.get("Right"): dx += player_speed
    
    canvas.move(player, dx, dy)
    root.after(30, update) # Цикл обновления (~33 FPS)

root.bind("<KeyPress>", lambda e: keys_pressed.update({e.keysym: True, e.char: True}))
root.bind("<KeyRelease>", lambda e: keys_pressed.pop(e.keysym, None) or keys_pressed.pop(e.char, None))

root.after(30, update)
root.mainloop()