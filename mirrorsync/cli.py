import questionary
import argparse
from . import server
from . import client

def main():
    """The main entry point for the interactive CLI."""
    
    # Check for non-interactive arguments first
    parser = argparse.ArgumentParser(description="MirrorSync: A file synchronization tool.")
    parser.add_argument('mode', nargs='?', help="Run in 'server' or 'client' mode directly.")
    args = parser.parse_args()

    mode = args.mode

    if not mode:
        # If no argument is given, show the interactive menu
        try:
            mode = questionary.select(
                "Welcome to MirrorSync! Choose a mode:",
                choices=[
                    "Server (Receive files from another device)",
                    "Client (Send files from this device)",
                ],
            ).ask()
        except (KeyboardInterrupt, TypeError):
            print("\nAborted.")
            return # Exit if user cancels
    
    if mode is None:
        print("\nAborted.")
        return

    # --- Run Server ---
    if mode.startswith("Server"):
        server.main()
        
    # --- Run Client ---
    elif mode.startswith("Client"):
        try:
            # Get connection details interactively
            server_ip = questionary.text("Enter the Server IP Address:").ask()
            if not server_ip: raise KeyboardInterrupt

            auth_code = questionary.text(
                "Enter the 6-Digit Auth Code:",
                validate=lambda text: len(text) == 6 and text.isdigit()
            ).ask()
            if not auth_code: raise KeyboardInterrupt

        except KeyboardInterrupt:
            print("\nClient setup aborted.")
            return

        # Start the client with the provided details
        # Note: We assume the client syncs the current directory by default
        client.main(server_ip=server_ip, auth_code=auth_code, directory='.')

if __name__ == '__main__':
    main()
