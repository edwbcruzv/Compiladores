from Lib_Compiladores import *


# gramatica G
# E-> E or T | T
# T-> T and C | C
# C-> C + | C * | C ? | F
# F-> ( E ) | [simbolo-simbolo] | simbolo

# gramatica Gp
# E-> T Ep
# EP-> or T Ep | E
# T-> C Tp
# Tp-> and C Tp | E
# C-> F Cp
# Cp-> + F Cp | * F Cp | ? F Cp | E
# F-> ( E ) | [simbolo-simbolo] | simbolo

class ERtoAFD:
    
    self.Token_epsilon=0
    self.Token_OR=10
    self.Token_AND=20
    self.Token_MAS=30
    self.Token_MULT=40
    self.Token_OPCION=50
    self.Token_PAR_IZQ=60
    self.Token_PAR_DER=70

    def __init__(self,exp_regular,a_lexico):
        self.a_lexico=a_lexico
        self.Lista_Lexemas=self.a_lexico.yylex(exp_regular)
        self.sub_indice=0
        if not(isinstance(self.Lista_Lexemas,list)):
            return None


    def Convierte(self,exp_regular):
        pass

    # E-> T Ep
    def E(self,exp_regular):

        if self.T(exp_regular):

            if self.Ep(exp_regular):
                return True

        return False

    # EP-> or T Ep | E
    def Ep(self,exp_regular):
        token=self.getToken()

        if token == self.Token_OR:

            if self.T(exp_regular):

                if self.Ep(exp_regular):
                    return True
        elif token == self.Token_epsilon:
            return True
        return False

    # T-> C Tp
    def T(self,exp_regular):

        if self.C(exp_regular):

            if self.Tp(exp_regular):
                return True
        return False
    
    # Tp-> and C Tp | E
    def Tp(self,exp_regular):
        token=self.getToken()
        if token == self.Token_AND:

            if self.C(exp_regular):

                if self.Tp(exp_regular):
                    return True
        elif token == self.Token_epsilon:
            return True
        return False
    
    # C-> F Cp
    def C(self,exp_regular):

        if self.F():

            if self.Cp():
                return True
        return False
    
    # Cp-> + F Cp | * F Cp | ? F Cp | E
    def Cp(self,exp_regular):
        token=self.getToken()
        if token == self.Token_MAS 
            or token == self.Token_MULT 
            or token == self.Token_OPCION:

            if self.F():

                if self.Cp():
                    return True
                
        elif token == self.Token_epsilon:
    
    # F-> ( E ) | [simbolo-simbolo] | simbolo
    def F(self,exp_regular):
        token=self.getToken()


    def getToken(self):
        lexema=Lista_Lexemas[self.sub_indice]
        sub_indice+=1 # se incrementa el arreglo despues de la llamada

        return lexema[1] #regresamos el token
    
    def undoToken(self);
        pass