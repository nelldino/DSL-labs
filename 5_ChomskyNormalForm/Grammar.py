# Variant12
class Grammar:
    def __init__(self, non_terminals, terminals, rules):
        self.non_terminals = non_terminals
        self.terminals = terminals
        self.rules = rules

    def eliminate_empty_string(self):
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
                # If the production becomes empty, remove it entirely
                if not updated_productions:
                    updated_grammar.pop(variable, None)
        self.rules = updated_grammar
        return updated_grammar

    def eliminate_renaming(self):
        updated_grammar = self.rules.copy()
        for variable, productions in self.rules.items():
            new_productions = []
            for production in productions:
                if len(production) == 1 and production in self.rules.keys():
                    new_productions.extend(self.rules[production])
                else:
                    new_productions.append(production)
            updated_grammar[variable] = new_productions

        keys_to_remove = [variable for variable, productions in updated_grammar.items() if
                          any(len(production) == 1 and production in self.rules.keys() for production in productions)]

        for key in keys_to_remove:
            updated_grammar.pop(key)

        self.rules = updated_grammar
        return updated_grammar

    def eliminate_inaccessible(self):
        reachable = set()
        reachable.add('S')  # Start symbol
        updated_grammar = {}
        while True:
            old_len = len(reachable)
            for variable, productions in self.rules.items():
                if variable in reachable:
                    for production in productions:
                        for symbol in production:
                            if symbol in self.rules:
                                reachable.add(symbol)
            if len(reachable) == old_len:
                break
        for variable, productions in self.rules.items():
            if variable in reachable:
                updated_grammar[variable] = productions
        self.rules = updated_grammar
        return updated_grammar

    def eliminate_nonproductive(self):
        productive = set()
        updated_grammar = self.rules.copy()
        terminals = {symbol for productions in self.rules.values() for production in productions for symbol in
                     production if symbol not in self.rules}

        while True:
            old_len = len(productive)
            for variable, productions in updated_grammar.items():
                for production in productions:
                    if all(symbol in productive or symbol in terminals for symbol in production):
                        productive.add(variable)
            if len(productive) == old_len:
                break

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

    def create_new_non_terminal(self):
        alphabet = '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        # First, try to find a single unused letter from the Latin alphabet
        for letter in alphabet:
            if letter not in self.non_terminals:
                self.non_terminals.append(letter)
                return letter

        # If all single letters are used, start combining them with numbers
        for letter in alphabet:
            for num in range(100):  # Assuming 100 is enough to avoid conflicts
                new_symbol = f'{letter}{num}'
                if new_symbol not in self.non_terminals:
                    self.non_terminals.append(new_symbol)
                    return new_symbol

        # If all combinations are exhausted, raise an error
        raise ValueError("Exhausted all possible non-terminal symbols.")

    def to_cnf(self, print_steps=True):
        # Additional steps to convert to CNF
        rhs_to_non_terminal = {}
        old_non_terminals = list(self.rules)

        new_rules = {}
        for non_terminal in list(self.rules):
            new_rules[non_terminal] = set()
            for production in self.rules[non_terminal]:
                # Case for productions with more than 2 symbols
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

        # Handle mixed productions
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

        # Reorder the rules to match the original order + new non-terminals
        self.rules = {nt: new_rules[nt] for nt in old_non_terminals +
                      list(set(new_rules) - set(old_non_terminals))}

        # Return the modified grammar
        return self.rules

    def print_grammar(self):
        for variable, productions in self.rules.items():
            print(f"{variable} -> {' | '.join(productions)}")


if __name__ == "__main__":
    non_terminals = ['S', 'A', 'B', 'C', 'E']
    terminals = ['a', 'b']
    grammar_rules = {
        'S': ['A'],
        'A': ['aX', 'bX'],
        'X': ['BX', 'ε', 'b'],
        'B': ['AD'],
        'D': ['aD'],
        'C': ['Ca']
    }

    grammar = Grammar(non_terminals, terminals, grammar_rules)

    print("Original Grammar:")
    grammar.print_grammar()
    print("\nAfter eliminating empty string productions:")
    grammar.eliminate_empty_string()
    grammar.print_grammar()
    print("\nAfter eliminating renaming:")
    grammar.eliminate_renaming()
    grammar.print_grammar()
    print("\nAfter eliminating inaccessible symbols:")
    grammar.eliminate_inaccessible()
    grammar.print_grammar()
    print("\nAfter eliminating non-productive symbols:")
    grammar.eliminate_nonproductive()
    grammar.print_grammar()
    print("\nAfter CNF:")
    grammar.to_cnf()
    grammar.print_grammar()