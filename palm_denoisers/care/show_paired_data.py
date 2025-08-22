import matplotlib.pyplot as plt
from tifffile import imread

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