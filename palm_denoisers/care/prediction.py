import numpy as np
import matplotlib.pyplot as plt

from tifffile import imread
from csbdeep.utils import plot_some, normalize
from csbdeep.models import CARE


y = imread('simulation_data/HD/0.5/Training10000.tif')
x = imread('simulation_data/HD/0.5/Training10000.tif')
axes = 'YX'
print('image size =', x.shape)
print('image axes =', axes)

plt.figure(figsize=(13,5))
plt.subplot(1,2,1)
plt.imshow(x, cmap="magma")
plt.colorbar()
plt.title("low")
plt.subplot(1,2,2)
plt.imshow(y, cmap="magma")
plt.colorbar()
plt.title("high")
plt.show()

model = CARE(config=None, name='my_model_spt', basedir='models')
restored = model.predict(x, axes)

plt.figure(figsize=(15,10))
plot_some(np.stack([x,restored,y]),
          title_list=[['low','CARE','GT']], 
          pmin=2,pmax=99.8)

plt.figure(figsize=(10,5))
for _x,_name in zip((x,restored,y),('low','CARE','GT')):
    plt.plot(normalize(_x,1,99.7)[44], label = _name, lw = 2)

plt.legend()
plt.show()