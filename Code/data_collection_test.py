from qiskit import QuantumCircuit, QuantumRegister
from qiskit_ibm_runtime import SamplerV2 as Sampler, QiskitRuntimeService
from qiskit_aer import AerSimulator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit.transpiler import TranspileLayout
import pandas as pd
import time

# Initializing circuit
num_qubits = 5
qc = QuantumCircuit(num_qubits)

# Creating Circuit
qc.h(0)
for qubit in range(num_qubits-1):
    qc.cx(qubit, qubit+1)
qc.measure_all()

# Drawing circuit
print(qc.draw())

print("="*100)

# Connecting to IBM quantum computer service
service = QiskitRuntimeService(channel="ibm_quantum", token="")

# Selecting computer
real_backend = service.backend(name="ibm_sherbrooke")
prop = real_backend.properties()

# Simulating computer
aer = AerSimulator.from_backend(real_backend)

# Circuit optimization
pm = generate_preset_pass_manager(backend=aer, optimization_level=1)
isa_qc = pm.run(qc)

# Initializing simulation
sampler = Sampler(backend=aer)
sampler.options.default_shots = 10_000

# Initializing csv file with first simulation
# Running simulation
result = sampler.run(pubs=[isa_qc]).result()

# Exporting distribution results
dists = result[0].data.meas.get_counts()
df = pd.DataFrame(dists,index=[0])
dist_columns = sorted(df.columns,key=lambda col: int(col,2))
df = df[dist_columns]
df.to_csv("test_data.csv",index=False)
print("Exported data for simulation 0")

# Running next simulation in x seconds
time.sleep(2)

# Collecting data once every x seconds
simulation = 1
while True:
    # Running simulation
    result = sampler.run(pubs=[isa_qc]).result()

    # Exporting distribution results
    dists = result[0].data.meas.get_counts()
    df = pd.DataFrame(dists,index=[simulation])
    dist_columns = sorted(df.columns,key=lambda col: int(col,2))
    df = df[dist_columns]
    df.to_csv("test_data.csv",mode='a',index=False, header=False)
    print(f"Exported data for simulation {simulation}")
    simulation += 1

    # Running next simulation in x seconds
    time.sleep(2)
