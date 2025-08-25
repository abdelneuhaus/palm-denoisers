"""
Our pipeline is:
    - dimension: temporal (time = batch if artefacts)
    - Fixed pattern suppression
    - Variance stabilization
    - Noise2Self-CB: +spatial features +balance training data
"""
import time as time
import tifffile as tiff
import matplotlib.pyplot as plt

from aydin.restoration.denoise.noise2selffgr import Noise2SelfFGR
from aydin.it.transforms.histogram import HistogramEqualisationTransform
from aydin.it.transforms.fixedpattern import FixedPatternTransform


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
histogram_transform = HistogramEqualisationTransform()
preprocessed = histogram_transform.preprocess(noisy_image)
fixedpattern_transform = FixedPatternTransform(axes=[1, 2])
noisy_image = fixedpattern_transform.preprocess(preprocessed)
debut = time.time()
n2s = Noise2SelfFGR(variant="cb")
n2s.train(noisy_image)
denoised_image = n2s.denoise(noisy_image)
end = time.time()
print(f"Restoration took {(end-debut)/60} minutes")
postprocessed = histogram_transform.postprocess(denoised_image)

plt.imshow(denoised_image[200], cmap="gray")
plt.show()
tiff.imwrite("C:/Git/palm-denoisers/local/n2s/highSNR_denoised_n2s.tif", denoised_image.astype("float16"))