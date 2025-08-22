import numpy as np
import threading
import matplotlib.pyplot as plt

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


# def preprocessing(project_folder, patch_size, patches_per_image, save_file):
#     print("Raw Data loading...")
#     raw_data = RawData.from_folder(basepath=project_folder, 
#                                source_dirs=['Low'], 
#                                target_dir='High', 
#                                axes='YX')
#     print("Raw Data loaded. Creating patches...")
#     X, Y, XY_axes = create_patches(raw_data=raw_data, 
#                                patch_size=(patch_size,patch_size), 
#                                patch_filter=no_background_patches(0),
#                                n_patches_per_image = patches_per_image, 
#                                save_file=save_file)
#     print("Patches created")
#     show_some_patches(X, Y, XY_axes)



def launch_preprocessing_thread(project_folder, patch_size, patches_per_image, save_file, callback=None):
    """Lance preprocessing dans un thread pour ne pas bloquer la GUI."""
    worker = threading.Thread(target=_preprocessing_worker, 
                              args=(project_folder, patch_size, patches_per_image, save_file, callback),
                              daemon=True)
    worker.start()


def _preprocessing_worker(project_folder, patch_size, patches_per_image, save_file, callback=None):
    print("Raw Data loading...")
    raw_data = RawData.from_folder(basepath=project_folder, 
                                   source_dirs=['Low'], 
                                   target_dir='High', 
                                   axes='YX')
    print("Raw Data loaded. Creating patches...")
    X, Y, XY_axes = create_patches(raw_data=raw_data, 
                                   patch_size=(patch_size, patch_size), 
                                   patch_filter=no_background_patches(0),
                                   n_patches_per_image=patches_per_image, 
                                   save_file=save_file)
    print("Patches created")
    show_some_patches(X, Y, XY_axes)
    
    if callback:
        callback()
