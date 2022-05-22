from pylab import imread
from csdt_stl_tools import numpy2stl

# from scipy.misc import imresize
from scipy.ndimage import gaussian_filter
A = 256 * imread("download (1).png")
filename = "this.stl"
A = A[:, :, 2] + 1.0*A[:, :, 0]  # Compose RGBA channels to give depth
A = gaussian_filter(A, 1)  # smoothing
p = numpy2stl(A, "examples/NASA.stl", scale=0.05, mask_val=5., solid=True)
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
