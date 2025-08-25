import numpy as np
import matplotlib.pyplot as plt

from multiprocessing import Process, Queue
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



def _preprocessing_worker(project_folder, patch_size, patches_per_image, save_file, queue):
    """Travailleur lancé dans un autre processus."""
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
    print("Patches created")

    queue.put({
        "status": "done",
        "shape": (X.shape, Y.shape),
        "axes": XY_axes,
        "preview_X": X[:8],
        "preview_Y": Y[:8],
    })


def launch_preprocessing_process(project_folder, patch_size, patches_per_image, save_file, callback=None, root=None):
    """Lance preprocessing dans un Process pour éviter le GIL."""
    from multiprocessing import Queue
    queue = Queue()

    worker = Process(
        target=_preprocessing_worker,
        args=(project_folder, patch_size, patches_per_image, save_file, queue),
        daemon=True
    )
    worker.start()

    # Check queue periodically
    def check_queue():
        if not queue.empty():
            result = queue.get()
            if callback:
                callback(result)
        else:
            if root is not None:
                root.after(100, check_queue)  # check again after 100 ms

    if root is not None:
        root.after(100, check_queue)