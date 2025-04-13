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



def add_regs(qc, a, b, c):
    '''
    Add two registers a and b together, using an ancilla register c, all of the same length.
    Not exactly necessary to keep these at the same length, but need more work to decouple that,
    so for now I'll just check against different lengths. - Sas
    '''
    assert len(a) == len(b) == len(c)

    for i in range(len(a)):
        qc.ccx(a[i], b[i], c[i])    # c1 = a AND b. can be XOR'd, or directly CCXed
        qc.cx(a[i], b[i])           # b = a XOR b
        if i > 0:
            qc.ccx(b[i], c[i-1], c[i])    # c1 = (b AND c0) XOR c1   - might be problematic
            qc.cx(c[i-1], b[i])           # b = c0 XOR b
        


        