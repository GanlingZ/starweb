import tkinter as tk
import random

class LoveSamoyed:
    def __init__(self, root):
        self.root = root
        
        # --- Settings ---
        self.pixel_scale = 5
        self.walk_speed = 4
        
        # --- Window Setup ---
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        
        # Cross-platform transparency
        self.is_windows = False
        try:
            self.root.wm_attributes("-transparent", True)
            self.root.config(bg='systemTransparent')
            self.bg_color = 'systemTransparent'
        except tk.TclError:
            self.is_windows = True
            self.root.config(bg='white')
            self.root.wm_attributes("-alpha", 1.0)
            self.root.wm_attributes("-transparentcolor", "white")
            self.bg_color = 'white'

        # Dimensions
        self.grid_w = 26
        self.grid_h = 24
        self.w = self.grid_w * self.pixel_scale
        self.h = self.grid_h * self.pixel_scale
        
        self.canvas = tk.Canvas(root, width=self.w, height=self.h, 
                                bg=self.bg_color, highlightthickness=0)
        self.canvas.pack()

        # --- MOUSE INPUTS ---
        self.canvas.bind('<Button-1>', self.start_drag)
        self.canvas.bind('<B1-Motion>', self.do_drag)
        self.canvas.bind('<ButtonRelease-1>', self.stop_drag)
        self.drag_data = {"x": 0, "y": 0, "is_dragging": False}

        # --- State ---
        self.state = "IDLE" 
        self.timer = 0
        self.anim_index = 0
        self.facing_right = True
        
        # FX Systems
        self.hearts = [] # List to store active hearts
        
        # Position
        self.screen_w = root.winfo_screenwidth()
        self.screen_h = root.winfo_screenheight()
        self.x = self.screen_w // 2
        self.y = self.screen_h // 2
        self.target_x = self.x
        self.target_y = self.y
        
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")

        # --- Colors ---
        self.colors = {
            '1': '#1a1a1a',  # Outline
            '2': '#ffffff',  # Fur
            '3': '#ffb7c5',  # Pink (Tongue/Ears)
            '4': '#d1d1d1',  # Grey Shading
            '5': '#ff69b4',  # Hot Pink (Hearts)
        }

        self.define_sprites()
        
        # Start Loop
        self.root.after(100, self.update_behavior)
        self.root.after(50, self.update_animation)

    def define_sprites(self):
        self.sprites = {}
        
        # IDLE
        self.sprites['idle'] = [
            "..........................",
            ".........111...111........", 
            "........12221.12221.......", 
            ".......1222221222221......",
            "......122222222222221.....",
            ".....12222222222222221....",
            "....1222112222211222221...", 
            "...122222222122222222221..",
            "..12222222211122222222221.", 
            "..12222222223222222222221.", 
            ".1222222222222222222222221",
            "12222222222222222222222221",
            "12222442222222222224422221", 
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            ".122222222222222222222221.",
            "..111111...........11111..", 
            "..........................",
            "..........................",
            ".........................."
        ]

        # WALK
        self.sprites['walk1'] = [ 
            "..........................",
            "......11..................",
            ".....1221.................", 
            "....122221................",
            "....121221...1111.........", 
            "....122221111222211.......", 
            "....1222222222222221......",
            "....12244222222222221.....", 
            ".....12222222222222221....",
            ".....12222222222222221....", 
            ".....122222222222222211...",
            ".....1222222222222222221..", 
            ".....1222222222222222221..", 
            "......12222222222222221...", 
            "......1222222222222221....", 
            ".......112221...12221.....",
            "........12221...12221.....",
            ".........111.....111......",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            ".........................."
        ]
        
        self.sprites['walk2'] = [ 
            "..........................",
            "......11..................",
            ".....1221.................", 
            "....122221................",
            "....121221...1111.........", 
            "....122221111222211.......", 
            "....1222222222222221......",
            "....12244222222222221.....", 
            ".....12222222222222221....",
            ".....12222222222222221....", 
            ".....122222222222222211...",
            ".....1222222222222222221..", 
            ".....1222222222222222221..", 
            "......122222222222222211..", 
            "......12222222222222211...", 
            "........12221.12221.......", 
            ".........1221.1221........",
            "..........11...11.........",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            ".........................."
        ]

        # BARK (Smoothed bottom, no feet)
        self.sprites['bark'] = [
            "..........................",
            ".........111...111........", 
            "........12221.12221.......", 
            ".......1222221222221......",
            "......122222222222221.....",
            ".....12222222222222221....",
            "....1222112222211222221...", 
            "...122222222222222222221..",
            "..12222222211122222222221.", 
            "..12222222111112222222221.", 
            ".1222222221333122222222221", 
            "12222222221111122222222221",
            "12222442222222222224422221", 
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            "12222222222222222222222221",
            ".122222222222222222222221.",
            "..122222...........12222..", 
            "..........................",
            "..........................",
            ".........................."
        ]

        # SLEEP
        self.sprites['sleep'] = [
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "......11...11.............", 
            ".....1221.1221...11...11..", 
            ".....1221.1221..1221.1221.",
            "....12222222221.1221.1221.",
            "...1222222222221222222221.", 
            "..12312222222222222222221.", 
            ".122212222222222222222221.",
            ".121122222222222222222221.", 
            ".123222222222222222222221.", 
            "..1112222222222222222221..",
            ".....111111111111111111...",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            "..........................",
            ".........................."
        ]
        
        # TIPPY TAPS
        self.sprites['tippy_a'] = self.sprites['idle'][:] 
        self.sprites['tippy_a'][21] = "..122221.................." 
        
        self.sprites['tippy_b'] = self.sprites['idle'][:] 
        self.sprites['tippy_b'][21] = "...................122221." 

    # --- DRAGGING & HEARTS ---
    def start_drag(self, event):
        self.drag_data["x"] = event.x
        self.drag_data["y"] = event.y
        self.drag_data["is_dragging"] = True
        self.state = "DRAG"
        # Spawn hearts on click
        self.spawn_hearts(3)

    def do_drag(self, event):
        dx = event.x - self.drag_data["x"]
        dy = event.y - self.drag_data["y"]
        self.x += dx
        self.y += dy
        self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
        
        # Chance to spawn trail hearts while moving
        if random.random() < 0.3:
            self.spawn_hearts(1)

    def stop_drag(self, event):
        self.drag_data["is_dragging"] = False
        self.state = "IDLE"
        self.timer = 50

    def spawn_hearts(self, count):
        for _ in range(count):
            # Heart starting position (relative to dog center)
            # Center is approx grid_w/2 (13), grid_h/2 (12)
            hx = (self.grid_w // 2) * self.pixel_scale
            hy = (self.grid_h // 2) * self.pixel_scale
            
            # Random offsets
            offset_x = random.randint(-20, 20)
            offset_y = random.randint(-10, 10)
            
            self.hearts.append({
                'x': hx + offset_x,
                'y': hy + offset_y,
                'life': 20, # How many frames it lasts
                'speed': random.randint(1, 3)
            })

    # --- AI BRAIN ---
    def update_behavior(self):
        if self.drag_data["is_dragging"]:
            self.root.after(100, self.update_behavior)
            return

        if self.timer > 0:
            self.timer -= 1
        else:
            roll = random.random()
            
            if self.state == "SLEEP":
                if roll < 0.8: self.timer = 50
                else: 
                    self.state = "IDLE"
                    self.timer = 20
            else:
                if roll < 0.35:
                    self.state = "IDLE"
                    self.timer = 50 
                elif roll < 0.6:
                    self.state = "WALK"
                    margin = 50
                    self.target_x = random.randint(margin, self.screen_w - margin - self.w)
                    self.target_y = random.randint(margin, self.screen_h - margin - self.h)
                    self.timer = 200 
                elif roll < 0.75:
                    self.state = "TIPPY_TAPS"
                    self.timer = 30
                elif roll < 0.85:
                    self.state = "BARK"
                    self.timer = 15
                else:
                    self.state = "SLEEP"
                    self.timer = 150 

        self.root.after(100, self.update_behavior)

    # --- ANIMATION ---
    def update_animation(self):
        self.anim_index += 1
        current_sprite = "idle"
        
        # 1. Update Hearts Physics
        for h in self.hearts:
            h['y'] -= h['speed'] # Float up
            h['life'] -= 1
        # Remove dead hearts
        self.hearts = [h for h in self.hearts if h['life'] > 0]
        
        # 2. Movement Logic
        if self.state == "WALK" and not self.drag_data["is_dragging"]:
            dx = 0
            dy = 0
            if abs(self.target_x - self.x) > self.walk_speed:
                dx = self.walk_speed if self.target_x > self.x else -self.walk_speed
            if abs(self.target_y - self.y) > self.walk_speed:
                dy = self.walk_speed if self.target_y > self.y else -self.walk_speed
            
            if dx == 0 and dy == 0:
                self.state = "IDLE"
                self.timer = 40
            
            self.x += dx
            self.y += dy
            self.root.geometry(f"+{int(self.x)}+{int(self.y)}")
            
            if dx > 0: self.facing_right = True
            elif dx < 0: self.facing_right = False
            
            current_sprite = "walk1" if (self.anim_index // 3) % 2 == 0 else "walk2"

        elif self.state == "TIPPY_TAPS":
            current_sprite = "tippy_a" if (self.anim_index // 2) % 2 == 0 else "tippy_b"
        elif self.state == "BARK":
            current_sprite = "bark"
        elif self.state == "SLEEP":
            current_sprite = "sleep"
        elif self.state == "DRAG":
            current_sprite = "idle"
        
        self.draw_frame(current_sprite)
        self.root.after(50, self.update_animation)

    def draw_frame(self, sprite_name):
        self.canvas.delete("all")
        
        grid = self.sprites[sprite_name]
        
        for r, row in enumerate(grid):
            for c, char in enumerate(row):
                if char in self.colors:
                    draw_c = c
                    if not self.facing_right:
                        draw_c = (self.grid_w - 1) - c
                    
                    x1 = draw_c * self.pixel_scale
                    y1 = r * self.pixel_scale
                    x2 = x1 + self.pixel_scale
                    y2 = y1 + self.pixel_scale
                    
                    self.canvas.create_rectangle(x1, y1, x2, y2, 
                                                 fill=self.colors[char], 
                                                 outline="")
        
        # FX Layers
        if self.state == "SLEEP":
            self.draw_moving_zzz()
        elif self.state == "BARK":
            self.draw_woof()
        elif self.state == "TIPPY_TAPS":
            self.draw_sparkles()
            
        # Draw Hearts (Always on top)
        self.draw_hearts()

    def draw_hearts(self):
        for h in self.hearts:
            hx, hy = h['x'], h['y']
            sz = self.pixel_scale
            # Mini Heart Shape
            # .X.X.
            # XXXXX
            # .XXX.
            # ..X..
            
            color = self.colors['5']
            
            # Row 0
            self.canvas.create_rectangle(hx, hy, hx+sz, hy+sz, fill=color, outline="")
            self.canvas.create_rectangle(hx+2*sz, hy, hx+3*sz, hy+sz, fill=color, outline="")
            
            # Row 1
            self.canvas.create_rectangle(hx-sz, hy+sz, hx+4*sz, hy+2*sz, fill=color, outline="")
            
            # Row 2
            self.canvas.create_rectangle(hx, hy+2*sz, hx+3*sz, hy+3*sz, fill=color, outline="")
            
            # Row 3
            self.canvas.create_rectangle(hx+sz, hy+3*sz, hx+2*sz, hy+4*sz, fill=color, outline="")

    def draw_moving_zzz(self):
        step = (self.anim_index // 5) % 4
        z_color = '#1a1a1a'
        base_x = 13 * self.pixel_scale 
        base_y = 12 * self.pixel_scale
        
        offsets = []
        if step >= 1: offsets.append((0, 0))
        if step >= 2: offsets.append((15, -20))
        if step >= 3: offsets.append((25, -45))
        
        for ox, oy in offsets:
            sx, sy = base_x + ox, base_y + oy
            sz = self.pixel_scale
            self.canvas.create_rectangle(sx, sy, sx+3*sz, sy+sz, fill=z_color, outline="")
            self.canvas.create_rectangle(sx+sz, sy+sz, sx+2*sz, sy+2*sz, fill=z_color, outline="")
            self.canvas.create_rectangle(sx, sy+2*sz, sx+3*sz, sy+3*sz, fill=z_color, outline="")

    def draw_woof(self):
        cx, cy = 20 * self.pixel_scale, 8 * self.pixel_scale
        sz = self.pixel_scale
        if self.facing_right:
            self.canvas.create_line(cx, cy, cx+2*sz, cy-2*sz, width=2, fill='#1a1a1a')
            self.canvas.create_line(cx+2*sz, cy, cx+4*sz, cy, width=2, fill='#1a1a1a')
            self.canvas.create_line(cx, cy+2*sz, cx+2*sz, cy+4*sz, width=2, fill='#1a1a1a')
        else:
            cx = (self.w) - cx
            self.canvas.create_line(cx, cy, cx-2*sz, cy-2*sz, width=2, fill='#1a1a1a')
            self.canvas.create_line(cx-2*sz, cy, cx-4*sz, cy, width=2, fill='#1a1a1a')
            self.canvas.create_line(cx, cy+2*sz, cx-2*sz, cy+4*sz, width=2, fill='#1a1a1a')

    def draw_sparkles(self):
        frame = (self.anim_index // 3) % 2
        color = '#ffb7c5' 
        if frame == 0:
            self.canvas.create_rectangle(2*self.pixel_scale, 5*self.pixel_scale, 3*self.pixel_scale, 6*self.pixel_scale, fill=color, outline="")
            self.canvas.create_rectangle(24*self.pixel_scale, 5*self.pixel_scale, 25*self.pixel_scale, 6*self.pixel_scale, fill=color, outline="")

if __name__ == '__main__':
    root = tk.Tk()
    pet = LoveSamoyed(root)
    root.mainloop()