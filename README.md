# QuantumCompiler (qcompile)
 A quantum compiler takes an abstract quantum circuit and decomposes it into hardware specific commands. In this repo I have implemented a 'quantum compiler' which translates a quantum circuit with some of the most common single and double qbit gates into a circuit only composed of Rx, Rz and Cz gates. More specifically, the compiler takes a qiskit.QuantumCircuit object and produces a 'compiled' qiskit.QuantumCircuit object which should have the same state vector (up to a complex phase). I have also added a jupyter notebook called 'Building the Compiler.ipynb' which breaks down the process for creating a simple compiler for yourself! 
 
 ## Getting started with qcompile 
Simply clone this repository locally, open a terminal in this folder and install it using the command: pip install -e .

To begin, there are two main modules in this package: comp_utils.py and qcomp.py

## comp_utils 
Begin by: `from qcompile import comp_utils`

This module contains a bunch of utility functions which help make the process of creating your own compiler much easier. In this section I will cover some of these useful functions (the reader is encouraged to look through the file to learn more).

The read_circ function allows users to read a qiskit.QuantumCircuit object and extract the meta data from that circuit. This command returns a list called gate_lst and an int called num_qbits:  `gate_lst, num_qbits =  comp_utils.read_circ(circ) `. The num_qbits represents the number of quantum bits in your quantum circuit (for simplicity I have assumed #qbits = #bits). 

![read circ](/images/read_circ.PNG?raw=true)

The gate_lst is an ordered list in which each entry is a tuple containing: `(gate_str, qbit_lst, parameters)`. The gate_str is a string which represents the type of gate being applied, the qbit_lst corresponds to the list of ints which are indicies for qbits the gate is being applied to (for control gates the first qbit index in the list is the control qbit and the second is the target qbit), the parameters is a list of floats which are the parameters for that gate (for Rx, Ry, Rz gates). This is all of the meta data required to re-create the circuit. 

The gate_lst can then be manipulated as required (by adding tuples or removing them) to augment the circuit as needed.

The general_replace function allows users a simple function to manipulate a gate_lst. This function takes a list (gate_lst), a gate_str and a list of replacement gate tuples *tuples of the form (gate_str, qbit_lst, parameters* in order to replace every instance of the gate 'gate_str' with the set of gates provided in the replacement gate tuples. Users should take care by making sure they provide a valid list of replacement gate tuples and the replacements DO NOT contain the gate given by 'gate_str'. `comp_utils.general_replace(gate_lst, 'gate_str', [replacement_tuples])` 

![general replace](/images/general_replace.PNG?raw=true)

Note, users should check the source code for this function to find out about some of the additional features of this function (such as the ability to pass functions instead of parameters and qbit_lst). 

Finally, The write_circ function takes a gate_lst as wells as an int (num_qbits) to produce a new qiskit.QuantumCircuit object which contains 'num_qbits' qbits and has all of the gates applied as described in the gate_lst. `new_circ = comp_utils.write_circ(gate_lst, num_qbits)`

![write circ](/images/write_circ.PNG?raw=true)

Now we have an easy way of reading our quantum circuits, augmenting the associated gate_lst and turning this augmented gate_lst into a new quantum circuit! 

## qcomp 
Begin by: `from qcompile import qcomp`

In this module, I have the implementation of two quantum compilers as well as a qbit router. I provide a detailed explanation (pretty much a derivation) for each of these functions in the jupyter notebook 'Building the Compiler.ipynb'. 

Example function calls: 

`compiled_circ = qcomp.simple_compiler(circ)` , which uses the simple compiler (translator) to compile the circuit 

`compiled_circ = qcomp.compiler(circ)` , which uses the optimized complier to compile the circuit 

`routed_circ = qcomp.circ_router(circ, topology)` , which takes a compiled circuit and a dict (topology) *assumed to be ring topology* to route the quantum circuit using swap gates.


## Acknowledgements: 
- QOSF : for introducing me to this aspect of quantum computing and providing many resources for me to reference 

If you have any further questions about this project, feel free to email me @ jbsoni@uwaterloo.ca 
