import enum
import re
from graphviz import Digraph

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

class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type.value}, {self.value})'

    def __repr__(self):
        return self.__str__()

class ASTNode:
    def __init__(self, type, value):
        self.type = type
        self.value = value
        self.children = []

    def add_child(self, child_node):
        self.children.append(child_node)

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

def parse(tokens):
    ast = AST()
    current_keyword = None
    current_values = {}
    keyword_stack = []

    for token in tokens:
        if token.type == TokenType.KEYWORD:
            current_keyword = token.value
            keyword_stack.append(current_keyword)
        elif token.type == TokenType.EQUALS:
            pass  # Ignore the equals sign
        elif token.type == TokenType.STRING or token.type == TokenType.VARIABLE:
            current_value = token.value.strip('"\', ')  # Strip quotes and whitespace
            if current_keyword and current_value:
                if current_keyword not in current_values:
                    current_values[current_keyword] = []
                current_values[current_keyword].append(current_value)
        elif token.type == TokenType.NUMBER:
            current_value = token.value
            if current_keyword and current_value:
                if current_keyword not in current_values:
                    current_values[current_keyword] = []
                current_values[current_keyword].append(current_value)

    # Construct AST nodes for each keyword and its associated values
    for keyword in keyword_stack:
        keyword_node = ASTNode(TokenType.KEYWORD, keyword)
        values = current_values.get(keyword, [])
        for value in values:
            if isinstance(value, int) or (isinstance(value, str) and value.isdigit()):
                # Handle numbers
                value_node = ASTNode(TokenType.NUMBER, value)
            elif isinstance(value, str) and value.startswith('"') and value.endswith('"'):
                # Handle strings enclosed in double quotes
                value_node = ASTNode(TokenType.STRING, value.strip('"'))
            elif isinstance(value, str) and value.startswith("'") and value.endswith("'"):
                # Handle strings enclosed in single quotes
                value_node = ASTNode(TokenType.STRING, value.strip("'"))
            else:
                # Handle other string values
                value_node = ASTNode(TokenType.STRING, value)
            keyword_node.add_child(value_node)
        ast.insert(keyword_node)

    return ast


def test():
    input_string = """
    send(
        email="dcretu@example.com",
        cc=["cc1@example.com", "cc2@example.com"],
        subject=Important Email,
        body=LFA laboratory work 3
    )
    """
    print("Input string:", input_string)

    # Lexical analysis
    tokens = lex(input_string)
    print("Tokens:", tokens)

    # Parsing
    ast = parse(tokens)
    print("AST construction complete.")
    ast.visualize()

test()