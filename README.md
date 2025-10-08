# MirrorSync

A simple but powerful command-line tool to synchronize files and folders between two devices on your local network in real-time.

## Features

- Real-time synchronization of file creation, deletion, modification, and moves.
- Works between any two computers on the same network.
- Simple, one-time authentication using a 6-digit code.
- Cross-platform support for Linux, macOS, and Windows.

## How to Use

1. Run `sync-server` on one machine. Note the IP Address and Auth Code.
2. Run `sync-client /path/to/folder` on another machine.
3. Enter the IP and Auth Code when prompted.
4. Any changes in the client's folder will now be mirrored on the server.
