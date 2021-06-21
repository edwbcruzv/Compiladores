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


class GG():
    Arreglo = []
    it = 0
    vf = list()

    def __init__(self, lista_lexemas):
        self.Arreglo = lista_lexemas

    def evalua(self):
        valor = []#este valor
        print(valor,"evalua") 
        if self.G(valor): #es el mismo que se pasa a esta
            Token = self.gettoken()
            if Token == -1 : ## ya no hay mas tokens
                self.vf = valor # es decir al final ya se calculo el valor final de la operación
                del self
                return True
        return False ## con este false
    
    def G(self,valor):
        print(valor,"G")
        if self.L(valor):
            valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
            return True
        return False

    ALLOC3 = []
    def L(self,valor):
        print(valor,"L")
        if self.R(valor):
            Token = self.gettoken()
            if Token == 59:## token de ;
                valor[len(valor)-1] += ';'
                Token = self.gettoken()
                if Token == 10:## token de salto de
                    valor[len(valor)-1] += '\n'
                    print(valor,"REGLA COMP")
                    if self.Lp():
                        for i in range(1,len(self.ALLOC3)):
                            self.ALLOC3[i] = self.ALLOC3[i-1] + self.ALLOC3[i]
                        valor.append(self.ALLOC3[len(self.ALLOC3)-1])
                        print(valor, "L")
                        return True
                    return False
        return False

    def Lp(self):
        v2 =[]
        print(v2,"lp")
        if self.R(v2):
            Token = self.gettoken()
            if Token == 59:## token de ;
                v2[len(v2)-1] += ';'
                Token = self.gettoken()
                if Token == 10:## token de salto de
                    v2[len(v2)-1] += '\n'
                    self.ALLOC3.append(v2[len(v2)-1])
                    print(self.ALLOC3, "PILA3")
                    if self.Lp():
                        if self.gettoken() == -1:
                            self.undotoken()
                            return True
                        for i in range(1,len(self.ALLOC3)):
                            self.ALLOC3[i] = self.ALLOC3[i-1] + self.ALLOC3[i]
                        print(self.ALLOC3, "ddd")
                        return True
                    return False
        self.undotoken()
        return True

    def R(self,valor):
        v2=[]
        print(valor,"R")
        if self.I(valor):
            Token = self.gettoken()
            if Token == 210: ## flecha ->
                valor[len(valor)-1] += '->'
                if self.X(v2):
                    valor.append(v2[len(v2)-1])
                    valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
                    return True
                return False
        return False
        
    def I(self,valor):
        print(valor,"I")
        Token = self.gettoken()
        if Token == 329: ##simbolos
            valor.append(self.getlexema())
            return True
        return False

    ALLOC2 = []
    def X(self,valor):
        print(valor, "X")
        if self.D():
            for i in range(1,len(self.ALLOC)):
                self.ALLOC[i] = self.ALLOC[i-1] + self.ALLOC[i]
            valor.append(self.ALLOC[len(self.ALLOC)-1])     
            print(valor,"LD")       
            self.ALLOC = [] ## reinicia Lados derechos
            #valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
            if self.Xp():
                if self.ALLOC2 == []:
                    return True
                for i in range(1,len(self.ALLOC2)):
                    self.ALLOC2[i] = self.ALLOC2[i-1] + self.ALLOC2[i]
                valor.append(self.ALLOC2[len(self.ALLOC2)-1])            
                self.ALLOC2 = [] ## reinicia Lados derechos
                valor[len(valor)-1] = valor[len(valor)-2] + valor[len(valor)-1]
                return True
        return False

    def Xp(self):
        Token = self.gettoken()
        if Token == 179: ## or |
            #self.ALLOC2.append('|')
            self.ALLOC.append(self.getlexema())
            if self.D():
                #ALLOC -> [|,@]
                print()
                for i in range(1,len(self.ALLOC)):
                    self.ALLOC[i] = self.ALLOC[i-1] + self.ALLOC[i]
                #ALLOC2 -> [|@]
                self.ALLOC2.append(self.ALLOC[len(self.ALLOC)-1]) 
                #ALLOC2 -> [|E,|@]
                print(self.ALLOC2,"|LD")
                self.ALLOC = []
                #ALLOC -> []
                if self.Xp():
                    return True
                return False
        self.undotoken()
        return True
    
    ALLOC = []

    def D(self):
        Token = self.gettoken()
        if Token == 329: ## cualquier
            self.ALLOC.append(self.getlexema())
            if self.Dp():
                return True
        return False
    
    
    def Dp(self):
        t = self.gettoken()
        if t == 32:
            Token = self.gettoken()
            if Token == 329: ## cualquier
                self.ALLOC.append(self.getlexema())
                if self.Dp():
                    return True
        self.undotoken()
        return True
    
    def gettoken(self):
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


