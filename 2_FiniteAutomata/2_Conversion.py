class RegularGrammar:
    def __init__(self):
        self.VN = set()  # Non-terminals
        self.VT = set()  # Terminals
        self.P = {}      # Productions
        self.S = None    # Start symbol

    def add_production(self, left, right):
        if left not in self.P:
            self.P[left] = []
        self.P[left].append(right)

    def convert_from_finite_automaton(self, fa):
        # Add non-terminals
        for state in fa.states:
            self.VN.add(state)

        # Add terminals
        self.VT = fa.alphabet

        # Start symbol
        self.S = fa.start_state

        # Add productions
        for (state, char), next_states in fa.transitions.items():
            if len(next_states) == 1:
                next_state = next_states.pop()  # Get the next state
                if next_state in fa.accept_states:
                    self.add_production(state, char)
                else:
                    self.add_production(state, char + next_state)
            else:
                for next_state in next_states:
                    if next_state in fa.accept_states:
                        self.add_production(state, char)
                    else:
                        self.add_production(state, char + next_state)

    def __str__(self):
        productions_str = "\n".join([f"{left} -> {' | '.join(right)}" for left, right in self.P.items()])
        return f"VN: {', '.join(self.VN)}\nVT: {', '.join(self.VT)}\nProductions:\n{productions_str}\nStart symbol: {self.S}"


# Define the finite automaton
class FiniteAutomaton:
    def __init__(self):
        self.states = {'q0', 'q1', 'q2', 'q3'}
        self.alphabet = {'a', 'b', 'c'}
        self.transitions = {
            ('q0', 'b'): {'q0'},
            ('q0', 'a'): {'q1'},
            ('q1', 'c'): {'q1'},
            ('q1', 'a'): {'q2'},
            ('q3', 'a'): {'q1', 'q3'},  # Changed to a set as it's now nondeterministic
            ('q2', 'a'): {'q3'}
        }
        self.start_state = 'q0'
        self.accept_states = {''}

    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), None)
                if next_states is None or len(next_states) != 1:
                    return False
        return True

# Create the finite automaton
fa = FiniteAutomaton()

# Conversion
fa = FiniteAutomaton()
rg = RegularGrammar()
rg.convert_from_finite_automaton(fa)

# Print Regular Grammar
print("Regular Grammar converted from Finite Automaton:")
print(rg)
if fa.is_deterministic():
    print("The finite automaton is deterministic.")
else:
    print("The finite automaton is non-deterministic.")