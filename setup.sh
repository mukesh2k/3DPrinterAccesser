#!/bin/bash
apt install python3
apt install pip
apt-get install bluez-tools
apt-get install git
apt-get update
apt-get upgrade
git clone https://github.com/juliagoda/CH341SER.git
cd CH341SER
make clean
make
make load
usermod -a -G dialout mukesh
chmod a+rw /dev/ttyUSB0
cd ..
wget https://dl.slic3r.org/linux/old/slic3r-linux-x86_64-1-2-9-stable.tar.gz
tar -zxvf slic3r-linux-x86_64-1-2-9-stable.tar.gz
cd slic3r-linux-x86_64-1-2-9-stable/bin
wget https://raw.githubusercontent.com/mukesh2k/3DPrinterAccesser/main/main.py
wget https://raw.githubusercontent.com/mukesh2k/3DPrinterAccesser/main/config.ini
wget https://raw.githubusercontent.com/mukesh2k/3DPrinterAccesser/main/braille.ttf
pip install pyserial
pip install matplotlib
pip install csdt_stl_tools
pip install Pillow