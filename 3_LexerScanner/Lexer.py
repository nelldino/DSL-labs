import re

# Token types
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

# Token class
class Token:
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return f'Token({self.type}, {self.value})'

    def __repr__(self):
        return self.__str__()

# Lexer class
class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = self.text[self.pos]
        self.keywords = ['send', 'attach', 'template', 'cc', 'bcc', 'subject', 'body']

    def error(self):
        raise Exception('Invalid character')

    def advance(self):
        self.pos += 1
        if self.pos < len(self.text):
            self.current_char = self.text[self.pos]
        else:
            self.current_char = None

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        result = ''
        while self.current_char is not None and self.current_char != '"':
            result += self.current_char
            self.advance()
        self.advance()  # Skip closing quote
        return result

    def variable(self):
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        return result

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char == '=':
                self.advance()
                return Token(EQUALS, '=')

            if self.current_char == ',':
                self.advance()
                return Token(COMMA, ',')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')

            if self.current_char == '[':
                self.advance()
                return Token(LBRACKET, '[')

            if self.current_char == ']':
                self.advance()
                return Token(RBRACKET, ']')

            if self.current_char == '\n':
                self.advance()
                return Token(NEWLINE, '\n')

            if self.current_char.isdigit():
                return Token(NUMBER, self.integer())

            if self.current_char == '"':
                self.advance()
                return Token(STRING, self.string())

            if self.current_char.isalpha():
                token_value = self.variable()
                if token_value.lower() in self.keywords:
                    return Token(KEYWORD, token_value.lower())
                else:
                    return Token(VARIABLE, token_value)

            self.error()

        return Token(EOF, None)

# Example of a mail
text = """
send(
    email="edumitrucretu@example.com",
    cc=["cc1@example.com", "cc2@example.com"],
    bcc=["bcc1@example.com", "bcc2@example.com"],
    subject="Important Email",
    body="LFA laboratory work3"
)
attach(file="lab_report.pdf")
template(name="report_template")
"""

lexer = Lexer(text)
token = lexer.get_next_token()
while token.type != EOF:
    print(token)
    token = lexer.get_next_token()
