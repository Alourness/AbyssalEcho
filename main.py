import tkinter as tk
import math
import random
class Game:
    def __init__(self, root):
        self.root=root
        self.root.title("2D Top-Down Game - Level 2")
        self.root.geometry("800x600")
        self.root.resizable(False,False)
        self.canvas=tk.Canvas(root,width=800,height=600,bg="#1a1a1a")
        self.canvas.pack(fill="both",expand=True)
        self.player_x=400
        self.player_y=300
        self.player_size=18
        self.player_id=self.canvas.create_polygon(self.player_x,self.player_y-self.player_size,self.player_x+self.player_size,self.player_y,self.player_x,self.player_y+self.player_size,self.player_x-self.player_size,self.player_y,fill="#9b59b6",outline="#8e44ad",width=2)
        self.player_speed=4.5
        self.hp=100
        self.enemies=[]
        self.projectiles=[]
        self.keys_pressed={}
        self.root.bind("<KeyPress>",self.on_key_press)
        self.root.bind("<KeyRelease>",self.on_key_release)
        self.ui_text=self.canvas.create_text(20,20,anchor="nw",fill="white",font=("Arial",12,"bold"),text="Level: 2 | HP: 100/100 | Shoot with SPACE")
        for _ in range(4): self.spawn_enemy()
        self.update_game()
    def on_key_press(self,event):
        self.keys_pressed[event.keysym]=True
        self.keys_pressed[event.char]=True
        if event.keysym=="space": self.shoot()
    def on_key_release(self,event):
        self.keys_pressed.pop(event.keysym,None)
        self.keys_pressed.pop(event.char,None)
    def shoot(self):
        p_id=self.canvas.create_oval(self.player_x-4,self.player_y-4,self.player_x+4,self.player_y+4,fill="#00ffff",outline="")
        self.projectiles.append({"id":p_id,"dx":8,"dy":0})
    def spawn_enemy(self):
        x=random.choice([-30,830])
        y=random.randint(50,550)
        e_id=self.canvas.create_rectangle(x,y,x+20,y+20,fill="#e74c3c",outline="")
        self.enemies.append({"id":e_id,"speed":2.2})
    def update_game(self):
        dx,dy=0,0
        if self.keys_pressed.get("w")or self.keys_pressed.get("Up"): dy-=self.player_speed
        if self.keys_pressed.get("s")or self.keys_pressed.get("Down"): dy+=self.player_speed
        if self.keys_pressed.get("a")or self.keys_pressed.get("Left"): dx-=self.player_speed
        if self.keys_pressed.get("d")or self.keys_pressed.get("Right"): dx+=self.player_speed
        self.player_x=max(self.player_size,min(800-self.player_size,self.player_x+dx))
        self.player_y=max(self.player_size,min(600-self.player_size,self.player_y+dy))
        self.canvas.coords(self.player_id,self.player_x,self.player_y-self.player_size,self.player_x+self.player_size,self.player_y,self.player_x,self.player_y+self.player_size,self.player_x-self.player_size,self.player_y)
        for p in self.projectiles[:]:
            self.canvas.move(p["id"],p["dx"],p["dy"])
            p_coords=self.canvas.coords(p["id"])
            if not p_coords or p_coords[2]>800 or p_coords[0]<0:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)
                continue
            px,py=(p_coords[0]+p_coords[2])/2,(p_coords[1]+p_coords[3])/2
            hit=False
            for enemy in self.enemies[:]:
                e_coords=self.canvas.coords(enemy["id"])
                if not e_coords: continue
                if e_coords[0]<px<e_coords[2] and e_coords[1]<py<e_coords[3]:
                    self.canvas.delete(enemy["id"])
                    self.enemies.remove(enemy)
                    hit=True
                    break
            if hit:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)
        for enemy in self.enemies:
            e_coords=self.canvas.coords(enemy["id"])
            if not e_coords: continue
            ex,ey=(e_coords[0]+e_coords[2])/2,(e_coords[1]+e_coords[3])/2
            angle=math.atan2(self.player_y-ey,self.player_x-ex)
            edx=math.cos(angle)*enemy["speed"]
            edy=math.sin(angle)*enemy["speed"]
            self.canvas.move(enemy["id"],edx,edy)
            if math.hypot(self.player_x-ex,self.player_y-ey)<20:
                self.hp-=1
                if self.hp<=0:
                    self.canvas.create_text(400,300,text="GAME OVER",fill="#e74c3c",font=("Arial",36,"bold"),anchor="center")
                    return
        if len(self.enemies)<8 and random.random()<0.05:
            self.spawn_enemy()
        self.canvas.itemconfig(self.ui_text,text=f"Level: 2 | HP: {max(0,self.hp)}/100 | Enemies: {len(self.enemies)}")
        self.root.after(16,self.update_game)
if __name__=="__main__":
    root=tk.Tk()
    game=Game(root)
    root.mainloop()