# Main file for Quantum Compiler
from qiskit import *


def main():
    circ = qiskit.QuantumCircuit(3)
    circ.h(0)
    circ.cx(0, 2)
    circ.z(1)
    circ.draw()

    meta = circ.data
    print(meta)
    print(type(meta))

    inst = circ.to_instruction()
    print(inst)
    print(inst.decompositions)
    print(inst.definition)
    print(inst.params)

    return


if __name__ == '__main__':
    main()
