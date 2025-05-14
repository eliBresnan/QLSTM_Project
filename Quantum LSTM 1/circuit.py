from qiskit import QuantumCircuit
from qiskit.quantum_info import Statevector, Pauli
from globals import *


class VQC:

    def __init__(self, parameters, N_qubits=DATA_DIMENSIONS*2, depth = VARIATIONAL_DEPTH):
          
        self.NQ = N_qubits
        self.depth = depth 

        # this stores a list of 3 dimensions of rotation gradients...
        # ...inside a list of layers
        # ...inside a list of qubits
        # so the total number of parameters for a circuit is 3*depth*N_qubits
        self.gradient_parameters = parameters

        l = 1
        while l < depth:
            for q in range(self.NQ):
                self.gradient_parameters[q].append([0,0,0]) 
            l += 1

        self.qc = None

        self.measurement = None

        return
        
    # takes vector and encodes it into angles (Bloch Vectors)
    def encode_vector(self,data_vec):

        # Check for size inconsistency
        if len(data_vec) != self.NQ:
            print("Vector size does not match Number of Qubits")
            print("nV -> ",len(data_vec)," | nQ -> ",self.NQ)
            return
        
        theta_y = None
        theta_z = None
        for i in range(self.NQ):
  
            # superpose qubit
            self.qc.h(i)                    

            # Calculate rotation angles
            theta_y = np.arctan(data_vec[i]) 
            theta_z = np.arctan(data_vec[i] ** 2) # x^2 creates "higher-order terms" after entanglement

            # Rotate around y and z axis
            self.qc.ry(theta_y,i)
            self.qc.rz(theta_z,i)

        return

    def variational_layer(self):

        x = None
        y = None
        for l in range(self.depth):

            # cycle through qubits to apply cnots
                # All qubits with a fixed adjacency 1 and 2 get entangled
            if self.qc.num_qubits == 2:
                self.qc.cx(0,1)
            else:
                for a in range(1,3):
                    x = 0
                    y = a
                    while x < self.qc.num_qubits:
                        self.qc.cx(x,y)
                        x += 1
                        y =  (y+1) % self.qc.num_qubits

            # Apply Gradients
            for i in range(self.NQ):
                self.qc.rx(self.gradient_parameters[i][l][0],i)
                self.qc.ry(self.gradient_parameters[i][l][1],i)
                self.qc.rz(self.gradient_parameters[i][l][2],i)
            
        #print(self.qc)
        return

    def run(self, data_array):

       # print("Running a circuit")
        
        # reset qc
        self.qc = QuantumCircuit(self.NQ) 

        # run layers of circuit
        self.encode_vector(data_array)
        self.variational_layer()
        
        # Measures qubits
        state = Statevector.from_instruction(self.qc)
        self.measurement = []
        op = None 
        expval = None
        for i in range(self.NQ):
            op = Pauli(f'{"I"*(self.NQ-1-i)}Z{"I"*(i)}')
            expval = state.expectation_value(op)
            self.measurement.append(expval.real)
            #print(f"⟨Z⟩ on qubit {i}: {expval.real}")
        return
        
    # only returns second half of qubits measurments to get output vectors when truncate==True
    def get_result(self, truncate=True):
        if self.measurement == None:
            print("Circuit must be run first")
            return
        return ([self.measurement[i] + self.measurement[DATA_DIMENSIONS+i] for i in range(DATA_DIMENSIONS)] ) if truncate==True else self.measurement
        #return (self.measurement[DATA_DIMENSIONS:] if truncate==True else self.measurement)
    
    def shift_param(self,shift,qubit,layer,dimension):
        self.gradient_parameters[qubit][layer][dimension] += shift
        return

    # updates single parameter with gradient
    def update_parameter(self,gradient,qubit,layer,dimension,shift = 0):
       # print("updating param with gradient ",gradient)
        self.gradient_parameters[qubit][layer][dimension] += shift - (GET_LEARNING_RATE()*gradient)
        return


    # returns array of parameter states in following format:
        # (e.g. q1l1 = depth layer 1 of qubit 1)
        # Circuit Parameters = 
        # [
        #   [
        #      [ q0l0.alpha, q0l0.beta, g0l0.gamma]
        #      [ q0l1.alpha, q0l1.beta, g0l1.gamma]
        #   ],
        #   [
        #      [ q1l0.alpha, q1l0.beta, g1l0.gamma]
        #      [ q1l1.alpha, q1l1.beta, g1l1.gamma]
        #   ]
        #   etc.
        # ]

    def is_trivial(self,q,l,d):
        return self.gradient_parameters[q][l][d] == 0

    def get_parameters(self):
        return self.gradient_parameters
    
    