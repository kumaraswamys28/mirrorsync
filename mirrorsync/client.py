import socket
import os
import time
import json
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from .config import SERVER_PORT

def send_request(server_ip, auth_code, header, filepath=None):
    """Establishes connection and sends a request to the server."""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((server_ip, SERVER_PORT))

            # Step 1: Authenticate with the server
            s.sendall(auth_code.encode())
            if s.recv(2) != b'OK':
                print("[x] Authentication failed. Please check the auth code.")
                return

            # Step 2: Proceed with sync logic
            s.sendall(json.dumps(header).encode())
            if header['action'] == 'upsert' and filepath:
                if s.recv(2) == b'OK':
                    with open(filepath, 'rb') as f:
                        while chunk := f.read(1024):
                            s.sendall(chunk)
                    print(f"[✓] Synced (upsert): {header['path']}")
            elif header['action'] == 'delete':
                 print(f"[✓] Synced (delete): {header['path']}")

    except ConnectionRefusedError:
        print(f"[x] Connection refused. Is the server running at {server_ip}?")
    except Exception as e:
        print(f"[x] Failed to sync {header['path']}. Error: {e}")

class FileSyncHandler(FileSystemEventHandler):
    """Handles file system events and triggers sync requests."""
    def __init__(self, watch_path, server_ip, auth_code):
        self.watch_path = os.path.abspath(watch_path)
        self.server_ip = server_ip
        self.auth_code = auth_code

    def get_relative_path(self, path):
        """Gets the file path relative to the watched directory."""
        return os.path.relpath(path, self.watch_path)

    def on_created(self, event):
        if not event.is_directory:
            header = {'action': 'upsert', 'path': self.get_relative_path(event.src_path)}
            send_request(self.server_ip, self.auth_code, header, event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            header = {'action': 'upsert', 'path': self.get_relative_path(event.src_path)}
            send_request(self.server_ip, self.auth_code, header, event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            header = {'action': 'delete', 'path': self.get_relative_path(event.src_path)}
            send_request(self.server_ip, self.auth_code, header)

    def on_moved(self, event):
        if not event.is_directory:
            del_header = {'action': 'delete', 'path': self.get_relative_path(event.src_path)}
            send_request(self.server_ip, self.auth_code, del_header)
            up_header = {'action': 'upsert', 'path': self.get_relative_path(event.dest_path)}
            send_request(self.server_ip, self.auth_code, up_header, event.dest_path)

def main(server_ip=None, auth_code=None, directory='.'):
    """
    Starts the client file watcher.
    Accepts connection details as arguments so it can be called from another script.
    """
    if not os.path.isdir(directory):
        print(f"[x] Error: Directory '{directory}' does not exist.")
        return
    
    if not server_ip or not auth_code:
        print("[x] Error: Server IP and Auth Code must be provided to start the client.")
        return
    
    print(f"[*] Watching directory: '{os.path.abspath(directory)}'")
    
    # Pass connection details to the handler
    event_handler = FileSyncHandler(directory, server_ip, auth_code)
    observer = Observer()
    observer.schedule(event_handler, directory, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
    print("\n[*] Client stopped.")

if __name__ == '__main__':
    # This block allows you to run this file directly for testing purposes,
    # separate from the main `mirrorsync` CLI command.
    print("--- Running client in direct test mode ---")
    ip_addr = input("Enter Server IP: ")
    auth = input("Enter Auth Code: ")
    main(server_ip=ip_addr, auth_code=auth)
