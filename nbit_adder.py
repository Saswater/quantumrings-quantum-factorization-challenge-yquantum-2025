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
from helpers import *

def main():
    provider, backend = init()

    shots = 10
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
    # qc.x(a[1])
    # qc.x(b[0])
    qc.x(b[1])

    add_regs(qc, a,b,c)
    measure_reg(qc, b, out)

    # Execute the circuit
    job = backend.run(qc, shots=shots)
    job_monitor(job)
    result = job.result()
    counts = result.get_counts()

    #visualize
    print(counts)


if __name__ == "__main__":
    main()
