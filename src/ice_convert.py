import time
from multiprocessing import Pool

import netCDF4 as nc
import numpy as np
from numpy.ma import MaskedArray
from tqdm import tqdm

h_max_8 = np.array([0, 0.1, 0.3, 0.7, 1.2, 2.5, 4, 5.5])

h_max_5 = np.array([0, 0.6, 1.3, 2.2, 3.8])

t11 = 1 / 6
t21 = 2 / 6
t31 = 1 / 2
t32 = 1 / 6
t42 = 1 - t32
t53 = 1
t54 = 3 / 16
t64 = 1 - t54

thic_range_8 = np.array([0.26255049875,
                         0.335872335397,
                         0.430928571961,
                         0.554544662295,
                         0.71581299552,
                         0.926887944603,
                         1.20407493686, 0])


def convert_5_8(thic_vect_5, conc_vect_5, time, point_x, point_y):
    h_max = thic_vect_5[4]
    if (h_max - 3.8) > 0.2:
        t65 = 0.2 / (h_max - 3.8)
    else:
        t65 = 1
    if (h_max - 3.8) > 1.5:
        t75 = 1.5 / (h_max - 3.8)
    else:
        t75 = 1 - t65
    if (h_max - 5.5) > 0:
        t85 = (h_max - 5.5) / (h_max - 3.8)
    elif (h_max - 5.2) > 0:
        t85 = 1 - t75 - t65
    else:
        t85 = 0

    transfer_mat = np.array([[t11, 0, 0, 0, 0],
                             [t21, 0, 0, 0, 0],
                             [0, t32, 0, 0, 0],
                             [0, t42, 0, 0, 0],
                             [0, 0, t53, t54, 0],
                             [0, 0, 0, t64, t65],
                             [0, 0, 0, 0, t75],
                             [0, 0, 0, 0, t85]])
    conc_vect_8 = np.matmul(transfer_mat, conc_vect_5)
    thic_vect_8 = h_max_8 + h_max * conc_vect_8
    for i in range(7):
        if thic_vect_8[i] > h_max_8[i + 1]: thic_vect_8[i] = h_max_8[i + 1]
    thic_vect_8[7] = h_max
    return conc_vect_8, thic_vect_8


def generate_vectors(dat_c, dat_t):
    vect = []
    for t in range(24):
        for x in range(406):
            for y in range(452):
                thic_vect_5 = dat_t[t, :, y, x]
                conc_vect_5 = dat_c[t, :, y, x]
                vect.append([thic_vect_5, conc_vect_5, t, x, y])
    return vect


def convert_5_8_wrapper_vect(v1):
    thic_vect_5 = v1[0]
    conc_vect_5 = v1[1]
    t1 = v1[2]
    point_x = v1[3]
    point_y = v1[4]
    conc_vect_8, thic_vect_8 = convert_5_8(thic_vect_5, conc_vect_5, time, point_x, point_y)
    return t1, point_y, point_x, conc_vect_8, thic_vect_8


def ice_with_8_categories(file_path, cpu_count=2):
    print('Pool has been created')
    ncid = nc.Dataset(file_path, 'r+')
    icethicavg_8 = np.zeros((24, 8, 452, 406))
    iceconcavg_8 = np.zeros((24, 8, 452, 406))
    ice_conc_5 = ncid['siconcat'][:, :, :, :]
    ice_thic_5 = ncid['sithicat'][:, :, :, :]

    ncid.close()
    if isinstance(ice_conc_5, MaskedArray):
        ice_conc_5 = ice_conc_5.filled(0)
        ice_thic_5 = ice_thic_5.filled(0)

    print('Starting to generate vectors')
    v = generate_vectors(ice_conc_5, ice_thic_5)
    print('Finished to generate vectors')

    out_values = []
    with Pool(processes=cpu_count) as p:

        with tqdm(total=len(v)) as progress_bar:
            for _, out in tqdm(enumerate(p.imap(convert_5_8_wrapper_vect, v))):
                out_values.append(out)
                progress_bar.update()
    print('Starting to fill ice values')
    for out in out_values:
        iceconcavg_8[out[0], :, out[1], out[2]] = out[3]
        icethicavg_8[out[0], :, out[1], out[2]] = out[4]
    print('Converting: done')

    return icethicavg_8, iceconcavg_8


if __name__ == '__main__':
    path = '../ARCTIC_1h_ice_grid_TUV_19740102-19740102.nc'
    icethicavg_8, iceconcavg_8 = ice_with_8_categories(path, cpu_count=2)
