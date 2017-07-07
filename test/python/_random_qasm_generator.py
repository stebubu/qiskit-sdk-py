import random
import string

try:
    import qiskit
except ImportError as ierr:
    sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
    import qiskit
from qiskit import QuantumProgram

class RandomQasmGenerator():
    """
    Generate random size circuits for profiling.
    """
    def __init__(self, seed=None,
                 maxQubits=5, minQubits=1,
                 maxDepth=100, minDepth=1):
        """
        Args:
          seed: Random number seed. If none, don't seed the generator.
          maxDepth: Maximum number of operations in a circuit.
          maxQubits: Maximum number of qubits in a circuit.
        """
        self.maxDepth = maxDepth
        self.maxQubits = maxQubits
        self.minDepth = minDepth
        self.minQubits = minQubits
        self.qp = QuantumProgram()
        self.qr = self.qp.create_quantum_registers('qr', maxQubits)
        self.cr = self.qp.create_classical_registers('cr', maxQubits)
        self.circuitNameList = []
        self.nQubitList = []
        self.depthList = []
        if seed is not None:
            random.seed(a=seed)
            
    def add_circuits(self, nCircuits, doMeasure=True):
        """Adds circuits to program.

        Generates a circuit with a random number of operations equally weighted
        between U3 and CX. Also adds a random number of measurements in
        [1,nQubits] to end of circuit.

        Args:
          nCircuits (int): Number of circuits to add.
          doMeasure (boolean): whether to add measurements
        """
        self.circuitNameList = []
        self.nQubitList = random.choices(
            range(self.minQubits, self.maxQubits+1), k=nCircuits)
        self.depthList = random.choices(
            range(self.minDepth, self.maxDepth+1), k=nCircuits)
        for i in range(nCircuits):
            circuitName = ''.join(random.choices(string.ascii_uppercase
                                                 + string.digits, k=10))
            self.circuitNameList.append(circuitName)
            nQubits = self.nQubitList[i]
            depth = self.depthList[i]
            circuit = self.qp.create_circuit(circuitName, ['qr'], ['cr'])
            for j in range(depth):
                if nQubits == 1:
                    opInd = 0
                else:
                    opInd = random.randint(0, 1)
                if opInd == 0: # U3
                    qind = random.randint(0, nQubits-1)
                    circuit.u3(random.random(), random.random(), random.random(),
                               self.qr[qind])
                elif opInd == 1: # CX
                    source, target = random.sample(range(nQubits), 2)
                    circuit.cx(self.qr[source], self.qr[target])
            if doMeasure:
                # add measurements to end of circuit
                nmeasure = random.randint(0, nQubits-1)
                for j in range(nmeasure):
                    qind = random.randint(0, nQubits-1)
                    circuit.measure(self.qr[qind], self.cr[qind])

    def get_circuit_names(self):
        return self.circuitNameList

    def getProgram(self):
        return self.qp
    
                    
