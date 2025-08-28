"""
Our pipeline is:
    - dimension: temporal (time = batch if artefacts)
    - Fixed pattern suppression
    - Variance stabilization
    - Noise2Self-CB: +spatial features +balance training data
"""

import numpy as np
import time as time
import tifffile as tiff
import matplotlib.pyplot as plt

from aydin.it.fgr import ImageTranslatorFGR
from aydin.restoration.denoise.noise2selffgr import Noise2SelfFGR
from aydin.it.transforms.range import RangeTransform
from aydin.it.transforms.padding import PaddingTransform
from aydin.it.transforms.fixedpattern import FixedPatternTransform
from aydin.it.transforms.variance_stabilisation import VarianceStabilisationTransform
from aydin.features.standard_features import StandardFeatureGenerator


# Basic Noise2Self using the “Feature Generation & Regression” approach-based restoration
# noisy_image = tiff.imread("C:/Git/palmdenoiser_data/lowSNR.tif")
# print("Image shape:", noisy_image.shape)
# debut = time.time()
# n2s = Noise2SelfFGR()
# n2s.train(noisy_image)
# denoised_image = n2s.denoise(noisy_image)
# end = time.time()
# print(f"Restoration took {(end-debut)/60} minutes")

# plt.imshow(denoised_image[0], cmap="gray")
# plt.show()
# tiff.imwrite("C:/Git/palm-denoisers/local/n2s/highSNR_denoised_n2s.tif", denoised_image.astype("float16"))


# Advanced Noise2Self with preprocessing and CatBoost network
noisy_image = tiff.imread("C:/Git/palmdenoiser_data/lowSNR.tif")
print("Image shape:", noisy_image.shape)

transforms = transforms = [{"class": VarianceStabilisationTransform, "kwargs": {"do_postprocess": True, "mode":"anscomb"}},
                           {"class": FixedPatternTransform, "kwargs": {"percentile":1.0, "sigma":0.5}}, # maybe not
                           {"class": RangeTransform, "kwargs": {"do_postprocess": True, "mode":"minmax", "percentile":None, "leave_as_float":False, "clip":True}},
                           {"class": PaddingTransform, "kwargs": {"pad_width":3, "min_length_to_pad":8, "mode":"reflect"}}]

debut = time.time()
n2s = Noise2SelfFGR(variant="cb", 
                    it_transforms=transforms, 
                    lower_level_args={"feature_generator": {"class": StandardFeatureGenerator, "kwargs": {"include_spatial_features": True}},
                                      "it": {"class": ImageTranslatorFGR, "kwargs": {"balance_training_data": True}}})

n2s.train(noisy_image)
denoised_image = n2s.denoise(noisy_image)

end = time.time()
print(f"Restoration took {(end-debut)/60} minutes")

plt.imshow(denoised_image[400], cmap="gray")
plt.show()
tiff.imwrite("C:/Git/palm-denoisers/local/n2s/highSNR_denoised_n2s.tif", np.array(denoised_image, dtype="uint16"))