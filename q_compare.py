import json
from qiskit.quantum_info import SparsePauliOp
import pennylane as qml
import time
import numpy as np
from qiskit.circuit import ParameterVector, QuantumCircuit
from qiskit.primitives import StatevectorEstimator
import csv

def qiskit_func(filename):
    with open(filename, 'r') as f:
        dict = json.load(f)
        op = SparsePauliOp.from_list([(k[::-1], v) for k, v in dict.items()])
        return op
    
def pennylane_func(filename, num_qubits):
    with open(filename, 'r') as f:  
        dict = json.load(f)
    coeffs = list(dict.values())
    wire_map = {i : i for i in range(num_qubits)}
    ops = [qml.pauli.string_to_pauli_word(i, wire_map=wire_map) for i in dict.keys()]
    return qml.Hamiltonian(coeffs, ops)

def run_qiskit(hamiltonian , num_qubits):
    layers = 2
    num_params = num_qubits * layers

    np.random.seed(42)
    params = np.random.uniform(-np.pi, np.pi, num_params)

    theta = ParameterVector('0', num_params)
    qc = QuantumCircuit(num_qubits)
    param_index = 0
    for _ in range(layers):
        # Ry rotations
        for i in range(num_qubits):
            qc.ry(theta[param_index], i)
            param_index += 1
        # CNOTs
        for i in range(num_qubits - 1):
            qc.cx(i, i+1)

    estimator = StatevectorEstimator()
    start_time = time.perf_counter()

    job = estimator.run([(qc, hamiltonian, params)])
    result = job.result()

    end_time = time.perf_counter()
    time_taken = end_time - start_time
    energy = result[0].data.evs
    return time_taken, energy

def run_pennylane(hamiltonian, num_qubits):
    device = qml.device('default.qubit', wires = num_qubits)
    np.random.seed(42)
    layers = 2
    num_params = num_qubits * layers
    params = np.random.uniform(-np.pi, np.pi, num_params)

    @qml.qnode(device)
    def cost_fn(weights):
        param_index = 0
        for _ in range(layers):
            for i in range(num_qubits):
                qml.RY(weights[param_index], wires=i)
                param_index += 1
            for i in range(num_qubits - 1):
                qml.CNOT(wires=[i, i+1])
    
        return qml.expval(hamiltonian)
    
    start_time = time.perf_counter()
    energy = cost_fn(params)
    end_time = time.perf_counter()

    time_taken = end_time - start_time
    return time_taken, energy

if __name__ == "__main__":
    q_h2 = qiskit_func('h2_hamiltonian.json')
    p_h2 = pennylane_func('h2_hamiltonian.json', 4)
    
    q_lih = qiskit_func('lih_hamiltonian.json')
    p_lih = pennylane_func('lih_hamiltonian.json', 12)

    results = []
    q_time, q_energy = run_qiskit(q_h2, 4)
    results.append(["H2", 4, "Qiskit", q_time, q_energy])
    
    p_time, p_energy = run_pennylane(p_h2, 4)
    results.append(["H2", 4, "PennyLane", p_time, p_energy])

    q_time, q_energy = run_qiskit(q_lih, 12)
    results.append(["LiH", 12, "Qiskit", q_time, q_energy])
    
    p_time, p_energy = run_pennylane(p_lih, 12)
    results.append(["LiH", 12, "PennyLane", p_time, p_energy])

    csv_filename = "benchmark_results.csv"
    with open(csv_filename, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Molecule", "Qubits", "Framework", "Time_Seconds", "Energy"])
        writer.writerows(results)

    print(f"Data saved to {csv_filename}")

