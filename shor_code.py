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
)
backend = provider.get_backend("scarlet_quantum_rings")
shots = 1024

provider.active_account()


# Block 2
def iqft_cct(qc, b, n):
    """
    The inverse QFT circuit

    Args:

        qc (QuantumCircuit):
                The quantum circuit

        b (QuantumRegister):
                The target register

        n (int):
                The number of qubits in the registers to use

    Returns:
        None

    """

    for i in range (n):
        for j in range (1, i+1):
            # for inverse transform, we have to use negative angles
            qc.cu1(  -math.pi / 2** ( i -j + 1 ), b[j - 1], b[i])
        # the H transform should be done after the rotations
        qc.h(b[i])
    qc.barrier()
    return

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




# Block 3
# Shor’s algorithm to factorize 15 using 7^x mod 15.
## Sas: no. = exponent + working bits
##  increasing inputbits (x = {0,1}^n) increases the range of values of x (exponent) that we calculate,
##  thus having more data to base our factorisation from
##  HOWEVER! also increases the number of Modular Exponentiation (U^2n) gates,
##  so ig it increases complexity in polynomial time?
###     apparently, this should be around ceil(2 log_2 N)    (e.g. N = 15, n ~~ 8, but can be smaller for small inputs)
inputbits = 5
##  workingbits should be able to encode all the values uptil N?
###     heuristic: math.ceil(log_2(N))
workingbits = 5 
numberofqubits = inputbits + workingbits
shots = 1024

N = 15
a = 7
## we change a using the CIRCUIT itself!!! no way to encode that here yet...
## SAME FOR N!!! the positioning of the gates determines a, N
##  also, changing workingbits doesn't necessarily change the structure
##  (the gaps between switches should be same?),
##  but it does need more gates in each U^2n for proper bit shifting.
##  lastly, changing n increases the number of U^2n's to make.

## gpt says precompute powers of a? for the number of inputbits
## these are then multiplied into the working bits if |x_k> = |1>
a_powers = [math.pow(a, math.pow(2, i)) % N for i in range(inputbits)]

## food for thought, may not even need to think about circuits? maybe could do just ket maths directly

# InitializeDebugger()

q = QuantumRegister(numberofqubits , 'q')
## Sas: ONLY NEEDED FOR MEASUREMENT! You measure a qubit INTO a classical bit
c = ClassicalRegister(inputbits , 'c')
qc = QuantumCircuit(q, c)

print(f"{qc.qubits=}, {qc.clbits=}, {qc.layout=}")

# Initialize source and target registers
## Sas: because all qubits are initialised as zeros, but we want to initialise the two registers.
##      We Hadamard the input registers into a superposition to calculate all possible exponents,
##      and X or NOT the last qubit to initialise the working register into 00..01 = 1 (because a^0 = 1)
for input_i in range(inputbits):
    qc.h(input_i)
qc.x(numberofqubits - 1)
qc.barrier()

# Modular exponentiation 7^x mod 15
## Sas: I HAVE NO CLUEEEEEEEEEEEEEE - next thing to figure out. TODO!!!
qc.cx(q[2],q[4] )
qc.cx(q[2],q[5] )
qc.cx(q[6],q[4] )
qc.ccx(q[1],q[5],q[3] )
qc.cx(q[3],q[5] )
qc.ccx(q[1],q[4],q[6] )
qc.cx(q[6],q[4] ) #
qc.barrier()

# IQFT. Refer to implementation from earlier examples
## Sas: iQFT all the input bits to extract the phase information. We shouldn't need to change this I think?
iqft_cct (qc, q, inputbits)

# Measure
for input_i in range(1, inputbits):
    qc.measure(q[input_i], c[input_i])

# Execute the circuit
job = backend.run(qc, shots=shots)
job_monitor(job)
result = job.result()
counts = result.get_counts()

#clean up
del q, c, qc
del result
del job

#visualize
plot_histogram(counts)



