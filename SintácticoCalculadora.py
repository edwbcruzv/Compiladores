'''
Datos :
Cadena  (cad)
Clase Léxica (hereda su analizador léxico, su AFD convertido)
'''

class calculadora : 
    Arreglo = []
    it = 0
    vf = 0.0
    def __init__(self, lista_lexemas):
        self.Arreglo = lista_lexemas

    def evalua(self):
        valor = 0.0 #este valor 
        if self.E(valor): #es el mismo que se pasa a esta
            Token = self.gettoken()
            if Token == fin_de_la_lista : ## ya no hay mas tokens
                vf = valor # es decir al final ya se calculo el valor final de la operación
                return True
        return False ## con este false 
        #solo se deberia decir que la cadena
        #no es correcta sinacticamente, cosa que ya hiciste con yylex
    
    ## E -> TE'
    def E(self, valor):
        if self.T(valor):
            if self.Ep(valor):
                return True
        return False

    ## E' -> +TE' | -TE' | epsilon
    def Ep(self, valor):
        Token = self.gettoken()
        v2 = 0.0
        if Token == ( TOKEN.MAS  or TOKEN.MENOS ):##10 o 20, 10 es el de la suma y 20 el de la resta
            ##estos numeros serian los tokens de A_Calculadora
            if self.T(v2):
                if Token == TOKEN.MAS:
                    valor += v2
                elif Token == TOKEN.MENOS:
                    valor -= v2
                if self.Ep(valor):
                    return True
            return False
        self.undotoken()
        return True

    ## T -> FT'
    def T(self, valor):
        if self.F(valor):
            if self.Tp(valor):
                return True
        return False
    
    ## T' -> *FT' | /FT' | epsilon 
    def Tp(self, valor):
        Token = self.gettoken()
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
        self.undotoken()
        return True

    ## F -> (E) | num

    def F(self,valor):
        Token = self.gettoken()
        if Token == TOKEN.PARI:
            if self.E(valor):
                Token = self.gettoken()
                if Token == TOKEN.PARD:
                    return True
            return False
        elif Token == TOKEN.NUM:
            valor = float(self.getlexema(self.it -1)) ##Ejemplo si 34.6+54/2 Lexema 34.6
            return True
        return False

    def gettoken(self):
    # Aqui no tiene atributo como tal
    # it es una variable iterable entera
    # cuando se llama gettoken,se regresa el token 
    # [38,70],[+,10] retornara 70 si it es 0
        Token = self.Arreglo[it][1]
        it+=1
        return Token

    def getlexema(self, i):
        return self.Arreglo[i][0]
            
    def undotoken(self):
    #solo se regresa en un indice para leer wl arreglo de los tokens
        it-=1  

class posfija :
    Arreglo = []
    it = 0
    vf = ''
    def __init__(lista_lexemas):
        ## se debe de poner aqui el arreglo de
        ## tokens que rwgresa
        ##Aqui se debe inicializar precisamente 
        self.Arreglo = lista_lexemas

    def evalua(self):
        valor = ''
        if self.E(valor):
            Token = self.gettoken()
            if Token == fin_de_los_lexemas:##fin de cadena
                vf = valor
                return True
        return False ## con este false 
        #solo se deberia decir que la cadena
        #no es correcta sinacticamente
    
    ## E -> TE'
    def E(self, valor):
        if self.T(valor):
            if self.Ep(valor):
                return True
        return False

    ## E' -> +TE' | -TE' | epsilon
    def Ep(self, valor):
        Token = self.gettoken()
        v2 = ''
        if Token == ( TOKEN.MAS or TOKEN.MENOS):
            if self.T(v2):
                if Token == TOKEN.MAS:#10
                    valor = valor + v2 + '+' # concatenacion
                elif Token == TOKEN.MENOS:#20
                    valor = valor + v2 + '-' # concatenacion
                if self.Ep(valor):
                    return True
            return False
        self.undotoken()
        return True

    ## T -> FT'
    def T(self, valor):
        if self.F(valor):
            if self.Tp(valor):
                return True
        return False
    
    ## T' -> *FT' | /FT' | epsilon 
    def Tp(self, valor):
        Token = self.gettoken()
        v2 = 0.0
        if Token == ( TOKEN.POR or TOKEN.ENTRE):
            if self.F(v2):
                if Token == TOKEN.POR:
                    valor = valor + v2 + '*' # concatenacion
                elif Token == TOKEN.ENTRE:
                    valor = valor + v2 + '/' # concatenacion
                if self.Tp(valor):
                    return True
            return False
        self.undotoken()
        return True

    ## F -> (E) | num

    def F(self,valor):
        Token = self.gettoken()
        if Token == TOKEN.PARI:#50
            if self.E(valor):
                Token = self.gettoken()
                if Token == TOKEN.PARD:#60
                    return True
            return False
        elif Token == TOKEN.NUM:#70
            valor = str(self.getLexema()) ##Ejemplo si 34.6+54/2 Lexema 34.6
            return True
        return False

    def gettoken(self):
    # Aqui no tiene atributo como tal
    # it es una variable iterable entera
    # cuando se llama gettoken,se regresa el token 
    # [38,70],[+,10] retornara 70 si it es 0
        Token = self.Arreglo[it][1]
        it+=1
        return Token

    def getlexema(self, i):
        return self.Arreglo[i][0]
            
    def undotoken(self):
    #solo se regresa en un indice para leer wl arreglo de los tokens
        it-=1 
