from pylab import imread
from stl_tools import numpy2stl

from scipy.misc import lena, imresize
from scipy.ndimage import gaussian_filter

A = 256 * imread("screenshot.png")
A = A[:, :, 2] + 1.0*A[:, :, 0]  # Compose RGBA channels to give depth
A = gaussian_filter(A, 1)  # smoothing
numpy2stl(A, "NASA.stl", scale=0.05, mask_val=5., solid=True)
