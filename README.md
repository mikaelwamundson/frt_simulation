# Project Description
This is a tool for making simulations of the fault ride thru capability (FRT), which is presented in milliseconds, of a synchronous machine connected to a power system.

Each evaluation of the fault ride thru capability consists of several simulations where the fault duration is increased until the machine looses synchronism with the power system.

The fault ride thru capability depends on several characteristics of the machine and power system, i.e. the inertia of the machine, reactances of the machine and step-up transformer, degree of excitation, voltage level in the power system, etc.

The idea is to study the effect on frt capability when moving in the U-Q window, i.e the operating point of the synchronous machine with respect to voltage and reactive power. At each different operating point perform a set of time domain simulations to evaluate the frt capability. The result will be presented as "iso curves" (curves corresponding to the same frt capability, in a U-Q plot.

The time to build ut the U-Q plot should be optimised.

## Model description
The simulation model is a FMU (Functional Mock-Up) model exported from OpenModelica. The Python package FmPy is used to parametrise and run simulations on the model in Python.

Results are saved as variables that can be cast to numpy arrays for further analysis.

## Dependiencies
The project is dependent on the following packages
- FmPy
- Numpy
- Matplotlib
- Pandas
