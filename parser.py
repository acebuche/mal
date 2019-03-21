from parsimonious.grammar import Grammar
from parsimonious.nodes import NodeVisitor

class Evaluator(NodeVisitor):
    def __init__(self, grammar, text):
        self.op = []
        ast = Grammar(grammar).parse(text)
        self.visit(ast)
  
    def generic_visit(self, node, children):
        if len(children) > 1:
            self.op = children
        return node.text

#Cuanto mas abajo en la lista mayor precedencia
grammar = """\
        exprIMP = (exprOR "->" exprIMP) / exprOR
        exprOR = (exprAND "|" exprOR) / exprAND
        exprAND = (exprBIN "&" exprAND) / exprBIN
        exprBIN = (exprUNA simbBIN exprBIN) / exprUNA
        exprUNA = (simbUNA (exprTERM / exprUNA)) / exprPAR
        exprPAR = ("(" exprIMP ")") / exprTERM
        simbUNA = "-" / "G" / ("F" !"alse") / "X"
        simbBIN = "U" / "R"
        exprTERM = "True" / "False" / var
        var = ~"[a-z]\d*"
        _ = ~"\s*"
"""

"""
Ejemplo de forma de uso de la clase Formula
Creamos una formula de nombre f con la expresion: (a->(bUc))
Posteriormente la imprimimos primero negada
y finalmente negada y pasada a la forma normal negativa

>>> from parser import Formula
>>> f=Formula("(a->(bUc))")
>>> print f.no()
-(a->(bUc))
>>> print f.no().nnf()
(a&(-bR-c))
"""

class Formula():
    def __init__(self, text):
        self.text = text   #La formula en formato texto
        self.isValid= True #Si la formula esta bien formada o no
        self.args=["None"] #Primer elemento de la lista es el operador o 'None' si es un literal
        lista=[]           #variable auxiliar para recoger el arbol de ast
        try:
            lista=Evaluator(grammar, self.text.replace(" ", "")).op
        except:
            self.isValid=False
        if len(lista) == 2: #Operador monario
            self.args=[lista[0], lista[1]]
        elif len(lista) == 3: #Operador binario
            if lista[0]=="(": #Caso especial de parentesis
                self.args=["(", lista[1]]
            else: #Resto de operadores binarios
                self.args=[lista[1], lista[0], lista[2]]

    # Metodo para poder imprimir las formulas
    def __str__(self):
        return self.text

    #Conjunto de metodos autofefinidos para hacer mas legible el programa
    def isLiteral(self):
        return len(self.args)==1

    def isUnary(self):
        return len(self.args)==2

    def isBinary(self):
        return len(self.args)==3

    def isNot(self):
        return self.args[0] == '-'

    def isParenthesis(self):
        return self.args[0] == '('

    def isNot(self):
        return self.args[0] == '-'

    def isG(self):
        return self.args[0] == 'G'

    def isF(self):
        return self.args[0] == 'F'

    def isX(self):
        return self.args[0] == 'X'

    def isImplication(self):
        return self.args[0] == '->'

    def isAnd(self):
        return self.args[0] == '&'

    def isOr(self):
        return self.args[0] == '|'

    def isU(self):
        return self.args[0] == 'U'

    def isR(self):
        return self.args[0] == 'R'

    def pText(self):
        return self.args[1]

    def qText(self):
        return self.args[2]

    # Los siguientes metodos devuelven formulas
    # p y q son los operandos en expresiones como "p AND q" o NOT p
    def p(self):
        return Formula(self.pText())

    def q(self):
        return Formula(self.qText())
    
    #Negacion de una formula dada.
    def no(self):
        if self.isBinary():
            return Formula("-(" + self.text + ")")
        else:
            return Formula("-" + self.text)
    
    # Forma normal negativa de una formula.
    # Las implicaciones tambien se han eliminado
    def nnf(self):
        if self.isLiteral(): return self.text
        # nnf (p) = (nnf p)
        elif self.isParenthesis():
            if self.p().isBinary(): return "(" + self.p().nnf() + ")"
            else :return self.p().nnf()
        # nnf (AND p q) = AND (nnf p) (nnf q) 
        elif self.isAnd(): return self.p().nnf() + '&' + self.q().nnf()
        # nnf (OR p q) = OR (nnf p) (nnf q) 
        elif self.isOr(): return self.p().nnf() + '|' + self.q().nnf()
        # nnf (IMPLIES p q) =  IMPLIES (nnf p) (nnf q) ========  OR (nnf (NOT p)) (nnf (q))
        elif self.isImplication(): return self.p().no().nnf() + '|' + self.q().nnf()
        #nnf (G p) = G (nnf p)
        elif self.isG(): return "G" + self.p().nnf()
        # nnf (F p) = F (nnf p)  
        elif self.isF(): return "F" + self.p().nnf()
        # nnf (X p) = X (nnf p) 
        elif self.isX(): return "X" + self.p().nnf()
        # nnf (p `U` q) = (nnf p) `U` (nnf q)
        elif self.isU(): return self.p().nnf() + 'U' + self.q().nnf()
        # nnf (p `R` q) = (nnf p) `R` (nnf q) 
        elif self.isR(): return self.p().nnf() + 'R' + self.q().nnf()
        # NOT con otro operador
        elif self.isNot():
            # nnf (NOT TRUE) = FALSE
            if self.pText() == 'True': return 'False' 
            # nnf (NOT FALSE) = TRUE
            elif self.pText()  == 'False': return 'True' 
            # nnf (NOT literal) = NOT literal
            elif self.p().isLiteral(): return self.text
            # nnf (NOT(NOT p)) = (nnf p)
            elif self.p().isNot(): return self.p().p().nnf()
            # nnf (NOT(G p)) = F (nnf(NOT p))
            elif self.p().isG(): return "F" + self.p().p().no().nnf()           
            # nnf (NOT(F p)) = G (nnf(NOT p))  
            elif self.p().isF(): return "G" + self.p().p().no().nnf()
            # nnf (NOT(X p)) = X (nnf(NOT p))
            elif self.p().isX(): return "X" + self.p().p().no().nnf()
            # parenthesis
            elif self.p().isParenthesis():
                # con literal
                if self.p().p().isLiteral(): return "-" + self.p().p().text
                # nnf (NOT(AND p q)) = OR (nnf (NOT p)) (nnf (NOT q))
                elif self.p().p().isAnd(): return "(" + self.p().p().p().no().nnf() + \
                    "|" + self.p().p().q().no().nnf() +")"
                # nnf (NOT(OR p q)) = AND (nnf (NOT p)) (nnf (NOT q)) 
                elif self.p().p().isOr(): return "(" + self.p().p().p().no().nnf() + \
                    "&" + self.p().p().q().no().nnf() +")"
                # nnf (NOT(IMPLIES p q)) =  AND (nnf p) (nnf (NOT q))
                elif self.p().p().isImplication(): return "(" + self.p().p().p().nnf() + \
                    "&" + self.p().p().q().no().nnf() +")"
                # nnf (NOT(p `U` q)) = (nnf(NOT p)) `R` (nnf (NOT q))
                elif self.p().p().isU(): return "(" + self.p().p().p().no().nnf() + \
                    "R" + self.p().p().q().no().nnf() +")"
                # nnf (NOT(p `R` q)) = (nnf(NOT p))  `U` (nnf (NOT q)) 
                elif self.p().p().isR(): return "(" + self.p().p().p().no().nnf() + \
                    "U" + self.p().p().q().no().nnf() +")"
                else: # Operadores no binarios: unarios, no es necesario insertar parentesis
                    return self.p().p().no().nnf()

