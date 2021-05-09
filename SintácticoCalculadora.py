'''
Datos :
Cadena  (cad)
Clase Léxica (hereda su analizador léxico, su AFD convertido)
'''

class calculadora : 
    def __init__(Obj):
        ## Obj es un objeto clase léxica
        ##Aqui se debe inicializar precisamente 
        pass

    def evalua(self):
        valor = 0.0
        if self.E(valor):
            Token = self.Obj.AnalizadorLexico.yylex()
            if Token == 0:
                valor = valor
                return True
        return False
    
    ## E -> TE'
    def E(self, valor):
        if self.T(valor):
            if self.Ep(valor):
                return True
        return False

    ## E' -> +TE' | -TE' | epsilon
    def Ep(self, valor):
        Token = self.Obj.AnalizadorLexico.yylex()
        v2 = 0.0
        if Token == ( TOKEN.MAS or TOKEN.MENOS):
            if self.T(v2):
                if Token == TOKEN.MAS:
                    valor += v2
                elif Token == TOKEN.MENOS:
                    valor -= v2
                if self.Ep(valor):
                    return True
            return False
        self.obj.AnalizadorLexico.Undotoken()
        return True

    ## T -> FT'
    def T(self, valor):
        if self.F(valor):
            if self.Tp(valor):
                return True
        return False
    
    ## T' -> *FT' | /FT' | epsilon 
    def Tp(self, valor):
        Token = self.Obj.AnalizadorLexico.yylex()
        v2 = 0.0
        if Token == ( TOKEN.POR or TOKEN.ENTRE):
            if self.F(v2):
                if Token == TOKEN.POR:
                    valor *= v2
                elif Token == TOKEN.ENTRE:
                    valor /= v2
                if self.Tp(valor):
                    return True
            return False
        self.obj.AnalizadorLexico.Undotoken()
        return True

    ## F -> (E) | num

    def F(self,valor):
        Token = self.Obj.AnalizadorLexico.yylex()
        if Token == TOKEN.PARI:
            if self.E(valor):
                Token = self.Obj.AnalizadorLexico.yylex()
                if Token == TOKEN.PARD:
                    return True
            return False
        elif Token == TOKEN.NUM:
            valor = float(self.Obj.AnalizadorLexico.getLexema()) ##Ejemplo si 34.6+54/2 Lexema 34.6
            return True
        return False

class posfija :

    