import time
from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image, ImageDraw, ImageFont
from printrun.printcore import printcore
from printrun import gcoder
import time

portal = "/dev/ttyUSB0"
baudrate = 115200
pather = "/home/pi/Desktop/3Dprinter/"


def fileScanner():
    print("Waiting for files to print")
    lis = []
    while len(lis) == 0:
        lis = os.listdir(pather)
        lis = [j for j in lis if "." in j and (
            j[j.index('.'):] == '.png' or j[j.index('.'):] == '.txt')]
    sort_list = sorted(lis)
    name = sort_list[0]
    if name[name.index('.'):] == ".png":
        try:
            w = int(name[name.index('_')+1:name.rindex('_')])
            h = int(name[name.rindex('_')+1:name.index('.')])
        except:
            print("Invalid file name configuration. File deleted")
            os.system(f"rm {pather}{sort_list[0]}")
            fileScanner()
            return
        PNG2STL(f"{pather}{name}", int(w), int(h), False)
    else:
        f = open(f"{pather}{name}", 'r')
        braille(f.read())
    os.system(f"rm {pather}{sort_list[0]}")
    print("done")
    pass


framesize = (300, 400)
hori_limit = 13
veri_limit = 10
fontsize=30
frame=True
def braille(inputString):
    global framesize,hori_limit,veri_limit,fontsize
    if frame==False:
        framesize = (1800,1850)
        hori_limit = 30
        veri_limit = 14
        fontsize=60
    else:
        framesize = (300, 400)
        hori_limit = 13
        veri_limit = 10
        fontsize=30
    inputString = inputString.lower()
    print(pather)
    font = ImageFont.truetype(f"{pather}braille.ttf", fontsize)
    convertedstring = ""
    inputString = inputString.split('\n')
    print(inputString)
    cur, curline = 0, 1
    start=True
    for i in inputString:
        if i.isspace():
            continue
        if start==False:
            convertedstring += f"\n\n"
            cur = 0
            curline += 1
            if curline == veri_limit:
                convertedstring,curline,cur=repeat(convertedstring,font)
        start=False
        i=i.split(" ")
        for j in i:
            if cur+len(j) < hori_limit:
                convertedstring += (j+" ")
                cur += len(j)+1
            elif cur+len(j) == hori_limit:
                convertedstring += j
                cur += len(j)
            else:
                convertedstring += f"\n\n{j} "
                cur = len(j)+1
                curline += 1
            if curline == veri_limit:
                convertedstring,curline,cur=repeat(convertedstring,font)
    if cur != 0 or curline != 0:
        bg = Image.new('RGBA', framesize, (0, 0, 0))
        draw = ImageDraw.Draw(bg)
        draw.text((10, 10), convertedstring,
                  font=font, fill=(255, 255, 255))
        bg.save(f'{pather}out.png')
    if frame==True:
        PNG2STL(f"{pather}out.png", 2.5, 70, True)
    else:
        PNG2STL(f"{pather}out.png", 3,180 , False)

def repeat(convertedstring,font):
    print(convertedstring)
    bg = Image.new('RGBA', framesize,(0, 0, 0))
    draw = ImageDraw.Draw(bg)
    draw.text((10, 10), convertedstring,
                  font=font, fill=(255, 255, 255))
    bg.save(f'{pather}out.png')
    if frame==True:
        PNG2STL(f"{pather}out.png", 2.5, 70, True)
    else:
        PNG2STL(f"{pather}out.png", 3,180 , False)
    print(
        "Take your print out. Remaining words will start print after 60 seconds")
    a = 60
    while a > 0:
        a -= 1
        print(a)
        time.sleep(1)
    return "",0,0

def PNG2STL(pngname, heightmm, widthmm, brallille):
    print("Converion of STL started")
    filename = "this.stl"
    if brallille == True:
        bg = Image.new('RGBA', framesize, (255, 255, 255))
        font = ImageFont.truetype(f"{pather}braille.ttf", fontsize)
        draw = ImageDraw.Draw(bg)
        draw.text((0, 0), "a", font=font, fill=(0, 0, 0))
        bg.save(f'{pather}white.png')
        try:
            dots = 256 * imread(f"{pngname}")
        except:
            print("Error")
            return
        # Compose RGBA channels to give depth
        dots = dots[:,:,2]+1.*dots[:, :, 0]
        dots /= 2
        surface = 256 * imread(f"{pather}white.png")
        os.system(f"rm {pather}out.png")
        os.system(f"rm {pather}white.png")
        surface = surface[:, :, 2] + 1.*surface[:, :, 0]
        dots += surface/2.25
        dots = gaussian_filter(dots, 1)  # smoothing
        p = numpy2stl(dots, "fun.stl", scale=0.0235,
                      mask_val=5., solid=True, max_width=150)
    else:
        print(pngname)
        try:
            dots = 256 * imread(f"{pngname}")
        except:
            print("Error")
            return
        dots = dots[:,:,2]+1.*dots[:, :, 0]
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
    file1 = open(f"{pather}{filename}", "w")
    file1.write("")
    file1.close()
    file1 = open(f"{pather}{filename}", "a")
    for j in p:
        if l == 0:
            l += 1
            continue
        q = ""
        file1.write(j+"\n")
    file1.close()
    print("Writing of STL complete")
    os.system(
        f"{pather}PrusaSlicer-version_2.4.2-armhf.AppImage -s {pather}{filename} --load {pather}config.ini")
    print("Gcode produced")
    return
    serialWriter(GcodeParser())

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
        gCode_commands.append(each)
    print("Done")
    return gCode_commands

def serialWriter(gcode):
    p = printcore(portal, baudrate)
    gcode = gcoder.LightGCode()
    while not p.online:
        time.sleep(0.1)
    p.startprint(gcode)
    while p.printing():
        pass

if __name__ == "__main__":
    while 1:
        fileScanner()
        print("Take your print out. Next print will start after 60 seconds")
        a = 60
        while a > 0:
            a -= 1
            print(a)
            time.sleep(1)