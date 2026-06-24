# Dynamically creates custom gate architecture and operations required to simulate Shor's algorithm
# using Qiskit. Given some coprime modulus N to factor, executing this file will attempt to factor
# via Shors algorithm.
#
# Author: Carson Ihrke
# Date: June 24 (modified)

import numpy as np
from math import gcd, ceil, log2
from typing import Any
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit.circuit.library import QFTGate, UnitaryGate
from qiskit_aer import Aer


# constructs a controlled unitary matrix performing: |x> -> |(a_power * x) % N>
# @params: number of target qubits (num_qubits), modulus (N), base guess (a_power)
# @return: gate representing permutation matrix (gate.control())
def controlled_modular_multiplication(num_qubits, N, a_power):

    # initialize an empty operator matrix matching the size of the target register
    matrix = np.zeros((2**num_qubits, 2**num_qubits))
    
    # define permutation mappings for valid inputs under the modulus
    for x in range(2**num_qubits):
        if x < N:
            matrix[(a_power * x) % N, x] = 1
        else:
            matrix[x, x] = 1  # identity mapping for out-of-bounds states
    
    # convert the raw mathematical matrix into a qiskit standard unitary gate
    gate = UnitaryGate(matrix)
    gate.name = f"mod_{a_power}"
    
    # return the gate modified to accept a control qubit constraint
    return gate.control()

# Assembles the complete Shor's Quantum Circuit infrastructure.
# @params: modulus (N), base guess (a)
# @return: quantum circuit (qc), number of control bits (num_control)
def build_generalized_shor(N, a):

    # DIMENSION CALCULATION & BIT ALLOCATION
    n = ceil(log2(N))
    num_target = n          # Target register holds the modular arithmetic states
    num_control = 2 * n     # Control register size provides precision tracking for phases
    
    print(f"   [Circuit Build] Allocating {num_control} Control Qubits & {num_target} Target Qubits...")
    
    # Initialize quantum and classical memory structures
    c_reg = QuantumRegister(num_control, name='control')
    t_reg = QuantumRegister(num_target, name='target')
    bits = ClassicalRegister(num_control, name='m')
    
    qc = QuantumCircuit(c_reg, t_reg, bits)
    
    # STATE INITIALIZATION
    # Flip target register lowest bit from |0> to |1> using a Pauli-X gate
    qc.x(t_reg[0]) 
    
    # Place all control qubits into an equal superposition using Hadamard gates
    qc.h(c_reg)    
    
    # CONTROLLED GATE CONSTRUCTION (SUPERPOSITION PERIODICITY)
    print(f"   [Circuit Build] Appending controlled modular exponentiation gates...")
    for k in range(num_control):
        # Calculate the base element value scaled exponentially for this control wire stage
        a_power = pow(a, 2**k, N)
        
        # Build the specific modular transformation gate instance
        mod_gate = controlled_modular_multiplication(num_target, N, a_power)
        
        # Wire up the gate: Controlled by wire 'k', acting across the entire target register space
        qc.append(mod_gate, [c_reg[k]] + list(range(num_control, num_control + num_target)))
        
    # INVERSE QUANTUM FOURIER TRANSFORM
    print(f"   [Circuit Build] Applying Inverse QFT to extract period phase frequencies...")
    qft_inv = QFTGate(num_control).inverse()
    qc.append(qft_inv, c_reg)
    
    # MEASUREMENT AND WAVE COLLAPSE
    print(f"   [Circuit Build] Mapping quantum control lines to classical readout register...")
    qc.measure(c_reg, bits)
        
    return qc, num_control


# Streamlined execution engine driving only the measurement counts simulator.
# @params: modulus (N), base guess (a_base)
# @return: number of measurement results (counts), number of control qubits (n_ctrl), base guess (a_to_test)
def run_quantum_factorization(N, a_base=None):

    print(f"\n[Quantum Engine] Initializing Qiskit Aer State Simulation Core...")
    backend_qasm: Any = Aer.get_backend('qasm_simulator')
    
    # Validate coprime conditions for base 'a' selection
    a_to_test = a_base if a_base else 2
    if gcd(a_to_test, N) != 1:
        print(f"   [Warning] Base a={a_to_test} shares a factor with N={N}. Defaulting base to 2.")
        a_to_test = 2 
        
    print(f"[Quantum Engine] Compiling Shor's circuit architecture for N={N}, a={a_to_test}...")
    circuit, n_ctrl = build_generalized_shor(N, a_to_test)
    
    print(f"[Quantum Engine] Transpiling logical gates into physical backend instructions...")
    t_circuit = transpile(circuit, backend_qasm)
    
    print(f"[Quantum Engine] Executing 100 registration shots on QASM simulator engine...")
    counts = backend_qasm.run(t_circuit, shots=100).result().get_counts()
    print(f"[Quantum Engine] Execution completed successfully.\n")
    
    return counts, n_ctrl, a_to_test

def main():

    N = 33
    print("=" * 75)
    print(f"   RUNNING SHOR'S QUANTUM FACTORIZATION SIMULATION FOR N = {N}")
    print("=" * 75)
    
    counts, _, a_used = run_quantum_factorization(N, a_base=2)
    
    print("-" * 75)
    print("   SIMULATOR OUTPUT READOUT (CONSTRUCTIVE INTERFERENCE HIGH FREQUENCIES)")
    print("-" * 75)
    print(f"Sample execution using base a={a_used} generated counts allocation:\n{counts}\n")

if __name__ == "__main__":
    main()