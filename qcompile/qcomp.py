# Main file for Quantum Compiler
from . import comp_utils as utils
import numpy as np


def simple_compiler(circ):
    """
    A simple quantum compiler that produces a new quantum circuit from
    the restricted subset of available gates.

    :param circ: qiskit.QuantumCircuit object
    :return: compiled_circ: new qiskit.QuantumCircuit object
    """

    gate_lst, num_qbits = utils.read_circ(circ)

    # replace CNOT:
    replacement_gates = [('H', utils.get_second, []), ('Cz', [], []), ('H', utils.get_second, [])]
    utils.general_replace(gate_lst, 'Cx', replacement_gates)

    # replace Identity:
    replacement_gates = [('Rz', [], [0])]
    utils.general_replace(gate_lst, 'I', replacement_gates)

    # replace Hadamard:
    replacement_gates = [('Rz', [], [np.pi / 2]), ('Rx', [], [np.pi / 2]), ('Rz', [], [np.pi / 2])]
    utils.general_replace(gate_lst, 'H', replacement_gates)

    # replace X:
    replacement_gates = [('Rx', [], [np.pi])]
    utils.general_replace(gate_lst, 'X', replacement_gates)

    # replace Z:
    replacement_gates = [('Rz', [], [np.pi])]
    utils.general_replace(gate_lst, 'Z', replacement_gates)

    # replace y:
    replacement_gates = [('Rz', [], [-np.pi / 2]), ('Rx', [], [np.pi]), ('Rz', [], [np.pi / 2])]
    utils.general_replace(gate_lst, 'Y', replacement_gates)

    # replace Ry(theta):
    replacement_gates = [('Rz', [], [-np.pi / 2]), ('Rx', [], utils.get_first), ('Rz', [], [np.pi / 2])]
    utils.general_replace(gate_lst, 'Ry', replacement_gates)

    compiled_circ = utils.write_circ(gate_lst, num_qbits)

    return compiled_circ


def compiler(circ):
    """
    A quantum compiler that produces a new quantum circuit from the
    restricted subset of available gates.

    :param circ:
    :return:
    """

    gate_lst, num_qbits = utils.read_circ(circ)

    # Preprocessing (Step1):

    utils.general_replace(gate_lst, 'I', [])  # remove Identity

    length = len(gate_lst)
    for index in range(length - 1):  # iterate over the lst and remove redundant Cx, Cz gates

        if index >= (len(gate_lst) - 1):  # by removing the repetitive Cz and Cx gates
            break  # we reduce the size of the list, so we need to check this edge case

        curr_gate_str = gate_lst[index][0]
        curr_qbit_lst = gate_lst[index][1]

        if curr_gate_str in ['Cx', 'Cz']:  # Check if this gate is a Cz or Cx gate
            nxt_gate_str = gate_lst[index + 1][0]
            nxt_qbit_lst = gate_lst[index + 1][1]

            if ((nxt_gate_str == curr_gate_str) and  # check that we are applying a Cz or Cx gate twice
                    (nxt_qbit_lst == curr_qbit_lst)):  # consecutively on the same control and target qbits

                del gate_lst[index + 1]  # remove both gates
                del gate_lst[index]

    # Compile (similar to the simple compiler):

    # replace CNOT:
    replacement_gates = [('H', utils.get_second, []), ('Cz', [], []), ('H', utils.get_second, [])]
    utils.general_replace(gate_lst, 'Cx', replacement_gates)

    # replace Hadamard:
    replacement_gates = [('Rz', [], [np.pi / 2]), ('Rx', [], [np.pi / 2]), ('Rz', [], [np.pi / 2])]
    utils.general_replace(gate_lst, 'H', replacement_gates)

    # replace X:
    replacement_gates = [('Rx', [], [np.pi])]
    utils.general_replace(gate_lst, 'X', replacement_gates)

    # replace Z:
    replacement_gates = [('Rz', [], [np.pi])]
    utils.general_replace(gate_lst, 'Z', replacement_gates)

    # replace y:
    replacement_gates = [('Rz', [], [-np.pi / 2]), ('Rx', [], [np.pi]), ('Rz', [], [np.pi / 2])]
    utils.general_replace(gate_lst, 'Y', replacement_gates)

    # replace Ry(theta):
    replacement_gates = [('Rz', [], [-np.pi / 2]), ('Rx', [], utils.get_first), ('Rz', [], [np.pi / 2])]
    utils.general_replace(gate_lst, 'Ry', replacement_gates)

    # simplification (Step2):

    index = 0
    while index < len(gate_lst) - 1:
        #         print('index: {}'.format(index))
        curr_gate_str = gate_lst[index][0]
        curr_qbit_lst = gate_lst[index][1]
        curr_qbit_params = gate_lst[index][2]

        if curr_gate_str in ['Rx', 'Rz']:  # Check if this gate is a Rz or Rx gate
            i = 1  # another dummy index to look at gates ahead
            while index + i < len(gate_lst):
                #                 print('dummy: {}'.format(i))
                nxt_gate_str = gate_lst[index + i][0]
                nxt_qbit_lst = gate_lst[index + i][1]
                nxt_qbit_params = gate_lst[index + i][2]

                if ((nxt_gate_str == curr_gate_str) and  # check that we are applying a Rz or Rx gate twice
                        (nxt_qbit_lst == curr_qbit_lst)):  # consecutively on the same control and target qbits

                    del gate_lst[index + i]  # remove both gates
                    del gate_lst[index]

                    new_gate = (curr_gate_str, curr_qbit_lst, [curr_qbit_params[0] + nxt_qbit_params[0]])
                    gate_lst.insert(index, new_gate)  # add the combined gate and
                    break  # break current while loop

                elif ((nxt_gate_str != curr_gate_str) and  # if the next gate applied to the same qbit is different
                      (nxt_qbit_lst == curr_qbit_lst or  # i.e instead of another Rx gate we apply a Rz or a Cz to
                       curr_qbit_lst[0] in nxt_qbit_lst)):  # the same qbit then

                    index += 1  # move forward nothing left here to simplify
                    break

                else:  # the next gate is being applied to a different set of qbits
                    i += 1  # so we can safely check the next gate in the list

            index += 1

        else:
            index += 1

    compiled_circ = utils.write_circ(gate_lst, num_qbits)

    return compiled_circ


