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

<img width="548" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/991c00a2-8d53-48e7-a019-82e15e9a147f">

In my variant, I have 3 different regular expressions and made a program for each of them. 

First regular expression:

    regex1 = "(S|T)(U|V)W*(Y^+)24"

I have a function for generating a string:

    def generate_string():
        string = random.choice(['S', 'T'])
        string += random.choice(['U', 'V'])
        string += 'W' * random.randint(0, 5)
        string += 'Y' * random.randint(1, 5)  # Ensure at least one Y
        string += '24'
    return string
'|' means either first or second characther will appear, which is why I used a random.choice for S, T, U and V. '*' symbol means that the preceding character will have 0 or more occurences ( according to the lab task, it will have at most 5 occurances). The '+' sign matches one or more occurences of the preceding character.'24' is a character that have to appear in each generated string.

Second regular expression:

    regex2 = "L(M|N)O^3P*Q(2|3)"

The function that will generate the strings:

    def generate_string():
        string = 'L'
        string += random.choice(['M', 'N'])
        string += 'O' * 3
        p_count = random.randint(0, 5)
        string += 'P' * p_count
        string += 'Q'
        string += random.choice(['2', '3'])
     return string

Here I applied the same logic as for the first regular expression. In this case, we have the '^3' symbol, which means that the preceding character must have three occurences.

Third regular expression:

    regex3 = "R*S(T|U|V)W(X|Y|Z)^2"

The function that will generate the strings:

      def generate_string():
          string = 'R' * random.randint(0, 5)
          string += 'S'
          string += random.choice(['T', 'U', 'V'])
          string += 'W'
          string += random.choice(['X', 'Y', 'Z'])
          string += random.choice(['X', 'Y', 'Z'])
       return string

In this case, 'R' will have 0 or more occurences. 'S' character must appear in each generated string. Then 'T', 'U', or 'V' can occur in each string. 'W' is another characther that has to appear. Then, 'X', 'Y' or 'Z' might be generated and '^2' means that it has to appear twice.

## Conclusions / Screenshots / Results

**Results**

Results for first regular expression:

<img width="200" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/12b56e7a-512d-45aa-9800-0f706dd26a27">
<img width="196" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/da7315cd-c83e-461a-be94-0e61c424c0f0">

Results for second regular expression:

<img width="190" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/429348b0-962a-4078-a2b2-94d062874da5">
<img width="191" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/2b32a84a-b71f-4665-8228-77ceda7a635a">

Results for third generated expression:

<img width="188" alt="Screenshot 2024-03-30 203808" src="https://github.com/nelldino/DSL-labs/assets/120444803/b4bd7d3c-405e-4a2d-81b6-15cf0609d8a6">
<img width="187" alt="image" src="https://github.com/nelldino/DSL-labs/assets/120444803/e2856619-6dca-4445-91d6-0b9cf07a1ae4">

