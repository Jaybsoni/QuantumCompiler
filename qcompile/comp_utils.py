# Main file for Quantum Compiler Utility Functions
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
S = qiskit.circuit.library.standard_gates.swap.SwapGate

list_of_gates = [Id, H, X, Y, Z, Rx, Ry, Rz, Cx, Cz, S]  # storing the gate types in list
gate_str_dict = {0: 'I', 1: 'H', 2: 'X', 3: 'Y', 4: 'Z', 5: 'Rx', 6: 'Ry', 7: 'Rz', 8: 'Cx', 9: 'Cz', 10: 'S'}
gate_func_dict = {'I': qiskit.QuantumCircuit.id,  # A dict relating the gate (str) to its qiskit func call
                  'H': qiskit.QuantumCircuit.h,   # I use this to create the final (compiled) qiskit circuit object
                  'X': qiskit.QuantumCircuit.x,
                  'Y': qiskit.QuantumCircuit.y,
                  'Z': qiskit.QuantumCircuit.z,
                  'Rx': qiskit.QuantumCircuit.rx,
                  'Ry': qiskit.QuantumCircuit.ry,
                  'Rz': qiskit.QuantumCircuit.rz,
                  'Cx': qiskit.QuantumCircuit.cx,
                  'Cz': qiskit.QuantumCircuit.cz,
                  'S': qiskit.QuantumCircuit.swap}

# Functions ------------------------------------------------------------------------------------------------


def read_circ(circ):
    """
    Takes a qiskit circuit and creates list of tuples (gate_lst),
    returns the gate_lst along with the num of qbits.
    This list will be used to re-construct the circuit afterwards.

    :param circ: Qiskit QuantumCircuit object
    :return: gate_lst, num_qbits: a list of tuples and an int
    """

    gate_lst = []
    num_qbits = circ.num_qubits

    meta_data = circ.data              # read circuit meta data
    for element in meta_data:
        gate_type = type(element[0])                                 # read the gate type
        gate_str = gate_str_dict[list_of_gates.index(gate_type)]     # determine the gate_str from its type
        qbit_lst = [qbit.index for qbit in element[1]]               # list of the qbit indicies that the gate acts on
        parameter_lst = element[0].params                            # list of parameters used by the gate

        gate_lst.append((gate_str, qbit_lst, parameter_lst))    # store these directly into tuple
        # store all such tuples in a list (in order)
    return gate_lst, num_qbits


def write_circ(gate_lst, num_qbits):
    """
    Takes a gate_lst and num_qbits to create a qiskit quantum circuit object.
    We assume that the circuit has the same number of qbits and bits, and we measure
    each qbit to its associated bit at the end of the circuit for simplicity

    :param gate_lst: list of tuples, containing the meta_data of the circuit
    :param num_qbits: int, number of qbits in circuit
    :return: circ: Qiskit QuantumCircuit object
    """

    circ = qiskit.QuantumCircuit(num_qbits)  # construct an empty circuit with specified number of qbits
    for gate in gate_lst:                    # iterate over list of gate information
        gate_str = gate[0]
        qbits = gate[1]

        if gate_str in ['Cx', 'Cz', 'S']:                         # apply Cx, Cz, or S gates
            gate_func_dict[gate_str](circ, qbits[0], qbits[1])

        elif gate_str in ['Rx', 'Ry', 'Rz']:                      # apply Rx, Ry or Rz gates with parameter
            parameter = gate[2][0]
            gate_func_dict[gate_str](circ, parameter, qbits)

        else:                                                     # apply single qbit non parameterized gates
            gate_func_dict[gate_str](circ, qbits)

    return circ                   # return final circuit


