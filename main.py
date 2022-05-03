import time
from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image
import serial


def serialConnector():
    portal = "/dev/ttyUSB0"
    cache = ""
    serialPort = serial.Serial(port=portal, baudrate=115200,
                               bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.open()
    fileScanner()
    run()
    Gcodes = GcodeParser()
    # print(Gcodes)
    print(len(Gcodes))
    for u in Gcodes:
        print(u)
    return
    i = 0
    while i < len(Gcodes):
        val = print(serialPort.read())
        if len(cache) == 4:
            cache.replace(cache[0], "")
        cache += val
        if cache == "wait":
            os.system(f"echo {Gcodes[i]} > {portal}")
            i += 1
            time.sleep(0.5)
    print("Completed")


def modifiedtime(lis):
    stat = os.stat(pather+f"/{lis}")
    return stat.st_mtime


def fileScanner():
    lis = []
    global pather
    pather = os.getcwd()
    print("running")
    while len(lis) == 0:
        lis = os.listdir()
        lis = [i for i in lis if "." in i and i[i.index('.'):] == '.png']
    sort_list = sorted(lis, key=modifiedtime)
    # TODO run(sort_list[0])
    os.system(f"rm {sort_list[0]}")
    print("done")
    pass


def GcodeParser():
    a = ""
    with open("this.gcode") as f:
        a += "".join(line for line in f if not line.isspace())
    a = a.splitlines()
    i = 0
    gCode_commands = []
    for each in a:
        if ';' in each:
            each = each[:each.index(';')]
            if each == '':
                continue
        gCode_commands.append(each)
    return gCode_commands


def run(pngname):
    filename = "this.stl"
    A = 256 * imread(pngname)
    pic = Image.open(pngname)
    w, h = pic.size
    print(str(w)+str(h))
    A = A[:, :, 2] + 1.0*A[:, :, 0]  # Compose RGBA channels to give depth
    A = gaussian_filter(A, 1)  # smoothing
    p = numpy2stl(A, "fun.stl", scale=0.05,
                  mask_val=5., solid=True, max_width=w)
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


# fileScanner()
Gcodes = GcodeParser()
# print(Gcodes)
for u in Gcodes:
    print(u)
