import numpy as np
import matplotlib.pyplot as plt

from tifffile import imread
from csbdeep.utils import axes_dict, plot_some, plot_history
from csbdeep.utils.tf import limit_gpu_memory
from csbdeep.io import load_training_data
from csbdeep.models import Config, CARE


data_pathway = 'care_data.npz'
(X,Y), (X_val,Y_val), axes = load_training_data(data_pathway, validation_split=0.1, verbose=True)
c = axes_dict(axes)['C']
n_channel_in, n_channel_out = X.shape[c], Y.shape[c]

def show_some_data(X_val, Y_val):    
    plt.figure(figsize=(12,5))
    plot_some(X_val[:5],Y_val[:5])
    plt.suptitle('Example validation patches (top: source, bottom: target)')
    plt.show()

# show_some_data(X_val, Y_val)

config = Config(axes, 
                n_channel_in, 
                n_channel_out, 
                unet_kern_size=3, 
                train_batch_size=32, 
                train_steps_per_epoch=60, 
                train_epochs=50, 
                unet_n_depth=4, 
                train_learning_rate=0.0004)

print(config)
vars(config)
model = CARE(config, 'test_local', basedir='models')
model.keras_model.summary()

history = model.train(X,Y, validation_data=(X_val,Y_val))

print(sorted(list(history.history.keys())))
plt.figure(figsize=(16, 5))
plot_history(history, ['loss', 'val_loss'], ['mse', 'val_mse', 'mae', 'val_mae'])

plt.figure(figsize=(20,12))
_P = model.keras_model.predict(X_val[:5])
if config.probabilistic:
    _P = _P[...,:(_P.shape[-1]//2)]
plot_some(X_val[:5],Y_val[:5],_P,pmax=99.5)
plt.suptitle('5 example validation patches\n'      
             'top row: input (source), '          
             'middle row: target (ground truth), '
             'bottom row: predicted from source')
plt.show()