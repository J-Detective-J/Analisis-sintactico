import re
from graphviz import Digraph


# Tokenizador

def tokenize(expr):
    token_spec = [
        ('NUM',   r'\d+'),
        ('ID',    r'[a-zA-Z]+'),
        ('PLUS',  r'\+'),
        ('MINUS', r'-'),
        ('MUL',   r'\*'),
        ('DIV',   r'/'),
        ('LPAREN', r'\('),
        ('RPAREN', r'\)'),
        ('SKIP',  r'[ \t]+'),
    ]
    tok_regex = '|'.join(f'(?P<{name}>{regex})' for name, regex in token_spec)
    tokens = []
    
    for match in re.finditer(tok_regex, expr):
        kind = match.lastgroup
        value = match.group()
        if kind != 'SKIP':
            tokens.append((kind, value))
    
    tokens.append(('EOF', None))
    return tokens


# Nodo del árbol

class Node:
    def __init__(self, value):
        self.value = value
        self.children = []



# Parser

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def current(self):
        return self.tokens[self.pos]

    def eat(self, token_type):
        if self.current()[0] == token_type:
            self.pos += 1
        else:
            raise SyntaxError(f"Se esperaba {token_type}")

   
    def E(self):
        node = self.T()
        while self.current()[0] in ('PLUS', 'MINUS'):
            op = self.current()[1]
            self.eat(self.current()[0])
            new_node = Node(op)
            new_node.children.append(node)
            new_node.children.append(self.T())
            node = new_node
        return node


    def T(self):
        node = self.F()
        while self.current()[0] in ('MUL', 'DIV'):
            op = self.current()[1]
            self.eat(self.current()[0])
            new_node = Node(op)
            new_node.children.append(node)
            new_node.children.append(self.F())
            node = new_node
        return node


    def F(self):
        token = self.current()
        
        if token[0] == 'NUM':
            self.eat('NUM')
            return Node(token[1])
        
        elif token[0] == 'ID':
            self.eat('ID')
            return Node(token[1])
        
        elif token[0] == 'LPAREN':
            self.eat('LPAREN')
            node = self.E()
            self.eat('RPAREN')
            return node
        
        else:
            raise SyntaxError("Error en F")


# Generar Graphviz


def build_graph(node, dot=None, parent=None, counter=None):
    if dot is None:
        dot = Digraph()
        dot.attr(rankdir='TB')
    
    if counter is None:
        counter = [0]

    node_id = str(counter[0])
    counter[0] += 1

    dot.node(node_id, node.value)

    if parent is not None:
        dot.edge(parent, node_id)

    for child in node.children:
        build_graph(child, dot, node_id, counter)

    return dot


# Procesar archivo

def process_file():
    with open("entrada.txt", 'r') as f:
        lines = f.readlines()
    
    contador = 1 
    
    for line in lines:
        expr = line.strip()
        
        if not expr:
            continue
        
        print(f"Procesando: {expr}")
        
        tokens = tokenize(expr)
        parser = Parser(tokens)
        tree = parser.E()
        
        dot = build_graph(tree)
        dot.render(f"arbol-cadena_{contador}", format="png", cleanup=True)
        
        contador += 1


if __name__ == "__main__":
    process_file()
