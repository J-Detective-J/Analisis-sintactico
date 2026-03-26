import re
import time
from graphviz import Digraph


# TOKENIZADOR
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



# NODO
class Node:
    def __init__(self, value):
        self.value = value
        self.children = []



# PARSER LL(1)
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
            new_node.children = [node, self.T()]
            node = new_node
        return node

    def T(self):
        node = self.F()
        while self.current()[0] in ('MUL', 'DIV'):
            op = self.current()[1]
            self.eat(self.current()[0])
            new_node = Node(op)
            new_node.children = [node, self.F()]
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



# RECORRIDO LL(1)
def graph_traversal(root):
    dot = Digraph()
    counter = [0]

    def dfs(node, parent_id=None):
        node_id = str(counter[0])
        label = f"|{counter[0]}|\n{node.value}"
        dot.node(node_id, label)
        counter[0] += 1

        if parent_id is not None:
            dot.edge(parent_id, node_id)

        for child in node.children:
            dfs(child, node_id)

    dfs(root)
    return dot



# CYK

def cyk_trace(tokens):
    input_symbols = [t[0] for t in tokens if t[0] != 'EOF']
    n = len(input_symbols)

    grammar = {
        'E': [('E', 'PLUS_T'), ('E', 'MINUS_T'), ('T',)],
        'T': [('T', 'MUL_F'), ('T', 'DIV_F'), ('F',)],
        'F': [('LPAREN_E', 'RPAREN'), ('NUM',), ('ID',)],
        'PLUS_T': [('PLUS', 'T')],
        'MINUS_T': [('MINUS', 'T')],
        'MUL_F': [('MUL', 'F')],
        'DIV_F': [('DIV', 'F')],
        'LPAREN_E': [('LPAREN', 'E')],
    }

    table = [[set() for _ in range(n)] for _ in range(n)]
    trace = []

    # Inicializacion
    for i in range(n):
        for lhs, rules in grammar.items():
            for rule in rules:
                if len(rule) == 1 and rule[0] == input_symbols[i]:
                    table[i][i].add(lhs)
                    trace.append((i, i, lhs, None))

    # CYK
    for l in range(2, n + 1):
        for i in range(n - l + 1):
            j = i + l - 1
            for k in range(i, j):
                for lhs, rules in grammar.items():
                    for rule in rules:
                        if len(rule) == 2:
                            B, C = rule
                            if B in table[i][k] and C in table[k+1][j]:
                                table[i][j].add(lhs)
                                trace.append((i, j, lhs, (i, k, k+1, j)))

    return ('E' in table[0][n-1], trace)



# GRAFO CYK
def graph_cyk(trace):
    dot = Digraph()

    for step, (i, j, lhs, dep) in enumerate(trace):
        node_id = f"{i}_{j}_{step}"
        label = f"[{i},{j}] {lhs}"
        dot.node(node_id, label)

        if dep:
            i1, k, k1, j1 = dep

            left_id = f"{i1}_{k}_0"
            right_id = f"{k1}_{j1}_0"

            dot.edge(left_id, node_id)
            dot.edge(right_id, node_id)

    return dot



# PROCESAMIENTO
def process_file():
    with open("entrada.txt", "r") as f:
        lines = f.readlines()

    contador = 1

    for line in lines:
        expr = line.strip()

        if not expr:
            continue

        print(f"\nExpresión: {expr}")

        tokens = tokenize(expr)

        # LL 
        start_ll = time.perf_counter()
        parser = Parser(tokens)
        tree = parser.E()
        end_ll = time.perf_counter()

        #  CYK 
        start_cyk = time.perf_counter()
        result_cyk, trace = cyk_trace(tokens)
        end_cyk = time.perf_counter()

        # Recorrido LL 
        dot_trav = graph_traversal(tree)
        dot_trav.render(f"LL-cadena_{contador}", format="png", cleanup=True)

        # Grafo CYK 
        dot_cyk = graph_cyk(trace)
        dot_cyk.render(f"CYK-cadena_{contador}", format="png", cleanup=True)

        # Resultados
        print(f"LL: {(end_ll - start_ll):.6f} s")
        print(f"CYK:   {(end_cyk - start_cyk):.6f} s")
   

        contador += 1


if __name__ == "__main__":
    process_file()
