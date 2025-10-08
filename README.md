# MirrorSync

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A simple but powerful command-line tool to synchronize files and folders between two devices on your local network in real-time.



## ✨ Features

- **Real-Time Sync:** Instantly mirrors file creation, modification, deletion, and moves.
- **Interactive CLI:** A user-friendly menu to guide you through server or client setup.
- **Cross-Platform:** Works on Linux, macOS, and Windows.
- **Simple Authentication:** Secure your connection with a one-time 6-digit code.
- **Developer Friendly:** Packaged with modern tools for easy installation and contribution.

## 🚀 Installation

There are two ways to install MirrorSync, depending on your needs.

#### For End-Users (Recommended)

You can download a pre-built, single-click installer for your operating system.

1.  Go to the **[Releases Page](https://github.com/kumaraswamys28/mirrorsync/releases)** on GitHub.
2.  Download the latest installer for your system (`.deb` for Ubuntu/Debian, `.msi` for Windows, `.dmg` for macOS).
3.  Run the installer.

#### For Developers (from Source)

If you have Python and `pipx` installed, you can build the tool directly from the source code.

```bash
# 1. Clone the repository
git clone [https://github.com/kumaraswamys28/mirrorsync.git](https://github.com/kumaraswamys28/mirrorsync.git)

# 2. Navigate into the project folder
cd mirrorsync

# 3. Install using pipx
pipx install .
```

## 🖥️ How to Use

The tool is fully interactive.

1.  On the computer that will **receive** files, open a terminal and run:
    ```bash
    mirrorsync
    ```
    Choose **Server** from the menu. The tool will display the server's IP Address and a 6-digit Auth Code.

2.  On the computer that will **send** files, open a terminal and run:
    ```bash
    mirrorsync
    ```
    Choose **Client** from the menu.

3.  Enter the **IP Address** and **Auth Code** from the server machine when prompted.

Synchronization will begin immediately. Any changes made in the client's directory will be mirrored to a `server_sync_root` folder on the server.

## 📜 License

This project is licensed under the MIT License - see the `LICENSE` file for details.
