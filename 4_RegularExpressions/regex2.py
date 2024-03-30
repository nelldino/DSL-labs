import random

def generate_string():
    string = 'L'
    string += random.choice(['M', 'N'])
    string += 'O' * 3
    p_count = random.randint(0, 5)
    string += 'P' * p_count
    string += 'Q'
    string += random.choice(['2', '3'])
    return string

# Generate 5 strings that match the regular expression
regex1 = "L(M|N)O^3P*Q(2|3)"
for _ in range(5):
    generated_string = generate_string()
    print("Generated string:", generated_string)