def get_path(topology, start, end):
    """ Takes a dict (topology) representing the geometry of the
    connections, an int (start) representing the starting index
    and an int (end) representing the ending index and returns
    a list corresponding to the shortest path from end --> start
    (assuming a ring topology) """

    path_cw = []  # initialize the clockwise traversed path
    path_ccw = []  # initialize the counter clockwise traversed path

    path_cw.append(end)
    path_ccw.append(end)  # add the first point

    current = end
    while start not in topology[current]:  # traverse clockwise while adding each intermediate qbit index
        current = topology[current][1]
        path_cw.append(current)

    path_cw.append(start)

    current = end
    while start not in topology[current]:  # traverse counter clockwise while adding each intermediate qbit index
        current = topology[current][0]
        path_ccw.append(current)

    path_ccw.append(start)

    if len(path_cw) <= len(path_ccw):  # return the shorter among the two paths
        return path_cw
    else:
        return path_ccw


def get_swaps(path):
    """Take a list (path) between an end qbit index and
    a start qbit index. Return a list of tuples (replacement_gates)
    which correspond to the set of swap gates required to swap the
    end qbit with the start qbit"""

    replacement_gates = []

    for i in range(len(path) - 1):  # iterate over the path
        swap = ('S', [path[i], path[i + 1]], [])  # swap gate between consecutive qbits along the path
        replacement_gates.append(swap)
        # at this point, we have shifted each qbit along the path
    fix_offset = replacement_gates[:-1]  # by 1, this may be a problem if we swapped the control qbit
    fix_offset.reverse()  # along the path, so we need to fix the shift before we go ahead
    replacement_gates += fix_offset  # this simply involves performing the same swaps in the reverse order
    # excluding the very final swap in the first case
    return replacement_gates


def circ_router(circ, topology):
    """ Takes a compiled circuit, and a topology to produce a
    properly routed circuit. """

    gate_lst, num_qbits = utils.read_circ(circ)

    for index, gate in enumerate(gate_lst):  # iterate through the circuit
        curr_gate_str = gate_lst[index][0]
        curr_qbit_lst = gate_lst[index][1]
        curr_parms = gate_lst[index][2]

        if curr_gate_str == 'Cz':  # check if this gate is a cz gate
            cntrl_qbit = curr_qbit_lst[0]
            trgt_qbit = curr_qbit_lst[1]

            if not trgt_qbit in topology[cntrl_qbit]:  # check if the control and target qbits are 'connected'
                new_target = topology[cntrl_qbit][1]  # if not, choose a qbit that is connected to the control
                # to be the new target qbit
                path = get_path(topology, new_target,
                                trgt_qbit)  # find the path between the new target and the old target
                first_swaps = get_swaps(path)  # the swap gates required to swap new_target w/ old target
                path.reverse()
                swap_backs = get_swaps(path)  # the swap gates required to swap them back to original

                replacement_lst = first_swaps + [(curr_gate_str, [cntrl_qbit, new_target], curr_parms)] + swap_backs

                del gate_lst[index]  # we delete the old Cz gate
                for j, replacement in enumerate(replacement_lst):  # and add the swap + cz gate + swap back gates
                    gate_lst.insert(index + j, replacement)

    compiled_circ = utils.write_circ(gate_lst, num_qbits)  #

    return compiled_circ


