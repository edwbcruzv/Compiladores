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
# Cp-> + Cp | * Cp | ? Cp | E
# F-> ( E ) | [simbolo-simbolo] | simbolo

class ERtoAFD:

    def __init__(self,a_lexico):
        self.Token_epsilon=-1
        self.Token_OR=10
        self.Token_AND=20
        self.Token_MAS=30
        self.Token_MULT=40
        self.Token_OPCION=50
        self.Token_PAR_IZQ=60
        self.Token_PAR_DER=70
        self.Token_CORCH_IZQ=80
        self.Token_CORCH_DER=90
        self.Token_GUION=100
        self.Token_SIMBOLO=110

        self.a_lexico=a_lexico
        self.Lista_Lexemas=None
        self.AutomataResultado=None
        self.sub_indice=0
        if not(isinstance(self.Lista_Lexemas,list)):
            return None


    def CrearAFD(self,exp_regular):
        self.sub_indice=0
        #primero se pasa por el analizador lexico
        self.Lista_Lexemas=self.a_lexico.yylex(exp_regular)
        print(self.Lista_Lexemas)

        if self.Lista_Lexemas==None:
            print("analisis lexicamente incorrecto")
            return

        if self.E():
            print("analisis sintactico correcto")
            return
        else:
            print("analisis sintactico incorrecto")
            return

    # E-> T Ep
    def E(self):
        print("E(",self.getLexema(),")")

        if self.T():

            if self.Ep():
                return True
        self.undoToken()
        return False

    # EP-> or T Ep | $
    def Ep(self):
        print("Ep(",self.getLexema(),")")
        token=self.getToken()

        if token == self.Token_OR:
            
            if self.T():

                if self.Ep():
                    return True
        elif token == self.Token_epsilon:
            
            return True
        self.undoToken()
        return False

    # T-> C Tp
    def T(self):
        print("T(",self.getLexema(),")")
        if self.C():

            if self.Tp():
                return True
        self.undoToken()
        return False
    
    # Tp-> and C Tp | $
    def Tp(self):
        print("Tp(",self.getLexema(),")")
        token=self.getToken()
        if token == self.Token_AND:
            
            if self.C():

                if self.Tp():
                    return True
        elif token == self.Token_epsilon:
            
            return True
        self.undoToken()
        return False
    
    # C-> F Cp
    def C(self):
        print("C(",self.getLexema(),")")
        if self.F():

            if self.Cp():
                return True
        self.undoToken()
        return False
    
    # Cp-> + Cp | * Cp | ? Cp | $
    def Cp(self):
        print("Cp(",self.getLexema(),")")
        token=self.getToken()
        if token == self.Token_MAS or token == self.Token_MULT or token == self.Token_OPCION:

            if self.Cp():
                return True
                
        elif token == self.Token_epsilon:
            return True
        self.undoToken()
        return False
    
    # F-> ( E ) | [simbolo-simbolo] | simbolo
    def F(self):
        print("F(",self.getLexema(),")")
        token=self.getToken()

        if token==self.Token_PAR_IZQ:
            
            if self.E():

                if token==self.Token_PAR_DER:
                    return True

        elif token==self.Token_CORCH_IZQ:
            if token==self.Token_SIMBOLO:
                
                if token==self.Token_GUION:
                    if token==self.Token_SIMBOLO:
                        
                        if token==self.Token_CORCH_DER:
                            
                            return True
        elif token==self.Token_SIMBOLO:
            
            return True
        self.undoToken()
        return False


    def getToken(self):
        lexema=self.Lista_Lexemas[self.sub_indice]
        self.sub_indice+=1 # se incrementa el arreglo despues de la llamada
        return lexema[1] #regresamos el token

    def getLexema(self):
        lexema=self.Lista_Lexemas[self.sub_indice]
        return lexema[0] #regresamos el lexema
    
    def undoToken(self):
        self.sub_indice-=1