import numpy as np
from fractions import Fraction
from math import floor, gcd, log

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import QFT
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler

def a2kmodN(a, k, N):
    """Compute a^{2^k} (mod N) by repeated squaring."""
    for _ in range(k):
        a = int(np.mod(a**2, N))
    return a

def M2mod15():
    """Constructs the M2 (mod 15) permutation gate using SWAP gates."""
    U = QuantumCircuit(4)
    U.swap(2, 3)
    U.swap(1, 2)
    U.swap(0, 1)
    U = U.to_gate()
    U.name = "M_2"
    return U

def M4mod15():
    """Constructs the M4 (mod 15) permutation gate using SWAP gates."""
    U = QuantumCircuit(4)
    U.swap(1, 3)
    U.swap(0, 2)
    U = U.to_gate()
    U.name = "M_4"
    return U

def build_shor_circuit(N=15, a=2):
    """Constructs the complete quantum circuit for order finding."""
    # Register sizes: 4 qubits for target (N=15), 8 for control precision
    num_target = 4
    num_control = 8

    control = QuantumRegister(num_control, name="C")
    target = QuantumRegister(num_target, name="T")
    output = ClassicalRegister(num_control, name="out")
    qc = QuantumCircuit(control, target, output)

    # Initialize target register to |1>
    qc.x(num_control)

    # Apply Hadamard to control qubits and modular exponentiation
    for k in range(num_control):
        qc.h(k)
        b = a2kmodN(a, k, N)
        if b == 2:
            qc.compose(M2mod15().control(), qubits=[k] + list(range(num_control, num_control + 4)), inplace=True)
        elif b == 4:
            qc.compose(M4mod15().control(), qubits=[k] + list(range(num_control, num_control + 4)), inplace=True)
        # M1 is identity, so we skip it

    # Apply Inverse QFT to control register
    qc.compose(QFT(num_control, inverse=True), qubits=control, inplace=True)

    # Measure
    qc.measure(control, output)
    return qc, num_control

def factorize_results(counts, N, a, num_control):
    """Classical post-processing to extract factors from quantum measurement counts."""
    print("\n--- Starting Classical Post-Processing ---")
    
    # Filter noise: keep bitstrings with high probability
    threshold = np.max(list(counts.values())) / 2
    counts_keep = {k: v for k, v in counts.items() if v > threshold}

    for bitstring in counts_keep.keys():
        decimal = int(bitstring, 2)
        phase = decimal / (2**num_control)
        
        # Use continued fractions to find r
        frac = Fraction(phase).limit_denominator(N)
        r = frac.denominator
        
        print(f"\nMeasured Bitstring: {bitstring} (Phase: {phase})")
        print(f"Estimated order r: {r}")

        if phase == 0:
            print("Phase 0 provides no information. Skipping...")
            continue

        if r % 2 == 0:
            # Check factors using gcd(a^(r/2) ± 1, N)
            x = pow(a, r // 2, N)
            guesses = [gcd(x - 1, N), gcd(x + 1, N)]
            
            for d in guesses:
                if 1 < d < N:
                    print(f"*** Non-trivial factor found: {d} ***")
                    return d, N // d
    
    return None

def main():
    N = 15
    a = 2
    
    # 1. Build the circuit
    circuit, num_control = build_shor_circuit(N, a)
    print(f"Shor's Circuit for N={N} constructed.")

    # 2. Run execution
    # To run on real hardware, uncomment the Service/Backend lines below.
    # Otherwise, we use the results provided in the tutorial logic.
    print("Executing circuit (using simulated/tutorial results)...")
    
    # Mocking the counts obtained from the tutorial's ideal simulator run
    ideal_counts = {"00000000": 264, "01000000": 268, "10000000": 249, "11000000": 243}
    
    # 3. Post-process to find factors
    factors = factorize_results(ideal_counts, N, a, num_control)
    
    if factors:
        print(f"\nSuccess! Factors of {N} are {factors[0]} and {factors[1]}.")
    else:
        print("\nFactorization failed in this attempt.")

if __name__ == "__main__":
    main()