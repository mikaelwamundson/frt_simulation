#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 10:08:12 2026

@author: mikael
"""

import numpy as np
import run_simulation
import matplotlib.pyplot as plt
from scipy.interpolate import griddata


U_array = np.arange(0.8, 1.21, 0.05)
Q_array = np.arange(-20, 20.1, 5)
P = 25.0

U_real = np.zeros(shape=(len(U_array), len(Q_array)))
P_real = np.zeros(shape=(len(U_array), len(Q_array)))
Q_real = np.zeros(shape=(len(U_array), len(Q_array)))
cct = np.zeros(shape=(len(U_array), len(Q_array)))

min_step = 2

i = 0
for U in U_array:
    j = 0
    for Q in Q_array:
        if (j==0) and (i==0): # no calculations have been done. maximum interval
            U_real[i, j], P_real[i, j], Q_real[i, j], cct[i, j] =  run_simulation.find_cct('test.fmu',
                                                                                           U,
                                                                                           P,
                                                                                           Q,
                                                                                           100,
                                                                                           400,
                                                                                           min_step)
        elif (j==0) and (i!=0): # we are not on the first row but first column. use cct from previous row
            U_real[i, j], P_real[i, j], Q_real[i, j], cct[i, j] =  run_simulation.find_cct('test.fmu',
                                                                                       U,
                                                                                       P,
                                                                                       Q,
                                                                                       cct[i-1, j]-30,
                                                                                       cct[i-1, j]+30,
                                                                                       min_step)
        else: # we are not on first row or column. use cct from previous column
            U_real[i, j], P_real[i, j], Q_real[i, j], cct[i, j] =  run_simulation.find_cct('test.fmu',
                                                                                       U,
                                                                                       P,
                                                                                       Q,
                                                                                       cct[i, j-1]-30,
                                                                                       cct[i, j-1]+30,
                                                                                       min_step)
        j += 1
    i += 1
    
U_matrix, Q_matrix = np.meshgrid(np.linspace(np.min(U_array), np.max(U_array), 100), np.linspace(np.min(Q_array), np.max(Q_array), 100))
cct_matrix = griddata((np.asarray(U_real).ravel(), np.asarray(Q_real).ravel()), np.asarray(cct).ravel(), (U_matrix, Q_matrix), method="linear")

fig, ax = plt.subplots(figsize=(10, 10))
cs = ax.contour(U_real, Q_real, cct, levels=20, colors='C3')
#cs = ax.contour(U_matrix, Q_matrix, cct_matrix, levels=20, colors='C3')
ax.clabel(cs)
ax.grid()
ax.set_xlim(0.8, 1.2)
ax.set_ylim(-20, 20)
ax.set_xlabel('Generator voltage [p.u.]')
ax.set_ylabel('Generator reactive power [Mvar]')
