import socket
import threading
import os
import json
import random
from .config import SERVER_PORT

SERVER_HOST = '0.0.0.0'
SERVER_SYNC_ROOT = "server_sync_root"

def get_local_ip():
    """Finds the server's local network IP address."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def handle_client(conn, addr, auth_code):
    print(f"[+] New connection from {addr}")
    try:
        # Step 1: Authenticate the client
        client_code = conn.recv(6).decode()
        if client_code != auth_code:
            print(f"[!] Authentication failed for {addr}. Closing connection.")
            conn.send(b'NO')
            return
        conn.send(b'OK')

        # Step 2: Proceed with sync logic
        header_data = conn.recv(1024).decode()
        header = json.loads(header_data)
        action, rel_path = header.get('action'), header.get('path')
        if not action or not rel_path: return

        server_path = os.path.join(SERVER_SYNC_ROOT, rel_path)
        if action == 'upsert':
            os.makedirs(os.path.dirname(server_path), exist_ok=True)
            conn.send(b'OK')
            with open(server_path, 'wb') as f:
                while True:
                    data = conn.recv(1024)
                    if not data: break
                    f.write(data)
            print(f"[✓] Synced (upsert): {rel_path}")
        elif action == 'delete':
            if os.path.exists(server_path):
                os.remove(server_path)
            print(f"[✓] Synced (delete): {rel_path}")
    except Exception as e:
        print(f"[x] Error with client {addr}: {e}")
    finally:
        conn.close()

def main():
    os.makedirs(SERVER_SYNC_ROOT, exist_ok=True)
    auth_code = str(random.randint(100000, 999999))
    server_ip = get_local_ip()

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((SERVER_HOST, SERVER_PORT))
    s.listen(5)

    print("\n=========================================")
    print("           MirrorSync Server           ")
    print("=========================================")
    print(f"  IP Address:    {server_ip}")
    print(f"  Auth Code:     {auth_code}")
    print("=========================================")
    print(f"[*] Storing files in '{SERVER_SYNC_ROOT}/'")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr, auth_code)).start()
