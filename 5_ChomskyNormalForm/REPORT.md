# Chomsky Normal Form

### Course: Formal Languages & Finite Automata
### Author: Nelli Garbuz

----

## Overview
Chomsky Normal Form (CNF) is a specific form of context-free grammars in formal language theory, named after Noam Chomsky. In CNF, every production rule of the grammar is restricted to have one of two forms:
1. ```A → BC```
2. ```A → a```

In order to convert a grammar into Chomsky Normal Form, there are several rules that need to be respected: no ε-productions (there are no productions that produce an empty string),
no unit productions (eliminating unit productions, where a non-terminal directly produces another non-terminal),
no inaccessible symbols (all non-terminal symbols must be reachable from the start symbol),
no unproductive symbols (all non-terminal symbols must eventually derive terminal strings),
binary productions (all productions are either of the form ```A → BC``` (where B and C are non-terminals) or ```A → a``` (where a is a terminal))
## Objectives:
1. Learn about Chomsky Normal Form (CNF) [1].
2. Get familiar with the approaches of normalizing a grammar.
3. Implement a method for normalizing an input grammar by the rules of CNF.
    1. The implementation needs to be encapsulated in a method with an appropriate signature (also ideally in an appropriate class/type).
    2. The implemented functionality needs executed and tested.
    3. A **BONUS point** will be given for the student who will have unit tests that validate the functionality of the project.
    4. Also, another **BONUS point** would be given if the student will make the aforementioned function to accept any grammar, not only the one from the student's variant.
## Implementation description

