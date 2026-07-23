import imageio.v3 as iio
import numpy as np



robust_gif_files = []
compare_gif_files = []
for i in range(10):
    robust_gif_files.append(iio.imread('robust' + str(i+1) + '.gif'))
    robust_gif_files[i] = robust_gif_files[i][:, :, 175:225]
    compare_gif_files.append(iio.imread('compare' + str(i+1) + '.gif'))
    compare_gif_files[i] = compare_gif_files[i][:, :, 175:225]

robust_merged = np.concatenate([f for f in robust_gif_files], axis=2)
compare_merged = np.concatenate([f for f in compare_gif_files], axis=2)
merged = np.concatenate([robust_merged, compare_merged], axis=1)

iio.imwrite(
    "concate.gif",
    merged,
)
