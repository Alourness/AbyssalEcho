import tkinter as tk
import math
import random
class Game:
    def __init__(self,root):
        self.root=root
        self.root.title("2D Top-Down Game - Level 1")
        self.root.geometry("800x640")
        self.root.resizable(False,False)
        self.canvas=tk.Canvas(root,width=800,height=640,bg="#0d0d12")
        self.canvas.pack(fill="both",expand=True)
        self.canvas.create_rectangle(0,0,800,45,fill="#161622",outline="#222233")
        self.ui_text=self.canvas.create_text(20,22,anchor="w",fill="#e0b0ff",font=("Consolas",11,"bold"),text="LEVEL: 1 | LIVES: 3 | ENEMIES REMAINING: 50")
        self.player_x=400
        self.player_y=340
        self.player_size=16
        self.player_id=self.canvas.create_polygon(self.player_x,self.player_y-self.player_size,self.player_x+self.player_size,self.player_y,self.player_x,self.player_y+self.player_size,self.player_x-self.player_size,self.player_y,fill="#b57edc",outline="#e0b0ff",width=2)
        self.player_speed=4.5
        self.lives=3
        self.enemies_remaining=50
        self.spawn_counter=0
        self.enemies=[]
        self.projectiles=[]
        self.player_trails=[]
        self.mouse_x=400
        self.mouse_y=340
        self.keys_pressed={}
        self.aim_line=self.canvas.create_line(0,0,0,0,fill="#9b59b6",dash=(4,4),width=1)
        self.ch_h=self.canvas.create_line(0,0,0,0,fill="#e0b0ff",width=2)
        self.ch_v=self.canvas.create_line(0,0,0,0,fill="#e0b0ff",width=2)
        self.canvas.bind("<Motion>",self.on_mouse_move)
        self.canvas.bind("<Button-1>",self.on_mouse_click)
        self.root.bind("<KeyPress>",self.on_key_press)
        self.root.bind("<KeyRelease>",self.on_key_release)
        for _ in range(5): self.spawn_enemy()
        self.update_game()
    def on_mouse_move(self,event):
        self.mouse_x=max(0,min(800,event.x))
        self.mouse_y=max(45,min(640,event.y))
    def on_mouse_click(self,event):
        if self.mouse_y<=45: return
        angle=math.atan2(self.mouse_y-self.player_y,self.mouse_x-self.player_x)
        p_id=self.canvas.create_oval(self.player_x-4,self.player_y-4,self.player_x+4,self.player_y+4,fill="#00ffff",outline="")
        self.projectiles.append({"id":p_id,"dx":math.cos(angle)*9,"dy":math.sin(angle)*9})
    def on_key_press(self,event):
        self.keys_pressed[event.keysym]=True
        self.keys_pressed[event.char]=True
    def on_key_release(self,event):
        self.keys_pressed.pop(event.keysym,None)
        self.keys_pressed.pop(event.char,None)
    def spawn_enemy(self):
        if self.enemies_remaining<=0: return
        side=random.choice(["top","bottom","left","right"])
        if side=="top": x,y=random.randint(0,800),55
        elif side=="bottom": x,y=random.randint(0,800),630
        elif side=="left": x,y=0,random.randint(55,640)
        else: x,y=800,random.randint(55,640)
        e_id=self.canvas.create_rectangle(x,y,x+20,y+20,fill="#ff3838",outline="#ff7675",width=1)
        self.enemies.append({"id":e_id,"speed":1.8,"offset":random.uniform(0,6.28),"trail":[]})
        self.enemies_remaining-=1
    def update_game(self):
        self.spawn_counter+=1
        if self.spawn_counter>=300:
            self.spawn_counter=0
            for _ in range(5): self.spawn_enemy()
        dx,dy=0,0
        if self.keys_pressed.get("w")or self.keys_pressed.get("Up"): dy-=self.player_speed
        if self.keys_pressed.get("s")or self.keys_pressed.get("Down"): dy+=self.player_speed
        if self.keys_pressed.get("a")or self.keys_pressed.get("Left"): dx-=self.player_speed
        if self.keys_pressed.get("d")or self.keys_pressed.get("Right"): dx+=self.player_speed
        self.player_x=max(self.player_size,min(800-self.player_size,self.player_x+dx))
        self.player_y=max(45+self.player_size,min(640-self.player_size,self.player_y+dy))
        self.canvas.coords(self.player_id,self.player_x,self.player_y-self.player_size,self.player_x+self.player_size,self.player_y,self.player_x,self.player_y+self.player_size,self.player_x-self.player_size,self.player_y)
        self.player_trails.append((self.player_x,self.player_y))
        if len(self.player_trails)>4:
            old_x,old_y=self.player_trails.pop(0)
            t_id=self.canvas.create_polygon(old_x,old_y-self.player_size,old_x+self.player_size,old_y,old_x,old_y+self.player_size,old_x-self.player_size,old_y,fill="",outline="#4a235a",width=1)
            self.root.after(80,lambda:self.canvas.delete(t_id))
        self.canvas.coords(self.aim_line,self.player_x,self.player_y,self.mouse_x,self.mouse_y)
        self.canvas.coords(self.ch_h,self.mouse_x-6,self.mouse_y,self.mouse_x+6,self.mouse_y)
        self.canvas.coords(self.ch_v,self.mouse_x,self.mouse_y-6,self.mouse_x,self.mouse_y+6)
        for p in self.projectiles[:]:
            self.canvas.move(p["id"],p["dx"],p["dy"])
            p_coords=self.canvas.coords(p["id"])
            if not p_coords or p_coords[2]>800 or p_coords[0]<0 or p_coords[3]>640 or p_coords[1]<45:
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
            base_angle=math.atan2(self.player_y-ey,self.player_x-ex)
            flank_angle=base_angle+math.sin(self.spawn_counter*0.05+enemy["offset"])*1.2
            edx=math.cos(flank_angle)*enemy["speed"]
            edy=math.sin(flank_angle)*enemy["speed"]
            self.canvas.move(enemy["id"],edx,edy)
            e_coords=self.canvas.coords(enemy["id"])
            ex,ey=(e_coords[0]+e_coords[2])/2,(e_coords[1]+e_coords[3])/2
            if math.hypot(self.player_x-ex,self.player_y-ey)<(self.player_size+8):
                self.lives-=1
                self.canvas.delete(enemy["id"])
                self.enemies.remove(enemy)
                flash=self.canvas.create_rectangle(0,45,800,640,fill="#ff0000",outline="")
                self.root.after(40,lambda:self.canvas.delete(flash))
                if self.lives<=0:
                    self.canvas.create_text(400,340,text="GAME OVER",fill="#ff3838",font=("Consolas",36,"bold"),anchor="center")
                    return
                break
        if not self.enemies and self.enemies_remaining<=0:
            self.canvas.create_text(400,340,text="VICTORY!",fill="#2ecc71",font=("Consolas",36,"bold"),anchor="center")
            return
        self.canvas.itemconfig(self.ui_text,text=f"LEVEL: 1 | LIVES: {self.lives} | ENEMIES REMAINING: {len(self.enemies)+self.enemies_remaining}")
        self.root.after(16,self.update_game)
if __name__=="__main__":
    root=tk.Tk()
    game=Game(root)
    root.mainloop()