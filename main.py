import time
from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image, ImageDraw, ImageFont
import serial

portal = "/dev/ttyUSB0"
cache = ""


def serialReader():
    global serialPort
    serialPort = serial.Serial(port=portal, baudrate=115200,
                               bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
    if serialPort.is_open():
        serialPort.close()
    serialPort.open()
    while 1:
        print(serialPort.readline())
    return


def serialWriter():
    fileScanner()
    Gcodes = GcodeParser()
    serialPort.writelines("sdasdad")
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


framesize = (300, 400)


def braille(inputString):
    inputString = inputString.lower()
    font = ImageFont.truetype('braille.ttf', 30)
    hori_limit = 22
    veri_limit = 10
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
            # PNG2Gcode("out.png", 2.5, 210)
            convertedstring = ""
            curline = 0
    if curline != 0:
        bg = Image.new('RGBA', framesize, (0, 0, 0))
        draw = ImageDraw.Draw(bg)
        draw.text((10, 10), convertedstring,
                  font=font, fill=(255, 255, 255))
        bg.save('out.png')
        PNG2Gcode("out.png", 2.5, 70, True)
    print(convertedstring)


def fileScanner():
    lis = []
    global pather
    pather = os.getcwd()
    print("running")
    while len(lis) == 0:
        lis = os.listdir()
        lis = [i for i in lis if "." in i and (
            i[i.index('.'):] == '.png' or i[i.index('.'):] == '.txt')]
    sort_list = sorted(lis, key=modifiedtime)
    name = sort_list[0]
    if name[name.index('.'):] == ".png":
        pass  # TODO
    else:
        pass  # TODO
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
        print(each)
        gCode_commands.append(each)
    return gCode_commands


def PNG2Gcode(pngname, heightmm, widthmm, brallille):
    filename = "this.stl"
    if brallille == True:
        bg = Image.new('RGBA', framesize, (255, 255, 255))
        font = ImageFont.truetype("braille.ttf", 30)
        draw = ImageDraw.Draw(bg)
        draw.text((0, 0), "a", font=font, fill=(0, 0, 0))
        bg.save('white.png')
        A = 256 * imread(pngname)
        A = A[:, :, 2] + 1.*A[:, :, 0]  # Compose RGBA channels to give depth
        A /= 2
        B = 256 * imread("white.png")
        B = B[:, :, 2] + 1.*B[:, :, 0]  # Compose RGBA channels to give depth
        A += B/2.25
        A = gaussian_filter(A, 1)  # smoothing
        print("Converion of STL started")
        p = numpy2stl(A, "fun.stl", scale=0.05,
                      mask_val=5., solid=True, max_width=150)
    else:
        A = 256 * imread(pngname)
        A = A[:, :, 2] + 1.*A[:, :, 0]
        A = gaussian_filter(A, 1)  # smoothing
        p = numpy2stl(A, "fun.stl", scale=heightmm*0.01,
                      mask_val=5., solid=True, max_width=widthmm)
    print("Converion of STL complete")
    print("Writing of STL started")
    STL2Gcode(p, filename)


def STL2Gcode(p, filename):
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
        q = ""
        # i = i.split()
        # for j in i:
        #     try:
        #         q += "{:f}".format(float(j))
        #     except:
        #         q += j
        #     q += " "
        file1.write(i+"\n")
    file1.close()
    print("Writing of STL complete")
    return
    os.system(f"mandoline {filename} -o this.stl")
    print("Gcode produced")
    # GcodeParser()


text = "Its not such a big problem, but If you paste a transparent background image on a transparent background using Image paste and pass a mass the edge will be black."
# #text = "you can see there are some black outlines around text. "
# text = "".join("a\n" for i in range(21))
braille(text)
#PNG2Gcode("download (1).png", 2, 70)
# Original flow
# fileScann
# if __name__ == "__main__":
#     print("hello")
#     thread1 = threading.Thread(target=fileScanner)
#     thread2 = threading.Thread(target=serialReader)
#     thread1.start()
#     thread2.start()
