# Main file for Quantum Compiler
from qiskit import *
import numpy as np

# All of the 'basic' qiskit gate types
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
gate_str_dict = {0: 'I', 1: 'H', 2: 'X', 3: 'Y', 4: 'Z', 5: 'Rx', 6: 'Ry', 7: 'Rz', 8: 'Cx', 9: 'Cz'}  # gate str label


def read_circ(circ):
    """ Takes a qiskit circuit and creates an array of tuples (gate_array),
     returns the gate_array along with the num of qbits """

    gate_array = []
    num_qbits = circ.num_qubits

    meta_data = circ.data
    for element in meta_data:
        gate_type = type(element[0])
        gate_str = gate_str_dict[list_of_gates.index(gate_type)]
        qbit_lst = [qbit.index for qbit in element[1]]
        parameter_lst = element[0].params

        gate_array.append((gate_str, qbit_lst, parameter_lst))

    return gate_array, num_qbits


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

    for i in read_circ(circ)[0]:
        print(i)

    return


if __name__ == '__main__':
    main()
