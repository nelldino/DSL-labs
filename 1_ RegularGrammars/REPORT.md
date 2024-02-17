#  Intro to formal languages. Regular grammars. Finite Automata.

### Course: Formal Languages & Finite Automata
### Author: Nelli Garbuz

----

## Theory
If needed, but it should be written by the author in her/his words.


## Objectives:

1. Discover what a language is and what it needs to have in order to be considered a formal one;

2. Provide the initial setup for the evolving project that you will work on during this semester. You can deal with each laboratory work as a separate task or project to demonstrate your understanding of the given themes, but you also can deal with labs as stages of making your own big solution, your own project. Do the following:

    a. Create GitHub repository to deal with storing and updating your project;

    b. Choose a programming language. Pick one that will be easiest for dealing with your tasks, you need to learn how to solve the problem itself, not everything around the problem (like    setting up the project, launching it correctly and etc.);

    c. Store reports separately in a way to make verification of your work simpler (duh)

According to your variant number, get the grammar definition and do the following:

  a. Implement a type/class for your grammar;

  b. Add one function that would generate 5 valid strings from the language expressed by your given grammar;

  c. Implement some functionality that would convert and object of type Grammar to one of type Finite Automaton;

  d. For the Finite Automaton, please add a method that checks if an input string can be obtained via the state transition from it;
   

## Implementation description

First of all, I implemented a class for my Grammar (Variant 12).
The constructor method, init(), initializes the grammar by defining the non-terminal symbols, terminal symbols, productions, and the start symbol.

The non-terminal and terminal symbols are defined as sets of strings.

The productions are defined as a dictionary, where each key is a non-terminal symbol, and the corresponding value is a list of strings representing the possible productions for that non-terminal symbol.

The start symbol of the grammar is defined as the string 'S'.

    def __init__(self):
        self.VN = {'S', 'F', 'D'}
        self.VT = {'a', 'b', 'c'}
        self.P = {
            'S': ['aF', 'bS'],
            'F': ['bF', 'cD', 'a'],
            'D': ['cS', 'a']
        }
        self.S = 'S'

After all of this, I added the function, which will generate 5 valid strings. 
The expand function is a recursive function responsible for expanding non-terminal symbols into strings of terminal symbols. It takes a symbol as an argument. 

It checks whether the symbol is a terminal symbol (VT) or a non-terminal symbol (VN).If the symbol is a terminal symbol, it is simply returned. If the symbol is a non-terminal symbol, a random production rule is chosen from the grammar's production rules for that non-terminal symbol.
For each symbol in the chosen production rule, expand is called recursively.
The expanded strings for each symbol in the production rule are concatenated using join to form the final expanded string for the non-terminal symbol.

If the symbol is neither a terminal nor a non-terminal symbol (e.g., an empty string or an unrecognized symbol), an empty string is returned.

    def generate_string(self):
        def expand(symbol):
            if symbol in self.VT:
                return symbol
            elif symbol in self.VN:
                production = random.choice(self.P[symbol])
                return ''.join(expand(s) for s in production)
            return ''

In the grammar class, I also have **to_finite_automaton** function. It initializes a new instance of the FiniteAutomaton class, which represents the finite automaton that will be generated from the context-free grammar.

It iterates over each non-terminal symbol (non_terminal) in the grammar's production rules (P). For each non-terminal symbol, it iterates over the list of production rules associated with that symbol (productions).

If the length of a production rule is 2, it means it follows the format A -> aB, where A is the current non-terminal symbol, a is a terminal symbol, and B is the next state.
If the length is 1, it means it follows the format A -> a or A -> B, where a is a terminal symbol or B is a non-terminal symbol.

For each production rule, it extracts the input character (input_char) and the next state (next_state).
It then adds a transition to the finite automaton's transitions dictionary. The key of this dictionary is a tuple containing the current non-terminal symbol and the input character, and the value is a set containing the next state(s).

If the input character is a terminal symbol (VT), it assumes a transition to an 'end' state and adds it to the transitions dictionary.
Otherwise, if the input character is a non-terminal symbol (VN), it assumes a transition directly to that non-terminal symbol.
Returning the Finite Automaton:

Once all productions have been processed, it returns the generated finite automaton (fa).

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

I also have the Finite Automaton class.
It defines attributes:

   **states:** A set containing all states of the automaton ({'S', 'F', 'D', 'end'}).
   
   **alphabet:** A set containing symbols in the alphabet of the automaton ({'a', 'b', 'c'}).
   
   **transitions:** A dictionary representing the transition function of the automaton.
                     Each key is a tuple (current_state, input_symbol) representing a transition.
                     Each value is a set containing next states reachable from the current state with the given input symbol.
                     
  **start_state:** A string representing the initial state of the automaton ('S').
  
  **accept_states:**  A set containing all accepting states of the automaton ({'end'}).
  
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

 The **string_belongs_to_language** method checks whether a given input string belongs to the language recognized by the finite automaton.
It takes input_string as an argument. It initializes current_states with the start state. It iterates over each character (char) in the input string:
For each state in current_states, it checks if there exists a transition with the current state and the current input character in the transitions dictionary.
If a transition exists, it updates next_states with the next states reachable from the current states with the given input character.
After iterating over all characters, it checks if any of the current states intersect with the accepting states ({'end'}).
If there's at least one intersection, it returns True, indicating that the input string belongs to the language. Otherwise, it returns False.

    def string_belongs_to_language(self, input_string):
        current_states = {self.start_state}
        for char in input_string:
            next_states = set()
            for state in current_states:
                if (state, char) in self.transitions:
                    next_states.update(self.transitions[(state, char)])
            current_states = next_states
        return len(current_states.intersection(self.accept_states)) > 0

## Conclusions / Screenshots / Results
**Results**

<img width="247" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/99e2358a-aecb-40df-83db-d0ccb2ff8db3">

<img width="279" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/63362fec-d9a1-4fa4-bdd0-c8196722f8fa">

Result in case the string can be obtained via the state transition:

<img width="296" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/aecd494c-de11-465f-9354-b8ed46d2bf86">

Result in case the string cannot be obtained via the state transition:

<img width="305" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/d46dcec9-17c9-402b-8058-e272a346df00">

