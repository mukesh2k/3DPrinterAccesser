import time
import threading
from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image, ImageDraw, ImageFont
import serial
from printrun.printcore import printcore
from printrun import gcoder
import time

portal = "/dev/ttyUSB0"
cache = ""


def serialReader():
    global serialPort
    serialPort = serial.Serial(port=portal, baudrate=115200,
                               bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    serialPort.close()
    serialPort.open()
    while 1:
        print(serialPort.readline())
    return


def serialWriter(gcode):
    p = printcore(portal, 115200)
    gcode = gcoder.LightGCode(gcode)
    while not p.online:
        time.sleep(0.1)
    p.startprint(gcode)
    while p.printing():
        pass


framesize = (300, 400)
hori_limit = 22
veri_limit = 10


def braille(inputString):
    inputString = inputString.lower()
    print(pather)
    font = ImageFont.truetype(f"{pather}braille.ttf", 30)
    convertedstring = ""
    inputString = inputString.split(' ')
    cur, curline = 0, 0
    for i in inputString:
        if cur+len(i) < hori_limit:
            convertedstring += (i+" ")
            cur += len(i)+1
        elif cur+len(i) == hori_limit:
            convertedstring += i
            cur += len(i)
        else:
            convertedstring += f"\n\n{i} "
            cur = len(i)+1
            curline += 1
        if curline == veri_limit:
            bg = Image.new('RGBA', framesize)

            draw = ImageDraw.Draw(bg)
            draw.text((100, 100), convertedstring, font=font)
            bg.save('out.png')
            PNG2Gcode("out.png", 2.5, 70, True)
            convertedstring = ""
            curline = 0
            cur = 0
    if cur != 0 or curline != 0:
        bg = Image.new('RGBA', framesize, (0, 0, 0))
        draw = ImageDraw.Draw(bg)
        draw.text((10, 10), convertedstring,
                  font=font, fill=(255, 255, 255))
        bg.save('out.png')
    PNG2Gcode("out.png", 2.5, 70, True)
    print(convertedstring)


def fileScanner():
    global pather
    # pather = "/home/mukesh/Documents/test/"
    pather = "/home/pi/Desktop/3Dprinter/"
    print("running")
    lis = []
    while len(lis) == 0:
        lis = os.listdir(pather)
        lis = [i for i in lis if "." in i and (
            i[i.index('.'):] == '.png' or i[i.index('.'):] == '.txt')]
    sort_list = sorted(lis)
    name = sort_list[0]
    if name[name.index('.'):] == ".png":
        w = name[name.index('_')+1:name.rindex('_')]
        h = name[name.rindex('_')+1:name.index('.')]
        PNG2Gcode(name, w, h, False)
    else:
        f = open(f"{pather}{name}", 'r')
        braille(f.read())
    os.system(f"rm {pather}{sort_list[0]}")
    print("done")
    pass


def GcodeParser():
    a = ""
    with open(f"{pather}this.gcode") as f:
        a += "".join(line for line in f if not line.isspace())
    a = a.splitlines()
    gCode_commands = []
    for each in a:
        if ';' in each:
            each = each[:each.index(';')]
            if each == '':
                continue
        # print(each)
        gCode_commands.append(each)
    return gCode_commands


def PNG2Gcode(pngname, heightmm, widthmm, brallille):
    filename = "this.stl"
    if brallille == True:
        bg = Image.new('RGBA', framesize, (255, 255, 255))
        font = ImageFont.truetype(f"{pather}braille.ttf", 30)
        draw = ImageDraw.Draw(bg)
        draw.text((0, 0), "a", font=font, fill=(0, 0, 0))
        bg.save('white.png')
        dots = 256 * imread(pngname)
        # Compose RGBA channels to give depth
        dots = dots[:, :, 2] + 1.*dots[:, :, 0]
        dots /= 2
        surface = 256 * imread("white.png")
        os.system(f"rm {pather}out.png")
        os.system(f"rm {pather}white.png")
        # Compose RGBA channels to give depth
        surface = surface[:, :, 2] + 1.*surface[:, :, 0]
        dots += surface/2.25
        dots = gaussian_filter(dots, 1)  # smoothing
        print("Converion of STL started")
        p = numpy2stl(dots, "fun.stl", scale=0.03,
                      mask_val=5., solid=True, max_width=150)
    else:
        dots = 256 * imread(pngname)
        dots = dots[:, :, 2] + 1.*dots[:, :, 0]
        dots = gaussian_filter(dots, 1)  # smoothing
        p = numpy2stl(dots, "fun.stl", scale=heightmm*0.01,
                      mask_val=5., solid=True, max_width=widthmm)
    print("Converion of STL complete")
    print("Writing of STL started")
    STL2Gcode(p, filename)


def STL2Gcode(p, filename):
    p = str(p)
    p = p.split("\\n")
    l = 0
    file1 = open(f"{pather}{filename}", "w")  # append mode
    file1.write("")
    file1.close()
    file1 = open(f"{pather}{filename}", "a")
    for i in p:
        if l == 0:
            l += 1
            continue
        q = ""
        file1.write(i+"\n")
    file1.close()
    print("Writing of STL complete")
    os.system(
        f"{pather}PrusaSlicer-version_2.4.2-armhf.AppImage -s {pather}{filename} -o {pather}this.gcode")
    print("Gcode produced")
    # GcodeParser()


text = "Its not such a big problem, but If you paste a transparent background image on a transparent background using Image paste and pass a mass the edge will be black."
# #text = "you can see there are some black outlines around text. "
# text = "".join("a\n" for i in range(21))
# braille(text)
#PNG2Gcode("download (1).png", 2, 70)
# Original flow
# fileScann
pather = "/home/pi/Desktop/3Dprinter/"

if __name__ == "__main__":
    # while 1:
    #     t = threading.Thread(target=fileScanner)

    # fileScanner()
    GcodeParser()
