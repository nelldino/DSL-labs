# Regular expressions

### Course: Formal Languages & Finite Automata
### Author: Nelli Garbuz

----

## Overview

Regular expressions, often abbreviated as regex or regexp, are sequences of characters that define a search pattern. They are a powerful tool used in computer science, particularly in string manipulation tasks, such as searching, parsing, and replacing text. Originally developed in theoretical computer science and formal language theory, regular expressions have found widespread use in programming languages, text editors, command-line utilities, and various other software applications.

At their core, regular expressions consist of literal characters (e.g., letters, digits, punctuation marks) and metacharacters (special symbols with predefined meanings). These metacharacters provide a way to specify flexible patterns rather than fixed strings. Some common metacharacters include:

Usually such patterns are used by string-searching algorithms for "find" or "find and replace" operations on strings, or for input validation. Also, Regex can be used any time you need to query string-based data, such as, analyzing command line output
, parsing user input
, examining server or program logs
, handling text files with a consistent syntax, like a CSV
, reading configuration files
, searching and refactoring code

## Objectives:

1.Write and cover what regular expressions are, what they are used for;

Below you will find 3 complex regular expressions per each variant. Take a variant depending on your number in the list of students and do the following:

a. Write a code that will generate valid combinations of symbols conform given regular expressions (examples will be shown).

b. In case you have an example, where symbol may be written undefined number of times, take a limit of 5 times (to evade generation of extremely long combinations);

c. Bonus point: write a function that will show sequence of processing regular expression (like, what you do first, second and so on)

## Implementation description

**Variant 4** 

![image](https://github.com/nelldino/DSL-labs/assets/120444803/7b0ab7d7-9695-47f2-aad9-8d1a5bfa7bd8)


In my variant, I have 3 different regular expressions, but since all of the regular expression above have the same symbols, I will explain how the code works for the first regex.

Some of the symbols that my code will handle are:

"|" - either first character will be output, etiher the next one

"*" - zero or more occurences (up to 5) of a character

"+" - one or more occurences (up to 5) of a character

"^n" - n occurences of the character

First regular expression:

    regex1 = "(S|T)(U|V)W*(Y^+)24"

Whenever the | symbol is present, it indicates alternative options. In the regular expression, characters to choose from are isolated within parentheses.
The code first handles and searches for the matching parentheses.
If the current character is '(', it finds the closing parenthesis ')' to determine the group.
It then chooses a character randomly from the group defined within the parentheses separated by '|'.
The chosen character is appended to the generated_string.

        if char == '(':
            closing_index = regex.find(')', i)
            group = regex[i+1:closing_index]
            chosen_char = random.choice(group.split('|'))
            generated_string += chosen_char

The * symbol signifies zero or more occurrences of the preceding character.
A random integer between 0 and 4 is generated, representing the number of repetitions.
The last character of the generated string is then repeated by the determined number of repetitions and appended to the generated string.
If generated_string is empty, an empty string is appended.

        repetitions = random.randint(0, 4)
        generated_string += generated_string[-1] * repetitions if generated_string else ''

The + symbol represents one or more occurrences of the preceding character.
Similar to *, a random integer between 1 and 4 is generated, indicating the number of repetitions.
The last character of the generated string is repeated by the determined number of repetitions and appended to the generated string.
If generated_string is empty, an empty string is appended.

            repetitions = random.randint(1, 4)
            generated_string += generated_string[-1] * repetitions if generated_string else ''

This pattern signifies exactly n occurrences of the preceding character.
The code checks if there is at least one more character in the regex after the current character to avoid index out-of-range errors.
It then checks if the next character in the regular expression is a digit.
If both conditions are true, the digit character after the current character is converted into an integer (n) and assigned to the repetitions variable.
Next, the last character of the string (generated_string[-1]) will be repeated n - 1 times, since one occurrence of the character was already added.

            if i + 1 < len(regex) and regex[i + 1].isdigit():
                repetitions = int(regex[i + 1])
                generated_string += generated_string[-1] * (repetitions - 1)

Additionally, the code includes print statements to show step-by-step how the characters are appended to the generation of the strings, providing clarity on the progression of string generation.

            print(f"Added {chosen_char}->{generated_string}")
            print("Current string:", generated_string)
## Conclusions / Screenshots / Results

**Results**

Results for first regular expression:

![image](https://github.com/nelldino/DSL-labs/assets/120444803/832b0c32-91c9-443f-a2c9-7f755799c0cf)
![image](https://github.com/nelldino/DSL-labs/assets/120444803/11be2437-d6e5-48a4-8942-62ddd27a32a3)

Results for second regular expression:

![image](https://github.com/nelldino/DSL-labs/assets/120444803/3d0101e4-9c2f-41da-8e07-5145fee42671)
![image](https://github.com/nelldino/DSL-labs/assets/120444803/56c93a94-13bf-4710-a3ae-080cea428103)

Results for third generated expression:

![image](https://github.com/nelldino/DSL-labs/assets/120444803/1907ba35-bb75-497f-8800-f7c4f7ec42b7)
![image](https://github.com/nelldino/DSL-labs/assets/120444803/f9fcef76-1f66-4538-9b4b-978ac4eda0ce)


