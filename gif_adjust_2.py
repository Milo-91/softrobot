import imageio.v3 as iio
import numpy as np



gif_file = iio.imread('animation.gif')
gif_file = gif_file[:, :, 175:225]

iio.imwrite(
    "cutted.gif",
    gif_file,
)
