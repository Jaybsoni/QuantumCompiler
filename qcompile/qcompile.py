# Main file for Quantum Compiler
from qiskit import *
import numpy as np

# All of the qiskit gate types
Id = qiskit.circuit.library.standard_gates.i.IGate
H = qiskit.circuit.library.standard_gates.h.HGate
X = qiskit.circuit.library.standard_gates.x.XGate
Y = qiskit.circuit.library.standard_gates.y.YGate
Z = qiskit.circuit.library.standard_gates.z.ZGate
Rx = qiskit.circuit.library.standard_gates.rx.RXGate
Ry = qiskit.circuit.library.standard_gates.ry.RYGate
Rz = qiskit.circuit.library.standard_gates.rz.RZGate
Cx = qiskit.circuit.library.standard_gates.x.CXGate
Cz = qiskit.circuit.library.standard_gates.z.CZGate

list_of_gates = [Id, H, X, Y, Z, Rx, Ry, Rz, Cx, Cz]  # storing the gate types in list


def read_circ(circ):
    """ Takes a qiskit circuit and creates an array of tuples (gate_array) """
    num_qbits = circ.num_qbits
    





def main():
    circ = qiskit.QuantumCircuit(3)
    circ.i(0)
    circ.h(0)
    circ.x(0)
    circ.y(0)
    circ.z(0)
    circ.rx(np.pi/2, 0)
    circ.ry(np.pi/2, 0)
    circ.rz(np.pi/2, 0)
    circ.cx(0, 2)
    circ.cz(0, 2)

    circ.draw()
    plt.show()

    meta = circ.data
    for i in meta:
        print(i)
        print(i[0].params)

    # z = qiskit.circuit.library.standard_gates.h.HGate
    # print(z)

    return


if __name__ == '__main__':
    main()
