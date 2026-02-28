import numpy as np
from pennylane import qchem
import pennylane as qml
import json

def generate_hamiltonian(m, symbols, coordinates):
    molecule = qchem.Molecule(symbols, coordinates)
    H, qubits = qchem.molecular_hamiltonian(molecule)
    coeffs, ops = H.terms()
    string_ops = []
    wire_map = {i: i for i in range(qubits)}
    for op in ops:
        string_ops.append(qml.pauli.pauli_word_to_string(op, wire_map=wire_map))
    hamiltonian_dict = {string_ops[i]: float(coeffs[i]) for i in range(len(string_ops))}
    file_name = '{}_hamiltonian.json'.format(m)
    with open(file_name, 'w') as f:
        json.dump(hamiltonian_dict, f, indent=4)
    print("File {} saved".format(file_name))

generate_hamiltonian('h2',["H","H"], np.array([0.0, 0.0, 0.0, 0.0, 0.0, 1.4]))
generate_hamiltonian('lih',["Li","H"], np.array([0.0, 0.0, 0.0 , 0.0, 0.0, 1.5]))


