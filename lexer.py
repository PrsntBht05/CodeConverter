from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str
    name: str = None  # Used for identifiers

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.pos = 0
        self.tokens: List[Token] = []

    def tokenize(self) -> List[Token]:
        while self.pos < len(self.code):
            char = self.code[self.pos]
            if char.isspace():
                self.pos += 1
                continue
            elif char.isalpha() or char == '_':
                self.tokens.append(self.read_identifier_or_keyword())
            elif char.isdigit():
                self.tokens.append(self.read_number())
            elif char in '+-*/=':
                self.tokens.append(Token(type='OP', value=char))
                self.pos += 1
            elif char in '();{}':
                self.tokens.append(Token(type=char, value=char))
                self.pos += 1
            elif char == ',':
                self.tokens.append(Token(type='COMMA', value=char))
                self.pos += 1
            else:
                raise ValueError(f"Unexpected character: {char}")
        return self.tokens

    def read_identifier_or_keyword(self) -> Token:
        start = self.pos
        while self.pos < len(self.code) and (self.code[self.pos].isalnum() or self.code[self.pos] == '_'):
            self.pos += 1
        value = self.code[start:self.pos]
        if value in ('int', 'float', 'void', 'if', 'for'):
            return Token(type='KEYWORD', value=value)
        return Token(type='ID', value=value, name=value)

    def read_number(self) -> Token:
        start = self.pos
        while self.pos < len(self.code) and (self.code[self.pos].isdigit() or self.code[self.pos] == '.'):
            self.pos += 1
        return Token(type='NUMBER', value=self.code[start:self.pos])