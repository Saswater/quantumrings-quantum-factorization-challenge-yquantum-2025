# Block 1
import QuantumRingsLib
from QuantumRingsLib import QuantumRegister, AncillaRegister, ClassicalRegister, QuantumCircuit
from QuantumRingsLib import QuantumRingsProvider
from QuantumRingsLib import job_monitor
from QuantumRingsLib import JobStatus
from matplotlib import pyplot as plt
import numpy as np
# added below in case
import math

provider = QuantumRingsProvider(
    token='',
    name=''
)
backend = provider.get_backend("scarlet_quantum_rings")
shots = 10

provider.active_account()



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

def apply_constant_adder(qc, y, carries, C):
    """
    Adds constant C to register y using ripple-carry adder logic.
    Assumes y is n bits, and carries is (n-1) ancilla qubits.
    """
    C_bin = [int(b) for b in bin(C)[2:].zfill(len(y))][::-1]  # LSB first
    n = len(y)

    # Forward carry propagation
    for i in range(n - 1):
        if C_bin[i]:
            qc.cx(y[i], carries[i])
            qc.x(y[i])
        else:
            qc.cx(y[i], carries[i])

    # Final bit (MSB)
    if C_bin[-1]:
        qc.x(y[n - 1])

    # Backward cleanup (optional)
    for i in reversed(range(n - 1)):
        if C_bin[i]:
            qc.x(y[i])
            qc.cx(y[i], carries[i])
        else:
            qc.cx(y[i], carries[i])



def measure_reg(r):
    for i in range(bits):
        qc.measure(r[i], out[i])




def add_regs(a, b, c):
    for i in range(bits):
        if i == 0:
            qc.ccx(a[0], b[0], c[0])    # c0 = a AND b
            qc.cx(a[0], b[0])           # b = a XOR b
        else:
            qc.ccx(a[i], b[i], c[i])    # c1 = a AND b. can be XOR'd, or directly CCXed
            qc.cx(a[i], b[i])           # b = a XOR b
            qc.ccx(b[i], c[i-1], c[i])    # c1 = (b AND c0) XOR c1   - might be problematic
            qc.cx(c[i-1], b[i])           # b = c0 XOR b


bits = 4

# Registers
a = QuantumRegister(bits, "a")       # 3-bit number to add (unchanged)
b = QuantumRegister(bits, "b")       # 3-bit number to add into (in-place sum)
c = AncillaRegister(bits, "c")       # carry[0:3] and final cleanup bit
out = ClassicalRegister(bits, "out") # measurement

qc = QuantumCircuit(a, b, c, out)

# a = 011, b = 001, r = 100
## maybe another function to init regs?
qc.x(a[0])
qc.x(a[1])
# qc.x(b[0])
qc.x(b[1])

add_regs(a,b,c)
measure_reg(b)

# Execute the circuit
job = backend.run(qc, shots=shots)
job_monitor(job)
result = job.result()
counts = result.get_counts()

#visualize
print(counts)
