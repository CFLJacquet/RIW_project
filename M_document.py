class Document:

    def __init__(self, ID, title = "", summary = "", keywords = ""):
        self.IDdoc = ID
        self.title = title
        self.summary = summary
        self.keywords = keywords

    def __repr__(self):
        return "doc {} # {}".format(self.IDdoc, self.title)

    def concat(self):
        return self.title + self.summary + self.keywords


if __name__ == "__main__":
    
    # --- Test for document class ---
    collection = {}
    nb = ".I 3202"
    ID = int(nb[3:])
    collection[ID] = Document(ID)
    collection[ID].title = "   MANIP: A Computer System for Algebra and Analytic Differentiation"
    collection[ID].summary = "   A mathematical expression to be operated upon is written in FORTRAN-like \
notation and stored in the computer as a string of BCD characters with all\
blanks removed. It may be as complicated as desired (parentheses nested without\
restriction, etc.) so long as the entire expression (or any subsequent form)\
does not exceed 5000 characters. The problemm of performing algebraic operations\
and obtaining analytic derivatives was translated into that of identifying and\
manipulating character sequences. Programs which resulted were written in\
FORTRAN IV for a CDC 3600 and are discussed in detail."
    collection[ID].keywords = ""

    print(collection[ID])
    print(collection[ID].concat())
