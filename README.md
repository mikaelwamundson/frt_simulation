# Project Description
This is a tool for making simulations of the fault ride thru capability (FRT) of a synchronous machine connected to a power system.

Each evaluation of the fault ride thru capability consists of several simulations where the fault duration is increased until the machine looses synchronism with the power system.

The fault ride thru capability depends on several characteristics of the machine and power system, i.e. the inertia of the machine, reactances of the machine and step-up transformer, etc.

The idea is to vary parameters, perform simulations to evaluate the frt capability and report/present the result in a suitable way.

The number of needed simulations can quickly grow, resulting in a time consuming process.

## Model description
The simulation model is a FMU (Functional Mock-Up) model exported from OpenModelica. The Python package FmPy is used to parametrise and run simulations on the model in Python.

Results are saved as variables that can be cast to numpy arrays for further analysis.
