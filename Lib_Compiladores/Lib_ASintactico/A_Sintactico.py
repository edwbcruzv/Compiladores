'''
Datos :
Cadena  (cad)
Clase Léxica (hereda su analizador léxico, su AFD convertido)
'''

class Calculadora(): 
    Arreglo = []
    it = 0
    vf = list()

    def __init__(self, lista_lexemas):
        self.Arreglo = lista_lexemas

    def evalua(self):
        valor = []#este valor 
        if self.E(valor): #es el mismo que se pasa a esta
            Token = self.gettoken()
            if Token == -1 : ## ya no hay mas tokens
                self.vf = valor # es decir al final ya se calculo el valor final de la operación
                return True
        return False ## con este false 
        #solo se deberia decir que la cadena
        #no es correcta sinacticamente, cosa que ya hiciste con yylex
    
    ## E -> TE'
    def E(self, valor):
        #print(id(valor))
        print(valor)
        if self.T(valor):
            if self.Ep(valor):
                return True
        return False

    ## E' -> +TE' | -TE' | epsilon
    def Ep(self, valor):
        #print(id(valor))
        print(valor)
        Token = self.gettoken()
        v2 = []
        if Token ==  10  or Token == 20 :##10 o 20, 10 es el de la suma y 20 el de la resta
            ##estos numeros serian los tokens de A_Calculadora
            if self.T(v2):
                if Token == 10:
                    valor.append(v2[len(v2)-1])
                    valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
                elif Token == 20:
                    valor.append(v2[len(v2)-1])
                    valor[len(valor)-1] = valor[len(valor)-2] - valor[len(valor)-1]
                if self.Ep(valor):
                    return True
                return False
        self.undotoken()
        return True

    ## T -> FT'
    def T(self, valor):
        #print(id(valor))
        print(valor)
        if self.F(valor):
            if self.Tp(valor):
                return True
        return False
    
    ## T' -> *FT' | /FT' | epsilon 
    def Tp(self, valor):
        #print(id(valor))
        print(valor)
        Token = self.gettoken()
        v2 = []
        if Token == 30 or Token == 40:
            if self.F(v2):
                if Token == 30:
                    valor.append(v2[len(v2)-1])
                    valor[len(valor)-1] = valor[len(valor)-2] * valor[len(valor)-1]
                elif Token == 40:
                    valor.append(v2[len(v2)-1])
                    valor[len(valor)-1] = valor[len(valor)-2] / valor[len(valor)-1]
                if self.Tp(valor):
                    return True
                return False
        self.undotoken()
        return True

    ## F -> (E) | num

    def F(self,valor):
        #print(id(valor))
        print(valor)
        Token = self.gettoken()
        if Token == 50:
            if self.E(valor):
                Token = self.gettoken()
                if Token == 60:
                    return True
            return False
        elif Token == 70:
            valor.append(float(self.getlexema())) ##Ejemplo si 34.6+54/2 Lexema 34.6
            return True
        return False

    def gettoken(self):
    # Aqui no tiene atributo como tal
    # it es una variable iterable entera
    # cuando se llama gettoken,se regresa el token 
    # [38,70],[+,10] retornara 70 si it es 0
        Token = self.Arreglo[self.it][1]
        self.it+=1
        return Token

    def getlexema(self):
        return self.Arreglo[self.it-1][0]
            
    def undotoken(self):
    #solo se regresa en un indice para leer wl arreglo de los tokens
        self.it-=1  

    def evaluacion(self):
        return self.vf[len(self.vf)-1]

class Posfija(): 
    Arreglo = []
    it = 0
    vf = list()

    def __init__(self, lista_lexemas):
        self.Arreglo = lista_lexemas

    def evalua(self):
        valor = []#este valor 
        if self.E(valor): #es el mismo que se pasa a esta
            Token = self.gettoken()
            if Token == -1 : ## ya no hay mas tokens
                self.vf = valor # es decir al final ya se calculo el valor final de la operación
                return True
        return False ## con este false 
        #solo se deberia decir que la cadena
        #no es correcta sinacticamente, cosa que ya hiciste con yylex
    
    ## E -> TE'
    def E(self, valor):
        #print(id(valor))
        print(valor)
        if self.T(valor):
            if self.Ep(valor):
                return True
        return False

    ## E' -> +TE' | -TE' | epsilon
    def Ep(self, valor):
        #print(id(valor))
        print(valor)
        Token = self.gettoken()
        v2 = []
        if Token ==  10  or Token == 20 :##10 o 20, 10 es el de la suma y 20 el de la resta
            ##estos numeros serian los tokens de A_Calculadora
            if self.T(v2):
                if Token == 10:
                    valor.append(v2[len(v2)-1] + '+')
                    valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1] 
                elif Token == 20:
                    valor.append(v2[len(v2)-1] + '-')
                    valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
                if self.Ep(valor):
                    return True
            return False
        self.undotoken()
        return True

    ## T -> FT'
    def T(self, valor):
        #print(id(valor))
        print(valor)
        if self.F(valor):
            if self.Tp(valor):
                return True
        return False
    
    ## T' -> *FT' | /FT' | epsilon 
    def Tp(self, valor):
        #print(id(valor))
        print(valor)
        Token = self.gettoken()
        v2 = []
        if Token == 30 or Token == 40:
            if self.F(v2):
                if Token == 30:
                    valor.append(v2[len(v2)-1] + '*')
                    valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
                elif Token == 40:
                    valor.append(v2[len(v2)-1] + '/')
                    valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
                if self.Tp(valor):
                    return True
            return False
        self.undotoken()
        return True

    ## F -> (E) | num

    def F(self,valor):
        #print(id(valor))
        print(valor)
        Token = self.gettoken()
        if Token == 50:
            if self.E(valor):
                Token = self.gettoken()
                if Token == 60:
                    return True
            return False
        elif Token == 70:
            if len(self.getlexema())>1:
                valor.append('('+self.getlexema()+')') ##Ejemplo si 34.6+54/2 Lexema 34.6
            else:
                valor.append(self.getlexema())
            return True
        return False

    def gettoken(self):
    # Aqui no tiene atributo como tal
    # it es una variable iterable entera
    # cuando se llama gettoken,se regresa el token 
    # [38,70],[+,10] retornara 70 si it es 0
        Token = self.Arreglo[self.it][1]
        self.it+=1
        return Token

    def getlexema(self):
        return self.Arreglo[self.it-1][0]
            
    def undotoken(self):
    #solo se regresa en un indice para leer wl arreglo de los tokens
        self.it-=1  

    def evaluacion(self):
        return self.vf[len(self.vf)-1]

'''
A = [["4",70],["/",40],["45",70],["-1",-1]]

f = calculadora(A)
a = f.evalua()
b = f.evaluacion()

d = posfija(A)
c = d.evalua()
t = d.evaluacion()
print(a,b)
print(c,t)
'''
