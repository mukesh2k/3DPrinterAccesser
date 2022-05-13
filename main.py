import time
from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image, ImageDraw, ImageFont
import serial


def serialConnector():
    # TODO serial connector
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


def braille(inputString):
    inputString = inputString.lower()
    font = ImageFont.truetype('braille.ttf', 100)
    framesize = (2100, 2200)
    hori_limit = 22
    veri_limit = 21
    convertedstring = ""
    inputString = inputString.split(' ')
    cur = 0
    for i in inputString:
        if cur+len(i) < hori_limit:
            convertedstring += (i+" ")
            cur += len(i)
        elif cur+len(i) == hori_limit:
            convertedstring += (i+" ")
            cur += len(i)
        else:
            convertedstring += f"\n{i}"
            cur = len(i)
    bg = Image.new('RGBA', framesize)
    draw = ImageDraw.Draw(bg)
    draw.text((100, 100), convertedstring, font=font)
    bg.save('out.png')


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
    gCode_commands = []
    for each in a:
        if ';' in each:
            each = each[:each.index(';')]
            if each == '':
                continue
        gCode_commands.append(each)
    return gCode_commands


def PNG2Gcode(pngname, heightmm, widthmm):
    filename = "this.stl"
    A = 256 * imread(pngname)
    pic = Image.open(pngname)
    A = A[:, :, 2] + 1.0*A[:, :, 0]  # Compose RGBA channels to give depth
    A = gaussian_filter(A, 1)  # smoothing
    p = numpy2stl(A, "fun.stl", scale=heightmm*0.01,
                  mask_val=5., solid=True, max_width=widthmm)
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


# text = "Its not such a big problem, but If you paste a transparent background image on a transparent background using Image paste and pass a mass the edge will be black."
# #text = "you can see there are some black outlines around text. "
# text = "".join("a\n" for i in range(21))
# braille(text)

p = GcodeParser()
for i in p:
    print(f"echo {i} > ttfasdas")
