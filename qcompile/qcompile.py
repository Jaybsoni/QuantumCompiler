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
gate_func_dict = {'I': qiskit.QuantumCircuit.id,  # A dict relating the gate (str) to its qiskit func call
                  'H': qiskit.QuantumCircuit.h,   # I use this to create the final (compiled) qiskit circuit object
                  'X': qiskit.QuantumCircuit.x,
                  'Y': qiskit.QuantumCircuit.y,
                  'Z': qiskit.QuantumCircuit.z,
                  'Rx': qiskit.QuantumCircuit.rx,
                  'Ry': qiskit.QuantumCircuit.ry,
                  'Rz': qiskit.QuantumCircuit.rz,
                  'Cx': qiskit.QuantumCircuit.cx,
                  'Cz': qiskit.QuantumCircuit.cz}


def read_circ(circ):
    """ Takes a qiskit circuit and creates an array of tuples (gate_lst),
     returns the gate_lst along with the num of qbits """

    gate_lst = []
    num_qbits = circ.num_qubits

    meta_data = circ.data
    for element in meta_data:
        gate_type = type(element[0])
        gate_str = gate_str_dict[list_of_gates.index(gate_type)]
        qbit_lst = [qbit.index for qbit in element[1]]
        parameter_lst = element[0].params

        gate_lst.append((gate_str, qbit_lst, parameter_lst))

    return gate_lst, num_qbits


def write_circ(gate_lst, num_qbits):
    """ Takes a gate_lst and num_qbits to create a qiskit quantum circuit object.
     We assume that the circuit has the same number of qbits and bits, and we measure
     each qbit to its associated bit at the end of the circuit for simplicity. """

    circ = qiskit.QuantumCircuit(num_qbits)
    for gate in gate_lst:
        gate_str = gate[0]
        qbits = gate[1]

        if gate_str in ['Cx', 'Cz']:
            gate_func_dict[gate_str](circ, qbits[0], qbits[1])

        elif gate_str in ['Rx', 'Ry', 'Rz']:
            parameter = gate[2][0]
            gate_func_dict[gate_str](circ, qbits, parameter)

        else:
            gate_func_dict[gate_str](circ, qbits)

    return circ


def general_replace(gate_lst, gate_name, replacement_gates):
    """ searches through gate_lst for all instances of 'gate_name' gate and
     replaces them with the set of gates stored in replacement_gates which is
     a list of gate tuples. """

    for index, gate in enumerate(gate_lst):
        gate_str = gate[0]

        if gate_str == gate_name:
            del gate_lst[index]

            for i, new_gate in enumerate(replacement_gates):
                gate_lst.insert(index + i, new_gate)

    return


# def specific_replace(gate_lst, rm_index_lst, replacement_gate, param_func=None):
#     gate = gate_lst[gate_index]
#     gate_str = gate[0]
#     qbits = gate[1]
#     params = gate[2][0]
#
#     if param_func is not None:
#         params = param_func(params[0])


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
    qiskit.QuantumCircuit.i(circ, 0)
    circ.h([0, 1, 2])

    for i in read_circ(circ)[0]:
        print(i)

    # mylst = [1, 2, 3, 4, 5]
    # print(mylst)
    # del mylst[1]
    # print(mylst)

    return


if __name__ == '__main__':
    main()
