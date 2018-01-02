import json
import pickle

# --------------------------------------
# Request tokenizer 
# --------------------------------------


with open('CACM_index_inverse.json', 'r') as f:
    INDEX_DATA = json.load(f)

with open('CACM_collection_docs', 'rb') as f:
    u = pickle.Unpickler(f)
    COLLECTION = u.load()
COLLECTION_IDS = range(1, len(COLLECTION))

def get_postings(word):
    """ Returns a tuple (postings (with tf-idf), postings) if word in index """
    try: 
        doc_tfidf = [ list(x[2]) for x in INDEX_DATA if x[0] == word ][0]
        postings = [ docID[0] for docID in doc_tfidf ]
    except:
        doc_tfidf = [[0, 0]]
        postings = []
        print("word '{}' not found in index".format(word))
    
    return doc_tfidf, postings


# Token types (EOF = end-of-file)
OPERAND, AND, OR, LPAREN, RPAREN, NOT, EOF = ('OPERAND', 'AND', 'OR', '(', ')', 'NOT', 'EOF')

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
            elif elt == 'not':
                tokens.append(Token(NOT, 'not'))
            else:
                tokens.append(Token(OPERAND, get_postings(elt)[1]))
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

class UnaryOp:
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def __repr__(self):
        return "UnaryOp_node(not: {})".format(self.expr)

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
        """factor : NOT factor | INTEGER | LPAREN expr RPAREN"""
        token = self.current_token
        if token.type == NOT:
            self.eat(NOT)
            node = UnaryOp(token, self.factor())
            return node 
        elif token.type == OPERAND:
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
        self.parsed_tree = tree
    
    def visit_BinOp(self, node):
        if node.op.type == AND:
            return intersect(self.visit(node.left), self.visit(node.right))
        elif node.op.type == OR:
            return union(self.visit(node.left), self.visit(node.right))
    
    def visit_UnaryOp(self, node):
        op = node.op.type
        return [x for x in COLLECTION_IDS if x not in self.visit(node.expr)]

    def visit_Operand(self, node):
        return node.value

    def interpret(self):
        return self.visit(self.parsed_tree)

        
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
    
    t = "a1 and not (algorithmic or access)"
    l = Lexer(t)
    tree = Parser(l).parse()

    # --- to print tree
    # print(tree)

    # --- to evaluate tree
    eval_tree = Interpreter(tree).interpret()
    print(eval_tree)

    