# a means to augment the gates in the circuit
def general_replace(gate_lst, gate_name, replacement_gates):
    """
    searches through gate_lst for all instances of 'gate_name' gate and
    replaces them with the set of gates stored in replacement_gates which is
    a list of gate tuples.

    A gate tuple will contain ('new_gate_str', [new_qbits] or func, [params] or func)
    where 'new_gate_str' is the name of the new gate, [new_qbits] is a list of qbits
    the new gate will act on. Note if this is empty, then it acts on the same qbits
    as the old gate. if a func is provided, then it applies that func to the
    old list of qbits to determine the new list of qbits. Finally, [params] is
    a list of new parameters or a function which will be applied to the old parameters
    in order to determine the new parameters

    :param gate_lst: a list containing tuples eg. ('gate_str', [qbits], [params])
    :param gate_name: a str, represents the quantum gate being applied
    :param replacement_gates: a list of tuples, ('new_gate_str', [new_qbits] or func, [params] or func)
    :return: None
    """

    for index, gate in enumerate(gate_lst):  # iterate through the gate list
        gate_str = gate[0]

        if gate_str == gate_name:            # find and delete the gate tuple with name 'gate_name'
            qbits = gate[1]
            parms = gate[2]
            del gate_lst[index]

            for i, new_gate_tuple in enumerate(replacement_gates):  # replace it with the set of gates provided
                replacement_gate_name = new_gate_tuple[0]
                replacement_qbits = new_gate_tuple[1]
                replacement_params = new_gate_tuple[2]

                if type(replacement_qbits) != list:  # in some cases we may want the replacement_qbits to be a
                    # function of the current params, in this case replacement_params is not a list, but a function
                    replacement_qbits = [replacement_qbits(qbits)]

                elif not replacement_qbits:        # if no replacement qbit indicies have been specified,
                    replacement_qbits = qbits      # just apply the replacement gate on the same qbits as the old gate

                if type(replacement_params) != list:  # in some cases we may want the replacement_params to be a
                    # function of the current params, in this case replacement_params is not a list, but a function
                    replacement_params = [replacement_params(parms)]

                new_gate = (replacement_gate_name, replacement_qbits, replacement_params)
                gate_lst.insert(index + i, new_gate)

    return


def random_circ_generator(num_qbits=0, num_gates=0):
    """
    Generate a random qiskit circuit made up of the given 'simple'
    gates. One can specify the num of qbits and num of gates in the circuit.
    If unspecified, they will be randomly determined

    :param num_qbits: int, optional number of qbits in circuit
    :param num_gates: int, optional number of gates
    :return: qiskit QuantumCircuit object
    """

    if num_qbits == 0:
        num_qbits = random.randint(1, 5)  # randomly pick # of qbits 1 - 5

    if num_gates == 0:
        num_gates = random.randint(5, 25)  # randomly pick # of gates 5 - 25

    gate_lst = []

    for i in range(num_gates):                               # iterate over the number of gates

        if num_qbits == 1:                                       # if there  is only 1 qbit then,
            gate_index = random.randint(0, 7)                    # pick a single qbit gate at random
        else:
            gate_index = random.randint(0, 9)                    # pick any gate at random

        gate_str = gate_str_dict[gate_index]
        control_index = random.randint(0, num_qbits - 1)         # pick a qbit to apply gate too

        parameter = []
        qbits = [control_index]

        if gate_str in ['Cx', 'Cz']:                           # if the gate is a ControlX or ControlZ
            target_index = random.randint(0, num_qbits - 1)        # pick target qbit

            if target_index == control_index:                 # make sure its not the same as the control qbit
                if control_index == num_qbits - 1:
                    target_index = control_index - 1
                else:
                    target_index = control_index + 1

            qbits.append(target_index)

        elif gate_str in ['Rx', 'Ry']:                        # if the gate has a theta parameter
            parameter.append(random.random() * (2 * np.pi))   # randomly select parameter

        elif gate_str == 'Rz':                                # if the gate has a phi parameter
            parameter.append(random.random() * np.pi)         # randomly select parameter

        gate_lst.append((gate_str, qbits, parameter))   # add the meta_data to the gate_lst

    circ = write_circ(gate_lst, num_qbits)      # construct qiskit circuit
    return circ


def circ_equal(circ1, circ2):
    """
    Checks if two circuits generate the same statevector.
    If they are different it prints them.

    :param circ1: Qiskit QuantumCircuit object
    :param circ2: Qiskit QuantumCircuit object
    :return: Bool, True if the state vectors are equal
    """

    backend = Aer.get_backend('statevector_simulator')   # get simulator
    job1 = execute(circ1, backend)
    job2 = execute(circ2, backend)
    result1 = job1.result()
    result2 = job2.result()

    circ1_statevect = result1.get_statevector(circ1)
    mag_circ1_statevect = np.sqrt(circ1_statevect * np.conj(circ1_statevect))
    circ2_statevect = result2.get_statevector(circ2)
    mag_circ2_statevect = np.sqrt(circ2_statevect * np.conj(circ2_statevect))

    equal = np.isclose(mag_circ1_statevect, mag_circ2_statevect)  # check if entries are within tolerance of each other

    if not equal.all():
        print(np.round(circ1_statevect, decimals=3))
        print(np.round(mag_circ1_statevect, decimals=3))
        print(np.round(circ2_statevect, decimals=3))
        print(np.round(mag_circ2_statevect, decimals=3))

    return equal


def get_first(lst):
    return lst[0]  # kinda self explanatory


def get_second(lst):
    return lst[1]  # equally self explanatory


def main():
    return


if __name__ == '__main__':
    main()
