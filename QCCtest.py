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

# Give us your intro (Needed for Evaluations)
### your code here ###
NAME = ""
ROLLNO = ""
### ### ### ###


if __name__ == "__main__":
    print(NAME, ROLLNO)
    print(qiskit.__version__)
    print(np.__version__)