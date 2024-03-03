# Variant 12
# Q = {q0,q1,q2,q3},
# ∑ = {a,b,c},
# F = {q2},
# δ(q0,b) = q0,
# δ(q0,a) = q1,
# δ(q1,c) = q1,
# δ(q1,a) = q2,
# δ(q3,a) = q1,
# δ(q3,a) = q3,
# δ(q2,a) = q3.

import matplotlib.pyplot as plt
import networkx as nx

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
        self.accept_states = {'q2'}
        pass

    def nfa_to_dfa(self):
        dfa = FiniteAutomaton()
        dfa.alphabet = self.alphabet
        dfa.start_state = (self.start_state,)  # Start state represented as a tuple
        dfa.states = {dfa.start_state}
        dfa.transitions = {}
        dfa.accept_states = set()

        unprocessed_states = [dfa.start_state]

        while unprocessed_states:
            current_state = unprocessed_states.pop()

            for symbol in dfa.alphabet:
                next_states = set()
                for state in current_state:
                    next_states |= self.transitions.get((state, symbol), set())

                if next_states:
                    next_state = tuple(sorted(next_states))  # Convert set to tuple, sort for consistency
                    dfa.transitions[current_state, symbol] = next_state
                    if next_state not in dfa.states:
                        dfa.states.add(next_state)
                        unprocessed_states.append(next_state)
                        if any(state in self.accept_states for state in next_state):
                            dfa.accept_states.add(next_state)

        return dfa

    def __str__(self):
        transitions_str = "\n".join([f"{state} --{symbol}--> {next_state}" for (state, symbol), next_state in self.transitions.items()])
        accept_states_str = ", ".join(str(state) for state in self.accept_states)
        return f"States: {', '.join(map(str, self.states))}\nAlphabet: {', '.join(self.alphabet)}\nTransitions:\n{transitions_str}\nStart state: {self.start_state}\nFinal states: {accept_states_str}"

    def visualize(self):
        G = nx.DiGraph()

        # Add states
        for state in self.states:
            G.add_node(state)

        # Add transitions
        for (state, symbol), next_state in self.transitions.items():
            G.add_edge(state, next_state, label=symbol)

        # Add accept states
        for state in self.accept_states:
            G.nodes[state]['accept'] = True

        # Fixed layout
        pos = nx.circular_layout(G)

        # Increase figure size
        plt.figure(figsize=(8, 8))

        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_size=500)

        # Draw edges
        nx.draw_networkx_edges(G, pos)

        # Draw labels
        nx.draw_networkx_labels(G, pos)

        # Draw accept states with a double circle
        accept_states = [state for state, attr in G.nodes(data=True) if attr.get('accept')]
        nx.draw_networkx_nodes(G, pos, nodelist=accept_states, node_shape='o', node_size=500, linewidths=2,
                               edgecolors='r')

        # Draw symbols on edges
        edge_labels = nx.get_edge_attributes(G, 'label')
        for (start, end), label in edge_labels.items():
            if start == end:  # Self-transition
                x, y = pos[end]
                plt.text(x, y + 0.05, label, horizontalalignment='center', fontsize=10)
            else:
                nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, label_pos=0.5)

        plt.title('Finite Automaton')
        plt.axis('off')
        plt.show()


# Usage:
nfa = FiniteAutomaton()  # Define your NFA
dfa = nfa.nfa_to_dfa()  # Convert NFA to DFA
dfa.visualize()  # Visualize the NFA graphically
print("Deterministic Finite Automaton converted from Non-Deterministic Finite Automaton:")
print(dfa)
