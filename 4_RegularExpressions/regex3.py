import random

def generate_string():
    string = 'R' * random.randint(0, 5)
    string += 'S'
    string += random.choice(['T', 'U', 'V'])
    string += 'W'
    string += random.choice(['X', 'Y', 'Z'])
    string += random.choice(['X', 'Y', 'Z'])
    return string

# Generate 5 strings that match the regular expression
regex1 = "R*S(T|U|V)W(X|Y|Z)^2"
for _ in range(5):
    generated_string = generate_string()
    print("Generated string:", generated_string)
