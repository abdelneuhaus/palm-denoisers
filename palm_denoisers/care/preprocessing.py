import sys
import numpy as np
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


def preprocessing_worker(project_folder, patch_size, patches_per_image, save_file):
    """Fonction de preprocessing simple (sans Queue)."""
    print("Raw Data loading...")
    raw_data = RawData.from_folder(
        basepath=project_folder,
        source_dirs=['Low'],
        target_dir='High',
        axes='YX'
    )
    print("Raw Data loaded. Creating patches...")
    X, Y, XY_axes = create_patches(
        raw_data=raw_data,
        patch_size=(patch_size, patch_size),
        patch_filter=no_background_patches(0),
        n_patches_per_image=patches_per_image,
        save_file=save_file
    )
    print("Patches created.")

    return {
        "shape": (X.shape, Y.shape),
        "axes": XY_axes,
        "preview_X": X[:8],
        "preview_Y": Y[:8],
    }


if __name__ == "__main__":
    project_folder = sys.argv[1]
    patch_size = int(sys.argv[2])
    patches_per_image = int(sys.argv[3])
    save_file = sys.argv[4]

    result = preprocessing_worker(project_folder, patch_size, patches_per_image, save_file)
    print("Preprocessing finished.")
    print("Patch shapes:", result["shape"])
