# Main file for Quantum Compiler
from qiskit import *
import numpy as np
import random

# Constants ------------------------------------------------------------------------------------------------

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

# Functions ------------------------------------------------------------------------------------------------


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


def random_circ_generator(num_qbits=0, num_gates=0):
    """ Generate a random qiskit circuit made up of the given 'simple'
     gates. One can specify the num of qbits and num of gates in the circuit. """

    if num_qbits == 0:
        num_qbits = random.randint(1, 6)

    if num_gates == 0:
        num_gates = random.randint(1, 26)

    gate_lst = []

    for i in range(num_gates):
        gate_index = random.randint(0, 10)
        gate_str = gate_str_dict[gate_index]
        control_index = random.randint(0, num_qbits + 1)

        parameter = []
        qbits = [control_index]

        if gate_str in ['Cx', 'Cz']:
            target_index = random.randint(0, num_qbits + 1)
            while target_index == control_index:
                target_index = random.randint(0, num_qbits + 1)

            qbits.append(target_index)

        elif gate_str in ['Rx', 'Ry', 'Rz']:
            parameter.append(random.random() * (2 * np.pi))

        gate_lst.append((gate_str, qbits, parameter))

    circ = write_circ(gate_lst, num_qbits)
    return circ


def circ_equal(circ1, circ2):
    """ Checks if two circuits generate the same statevector. """

    backend = Aer.get_backend('statevector_simulator')
    job1 = execute(circ1, backend)
    job2 = execute(circ2, backend)
    result1 = job1.result()
    result2 = job2.result()

    circ1_statevect = result1.get_statevector(circ1)
    circ2_statevect = result2.get_statevector(circ2)

    equal = np.isclose(circ1_statevect, circ2_statevect)

    if not equal:
        print(circ1_statevect)
        print(circ2_statevect)

    return equal


def main():
    return


if __name__ == '__main__':
    main()
