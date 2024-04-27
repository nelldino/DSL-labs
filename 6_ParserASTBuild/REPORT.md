# Topic: Parser & Building an Abstract Syntax Tree

### Course: Formal Languages & Finite Automata
### Author: Nelli Garbuz

----

## Overview
A parser is a program or a component of a program that analyzes the syntax of input data to determine its structure according to a specified grammar or set of rules. In computer science, parsers are commonly used in areas such as compiler construction, natural language processing, and data processing.

In the context of programming languages, parsers take source code written in a particular language and break it down into its constituent parts, such as tokens or abstract syntax trees (ASTs), which can then be further processed by other components of a compiler or interpreter. Parsers typically validate whether the input conforms to the syntax rules of the language and may also perform some initial semantic analysis.


AST stands for Abstract Syntax Tree. It's a hierarchical representation of the syntactic structure of source code in a programming language. When source code is parsed, it's converted into an AST, which abstracts away from the specific details of the source code's textual representation and focuses on its structure.

In an AST, each node represents a syntactic construct in the code, such as expressions, statements, declarations, etc. The relationships between nodes represent the syntactic relationships between the corresponding constructs in the code. 
## Objectives:
1. Get familiar with parsing, what it is and how it can be programmed [1].
2. Get familiar with the concept of AST [2].
3. In addition to what has been done in the 3rd lab work do the following:
   1. In case you didn't have a type that denotes the possible types of tokens you need to:
      1. Have a type __*TokenType*__ (like an enum) that can be used in the lexical analysis to categorize the tokens. 
      2. Please use regular expressions to identify the type of the token.
   2. Implement the necessary data structures for an AST that could be used for the text you have processed in the 3rd lab work.
   3. Implement a simple parser program that could extract the syntactic information from the input text.


## Implementation description:

**Token Definition**

```TokenType``` enum defines distinct categories of tokens that the lexer can identify. Each enum member represents a specific type of token, such as keywords, variables, strings, numbers, etc. Enums provide a clear and structured way to categorize tokens.

 ```token_patterns ``` is a list of tuples  each specifying a token type and a corresponding regular expression pattern. Regular expressions are used to match specific patterns in the input string, enabling the lexer to recognize and tokenize different parts of the DSL.
 ```python
class TokenType(enum.Enum):
    KEYWORD = 'KEYWORD'
    VARIABLE = 'VARIABLE'
    STRING = 'STRING'
    NUMBER = 'NUMBER'
    EQUALS = 'EQUALS'
    COMMA = 'COMMA'
    LPAREN = 'LPAREN'
    RPAREN = 'RPAREN'
    LBRACKET = 'LBRACKET'
    RBRACKET = 'RBRACKET'
    NEWLINE = 'NEWLINE'
    EOF = 'EOF'

token_patterns = [
    (TokenType.STRING, r'"[^"]*"'),
    (TokenType.NUMBER, r'\b\d+\b'),
    (TokenType.KEYWORD, r'\b(send|attach|template|email|cc|bcc|subject|body)\b'),
    (TokenType.VARIABLE, r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
    (TokenType.EQUALS, r'='),
    (TokenType.COMMA, r','),
    (TokenType.LPAREN, r'\('),
    (TokenType.RPAREN, r'\)'),
    (TokenType.LBRACKET, r'\['),
    (TokenType.RBRACKET, r'\]'),
    (TokenType.NEWLINE, r'\n')
]
 ```
**Token Class**

 ```Token``` class encapsulates individual tokens produced during the lexical analysis phase. It serves as a data structure to represent each token's type and value.
 ```__init__``` method initializes a Token object with a given type and value.
  ```__str__``` ```__repr__```methods override the default string representation of a Token object, providing a human-readable representation for debugging and logging purposes.
```python
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type.value}, {self.value})'

    def __repr__(self):
        return self.__str__()
```
**ASTNode Class**

The ```ASTNode``` class represents nodes in the Abstract Syntax Tree (AST) constructed during parsing. AST nodes capture the hierarchical structure of the DSL's syntax.
```__init__```  method initializes an AST node with a specified type and value. Additionally, it initializes an empty list to store child nodes.
add_child: This method appends a child node to the list of children for the current node. It facilitates the construction of the AST hierarchy by adding child nodes to parent nodes.
```python
class ASTNode:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)
```
**AST Class**

The AST class manages the construction and manipulation of the Abstract Syntax Tree (AST) for the DSL.
```__init__```method initializes an empty AST with no root node.
```insert```method inserts a node into the AST. If the tree is empty, the inserted node becomes the root. Otherwise, the node is added as a child of an existing node.
```visualize``` method generates a graphical representation of the AST using the Graphviz library. It allows developers to visualize the structure of the AST, aiding in understanding and debugging the parsing process.
```python
class AST:
    def __init__(self):
        self.root = None

    def insert(self, node):
        if self.root is None:
            self.root = node
        else:
            self.root.add_child(node)

    def visualize(self):
        dot = Digraph()
        self._visualize(self.root, dot)
        dot.render('ast', view=True)

    def _visualize(self, node, dot, parent=None):
        if node is None:
            return
        node_id = f'{id(node)}'
        label = f'{node.type.value}: {node.value}'
        dot.node(node_id, label)
        if parent:
            dot.edge(parent, node_id)
        for child in node.children:
            self._visualize(child, dot, node_id)
```

**Lexical Analysis**

The lex function performs lexical analysis on the input string, converting it into a sequence of tokens.
It iterates over the input string character by character, attempting to match each character sequence against the defined token patterns.
When a match is found, a corresponding Token object is created and added to the list of tokens.
The function continues until it reaches the end of the input string, ensuring that all characters are processed.
```python
def lex(input_string):
    tokens = []
    position = 0
    while position < len(input_string):
        match = None
        for token_type, regex in token_patterns:
            regex = re.compile(regex)
            match = regex.match(input_string, position)
            if match:
                tokens.append(Token(token_type, match.group()))
                position = match.end()
                break
        if not match:
            position += 1  # Skip character if no match
    tokens.append(Token(TokenType.EOF, None))
    return tokens
```

**Parsing**

The parse function constructs the Abstract Syntax Tree (AST) from the sequence of tokens produced by the lexer.
It iterates over the tokens, identifying keywords and their associated values based on the DSL's syntax rules.
For each keyword encountered, the function creates an AST node representing the keyword and adds child nodes for its associated values.
Different types of values (such as strings and numbers) are handled appropriately, with corresponding AST nodes created for each value type.

**Vizualization and test**

The test function serves as a demonstration of the lexer and parser in action.
It defines an example DSL input string.
The input string is passed through the lexer (lex function) to produce a sequence of tokens.
The token sequence is then parsed (parse function) to construct the corresponding AST.
Finally, the AST is visualized (visualize method) using the Graphviz library to provide a graphical representation of its structure.

## Conclusions/ Screenshots/ Results:
![image](https://github.com/nelldino/DSL-labs/assets/120444803/773704e2-5586-44f0-a793-3007df82296d)
![image](https://github.com/nelldino/DSL-labs/assets/120444803/78bb5d19-90f2-4de5-ade8-804b1ba95994)
