import time
from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image
import serial


def serialConnector():
    serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=115200,
                               bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    i = 100000
    while i:
        print(serialPort.read())
        i -= 1
    time.sleep(5)
    print("Start")
    res = bytes("G28", 'utf-8')
    serialPort.write(res)
    time.sleep(4)
    serialPort.close()


def par():
    a = ""
    with open("this.gcode") as f:
        a += "".join(line for line in f if not line.isspace())
    a = a.splitlines()
    i = 0
    for each in a:
        if ';' in each:
            each = each[:each.index(';')]
            if each == '':
                continue
        print(each)


def run():
    filename = "this.stl"
    A = 256 * imread("screenshot.png")
    A = A[:, :, 2] + 1.0*A[:, :, 0]  # Compose RGBA channels to give depth
    A = gaussian_filter(A, 1)  # smoothing
    p = numpy2stl(A, "fun.stl", scale=0.05,
                  mask_val=5., solid=True, max_width=70)
    print("Converion of STL complete")
    p = str(p)
    p = p.split("\\n")
    l = 0
    file1 = open(filename, "w")  # append mode
    file1.write("")
    file1.close()
    file1 = open(filename, "a")
    for i in p:
        if l == 0:
            l += 1
            continue
        file1.write(i+"\n")
    file1.close()
    print("Writing of STL complete")
    os.system(f"slic3r-console -o this.gcode --load config.ini {filename}")
    print("Gcode produced")


par()
# run()
