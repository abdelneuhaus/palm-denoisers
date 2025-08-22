import matplotlib.pyplot as plt
import numpy as np

from csbdeep.utils import plot_some
from csbdeep.data import RawData, create_patches, no_background_patches


def show_some_patches(X, Y, XY_axes):
    print("shape of X,Y =", X.shape)
    print("axes  of X,Y =", XY_axes)
    for i in range(1):
        plt.figure(figsize=(16,4))
        sl = slice(8*i, 8*(i+1)), 0
        plot_some(X[sl], Y[sl], title_list=[np.arange(sl[0].start,sl[0].stop)])
        plt.show()


def preprocessing(project_folder, patch_size, patches_per_image, save_file):
    raw_data = RawData.from_folder(basepath=project_folder, 
                               source_dirs=['Low'], 
                               target_dir='High', 
                               axes='YX')
    X, Y, XY_axes = create_patches(raw_data=raw_data, 
                               patch_size=(patch_size,patch_size), 
                               patch_filter=no_background_patches(0),
                               n_patches_per_image = patches_per_image, 
                               save_file=save_file)
    show_some_patches(X, Y, XY_axes)