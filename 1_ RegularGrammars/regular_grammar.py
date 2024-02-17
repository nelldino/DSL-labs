# Variant 12:
# VN={S, F, D},
# VT={a, b, c},
# P={
#     S → aF
#     F → bF
#     F → cD
#     S → bS
#     D → cS
#     D → a
#     F → a
# }

import random

class FiniteAutomaton:
    def __init__(self):
        self.states = {'S', 'F', 'D', 'end'}
        self.alphabet = {'a', 'b', 'c'}
        self.transitions = {
            ('S', 'a'): {'F'},
            ('S', 'b'): {'S'},
            ('F', 'b'): {'F'},
            ('F', 'c'): {'D'},
            ('F', 'a'): {'end'},
            ('D', 'c'): {'S'},
            ('D', 'a'): {'end'}
        }
        self.start_state = 'S'
        self.accept_states = {'end'}

    def string_belongs_to_language(self, input_string):
        current_states = {self.start_state}
        for char in input_string:
            next_states = set()
            for state in current_states:
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
            current_states = next_states
        return len(current_states.intersection(self.accept_states)) > 0

class Grammar:
    def __init__(self):
        self.VN = {'S', 'F', 'D'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aF', 'bS'],
            'F': ['bF', 'cD', 'a'],
            'D': ['cS', 'a']
        }
        self.S = 'S'

    def generate_string(self):
        def expand(symbol):
            if symbol in self.VT:
                return symbol
            elif symbol in self.VN:
                production = random.choice(self.P[symbol])
                return ''.join(expand(s) for s in production)
            return ''

        return expand(self.S)

    def to_finite_automaton(self):
        fa = FiniteAutomaton()
        for non_terminal, productions in self.P.items():
            for production in productions:
                if len(production) == 2:  # Assuming productions like A -> aB
                    input_char = production[0]
                    next_state = production[1]
                    fa.transitions[(non_terminal, input_char)] = {next_state}
                elif len(production) == 1:  # Assuming productions like A -> a or A -> B
                    input_char = production
                    # Assuming 'end' state for terminal transitions
                    if input_char in self.VT:
                        fa.transitions[(non_terminal, input_char)] = {'end'}
                    else:
                        fa.transitions[(non_terminal, '')] = {input_char}
        return fa

grammar = Grammar()
fa = grammar.to_finite_automaton()
print("Generated strings from the grammar:")
for _ in range(5):
    print(grammar.generate_string())


print("\n")
print("Finite Automaton Transitions from CFG:")
for (state, input_char), next_states in fa.transitions.items():
    print(f"Transition: ({state}, '{input_char}') -> {next_states}")


fa = FiniteAutomaton()
user_input = input("\nEnter a string to check: ")
result = fa.string_belongs_to_language(user_input)
print(f"Does '{user_input}' belong to the language? {result}")
