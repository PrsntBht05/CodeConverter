from my_parser import ASTNode, VarDecl, Assignment, BinOp, Number, Identifier, IfStmt, ForStmt, Function
from typing import List

class CodeGenerator:
    def __init__(self):
        self.indent_level = 0

    def generate(self, nodes: List[ASTNode]) -> str:
        code = []
        for node in nodes:
            code.append(self.generate_node(node))
        return '\n'.join(code)

    def generate_node(self, node: ASTNode) -> str:
        if isinstance(node, VarDecl):
            return self.generate_var_decl(node)
        elif isinstance(node, Assignment):
            return self.generate_assignment(node)
        elif isinstance(node, BinOp):
            return self.generate_bin_op(node)
        elif isinstance(node, Number):
            return node.value
        elif isinstance(node, Identifier):
            return node.name
        elif isinstance(node, IfStmt):
            return self.generate_if_stmt(node)
        elif isinstance(node, ForStmt):
            return self.generate_for_stmt(node)
        elif isinstance(node, Function):
            return self.generate_function(node)
        return ''

    def generate_var_decl(self, node: VarDecl) -> str:
        indent = '    ' * self.indent_level
        if node.value:
            return f"{indent}{node.name} = {self.generate_node(node.value)}"
        return f"{indent}{node.name} = None"

    def generate_assignment(self, node: Assignment) -> str:
        indent = '    ' * self.indent_level
        return f"{indent}{node.name} = {self.generate_node(node.value)}"

    def generate_bin_op(self, node: BinOp) -> str:
        left = self.generate_node(node.left)
        right = self.generate_node(node.right)
        return f"{left} {node.op} {right}"

    def generate_if_stmt(self, node: IfStmt) -> str:
        indent = '    ' * self.indent_level
        code = [f"{indent}if {self.generate_node(node.condition)}:"]
        self.indent_level += 1
        for stmt in node.body:
            code.append(self.generate_node(stmt))
        self.indent_level -= 1
        return '\n'.join(code)

    def generate_for_stmt(self, node: ForStmt) -> str:
        indent = '    ' * self.indent_level
        init = self.generate_node(node.init).strip()
        condition = self.generate_node(node.condition)
        update = self.generate_node(node.update)
        if (isinstance(node.init, VarDecl) and node.init.value and isinstance(node.init.value, Number) and
            node.init.value.value == '0' and isinstance(node.condition, BinOp) and node.condition.op == '<' and
            isinstance(node.update, BinOp) and node.update.op == '+' and node.update.right.value == '1'):
            var_name = node.init.name
            end = node.condition.right.name if isinstance(node.condition.right, Identifier) else node.condition.right.value
            code = [f"{indent}for {var_name} in range({end}):"]
            self.indent_level += 1
            for stmt in node.body:
                code.append(self.generate_node(stmt))
            self.indent_level -= 1
            return '\n'.join(code)
        code = [init, f"{indent}while {condition}:"]
        self.indent_level += 1
        for stmt in node.body:
            code.append(self.generate_node(stmt))
        code.append(self.generate_node(node.update))
        self.indent_level -= 1
        return '\n'.join(code)

    def generate_function(self, node: Function) -> str:
        indent = '    ' * self.indent_level
        params = ', '.join(param.name for param in node.params)
        code = [f"{indent}def {node.name}({params}):"]
        self.indent_level += 1
        for stmt in node.body:
            code.append(self.generate_node(stmt))
        self.indent_level -= 1
        return '\n'.join(code)