from dataclasses import dataclass
from typing import List, Optional
from lexer import Token

@dataclass
class ASTNode:
    pass

@dataclass
class VarDecl(ASTNode):
    type: str
    name: str
    value: Optional[ASTNode]

@dataclass
class Assignment(ASTNode):
    name: str
    value: ASTNode

@dataclass
class BinOp(ASTNode):
    left: ASTNode
    op: str
    right: ASTNode

@dataclass
class Number(ASTNode):
    value: str

@dataclass
class Identifier(ASTNode):
    name: str

@dataclass
class IfStmt(ASTNode):
    condition: ASTNode
    body: List[ASTNode]

@dataclass
class ForStmt(ASTNode):
    init: ASTNode
    condition: ASTNode
    update: ASTNode
    body: List[ASTNode]

@dataclass
class Function(ASTNode):
    return_type: str
    name: str
    params: List[VarDecl]
    body: List[ASTNode]

class Parser:
    def __init__(self, tokens: List[Token]):
        self.tokens = tokens
        self.pos = 0

    def peek(self) -> Optional[Token]:
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected_type: str) -> Token:
        token = self.peek()
        if token and token.type == expected_type:
            self.pos += 1
            return token
        raise SyntaxError(f"Expected {expected_type}, got {token.type if token else 'EOF'} at position {self.pos}")

    def parse(self) -> List[ASTNode]:
        nodes = []
        while self.peek():
            if self.peek().type == 'KEYWORD' and self.peek().value in ('int', 'float', 'void'):
                if self.peek().value == 'void' or (self.pos + 2 < len(self.tokens) and self.tokens[self.pos + 1].type == 'ID' and self.tokens[self.pos + 2].type == '('):
                    nodes.append(self.parse_function())
                else:
                    nodes.extend(self.parse_var_decls())  # Changed to handle multiple declarations
            elif self.peek().type == 'KEYWORD' and self.peek().value == 'if':
                nodes.append(self.parse_if_stmt())
            elif self.peek().type == 'KEYWORD' and self.peek().value == 'for':
                nodes.append(self.parse_for_stmt())
            elif self.peek().type == 'ID':
                nodes.append(self.parse_assignment())
            else:
                raise SyntaxError(f"Unexpected token: {self.peek().value} at position {self.pos}")
        return nodes

    def parse_var_decls(self) -> List[VarDecl]:
        type_token = self.consume('KEYWORD')
        decls = []
        while True:
            name = self.consume('ID').value
            value = None
            if self.peek() and self.peek().type == 'OP' and self.peek().value == '=':
                self.consume('OP')
                value = self.parse_expression()
            decls.append(VarDecl(type_token.value, name, value))
            if self.peek() and self.peek().type == 'COMMA':
                self.consume('COMMA')
            else:
                break
        self.consume(';')
        return decls

    def parse_assignment(self) -> Assignment:
        name = self.consume('ID').value
        self.consume('OP')  # =
        value = self.parse_expression()
        self.consume(';')
        return Assignment(name, value)

    def parse_function(self) -> Function:
        return_type = self.consume('KEYWORD').value
        name = self.consume('ID').value
        self.consume('(')
        params = []
        if self.peek() and self.peek().type != ')':
            params.extend(self.parse_var_decls())
            while self.peek() and self.peek().type == 'COMMA':
                self.consume('COMMA')
                params.extend(self.parse_var_decls())
        self.consume(')')
        self.consume('{')
        body = []
        while self.peek() and self.peek().type != '}':
            if self.peek().type == 'KEYWORD' and self.peek().value in ('int', 'float', 'void'):
                body.extend(self.parse_var_decls())
            elif self.peek().type == 'ID':
                body.append(self.parse_assignment())
            else:
                raise SyntaxError(f"Unexpected token in function body: {self.peek().value}")
        self.consume('}')
        return Function(return_type, name, params, body)

    def parse_if_stmt(self) -> IfStmt:
        self.consume('KEYWORD')  # if
        self.consume('(')
        condition = self.parse_expression()
        self.consume(')')
        self.consume('{')
        body = []
        while self.peek() and self.peek().type != '}':
            if self.peek().type == 'KEYWORD' and self.peek().value in ('int', 'float', 'void'):
                body.extend(self.parse_var_decls())
            elif self.peek().type == 'ID':
                body.append(self.parse_assignment())
            else:
                raise SyntaxError(f"Unexpected token in if body: {self.peek().value}")
        self.consume('}')
        return IfStmt(condition, body)

    def parse_for_stmt(self) -> ForStmt:
        self.consume('KEYWORD')  # for
        self.consume('(')
        init = self.parse_var_decls()[0]  # Take first declaration for simplicity
        condition = self.parse_expression()
        self.consume(';')
        update = self.parse_expression()
        self.consume(')')
        self.consume('{')
        body = []
        while self.peek() and self.peek().type != '}':
            if self.peek().type == 'KEYWORD' and self.peek().value in ('int', 'float', 'void'):
                body.extend(self.parse_var_decls())
            elif self.peek().type == 'ID':
                body.append(self.parse_assignment())
            else:
                raise SyntaxError(f"Unexpected token in for body: {self.peek().value}")
        self.consume('}')
        return ForStmt(init, condition, update, body)

    def parse_expression(self) -> ASTNode:
        left = self.parse_term()
        if self.peek() and self.peek().type == 'OP' and self.peek().value in ('+', '-', '*', '/'):
            op = self.consume('OP').value
            right = self.parse_term()
            return BinOp(left, op, right)
        return left

    def parse_term(self) -> ASTNode:
        token = self.peek()
        if token.type == 'NUMBER':
            self.consume('NUMBER')
            return Number(token.value)
        elif token.type == 'ID':
            self.consume('ID')
            return Identifier(token.name)
        raise SyntaxError(f"Expected NUMBER or ID, got {token.type} at position {self.pos}")