Assigned variant:
![image](https://github.com/nelldino/DSL-labs/assets/120444803/f4286a49-85ae-44e6-b76e-f673ad55ed63)

The provided Python code in file ```Grammar.py``` defines a class Grammar that encapsulates a context-free grammar and includes methods for transforming it into Chomsky Normal Form. The conversion process involves several steps, according to all the rules of CNF.
The ```Grammar``` class is defined to define the components of a context-free grammar: non-terminals, terminals, production rules, and a start symbol.

```python
class Grammar:
    def __init__(self, non_terminals, terminals, rules):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules
```
**Eliminating epsilon productions**

The method, ```eliminate_empty_string``` aims to remove ε-productions (productions that derive an empty string) from the grammar.

It creates a copy of the original grammar to work with, initializing ```updated_grammar``` with the same rules. Then, it iterates over each production in the grammar.If a production contains an ε (empty string), it removes ε from the production and updates the grammar accordingly by removing ε from the list of productions for that variable.
It then iterates over all other productions in the grammar to replace any occurrences of the current variable with ε. This step is necessary to propagate the effect of removing ε from the current variable to other variables that might have used it in their productions.

```python
        updated_grammar = self.rules.copy()
        for variable, productions in self.rules.items():
            if "ε" in productions:
                updated_productions = productions.copy()
                updated_productions.remove("ε")
                updated_grammar[variable] = updated_productions
                # Replace other occurrences of the variable with ε
                for var, prod in self.rules.items():
                    for p in prod:
                        if variable in p:
                            updated_grammar[var].append(p.replace(variable, ""))
```
If the production of the current variable becomes empty after removing ε, it removes the entire production from the grammar.
Finally, it updates the original grammar with the changes made and returns the modified grammar.
```python
                if not updated_productions:
                    updated_grammar.pop(variable, None)
        self.rules = updated_grammar
        return updated_grammar
```
**Eliminating renaming (unit prodcuctions)**

The function ```eliminate_renaming``` is designed to remove unit productions (productions where a single non-terminal directly derives another non-terminal) from a grammar.

It begins by creating a copy of the original grammar to work with, initializing updated_grammar with the same rules.
It iterates over each variable in the grammar.
For each variable, it iterates over its productions.
If a production consists of a single non-terminal (i.e., its length is 1) and that non-terminal is also a key in the grammar (meaning it has its own productions), it replaces the production with the productions of the non-terminal it derives.
Otherwise, if the production does not consist of a single non-terminal, or if the non-terminal is not a key in the grammar, it adds the production as it is to the new set of productions for the current variable.
After processing all productions for a variable, it updates updated_grammar with the new set of productions for that variable.

```python
        updated_grammar = self.rules.copy()
        for variable, productions in self.rules.items():
            new_productions = []
            for production in productions:
                if len(production) == 1 and production in self.rules.keys():
                    new_productions.extend(self.rules[production])
                else:
                    new_productions.append(production)
            updated_grammar[variable] = new_productions
```

It identifies and collects the keys (variables) that have unit productions in their productions. These are the keys that will be removed from the grammar.
It removes the collected keys from updated_grammar, effectively eliminating the unit productions.
Finally, it updates the original grammar with the changes made and returns the modified grammar.

```python
        keys_to_remove = [variable for variable, productions in updated_grammar.items() if
                          any(len(production) == 1 and production in self.rules.keys() for production in productions)]

        for key in keys_to_remove:
            updated_grammar.pop(key)

        self.rules = updated_grammar
        return updated_grammar
```
**Eliminating inaccessible symbols**

The method eliminate_inaccessible removes symbols (variables) from the grammar that are not reachable from the start symbol.

It initializes a set called reachable and adds the start symbol ('S' in this case) to it. This set will keep track of all symbols that are reachable from the start symbol.
It initializes an empty dictionary called updated_grammar to store the updated grammar after removing unreachable symbols.
```python
        reachable = set()
        reachable.add('S')  # Start symbol
        updated_grammar = {}
```
It enters a loop that continues until no new symbols are added to the reachable set.
Inside the loop, it iterates over each variable and its productions in the original grammar.
For each production of a reachable variable, it iterates over the symbols in the production.
If a symbol in the production is itself a variable (i.e., it exists as a key in the grammar), it adds that symbol to the reachable set.
```python
        while True:
            old_len = len(reachable)
            for variable, productions in self.rules.items():
                if variable in reachable:
                    for production in productions:
                        for symbol in production:
                            if symbol in self.rules:
                                reachable.add(symbol)
```
After processing all productions of all reachable variables, it checks if any new symbols have been added to the reachable set since the last iteration. If not, it breaks out of the loop.
Once the loop completes, it iterates over the original grammar again.
For each variable, if it is present in the reachable set, it adds its productions to the updated_grammar.
Finally, it updates the original grammar with the reachable symbols and their productions, and returns the modified grammar.
```python
        for variable, productions in self.rules.items():
            if variable in reachable:
                updated_grammar[variable] = productions
        self.rules = updated_grammar
        return updated_grammar
```
**Eliminating unproductive symbols**

The function ```eliminate_nonproductive``` removes non-productive symbols (variables) from the grammar.
It initializes a set called productive to store the symbols that are determined to be productive.
It initializes a copy of the original grammar as updated_grammar.
It extracts all terminals from the grammar and stores them in a set called terminals.
```python
        productive = set()
        updated_grammar = self.rules.copy()
        terminals = {symbol for productions in self.rules.values() for production in productions for symbol in
                     production if symbol not in self.rules}
```
It enters a loop that continues until no new symbols are added to the productive set.
Inside the loop, it iterates over each variable and its productions in the updated_grammar.
For each production of a variable, it checks if all symbols in the production are either terminals or already determined to be productive. If so, it adds the variable to the productive set.
After processing all productions of all variables, it checks if any new symbols have been added to the productive set since the last iteration. If not, it breaks out of the loop.
```python
        while True:
            old_len = len(productive)
            for variable, productions in updated_grammar.items():
                for production in productions:
                    if all(symbol in productive or symbol in terminals for symbol in production):
                        productive.add(variable)
            if len(productive) == old_len:
                break
```
Once the loop completes, it iterates over the original grammar again.
For each variable, if it is present in the productive set, it keeps its productions in the updated_grammar.
If a variable is not in the productive set, it removes it from the updated_grammar.
Finally, it updates the original grammar with the productive symbols and their productions, and returns the modified grammar.

```python
        for variable, productions in self.rules.items():
            if variable in productive:
                updated_productions = []
                for production in productions:
                    if all(symbol in productive or symbol in terminals for symbol in production):
                        updated_productions.append(production)
                updated_grammar[variable] = updated_productions
            else:
                updated_grammar.pop(variable, None)

        self.rules = updated_grammar
        return updated_grammar
```
**Creating new non-terminals**

The method starts with a predefined alphabet comprising digits, uppercase Latin letters. This diverse set ensures a wide range of potential symbols for new non-terminals, reducing the likelihood of exhausting available symbols even in complex grammars.

Initially, the method attempts to find an unused symbol within the Latin alphabet portion of the alphabet string. It iterates through each character in the alphabet, checking whether it is already present in the non_terminals set of the grammar. If it finds an unused symbol, it adds this symbol to the non_terminals set and returns it for immediate use in the grammar transformation process.
```python
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for letter in alphabet:
            if letter not in self.non_terminals:
                self.non_terminals.append(letter)
                return letter

        for letter in alphabet:
            for num in range(100): 
                new_symbol = f'{letter}{num}'
                if new_symbol not in self.non_terminals:
                    self.non_terminals.append(new_symbol)
                    return new_symbol
```
**Convert to Chomsky Normal Form**
The method ```to_cnf``` converts a given context-free grammar (CFG) to Chomsky Normal Form (CNF). 

It initializes a dictionary ```rhs_to_non_terminal``` to keep track of new non-terminal symbols created during the conversion process.
It creates a list ```old_non_terminals``` containing the existing non-terminal symbols in the grammar.
It initializes a new dictionary ```new_rules``` to store the CNF rules generated during the conversion process.
```python
        rhs_to_non_terminal = {}
        old_non_terminals = list(self.rules)

        new_rules = {}
```
It iterates over each non-terminal symbol in the grammar.
For each non-terminal symbol, it iterates over its productions and converts them to CNF:
+ If a production has more than two symbols, it extracts the first two symbols and replaces them with a new non-terminal symbol.
  + If the combination of the first two symbols already has a corresponding new non-terminal symbol in ```rhs_to_non_terminal```, it uses that symbol. Otherwise, it generates a new non-terminal symbol using the ```create_new_non_terminal method``` and adds it to ```rhs_to_non_terminal```.
  + It replaces the first two symbols in the production with the new non-terminal symbol.
+ It adds the modified production to the set of productions for the current non-terminal symbol in ```new_rules```.

```python

        for non_terminal in list(self.rules):
            new_rules[non_terminal] = set()
            for production in self.rules[non_terminal]:
                while len(production) > 2:
                    # Extract the first two symbols
                    first_two_symbols = production[:2]

                    if first_two_symbols in rhs_to_non_terminal:
                        new_non_terminal = rhs_to_non_terminal[first_two_symbols]
                    else:
                        new_non_terminal = self.create_new_non_terminal()
                        new_rules[new_non_terminal] = {first_two_symbols}
                        rhs_to_non_terminal[first_two_symbols] = new_non_terminal
                    # Replace the first two symbols with the new non-terminal
                    production = new_non_terminal + production[2:]

                new_rules[non_terminal].add(production)
```
It handles mixed productions, where a production contains both terminals and non-terminals:
For each production in ```new_rules```, if a production has exactly two symbols and one of them is a terminal, it replaces the terminal with a new non-terminal symbol.
If the terminal already has a corresponding new non-terminal symbol in ```rhs_to_non_termina```l, it uses that symbol. Otherwise, it generates a new non-terminal symbol and adds it to ```rhs_to_non_terminal```.
It replaces the terminal with the new non-terminal symbol and adds the modified production to the set of productions for the current non-terminal symbol in ```new_rules```.
It reorders the rules in ```new_rules``` to match the original order of non-terminal symbols (```old_non_terminals```) followed by any new non-terminal symbols created during the conversion process.
```python
        for non_terminal, productions in list(new_rules.items()):
            temp_productions = productions.copy()
            for production in temp_productions:
                if len(production) == 2 and any(symbol in self.terminals for symbol in production):
                    new_production = []
                    for symbol in production:
                        if symbol in self.terminals:
                            if symbol in rhs_to_non_terminal:
                                new_non_terminal = rhs_to_non_terminal[symbol]
                            else:
                                new_non_terminal = self.create_new_non_terminal()
                                new_rules[new_non_terminal] = {symbol}
                                rhs_to_non_terminal[symbol] = new_non_terminal
                            new_production.append(new_non_terminal)
                        else:
                            new_production.append(symbol)
                    productions.remove(production)
                    productions.add(''.join(new_production))
```
It updates the rules attribute of the grammar object with the CNF rules stored in new_rules.
Finally, it returns the modified grammar in CNF.
```python
        self.rules = {nt: new_rules[nt] for nt in old_non_terminals +
                      list(set(new_rules) - set(old_non_terminals))}

        # Return the modified grammar
        return self.rules

```

### Unit Testing
The ```UnitTests.py``` file contains unit tests designed to verify the correctness of the Grammar class's functionality to transform an arbitrary context-free grammar into Chomsky Normal Form. These tests are implemented using Python's unittest framework. As setup, the tests create instances of the Grammar class with the grammar from variant 12. Through a series of targeted unit tests, it methodically verifies that each step of the transformation process aligns with the theoretical requirements of CNF and that the final transformed grammar is indeed in the correct form. The tests cover the elimination of epsilon productions, renaming productions, inaccessible symbols, and non-productive symbols, as well as the conversion to Chomsky Normal Form.
## Conclusions / Screenshots / Results

**Results**
Result for Chomsky Normal Form (variant 12):
![image](https://github.com/nelldino/DSL-labs/assets/120444803/07426ade-fe67-4325-acec-e79c2fdadff7)

Result for Chomsky Normal Form (variant 3):
![image](https://github.com/nelldino/DSL-labs/assets/120444803/17d3636b-50d2-422b-a1b7-f1f8d9da56d2)
