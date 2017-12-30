import pickle

# --------------------------------------
# Request tokenizer 
# --------------------------------------

with open('CACM_index_inverse', 'rb') as f :
    u = pickle.Unpickler(f)
    INDEX_DATA = u.load()

def get_postings(word):
    """ Returns the postings if word in index """
    try: 
        postings = [ list(x[2]) for x in INDEX_DATA if x[0] == word ][0]
    except:
        raise ValueError("word '{}' not found in index".format(word))
    
    return postings


# Token types (EOF = end-of-file)
OPERAND, AND, OR, LPAREN, RPAREN, EOF = ('OPERAND', 'AND', 'OR', '(', ')', 'EOF')

class Token:
    def __init__(self, t_type, value):
        self.type = t_type
        self.value = value
    
    def __str__(self):
        return "Token({}, {})".format(self.type, str(self.value))

    def __repr__(self):
        return self.__str__()

class Lexer:
    def __init__(self, text):
        self.text = text.lower()
        self.tokens = self.tokenize()
        self.pos = 0
        self.current_token = self.tokens[self.pos]

    def tokenize(self):
        bloc = self.text.replace('(',' ( ').replace(')', ' ) ').split()
        tokens = []
        for elt in bloc:
            if elt == '(':
                tokens.append(Token(LPAREN, '('))
            elif elt == ')':
                tokens.append(Token(RPAREN, ')'))
            elif elt == 'or':
                tokens.append(Token(OR, 'or'))
            elif elt == 'and':
                tokens.append(Token(AND, 'and'))
            else:
                tokens.append(Token(OPERAND, get_postings(elt)))
        tokens.append(Token(EOF, None))
        return tokens


    def get_next_token(self):
        self.current_token = self.tokens[self.pos]
        self.pos += 1
        return self.current_token


# --------------------------------------
# Tree builder
# --------------------------------------


class BinOp:
    def __init__(self, left, op, right):
        self.op = self.token = op
        self.left = left
        self.right = right
    
    def __repr__(self):
        return "BinOp_node(l: {} - o: {} - r: {})".format(self.left, self.op, self.right)

class Operand:
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def __repr__(self):
        return "Operand: {}".format(self.value)

class Parser:
    def __init__(self, lexer_obj):
        self.lexer = lexer_obj
        self.current_token = self.lexer.get_next_token()
    
    def error(self):
        raise Exception('Invalid syntax')
    
    def eat(self, token_type):
        if self.current_token.type == token_type :
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()
    
    def factor(self):
        token = self.current_token
        if token.type == OPERAND:
            self.eat(OPERAND)
            return Operand(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node

    def term(self):
        node = self.factor()

        while self.current_token.type == AND:
            token = self.current_token
            self.eat(AND)
            node = BinOp(left = node, op = token, right = self.factor())
        
        return node
    
    def expr(self):
        node = self.term()

        while self.current_token.type == OR:
            token = self.current_token
            self.eat(OR)
            node = BinOp(left=node, op=token, right=self.term())
        
        return node

    def parse(self):
        return self.expr()


# --------------------------------------
# Tree evaluator
# --------------------------------------

class NodeVisitor:
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))


class Interpreter(NodeVisitor):
    def __init__(self, tree):
        self.parser = tree
    
    def visit_BinOp(self, node):
        if node.op.type == AND:
            return intersect(self.visit(node.left), self.visit(node.right))
        elif node.op.type == OR:
            return union(self.visit(node.left), self.visit(node.right))
        
    def visit_Operand(self, node):
        return node.value

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)

        
def intersect(postings1,postings2):
    """ returns the intersection of the posting lists of 2 words """

    result = []

    while postings1 and postings2:
        if postings1[0] == postings2[0]:
            result.append(postings1[0])
            del postings1[0]
            del postings2[0]
        elif postings1[0] < postings2[0]:
            del postings1[0]
        else: 
            del postings2[0]

    return result

def union(postings1, postings2):
    """ returns the union of the posting lists of 2 words """

    result = list(set(postings1 + postings2))
    result = sorted(result)

    return result


if __name__ == "__main__":
    
    t = "(a1 and algorithmic)"
    l = Lexer(t)
    tree = Parser(l)

    eval_tree = Interpreter(tree)
    print(eval_tree.interpret())

    