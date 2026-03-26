import re


# Tokenizador

def tokenize(expr):
    tokens = re.findall(r'\d+|[()+\-*/]', expr)
    return tokens



# Parser base

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        if self.pos < len(self.tokens):
            return self.tokens[self.pos]
        return None

    def eat(self, token):
        if self.current() == token:
            self.pos += 1
        else:
            raise Exception(f"Error: se esperaba {token}")



# 1. Asociatividad IZQUIERDA (precedencia normal)

class ParserIzquierda(Parser):

    def parse(self):
        return self.E()

    def E(self):
        value = self.T()
        while self.current() in ('+', '-'):
            op = self.current()
            self.eat(op)
            if op == '+':
                value += self.T()
            else:
                value -= self.T()
        return value

    def T(self):
        value = self.F()
        while self.current() in ('*', '/'):
            op = self.current()
            self.eat(op)
            if op == '*':
                value *= self.F()
            else:
                value /= self.F()
        return value

    def F(self):
        if self.current() == '(':
            self.eat('(')
            value = self.E()
            self.eat(')')
            return value
        else:
            val = int(self.current())
            self.pos += 1
            return val



# 2. Asociatividad DERECHA

class ParserDerecha(Parser):

    def parse(self):
        return self.E()

    def E(self):
        left = self.T()
        if self.current() in ('+', '-'):
            op = self.current()
            self.eat(op)
            right = self.E()
            return left + right if op == '+' else left - right
        return left

    def T(self):
        left = self.F()
        if self.current() in ('*', '/'):
            op = self.current()
            self.eat(op)
            right = self.T()
            return left * right if op == '*' else left / right
        return left

    def F(self):
        if self.current() == '(':
            self.eat('(')
            value = self.E()
            self.eat(')')
            return value
        else:
            val = int(self.current())
            self.pos += 1
            return val



# 3. Precedencia INVERTIDA (+ mayor que *)

class ParserInvertido(Parser):

    def parse(self):
        return self.E()

    def E(self):
        value = self.T()
        while self.current() in ('*', '/'):
            op = self.current()
            self.eat(op)
            if op == '*':
                value *= self.T()
            else:
                value /= self.T()
        return value

    def T(self):
        value = self.F()
        while self.current() in ('+', '-'):
            op = self.current()
            self.eat(op)
            if op == '+':
                value += self.F()
            else:
                value -= self.F()
        return value

    def F(self):
        if self.current() == '(':
            self.eat('(')
            value = self.E()
            self.eat(')')
            return value
        else:
            val = int(self.current())
            self.pos += 1
            return val



# Lectura del archivo

def process_file():
    with open("entrada.txt", "r") as f:
        lines = f.readlines()

    contador = 1

    for line in lines:
        expr = line.strip()

        if not expr:
            continue


        tokens = tokenize(expr)


        try:
            res_izq = ParserIzquierda(tokens.copy()).parse()
            res_der = ParserDerecha(tokens.copy()).parse()
            res_inv = ParserInvertido(tokens.copy()).parse()

            print(f"\nExpresión: {expr}\n")
            print(f"  Izquierda  : {res_izq}")
            print(f"  Derecha    : {res_der}")
            print(f"  Invertida  : {res_inv}\n")

        except Exception as e:
            print(f"\nError en '{expr}': {e}")


if __name__ == "__main__":
    process_file()