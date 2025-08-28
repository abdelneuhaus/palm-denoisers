import numpy as np
import tifffile as tiff
import time, os
from concurrent.futures import ProcessPoolExecutor

# ---------------------------------------------------------------------
# >>> PARAMÈTRES À ADAPTER <<< ----------------------------------------
IMAGE_PATH  = "250521_dualview/2506_CARE_final_dataset/SPT/Cell01_high.tif"
COEFF_PATH  = "250521_dualview/2506_CARE_final_dataset/SPT/DualView.PT/DualView_2CFit.txt"
OUTPUT_PATH = "250521_dualview/2506_CARE_final_dataset/SPT/TEST.tif"
UP_FACTOR   = 1             # taille du bloc (ex. 10×10)
N_WORKERS   = os.cpu_count() or 1
# ---------------------------------------------------------------------

# ------------------ Fonctions utilitaires ----------------------------
def read_coefficients(path: str):
    with open(path, "r") as f:
        lines = f.readlines()
    if len(lines) < 3:
        raise ValueError("Fichier de coefficients mal formé.")
    return (list(map(float, lines[1].split())),
            list(map(float, lines[2].split())))

def calc_new_xy(x, y, cfx, cfy):
    x2, y2 = x*x, y*y
    x3, y3 = x2*x, y2*y
    new_x = (cfx[0]*x3 + cfx[1]*y3 + cfx[2]*x2*y + cfx[3]*x*y2 +
             cfx[4]*x2 + cfx[5]*y2 + cfx[6]*x*y + cfx[7]*x +
             cfx[8]*y + cfx[9])
    new_y = (cfy[0]*x3 + cfy[1]*y3 + cfy[2]*x2*y + cfy[3]*x*y2 +
             cfy[4]*x2 + cfy[5]*y2 + cfy[6]*x*y + cfy[7]*x +
             cfy[8]*y + cfy[9])
    return new_x, new_y

# -------------- Duplication sur blocs --------------------------------
def shift_on_blocks(img, cfx, cfy, up):
    h, w = img.shape
    H, W = h*up, w*up
    out  = np.zeros((H, W), dtype=np.float64)

    for y in range(h):
        for x in range(w):
            val = img[y, x]
            if val == 0:
                continue

            nx, ny = calc_new_xy(x, y, cfx, cfy)
            ix, iy = int(round(nx)), int(round(ny))

            if 0 <= ix < w and 0 <= iy < h:
                bx, by = ix*up, iy*up
                out[by:by+up, bx:bx+up] += val
    return out

# --------- Remplissage des zéros sur le stack final ------------------
def fill_zeros_with_neighbor_mean(frame):
    """Remplace les pixels ==0 par la moyenne des voisins non nuls."""
    zeros = frame == 0
    if not zeros.any():
        return frame

    # somme des 8 voisins et nombre de voisins non nuls
    padded = np.pad(frame, 1, mode="constant", constant_values=0)
    sum_nb   = np.zeros_like(frame, dtype=np.float64)
    count_nb = np.zeros_like(frame, dtype=np.int32)

    # Itère sur les 8 décalages
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            if dx == 0 and dy == 0:
                continue
            patch = padded[1+dy:1+dy+frame.shape[0],
                           1+dx:1+dx+frame.shape[1]]
            mask  = patch != 0
            sum_nb   += patch
            count_nb += mask

    # Moyenne calculée là où count>0
    mean_nb = np.zeros_like(frame, dtype=np.float64)
    valid   = count_nb > 0
    mean_nb[valid] = sum_nb[valid] / count_nb[valid]

    filled = frame.copy()
    filled[zeros & valid] = mean_nb[zeros & valid]
    # les positions où count==0 restent 0
    return filled

# ---------- Fonction appelée en parallèle ----------------------------
def _process_one(args):
    idx, frame, cx, cy, up = args
    return idx, shift_on_blocks(frame, cx, cy, up)

# ----------------------- Programme principal -------------------------
def main():
    img_stack        = tiff.imread(IMAGE_PATH)  # ex. 100 premières
    coeff_x, coeff_y = read_coefficients(COEFF_PATH)
    up, workers      = UP_FACTOR, N_WORKERS

    print(f"{len(img_stack)} images, blocs {up}×{up}, {workers} cœurs")
    t0 = time.time()

    # 1) décalage + duplication
    with ProcessPoolExecutor(max_workers=workers) as pool:
        results = pool.map(
            _process_one,
            ((i, frame, coeff_x, coeff_y, up)
             for i, frame in enumerate(img_stack)),
            chunksize=1
        )

        H, W = img_stack.shape[1]*up, img_stack.shape[2]*up
        shifted_stack = np.zeros((len(img_stack), H, W), dtype=np.float64)
        for idx, shifted in results:
            shifted_stack[idx] = shifted

    # 2) remplissage des zéros (post-processing)
    for k in range(len(shifted_stack)):
        shifted_stack[k] = fill_zeros_with_neighbor_mean(shifted_stack[k])

    # 3) enregistrement
    tiff.imwrite(OUTPUT_PATH, shifted_stack.astype(np.uint16))
    print(f"✅ Terminé en {time.time()-t0:.1f} s")

# ---------------------------------------------------------------------
if __name__ == "__main__":
    main()