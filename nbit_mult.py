from helpers import *



def multiply(qc, multiplicand, multiplier, result, carries):
    """
    - WRITTEN BY CHATGPT :(
    Multiplies two quantum registers using shift-and-add logic.

    Args:
        qc (QuantumCircuit): The quantum circuit.
        multiplicand (QuantumRegister): The register representing the multiplicand.
        multiplier (QuantumRegister): The register representing the multiplier.
        result (QuantumRegister): The register to store the result.
        carries (AncillaRegister): Ancilla qubits for carry propagation.

    Returns:
        None
    """
    n = len(multiplier)  # Number of bits in the multiplier

    for i in range(n):
        # Check if the i-th bit of the multiplier is 1
        qc.cx(multiplier[i], carries[0])  # Temporarily store the bit in carries[0]

        # Add the multiplicand shifted by i to the result
        for j in range(len(multiplicand)):
            if j + i < len(result):  # Ensure we don't exceed the result register size
                qc.ccx(carries[0], multiplicand[j], result[j + i])

        # Uncompute the temporary carry
        qc.cx(multiplier[i], carries[0])




def main():
    provider, backend = init()

    shots = 10
    bits = 4

    # Registers
    a = QuantumRegister(bits, "a")       # multiplier / dividend
    b = QuantumRegister(bits, "b")       # multiplicand / divisor
    c = QuantumRegister(bits, "c")       # result
    d = AncillaRegister(bits, "d")       # carry[0:3] and final cleanup bit
    out = ClassicalRegister(bits, "out") # measurement
    one = AncillaRegister(bits, "one")
    
    ##### REMEMBER TO ADD ALL THE REGS TO THIS!!!!!!!!!!!!!!!!!!!!1
    qc = QuantumCircuit(a, b, c, d, out, one)

    init_regs(qc, a, [0, 0, 1,0])        # 6
    init_regs(qc, b, [0, 0,1,1])        # 3
    init_regs(qc, one, [1])
    # init_regs(qc, b, [1, 0])

    # add_regs(qc, a, b, c, d)

    # multiply(qc, a, b, c, d)
    twos_comp(qc, a, one, c, d)
    # modulus(qc, a, b, c, d, out, one)
    
    measure_reg(qc, d, out)

    # Execute the circuit
    job = backend.run(qc, shots=shots)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts()

    #visualize
    print(counts)





if __name__ == "__main__":
    main()


