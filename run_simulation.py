# -*- coding: utf-8 -*-
"""
@author: mikael
"""

import numpy as np
from fmpy import read_model_description, simulate_fmu
#from fmpy.util import plot_result  # import the plot function
import matplotlib.pyplot as plt

def simulate(fmu, U, P, Q, fault_time):

    fmu = fmu
    
    md = read_model_description(fmu)
    
    t_start = 0.0 # simulation start time
    t_stop = 20.0 # simulation stop time
    dt = 0.001 # simulation step size
    t1 = 10.0 # fault start time
    t2 = t1 + fault_time*1e-3 # fault stop time
    ref_time = t1 - 1.0 # the reference time for evaluating true U, P and Q
    ref_idx = int(ref_time / dt)
    
    start_values = {'infiniteBus.v_0': U,
                    'plant.governor.SimpleLag1.K': 20.0,
                    'plant.governor.T_w': 1.0,
                    'plant.machine.P_0': P * 1e6,
                    'plant.machine.Q_0': Q * 1e6,
                    'pwFault.t1': t1,
                    'pwFault.t2': t2,
                    'plant.machine.H': 3.0,
                    'plant.machine.S10': 0.05,
                    'plant.machine.S12': 0.55,
                    'plant.exciter.E_MAX': 8,
                    'plant.exciter.E_MIN': -8}
    
    states = [v.name for v in md.modelVariables if v.variability == 'continuous' and v.causality == 'local']
    
    result = simulate_fmu(fmu,
                          start_time = t_start,
                          stop_time = t_stop,
                          output_interval = dt,
                          start_values = start_values,
                          output = states)              # simulate the FMU
    
    
    t = result['time']
    P_sim = result['plant.P'] * 1e-6
    Q_sim = result['plant.Q'] * 1e-6
    phi_sim = np.rad2deg(result['plant.machine.ANGLE'])
    U_sim = result['bus.v']
    out_of_step = np.max(phi_sim) > 180.0
    
    '''
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(t, U_sim)
    ax.set_xlim(0, 20)
    ax.grid()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(t, P_sim)
    ax.plot(t, Q_sim)
    ax.set_xlim(0, 20)
    ax.grid()
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(t, phi_sim, label='Fault duration: {:.0f} ms'.format(fault_time))
    ax.set_xlim(0, 20)
    ax.set_ylim(-25, 200)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Rotor angle [deg]')
    ax.legend()
    ax.grid()
    '''
    
    return U_sim[ref_idx], P_sim[ref_idx], Q_sim[ref_idx], out_of_step

def plot(fmu, U, P, Q, fault_1, fault_2):
    
    fmu = fmu
    
    md = read_model_description(fmu)
    
    t_start = 0.0 # simulation start time
    t_stop = 20.0 # simulation stop time
    dt = 0.001 # simulation step size
    t1 = 10.0 # fault start time
    t2 = t1 + fault_1*1e-3 # fault stop time
    
    start_values = {'infiniteBus.v_0': U,
                    'plant.governor.SimpleLag1.K': 20.0,
                    'plant.governor.T_w': 1.0,
                    'plant.machine.P_0': P * 1e6,
                    'plant.machine.Q_0': Q * 1e6,
                    'pwFault.t1': t1,
                    'pwFault.t2': t2,
                    'plant.machine.H': 3.0,
                    'plant.machine.S10': 0.05,
                    'plant.machine.S12': 0.55,
                    'plant.exciter.E_MAX': 8,
                    'plant.exciter.E_MIN': -8}
    
    states = [v.name for v in md.modelVariables if v.variability == 'continuous' and v.causality == 'local']
    
    result_1 = simulate_fmu(fmu,
                          start_time = t_start,
                          stop_time = t_stop,
                          output_interval = dt,
                          start_values = start_values,
                          output = states)              # simulate the FMU
    
    
    t_1 = result_1['time']
    phi_sim_1 = np.rad2deg(result_1['plant.machine.ANGLE'])
    
    t2 = t1 + fault_2*1e-3 # fault stop time
    start_values = {'infiniteBus.v_0': U,
                    'plant.governor.SimpleLag1.K': 20.0,
                    'plant.governor.T_w': 1.0,
                    'plant.machine.P_0': P * 1e6,
                    'plant.machine.Q_0': Q * 1e6,
                    'pwFault.t1': t1,
                    'pwFault.t2': t2,
                    'plant.machine.H': 3.0,
                    'plant.machine.S10': 0.05,
                    'plant.machine.S12': 0.55,
                    'plant.exciter.E_MAX': 8,
                    'plant.exciter.E_MIN': -8}
    
    result_2 = simulate_fmu(fmu,
                          start_time = t_start,
                          stop_time = t_stop,
                          output_interval = dt,
                          start_values = start_values,
                          output = states)              # simulate the FMU
    
    t_2 = result_2['time']
    phi_sim_2 = np.rad2deg(result_2['plant.machine.ANGLE'])
    
    fig, ax = plt.subplots(figsize=(12, 8))
    ax.plot(t_1, phi_sim_1, label='Fault duration: {:.0f} ms'.format(fault_1))
    ax.plot(t_2, phi_sim_2, label='Fault duration: {:.0f} ms'.format(fault_2))
    ax.set_xlim(0, 20)
    ax.set_ylim(-25, 200)
    ax.set_xlabel('Time [s]')
    ax.set_ylabel('Rotor angle [deg]')
    ax.legend()
    ax.grid()
    
    return

def find_cct(fmu, U, P, Q, low, high, min_step):
    high = high - ((high - low) % min_step)
    
    U_real, P_real, Q_real, oos = simulate(fmu, U, P, Q, low)

    if oos:
        raise ValueError("Out of step at interval start")
        
    U_real, P_real, Q_real, oos = simulate(fmu, U, P, Q, high)
    if not oos:
        raise ValueError("Does not fall out of step in interval")

    while high - low > min_step:
        mid = low + ((high - low) // (2 * min_step)) * min_step

        U_real, P_real, Q_real, oos = simulate(fmu, U, P, Q, mid)
        if oos:
            high = mid
        else:
            low = mid

    return U_real, P_real, Q_real, low
