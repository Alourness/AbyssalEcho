import tkinter as tk
import math
import random
class Game:
    def __init__(self,root):
        self.root=root
        self.root.title("2D Top-Down Game - Level 1")
        self.root.geometry("800x640")
        self.root.resizable(False,False)
        self.canvas=tk.Canvas(root,width=800,height=640,bg="#0a0a0f")
        self.canvas.pack(fill="both",expand=True)
        self.draw_background_debris()
        self.canvas.create_rectangle(0,0,800,45,fill="#12121c",outline="#1f1f2e",width=2)
        self.ui_text=self.canvas.create_text(20,22,anchor="w",fill="#d8b4fe",font=("Consolas",11,"bold"),text="LEVEL: 1 | LIVES: 3 | ENEMIES REMAINING: 50")
        self.player_x=400
        self.player_y=340
        self.player_size=16
        self.player_id=self.canvas.create_polygon(self.player_x,self.player_y-self.player_size,self.player_x+self.player_size,self.player_y,self.player_x,self.player_y+self.player_size,self.player_x-self.player_size,self.player_y,fill="#c084fc",outline="#f3e8ff",width=2)
        self.player_glow=self.canvas.create_polygon(self.player_x,self.player_y-(self.player_size+4),self.player_x+(self.player_size+4),self.player_y,self.player_x,self.player_y+(self.player_size+4),self.player_x-(self.player_size+4),self.player_y,fill="",outline="#a855f7",width=1)
        self.player_speed=4.5
        self.lives=3
        self.enemies_remaining=50
        self.spawn_counter=0
        self.enemies=[]
        self.projectiles=[]
        self.player_trails=[]
        self.particles=[]
        self.keys_pressed={}
        self.root.bind("<KeyPress>",self.on_key_press)
        self.root.bind("<KeyRelease>",self.on_key_release)
        for _ in range(5): self.spawn_enemy()
        self.update_game()
    def draw_background_debris(self):
        for _ in range(25):
            x,y=random.randint(20,780),random.randint(65,620)
            size=random.randint(3,7)
            self.canvas.create_polygon(x,y-size,x+size,y,x,y+size,x-size,y,fill="#151522",outline="#22223b",width=1)
    def on_key_press(self,event):
        self.keys_pressed[event.keysym]=True
        self.keys_pressed[event.char]=True
        char=event.char.lower()
        if char=="i": self.shoot("up")
        elif char=="k": self.shoot("down")
        elif char=="j": self.shoot("left")
        elif char=="l": self.shoot("right")
    def on_key_release(self,event):
        self.keys_pressed.pop(event.keysym,None)
        self.keys_pressed.pop(event.char,None)
    def shoot(self,direction):
        dx,dy=0,0
        if direction=="up": dy=-1
        elif direction=="down": dy=1
        elif direction=="left": dx=-1
        elif direction=="right": dx=1
        p_id=self.canvas.create_rectangle(self.player_x-6,self.player_y-6,self.player_x+6,self.player_y+6,fill="#e879f9",outline="#ffffff",width=1)
        self.projectiles.append({"id":p_id,"dx":dx*27,"dy":dy*27,"x":self.player_x,"y":self.player_y,"trail":[]})
        for _ in range(4):
            self.particles.append({"x":self.player_x,"y":self.player_y,"dx":random.uniform(-3,3),"dy":random.uniform(-3,3),"life":12,"color":"#d946ef","id":self.canvas.create_oval(self.player_x-2,self.player_y-2,self.player_x+2,self.player_y+2,fill="#e879f9",outline="")})
    def spawn_enemy(self):
        if self.enemies_remaining<=0: return
        side=random.choice(["top","bottom","left","right"])
        if side=="top": x,y=random.randint(0,800),55
        elif side=="bottom": x,y=random.randint(0,800),630
        elif side=="left": x,y=0,random.randint(55,640)
        else: x,y=800,random.randint(55,640)
        e_id=self.canvas.create_rectangle(x,y,x+20,y+20,fill="#ef4444",outline="#fca5a5",width=1)
        self.enemies.append({"id":e_id,"base_speed":random.uniform(1.2,2.4),"speed":2.0,"offset":random.uniform(0,6.28),"behavior_timer":random.randint(30,90),"mode":"flank","x":x,"y":y})
        self.enemies_remaining-=1
    def update_game(self):
        self.spawn_counter+=1
        if self.spawn_counter>=250:
            self.spawn_counter=0
            for _ in range(5): self.spawn_enemy()
        dx,dy=0,0
        if self.keys_pressed.get("w")or self.keys_pressed.get("W")or self.keys_pressed.get("Up"): dy-=self.player_speed
        if self.keys_pressed.get("s")or self.keys_pressed.get("S")or self.keys_pressed.get("Down"): dy+=self.player_speed
        if self.keys_pressed.get("a")or self.keys_pressed.get("A")or self.keys_pressed.get("Left"): dx-=self.player_speed
        if self.keys_pressed.get("d")or self.keys_pressed.get("D")or self.keys_pressed.get("Right"): dx+=self.player_speed
        self.player_x=max(self.player_size+15,min(800-self.player_size-15,self.player_x+dx))
        self.player_y=max(45+self.player_size+15,min(640-self.player_size-15,self.player_y+dy))
        if self.player_x<=self.player_size+16 or self.player_x>=800-self.player_size-16:
            for _ in range(2):
                self.particles.append({"x":self.player_x,"y":self.player_y,"dx":random.uniform(-4,4),"dy":random.uniform(-4,4),"life":8,"color":"#f0abfc","id":self.canvas.create_oval(self.player_x-2,self.player_y-2,self.player_x+2,self.player_y+2,fill="#f0abfc",outline="")})
        if self.player_y<=45+self.player_size+16 or self.player_y>=640-self.player_size-16:
            for _ in range(2):
                self.particles.append({"x":self.player_x,"y":self.player_y,"dx":random.uniform(-4,4),"dy":random.uniform(-4,4),"life":8,"color":"#f0abfc","id":self.canvas.create_oval(self.player_x-2,self.player_y-2,self.player_x+2,self.player_y+2,fill="#f0abfc",outline="")})
        self.canvas.coords(self.player_id,self.player_x,self.player_y-self.player_size,self.player_x+self.player_size,self.player_y,self.player_x,self.player_y+self.player_size,self.player_x-self.player_size,self.player_y)
        self.canvas.coords(self.player_glow,self.player_x,self.player_y-(self.player_size+4),self.player_x+(self.player_size+4),self.player_y,self.player_x,self.player_y+(self.player_size+4),self.player_x-(self.player_size+4),self.player_y)
        self.player_trails.append((self.player_x,self.player_y))
        if len(self.player_trails)>6:
            old_x,old_y=self.player_trails.pop(0)
            t_id=self.canvas.create_polygon(old_x,old_y-self.player_size,old_x+self.player_size,old_y,old_x,old_y+self.player_size,old_x-self.player_size,old_y,fill="",outline="#581c87",width=1)
            self.root.after(70,lambda:self.canvas.delete(t_id))
        for p in self.projectiles[:]:
            self.canvas.move(p["id"],p["dx"],p["dy"])
            p_coords=self.canvas.coords(p["id"])
            if not p_coords or p_coords[2]>800 or p_coords[0]<0 or p_coords[3]>640 or p_coords[1]<45:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)
                continue
            px,py=(p_coords[0]+p_coords[2])/2,(p_coords[1]+p_coords[3])/2
            p["trail"].append((px,py))
            if len(p["trail"])>3:
                tx,ty=p["trail"].pop(0)
                spark=self.canvas.create_oval(tx-3,ty-3,tx+3,ty+3,fill="#c084fc",outline="")
                self.root.after(50,lambda:self.canvas.delete(spark))
            hit=False
            for enemy in self.enemies[:]:
                e_coords=self.canvas.coords(enemy["id"])
                if not e_coords: continue
                if e_coords[0]<px<e_coords[2] and e_coords[1]<py<e_coords[3]:
                    self.canvas.delete(enemy["id"])
                    self.enemies.remove(enemy)
                    hit=True
                    for _ in range(8):
                        self.particles.append({"x":px,"y":py,"dx":random.uniform(-5,5),"dy":random.uniform(-5,5),"life":15,"color":"#f43f5e","id":self.canvas.create_rectangle(px-2,py-2,px+2,py+2,fill="#fca5a5",outline="")})
                    break
            if hit:
                self.canvas.delete(p["id"])
                self.projectiles.remove(p)
        for enemy in self.enemies:
            enemy["behavior_timer"]-=1
            if enemy["behavior_timer"]<=0:
                enemy["behavior_timer"]=random.randint(40,100)
                enemy["mode"]=random.choice(["flank","rush","retreat","circle"])
                enemy["base_speed"]=random.uniform(1.0,3.2)
            e_coords=self.canvas.coords(enemy["id"])
            if not e_coords: continue
            ex,ey=(e_coords[0]+e_coords[2])/2,(e_coords[1]+e_coords[3])/2
            dist_to_player=math.hypot(self.player_x-ex,self.player_y-ey)
            base_angle=math.atan2(self.player_y-ey,self.player_x-ex)
            if enemy["mode"]=="flank":
                angle=base_angle+math.sin(self.spawn_counter*0.06+enemy["offset"])*1.4
                enemy["speed"]=enemy["base_speed"]
            elif enemy["mode"]=="rush":
                angle=base_angle
                enemy["speed"]=enemy["base_speed"]*1.8
            elif enemy["mode"]=="retreat" and dist_to_player<150:
                angle=base_angle+math.pi
                enemy["speed"]=enemy["base_speed"]*1.2
            elif enemy["mode"]=="circle":
                angle=base_angle+math.pi/2
                enemy["speed"]=enemy["base_speed"]*1.4
            else:
                angle=base_angle
                enemy["speed"]=enemy["base_speed"]
            edx=math.cos(angle)*enemy["speed"]
            edy=math.sin(angle)*enemy["speed"]
            self.canvas.move(enemy["id"],edx,edy)
            e_coords=self.canvas.coords(enemy["id"])
            ex,ey=(e_coords[0]+e_coords[2])/2,(e_coords[1]+e_coords[3])/2
            if dist_to_player<(self.player_size+10):
                self.lives-=1
                self.canvas.delete(enemy["id"])
                self.enemies.remove(enemy)
                flash=self.canvas.create_rectangle(0,45,800,640,fill="#ef4444",outline="")
                self.root.after(40,lambda:self.canvas.delete(flash))
                if self.lives<=0:
                    self.canvas.create_text(400,340,text="GAME OVER",fill="#ef4444",font=("Consolas",36,"bold"),anchor="center")
                    return
                break
        for part in self.particles[:]:
            self.canvas.move(part["id"],part["dx"],part["dy"])
            part["life"]-=1
            if part["life"]<=0:
                self.canvas.delete(part["id"])
                self.particles.remove(part)
        if not self.enemies and self.enemies_remaining<=0:
            self.canvas.create_text(400,340,text="VICTORY!",fill="#4ade80",font=("Consolas",36,"bold"),anchor="center")
            return
        self.canvas.itemconfig(self.ui_text,text=f"LEVEL: 1 | LIVES: {self.lives} | ENEMIES REMAINING: {len(self.enemies)+self.enemies_remaining}")
        self.root.after(16,self.update_game)
if __name__=="__main__":
    root=tk.Tk()
    game=Game(root)
    root.mainloop()