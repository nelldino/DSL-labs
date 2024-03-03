#  Determinism in Finite Automata. Conversion from NDFA 2 DFA. Chomsky Hierarchy

### Course: Formal Languages & Finite Automata
### Author: Nelli Garbuz

----

## Overview
  A finite automaton is a mechanism used to represent processes of different kinds. It can be compared to a state machine as they both have similar structures and purpose as well. The word finite signifies the fact that an automaton comes with a starting and a set of final states. In other words, for process modeled by an automaton has a beginning and an ending.

  Based on the structure of an automaton, there are cases in which with one transition multiple states can be reached which causes non determinism to appear. In general, when talking about systems theory the word determinism characterizes how predictable a system is. If there are random variables involved, the system becomes stochastic or non deterministic.

  That being said, the automata can be classified as non-/deterministic, and there is in fact a possibility to reach determinism by following algorithms which modify the structure of the automaton.


## Objectives:

1.Understand what an automaton is and what it can be used for.

2.Continuing the work in the same repository and the same project, the following need to be added: 
  
  a. Provide a function in your grammar type/class that could classify the grammar based on Chomsky hierarchy.

  b. For this you can use the variant from the previous lab.

3.According to your variant number (by universal convention it is register ID), get the finite automaton definition and do the following tasks:

a. Implement conversion of a finite automaton to a regular grammar.

b. Determine whether your FA is deterministic or non-deterministic.

c. Implement some functionality that would convert an NDFA to a DFA.

d. Represent the finite automaton graphically (Optional, and can be considered as a bonus point):

You can use external libraries, tools or APIs to generate the figures/diagrams.

Your program needs to gather and send the data about the automaton and the lib/tool/API return the visual representation.

Please consider that all elements of the task 3 can be done manually, writing a detailed report about how you've done the conversion and what changes have you introduced. In case if you'll be able to write a complete program that will take some finite automata and then convert it to the regular grammar - this will be a good bonus point.
   

## Implementation description

For the first part of the laboratory work, I made a function to check the grammar of my variant, according to the rules for Chomsky hierarchy.

     def chomsky_classification(self):
        context_free = True
        context_sensitive = True
        regular = True

        for non_terminal, productions in self.P.items():
            for production in productions:
                # Check for regularity
                if len(production) > 2 or (len(production) == 2 and production[0] in self.VN):
                    regular = False

                # Check for context-free
                if non_terminal != self.S and len(production) > 1:
                    context_free = False

                # Check for context-sensitivity
                if len(production) < 2 or non_terminal == self.S:
                    continue
                for symbol in production[1:]:
                    if symbol in self.VN:
                        context_sensitive = False
                        break

        if context_sensitive:
            return "Type-1 (Context-sensitive) Grammar"
        elif context_free:
            return "Type-2 (Context-free) Grammar"
        elif regular:
            return "Type-3 (Regular) Grammar"
        else:
            return "Type-0 (Unrestricted) Grammar"

For the second part of the laboratory work, where I had to convert a FA to grammar, I created a class for Regular Grammar that includes the non-terminal and terminal symbols, productions and start state. Then, I made functions that will add the productions and convert the finite automaton.
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

The is_deterministic method checks if the finite automaton is deterministic by verifying that each state has exactly one transition for each input symbol.
    def is_deterministic(self):
        for state in self.states:
            for symbol in self.alphabet:
                next_states = self.transitions.get((state, symbol), None)
                if next_states is None or len(next_states) != 1:
                    return False
        return True

FiniteAutomaton Class represents a finite automaton.It has several attributes:

**states:** A set of states.

**alphabet:** A set of input symbols (terminals).

**transitions:** A dictionary representing state transitions where keys are tuples (state, input_symbol) and values are sets of next states.

**start_state:** The start state.

**accept_states:** A set of accepting states.

The nfa_to_dfa() method converts an NFA to a DFA using the subset construction algorithm.It initializes a new DFA and processes states of the NFA to generate corresponding states of the DFA along with transitions.It returns the resulting DFA.
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
        
The method visualize() it is used to make a graphical representation of the DFA

## Conclusions / Screenshots / Results
**Results**
The first part of the laboratory work

<img width="302" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/0c7073b9-7fb6-405e-89e6-5e413da88c7b">

Conversion of FA to Grammar

<img width="302" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/3b03ef54-ec84-4ffa-9cc5-dc37177e3496">

Conversion of NFA to DFA

<img width="530" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/30ddb567-ed38-47c9-a28d-709c3aa2dbd0">
<img width="291" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/84962d11-e63f-4f7a-abf7-1bd61d079599">



