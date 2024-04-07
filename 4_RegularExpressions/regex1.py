import random

def generate_string(regex):
    generated_string = ''
    i = 0
    while i < len(regex):
        char = regex[i]
        if char == '(':
            # Find the matching closing parenthesis
            closing_index = regex.find(')', i)
            # Extract the substring within the parentheses
            group = regex[i+1:closing_index]
            # Choose a character from the group
            chosen_char = random.choice(group.split('|'))
            generated_string += chosen_char
            print(f"Added {chosen_char}->{generated_string}")
            print("Current string:", generated_string)
            i = closing_index + 1  # Move to the next character after ')'
        elif char == '*':
            # Zero occurrences up to 5 occurrences
            repetitions = random.randint(0, 4)
            new_char = generated_string[-1] * repetitions if generated_string else ''
            generated_string += new_char
            print(f"Added {new_char}->{generated_string}")
            print("Current string:", generated_string)
            i += 1
        elif char == '+':
            # One occurrence up to 5 occurrences
            repetitions = random.randint(1, 4)
            new_char = generated_string[-1] * repetitions if generated_string else ''
            generated_string += new_char
            print(f"Added {new_char}->{generated_string}")
            print("Current string:", generated_string)
            i += 1
        elif char.startswith('^'):
            # Repeat the preceding character 'n' times
            repetitions = int(char[1:])
            new_char = generated_string[-1] * repetitions
            generated_string += new_char
            print(f"Added {new_char}->{generated_string}")
            print("Current string:", generated_string)
            i += 1
        elif char not in '()|':
            # Append the character as is (excluding parentheses and pipe symbol)
            generated_string += char
            print(f"Added {char}->{generated_string}")
            print("Current string:", generated_string)
            i += 1
        else:
            # Move to the next character if it's a symbol
            i += 1
    return generated_string

regex = "(S|T)(U|V)W*Y+24"
print("Regular Expression:", regex)
generated_string = generate_string(regex)
print("\nFinal Generated String:", generated_string)
