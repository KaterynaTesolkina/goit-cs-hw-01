class LexicalError(Exception):
    pass

class ParsingError(Exception):
    pass

class TokenType:
    INTEGER = "INTEGER"
    PLUS = "PLUS"
    MINUS = "MINUS"
    MUL = "MUL"
    DIV = "DIV"
    LPAREN = "LPAREN"
    RPAREN = "RPAREN"
    EOF = "EOF"

class Token:
    def __init__(self, type_, value):
        self.type = type_
        self.value = value
    def __repr__(self):
        return f"Token({self.type}, {repr(self.value)})"

class Lexer:
    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_char = text[self.pos] if text else None

    def advance(self):
        self.pos += 1
        self.current_char = self.text[self.pos] if self.pos < len(self.text) else None

    def skip_whitespace(self):
        while self.current_char and self.current_char.isspace():
            self.advance()

    def integer(self):
        result = ""
        while self.current_char and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def get_next_token(self):
        while self.current_char is not None:
            if self.current_char.isspace():
                self.skip_whitespace()
                continue
            if self.current_char.isdigit():
                return Token(TokenType.INTEGER, self.integer())
            if self.current_char == "+":
                self.advance(); return Token(TokenType.PLUS, "+")
            if self.current_char == "-":
                self.advance(); return Token(TokenType.MINUS, "-")
            if self.current_char == "*":
                self.advance(); return Token(TokenType.MUL, "*")
            if self.current_char == "/":
                self.advance(); return Token(TokenType.DIV, "/")
            if self.current_char == "(":
                self.advance(); return Token(TokenType.LPAREN, "(")
            if self.current_char == ")":
                self.advance(); return Token(TokenType.RPAREN, ")")
            raise LexicalError(f"Unexpected character: {self.current_char}")
        return Token(TokenType.EOF, None)

# AST node classes
class Num:
    def __init__(self, token):
        self.token = token
        self.value = token.value

class BinOp:
    def __init__(self, left, op, right):
        self.left = left
        self.op = op
        self.right = right

class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def error(self):
        raise ParsingError("Invalid syntax")

    def eat(self, token_type):
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        token = self.current_token
        if token.type == TokenType.INTEGER:
            self.eat(TokenType.INTEGER)
            return Num(token)
        elif token.type == TokenType.LPAREN:
            self.eat(TokenType.LPAREN)
            node = self.expr()
            self.eat(TokenType.RPAREN)
            return node
        self.error()

    def term(self):
        node = self.factor()
        while self.current_token.type in (TokenType.MUL, TokenType.DIV):
            token = self.current_token
            if token.type == TokenType.MUL:
                self.eat(TokenType.MUL)
            elif token.type == TokenType.DIV:
                self.eat(TokenType.DIV)
            node = BinOp(node, token, self.factor())
        return node

    def expr(self):
        node = self.term()
        while self.current_token.type in (TokenType.PLUS, TokenType.MINUS):
            token = self.current_token
            if token.type == TokenType.PLUS:
                self.eat(TokenType.PLUS)
            elif token.type == TokenType.MINUS:
                self.eat(TokenType.MINUS)
            node = BinOp(node, token, self.term())
        return node

class Interpreter:
    def __init__(self, parser):
        self.parser = parser

    def visit(self, node):
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name)
        return method(node)

    def visit_BinOp(self, node):
        if node.op.type == TokenType.PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == TokenType.MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == TokenType.MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == TokenType.DIV:
            return self.visit(node.left) / self.visit(node.right)

    def visit_Num(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.expr()
        return self.visit(tree)

def main():
    while True:
        try:
            text = input('Enter expression (or "exit" to quit): ')
            if text.lower() == "exit":
                break
            lexer = Lexer(text)
            parser = Parser(lexer)
            interpreter = Interpreter(parser)
            print(interpreter.interpret())
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
