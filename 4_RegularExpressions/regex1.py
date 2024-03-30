import random

def generate_string():
    string = random.choice(['S', 'T'])
    string += random.choice(['U', 'V'])
    string += 'W' * random.randint(0, 5)
    string += 'Y' * random.randint(1, 5)  # Ensure at least one Y
    string += '24'
    return string

# Generate 5 strings that match the regular expression
regex1 = "(S|T)(U|V)W*(Y^+)24"
for _ in range(5):
    generated_string = generate_string()
    print("Generated string:", generated_string)
