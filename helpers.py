import QuantumRingsLib
from QuantumRingsLib import QuantumRegister, AncillaRegister, ClassicalRegister, QuantumCircuit
from QuantumRingsLib import QuantumRingsProvider
from QuantumRingsLib import job_monitor
from QuantumRingsLib import JobStatus
from matplotlib import pyplot as plt
import numpy as np
# added below in case
import math


def init():
    provider = QuantumRingsProvider(
        token='',
        name=''
    )
    backend = provider.get_backend("scarlet_quantum_rings")
    provider.active_account()
    return provider, backend


def measure_reg(qc, r, out):
    for i in range(len(r)):
        qc.measure(r[i], out[i])



def twos_comp(qc, r, one, result, ancilla):
    """
    Compute the two's complement of a quantum register.

    Args:
        qc (QuantumCircuit): The quantum circuit.
        r (QuantumRegister): The quantum register to take the two's complement of.
        negative_r (QuantumRegister): An ancilla register to store intermediate results.

    Returns:
        None
    """
    # Step 1: Flip all the bits in the register (NOT operation)
    qc.x(ancilla[0])                # set 1st carry to 1
    for i in range(len(r)):     # for each digit
        qc.cx(r[i], result[i])      # copy r to result
        qc.x(result[i])             # invert result
        qc.ccx(result[i], ancilla[i], ancilla[i+1])     # next carry = result AND carry (i.e. 1 + 1 = "1"0, 1 carry)
        qc.cx(ancilla[i], result[i])                    # result = result XOR carry (i.e. 1 + 1 = 1"0", 0 current)

    qc.x(ancilla[0])                # reset
    for i in range(len(r)):     # for each digit
        qc.cx(result[i], r[i])      # copy r to result
        qc.x(r[i])             # invert result
        qc.ccx(r[i], ancilla[i], ancilla[i+1])     # next carry = result AND carry (i.e. 1 + 1 = "1"0, 1 carry)
        qc.cx(ancilla[i], r[i])                    # result = result XOR carry (i.e. 1 + 1 = 1"0", 0 current)
    
    
    # init_regs(qc, one, [1])
    # add_regs(qc, one, r, result, ancilla)
    # del one


def init_regs(qc, r, vals: list):
    assert len(r) >= len(vals)
    for i, val in enumerate(vals[::-1]):
        if val: qc.x(r[i])


def plot_histogram(counts, title=""):
    """
    Plots the histogram of the counts

    Args:

        counts (dict):
            The dictionary containing the counts of states

        titles (str):
            A title for the graph.

    Returns:
        None

    """
    fig, ax = plt.subplots(figsize=(10, 7))
    plt.xlabel("States")
    plt.ylabel("Counts")
    mylist = [key for key, val in counts.items() for _ in range(val)]

    unique, inverse = np.unique(mylist, return_inverse=True)
    bin_counts = np.bincount(inverse)

    plt.bar(unique, bin_counts)

    maxFreq = max(counts.values())
    plt.ylim(ymax=np.ceil(maxFreq / 10) * 10 if maxFreq % 10 else maxFreq + 10)
    plt.title(title)

    # Save the plot as an image file
    plt.savefig("histogram.png")
    plt.show()
    return



def add_regs(qc, a, b, r, c):
    '''
    Adds register a into b, using an ancilla register c, all of the same length.
    Not exactly necessary to keep these at the same length, but need more work to decouple that,
    so for now I'll just check against different lengths. - Sas
    '''
    assert len(a) == len(b) == len(r) == len(c), "Registers a, b, and c must have the same size"

    for i in range(len(a)):
        qc.ccx(a[i], b[i], c[i])    # c1 = a AND b. #####################3
        qc.cx(a[i], r[i])           # r = a XOR r
        qc.cx(b[i], r[i])           # r = b XOR r
        if i > 0:
            qc.ccx(r[i], c[i-1], c[i])    # c1 = (b AND c0) XOR c1  #########################
            qc.cx(c[i-1], r[i])           # b = c0 XOR b
    
    for i in range(len(c)):
        qc.ccx(a[i], b[i], c[i])    # c1 = a AND b. #####################3
        qc.cx(a[i], b[i])           # b = a XOR b
        if i > 0:
            qc.ccx(b[i], c[i-1], c[i])    # c1 = (b AND c0) XOR c1  #########################


# def modulus(qc, dividend, divisor, result, ancilla, one):
#     """
#     Compute the modulus of a quantum register using two's complement subtraction.

#     Args:
#         qc (QuantumCircuit): The quantum circuit.
#         dividend (QuantumRegister): The quantum register representing the dividend.
#         divisor (QuantumRegister): The quantum register representing the divisor.
#         result (QuantumRegister): The quantum register to store the result (remainder).
#         ancilla (QuantumRegister): An ancilla register for intermediate calculations.

#     Returns:
#         None
#     """
#     assert len(dividend) == len(divisor) == len(result), "Registers must have the same size"

#     # Step 1: Initialize the result register with the dividend
#     for i in range(len(dividend)):
#         qc.cx(dividend[i], result[i])

#     # Step 2: Compute the two's complement of the divisor
#     twos_comp(qc, divisor, one)

#     # Step 3: Add the two's complement of the divisor to the result (i.e., subtract the divisor)
#     add_regs(qc, divisor, result, ancilla)

#     # Step 4: Check if the result is negative (most significant bit is 1)
#     qc.cx(result[-1], ancilla[0])

#     # Step 5: If the result is negative, undo the subtraction
#     qc.x(ancilla[0])  # Negate the condition
#     add_regs(qc, divisor, result, ancilla)  # Undo subtraction
#     qc.x(ancilla[0])  # Restore the condition

#     # Step 6: Uncompute the two's complement of the divisor
#     twos_comp(qc, divisor, ancilla)




