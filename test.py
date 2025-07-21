"""
File for making the virtual environment
create a virtual enviroment

Install the libraries:
pip install -r requirements.txt

install pykernel later when prompted from notebook
"""

import qiskit
import numpy as np
import matplotlib.pyplot as plt

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.visualization import plot_bloch_multivector

from qiskit.quantum_info import Operator
from qiskit.circuit.library import CCXGate

print(qiskit.__version__)
print(np.__version__)