# QCompare: VQE Benchmarking Core

A pure Python execution profiler for comparing Variational Quantum Eigensolver (VQE) algorithms across different quantum frameworks. 

## The Problem
Comparing quantum software frameworks like Qiskit and PennyLane side-by-side is difficult due to differing mathematical conventions. The biggest hurdle is qubit endianness (Qiskit uses Little-Endian, while PennyLane uses Big-Endian). If you run the exact same Hamiltonian through both without correcting this, you get entirely different physical simulations and energy results. 

## What This Does
This core engine normalizes the endianness of Pauli strings before execution, ensuring a strict apples-to-apples comparison of backend compilation times and ground-state energy accuracy. 

It runs a direct 1v1 hardware-efficient ansatz (HEA) benchmark comparing Qiskit's `StatevectorEstimator` against PennyLane's `default.qubit`.

## Repository Structure
* `generate_hamiltonian.py`: Script to build and serialize molecular Hamiltonians using PySCF.
* `q_compare.py`: The main execution script that loads the Hamiltonians, normalizes the endianness, and runs the head-to-head circuit simulations.
* `h2_hamiltonian.json` / `lih_hamiltonian.json`: Pre-calculated Hamiltonian data for Hydrogen and Lithium Hydride.

## How to Run

1. Clone the repository:
   ```bash
   git clone [https://github.com/Rachel-Eva/QCompare.git](https://github.com/Rachel-Eva/QCompare.git)
   cd QCompare

2. Install the core quantum libraries:
   ```bash
   pip install qiskit pennylane numpy
3. Execute the benchmark:
   ```bash
   python q_compare.py

   
