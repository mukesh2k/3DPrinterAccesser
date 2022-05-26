#!/bin/bash
apt install python3
apt install pip
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
cd ~/Desktop
mkdir 3Dprinter
cd 3Dprinter
wget 
wget https://raw.githubusercontent.com/mukesh2k/3DPrinterAccesser/main/main.py
wget https://raw.githubusercontent.com/mukesh2k/3DPrinterAccesser/main/config.ini
wget https://raw.githubusercontent.com/mukesh2k/3DPrinterAccesser/main/braille.ttf
wget https://github.com/davidk/PrusaSlicer-ARM.AppImage/releases/download/version_2.4.2/PrusaSlicer-version_2.4.2-aarch64.AppImage
pip install printrun
pip install pyserial
pip install matplotlib
pip install csdt_stl_tools
pip install Pillow