import numpy as np
import matplotlib.pyplot as plt

from tifffile import imread
from csbdeep.utils import plot_some
from csbdeep.data import RawData, create_patches, no_background_patches


def show_paired_data(training_path, test_path):
    y = imread(training_path)
    x = imread(test_path)
    print('image size =', x.shape)

    plt.figure(figsize=(13,5))
    plt.subplot(1,2,1)
    plt.imshow(x, cmap  ="magma")
    plt.colorbar()
    plt.title("low")
    plt.subplot(1,2,2)
    plt.imshow(y, cmap  ="magma")
    plt.colorbar()
    plt.title("high")
    plt.show()


def do_data_processing():
    raw_data = RawData.from_folder(basepath='C:/Git/palmdenoiser_data/data/Training', 
                                source_dirs=['Low'], 
                                target_dir='High', 
                                axes='YX')

    X, Y, XY_axes = create_patches(raw_data=raw_data, 
                                patch_size=(64,64), 
                                patch_filter=no_background_patches(0),
                                n_patches_per_image = 1, 
                                save_file= 'care_data.npz')
    assert X.shape == Y.shape

    print("shape of X,Y =", X.shape)
    print("axes  of X,Y =", XY_axes)
    for i in range(1):
        plt.figure(figsize=(16,4))
        sl = slice(8*i, 8*(i+1)), 0
        plot_some(X[sl], Y[sl], title_list=[np.arange(sl[0].start,sl[0].stop)])
        plt.show()


if __name__ == "__main__":
    do_data_processing()