from matplotlib.pylab import imread
from csdt_stl_tools import numpy2stl
from scipy.ndimage import gaussian_filter
import os
from PIL import Image


def convertImage():
    img = Image.open('ss.jpeg')
    img = img.convert("RGBA")
    datas = img.getdata()

    newData = []
    for item in datas:
        if item[0] == 0 and item[1] == 0 and item[2] == 0:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)

    img.putdata(newData)
    img.save("img2.png", "PNG")


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


convertImage()
# run()
