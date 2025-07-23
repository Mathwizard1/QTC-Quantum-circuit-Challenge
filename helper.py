from qiskit import QuantumCircuit, qasm2, transpile
from qiskit_aer import AerSimulator

from qiskit.quantum_info import Operator, Statevector
from qiskit.circuit.library import CCXGate

import numpy as np
import pickle as pk

simulator = AerSimulator()
def run_transpiled_circuit(qc: QuantumCircuit, kwargs= {}):
    qc_sim = transpile(qc, simulator)
    result = simulator.run(qc_sim, **kwargs).result()
    
    return result.get_counts()

def get_random_initial_states(num_qubits= 1):
    state_bits = np.random.randint(low= 0, high= 2, size= (num_qubits,))
    return ''.join(map(str, state_bits))

class grader:
    def __init__(self, total):
        self._score = 0
        self._answer_list = {}
        self._task_flag = False

        self.total = total
        self.message = ""
        self.set_person()

    def set_person(self, name= "", rollno = ""):
        self.name = name
        self.rollno = rollno

    def display(self):
        print(f"{self.name}\nCurrent score: {self._score} / {self.total}")

    def intro_message(self):
        print(f'Welcome {self.name},\n{self.message}')

    def ans_print(self):
        for key in self._answer_list:
            print(key, self._answer_list[key],'\n')

    def ans_dump(self, file_name):
        print(f"{len(self._answer_list)} / {self.total} answers being saved.")

        self._answer_list['id'] = (self.name, self.rollno)
        
        #return self.ans_print()
        with open(f"{file_name}_{self.rollno}.dat", 'wb') as fp:
            pk.dump(self._answer_list, fp)
            fp.close()

    def check_task(self, obj, key, add_score= 1):
        if(self._task_flag):
            if(key not in self._answer_list):
                self._score += add_score
            self._answer_list[key] = obj
            print(f"Good Job {self.name}. You passed.✅")
        else:
          print("Try Again.🔄")    
        print("Your score:", self._score)   

    def circuit_store_qasm(self, qc_answer: QuantumCircuit):
        return qasm2.dumps(qc_answer)

    def circuit_compare_commonInitialState(self, qc_answer: QuantumCircuit, Qc_circuit: QuantumCircuit, method= "SV"):
        initial_state = Statevector.from_label(get_random_initial_states(Qc_circuit.num_qubits))
        answer1 = initial_state.evolve(qc_answer)
        answer2 = initial_state.evolve(Qc_circuit)
        
        if(method == "InvC"):
            pass
        # default StateVector check
        return self.circuit_compare_Statevector(answer1, answer2)

    def circuit_compare_Statevector(self, answer_state1: Statevector, answer_state2: Statevector):
        self._task_flag = answer_state1.equiv(answer_state2)
        return self._task_flag

############################################################
class QCC1(grader):
    def __init__(self):
        super().__init__(total= 6)
        self.message = "This the Quantum Circuit Challege, where you will be introduced to basic Qiskit and Quantum stuff.\nAll The best!"

    def file_dump(self):
        super().ans_dump("QCC_1")

    def Ex1(self, qc_answer: QuantumCircuit):
        Qc_circuit = QuantumCircuit(2)
        Qc_circuit.u(np.pi/2, 0, np.pi, 0)
        Qc_circuit.cx(0, 1)

        self.circuit_compare_commonInitialState(qc_answer, Qc_circuit)
        self.check_task(self.circuit_store_qasm(qc_answer), 'Ex1')

    def Ex2(self, counts):
        self._task_flag = False

        keys = tuple(counts.keys())
        if(len(counts) == 2): 
            self._task_flag = True

            for key in keys:
                first_bit = key[0]
                for bit in key:
                    if(bit != first_bit):
                        self._task_flag = False
                        return self.check_task(keys, 'Ex2')

        self.check_task(keys, 'Ex2')

    def Ex3(self, qc_answer: QuantumCircuit):
        Qc_circuit = QuantumCircuit(3)
        Qc_circuit.u(np.pi/2, 0, np.pi, 0)
        Qc_circuit.cx(0, 1)
        Qc_circuit.cx(0, 2)

        self.circuit_compare_commonInitialState(qc_answer, Qc_circuit)
        self.check_task(self.circuit_store_qasm(qc_answer), 'Ex3')

    def Ex4(self, qc_answer: QuantumCircuit):
        qc_answer = qc_answer.remove_final_measurements(inplace= False)
        
        Qc_circuit = QuantumCircuit(2)
        Qc_circuit.u(np.pi/2, 0, np.pi, range(2))

        initial_state = Statevector.from_label('00')
        final_answer = initial_state.evolve(qc_answer)
        initial_state = Statevector.from_label('10')
        answer = initial_state.evolve(Qc_circuit)

        self._task_flag = answer.equiv(final_answer)
        self.check_task(self.circuit_store_qasm(qc_answer), 'Ex4')

    def Ex5(self, qc_answer: QuantumCircuit):
        Qc_circuit = QuantumCircuit(1)
        Qc_circuit.u(np.pi/2, 0, np.pi, 0)
        Qc_circuit.u(0, 0, np.pi/2, 0)

        self.circuit_compare_commonInitialState(qc_answer, Qc_circuit)
        self.check_task(self.circuit_store_qasm(qc_answer), 'Ex5')

    def Ex6(self, number: np.ndarray, qc_answer: QuantumCircuit):
        qc_answer = qc_answer.remove_final_measurements(inplace= False)

        Qc_circuit = QuantumCircuit(3)
        for idx, bit in enumerate(number):
            if(bit): Qc_circuit.u(np.pi, 0, np.pi, idx)
        Qc_circuit.ccx(0,1,2)

        self.circuit_compare_commonInitialState(qc_answer, Qc_circuit)
        self.check_task([number.tolist(), self.circuit_store_qasm(qc_answer)], 'Ex6')

    def BonusEx(self, ans_matrix: np.ndarray):
        toffoli = CCXGate()
        toffoli_matrix = np.array(Operator(toffoli))
        self._task_flag = np.array_equal(ans_matrix, toffoli_matrix)
        self.check_task('yes','bonus')

if __name__ == "__main__":
    print(get_random_initial_states(4))