class LL1():
    cadena = ''
    lista_reglas = list()
    lista_terminales = list()
    lista_noterminales = list()

    def __init__(self, cadena, terminales):
        self.cadena = cadena
        self.lista_terminales = terminales
    
    def spleet(self):
        indice_actual = 0
        k = 0
        LI_actual = str()
        no_terminales = []

        A = [char for char in self.cadena]
        
        for i in range(0, len(A)-1):
            if A[i] == '-' and A[i+1] == '>':
                no_terminales.append(self.cadena[indice_actual:i])
                LI_actual = self.cadena[indice_actual:i]
            if A[i] == '>' and A[i-1] == '-':
                k = i+1
                continue
            if A[i] == '|':
                temp = LI_actual +"->"+ self.cadena[k:i]
                #print(temp, "DDD")
                self.lista_reglas.append(temp)
                k = i+1
            if A[i] == ';':
                temp = LI_actual +"->"+ self.cadena[k:i]
                #print(temp, "ult")
                self.lista_reglas.append(temp)
                k = i
            if A[i] == '\n':
                indice_actual = i+1

        self.lista_noterminales = no_terminales
    
    
    def izq(self,regla):
        for i in range(0,len(regla)-1):
            if regla[i] == '-':
                if regla[i+1] == '>':
                    return regla[0:i]

    def buscareglas(self,nt):
        Reglas = []
        for elem in self.lista_reglas:
            for i in range(0,len(elem)-1):
                if elem[i] == '-':
                    if elem[i+1] == '>':
                        if elem[0:i] == nt:
                            Reglas.append(elem)

        return Reglas

    def then(self, LD):
        t = ''
        for elem in self.lista_noterminales:
            if elem == LD[0:len(elem)]:
                t = elem
        return t

    Sig = []
    Comp = []
    def first(self, regla):

        RT = []
        nt = self.izq(regla)
        LD = regla[len(nt)+2:]
        s = ''
        
        for elem in self.lista_terminales:
            if LD.find(elem) == 0:
                self.Sig.append(elem)
        
        s = self.then(LD)

        if self.Sig == []:
            RT = self.buscareglas(s)
            for elem in RT:
                self.first(elem)
        
        if '@' in self.Sig:
            t = self.then(LD[len(s):])
            LR = []
            #print(t, "REGLASEC")
            if t != '':
                RT = self.buscareglas(t)
                for elem in RT:
                    self.first(elem)
            
        return self.Sig
    
    def follow(self, regla):
        pass



# A = [["E",329],["->",210],["T",329],[" ",32],["E'",329],[";",59],["\n",10],
#     ["E'",329],["->",210],["+",329],[" ",32],["T",329],[" ",32],["E'",329],["|",179],["-",329],[" ",32],["T",329],[" ",32],["E'",329],["|",179],["@",329],[";",59],["\n",10],
#     ["T",329],["->",210],["F",329],[" ",32],["T'",329],[";",59],["\n",10],
#     ["T'",329],["->",210],["*",329],[" ",32],["F",329],[" ",32],["T'",329],["|",179],["/",329],[" ",32],["F",329],[" ",32],["T'",329],["|",179],["@",329],[";",59],["\n",10],
#     ["F",329],["->",210],["num",329],["|",179],["(",329],[" ",32],["E",329],[" ",32],[")",329],[";",59],["\n",10],
#     ["$",-1]]

# f = GG(A)
# a = f.evalua()
# b = f.evaluacion()
# #print(a)
# print(b)

# T = LL1(b,["num", "+","-","*","/","(",")","@"])
# T.spleet()
# print(T.lista_reglas)
# print(T.lista_terminales)
# print(T.lista_noterminales)


# for elem in T.lista_reglas:
#     print("Regla", elem, T.first(elem))
#     T.Sig = []


