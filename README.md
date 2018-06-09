# qBittorrent-auto-mover
Move the files downloaded via qBittorrent automatically

It will check whether the torrents are finished and paused every 5 minutes, move those files to `DST` in `qb_auto.py` via `FastCopy.exe`, and delete the torrent info in qBittorrent.

## Getting Started

These instructions will give you installation guide and usage

### Prerequisites

NOTE: This script for windows only now

We suggest you using [Chocolatey](https://github.com/chocolatey/choco) and [Cmder](https://github.com/cmderdev/cmder)(You can install via Chocolatey) to use this program
```
# Install Chocolatey first via https://chocolatey.org/install

# Install Cmder
choco install -y cmder

# Execute cmds below in Cmder
choco install -y python3 fastcopy.portable
```
Set up your qBittorrent with WebUI enable and select `Bypass authentication for localhost`

### Install

First install the requirements
```
pip install -r requirements.txt
```

Configure the `DST` in `qb_auto.py`

### Usage

#### From Cmder

Run it from Cmder
```
./qb_auto.py
```

#### Install the script as a Windows Service via NSSM

[NSSM](https://nssm.cc/) aka the Non-Sucking Service Manager, can help us install any script as a Windows Service easily.

TODO: Test this with NSSM

## WARNING

- Sometime it will freeze the qBittorrent. Be patient.
- It will check that if any FastCopy process is existed, and wait for all FastCopy been exited, then execute the next job.
- FastCopy will open a minimized window or create a system tray. DO NOT close the windows or exit the program before the job is done. Otherwise it will cause some unexpected behavior.

## TODO

- use parameter rather than hard coded
- test with NSSM
- Linux Version
- multiple copy program to do it rather than using FastCopy only

## Authors

Yu-Chiang Huang <tjjh89017@hotmail.com>

## License

MIT License

Copyright (c) 2018 Date Huang

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
