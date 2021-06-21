from Lib_Compiladores import *
from Lib_Compiladores.CreadorAFNe import CreadorAFNe
from Lib_Compiladores.CreadorClaseLexica import CreadorClaseLexica
from Lib_Compiladores.CreadorALexico import CreadorALexico
import copy

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

        # nombre_AFN: "nombreAFN"
        # num_estados: num  (es un int)
        self.num_estados=0
        # str_lenguaje: "simbolo1,simbolo2,simbolo3"
        self.str_lenguaje=''
        self.str_estado_inicial="0"
        # str_estados_aceptacion: "edo1-edo2-edo3" o "[edo1,token]-[edo2,token]-[edo3,token]"
        self.str_estados_aceptacion=""
        # str_transiciones:"[edo,edo,simbolo]-[edo,edo,simbolo]-[edo,edo,simbolo]"
        self.str_transiciones=""

        self.auxA1=None
        self.auxA2=None
        self.aux_rango=''
        self.aux_simbolo=''

        self.a_lexico=a_lexico
        self.Lista_Lexemas=None
        self.AutomataResultado=None
        self.sub_indice=0
        self.creaAFN=CreadorAFNe()
        self.creaCLX=CreadorClaseLexica()
        self.creaALX=CreadorALexico()
        if not(isinstance(self.Lista_Lexemas,list)):
            return None


    def CrearAFD(self,nombre,exp_regular):
        self.sub_indice=0
        #primero se pasa por el analizador lexico
        self.Lista_Lexemas=self.a_lexico.yylex(exp_regular)
        print(self.Lista_Lexemas)

        if self.Lista_Lexemas==None:
            print("analisis lexicamente incorrecto")
            return None

        if self.E():
            print("analisis sintactico correcto")
            #self.auxA1.mostrarAutomata()
            clx,res=self.creaCLX.CrearClaseLexica("borrame",999,self.auxA1)
            print(res)
            alx,res=self.creaALX.CrearA_Lexico("ERtoAFD_"+nombre)
            print(res)
            alx.addClaseLexica(clx)
            alx.definirALexico()
            alx.getAFD().mostrarAutomata()
            return return alx
        else:
            print("analisis sintactico incorrecto")
            return None

    # E-> T Ep
    def E(self):
        print("E(",self.getLexema(),")")

        if self.T():
            if self.Ep():
                return True
        return False

    # EP-> or T Ep | $
    def Ep(self):
        print("Ep(",self.getLexema(),")")
        token=self.getToken()
        print("token=",token)
        if token == self.Token_OR:
            self.auxA2=copy.deepcopy(self.auxA1)
            self.auxA1=None
            print("swap")
            if self.T():
                if self.Ep():
                    self.auxA1.unirCon(self.auxA2)
                    print("unido")
                    return True
            # self.auxA1=None
            # self.auxA2=None
            return False
        # elif token == self.Token_epsilon: 
        #     return True
        self.undoToken()
        return True

    # T-> C Tp
    def T(self):
        print("T(",self.getLexema(),")")
        if self.C():
            if self.Tp():
                return True
        return False
    
    # Tp-> and C Tp | $
    def Tp(self):
        print("Tp(",self.getLexema(),")")
        token=self.getToken()
        print("token=",token)
        if token == self.Token_AND:    
            self.auxA2=copy.deepcopy(self.auxA1)
            self.auxA1=None
            print("swap")
            if self.C():#esperando automata
                
                if self.Tp():
                    self.auxA1.concatCon(self.auxA2)
                    print("concatenado")
                    return True
            # self.auxA1=None
            # self.auxA2=None
            return False
        # elif token == self.Token_epsilon:
        #     return True
        self.undoToken()
        return True
    
    # C-> F Cp
    def C(self):
        print("C(",self.getLexema(),")")
        if self.F():#se guarda un automata en A1
            if self.Cp(): #se hace una de las cerraduras a A1
                return True
        return False
    
    # Cp-> + Cp | * Cp | ? Cp | $
    def Cp(self):
        print("Cp(",self.getLexema(),")")
        token=self.getToken()
        print("token=",token)
        if token == self.Token_MAS or token == self.Token_MULT or token == self.Token_OPCION:
            if token == self.Token_MAS:
                self.auxA1.cerraduraPositiva()
                print("cerradura positiva")
            elif token == self.Token_MULT:
                self.auxA1.cerraduraKleene()
                print("cerradura kleene")
            elif token == self.Token_OPCION:
                self.auxA1.opcion()
                print("cerradura opcion")
            if self.Cp():
                
                return True
            # self.auxA1=None
            return False
        # elif token == self.Token_epsilon:
        #     return True
        self.undoToken()
        return True
    
    # F-> ( E ) | [simbolo-simbolo] | simbolo
    def F(self):
        print("F(",self.getLexema(),")")
        token=self.getToken()
        print("token=",token)
        if token==self.Token_PAR_IZQ:
            # print(" E(",self.getLexema(),")")
            # token=self.getToken()
            # print("token=",token)
            if self.E():

                if token==self.Token_PAR_DER:
                    return True
            return False
        elif token==self.Token_CORCH_IZQ:
            self.aux_rango=self.aux_rango+self.getThisLexema()
            print("  F(",self.getLexema(),")")
            token=self.getToken()
            print("token=",token)
            if token==self.Token_SIMBOLO:
                self.aux_rango=self.aux_rango+self.getThisLexema()
                print("  F(",self.getLexema(),")")
                token=self.getToken()
                print("token=",token)
                if token==self.Token_GUION:
                    self.aux_rango=self.aux_rango+self.getThisLexema()
                    print("  F(",self.getLexema(),")")
                    token=self.getToken()
                    print("token=",token)
                    if token==self.Token_SIMBOLO:
                        self.aux_rango=self.aux_rango+self.getThisLexema()
                        print("  F(",self.getLexema(),")")
                        token=self.getToken()
                        print("token=",token)
                        if token==self.Token_CORCH_DER:
                            self.aux_rango=self.aux_rango+self.getThisLexema()
                            transicion="[0,1,"+self.aux_rango+"]"
                            print(self.aux_rango)
                            self.auxA1,res=self.creaAFN.CrearAutomataAFN("AFN_temp","1",self.aux_rango,"0","1",transicion)
                            print(res)
                            self.aux_rango=""
                            return True
        elif token==self.Token_SIMBOLO: 
            self.aux_simbolo=self.getThisLexema()
            transicion="[0,1,"+self.aux_simbolo+"]"
            print(self.aux_simbolo)
            self.auxA1,res=self.creaAFN.CrearAutomataAFN("AFN_temp","1",self.aux_simbolo,"0","1",transicion)
            print(res)
            self.aux_simbolo=""
            return True
        aux_rango=''
        return False


    def getToken(self):
        lexema=self.Lista_Lexemas[self.sub_indice]
        self.sub_indice+=1 # se incrementa el arreglo despues de la llamada
        print("incremento a:",self.sub_indice)
        return lexema[1] #regresamos el token

    def getLexema(self):
        lexema=self.Lista_Lexemas[self.sub_indice]
        return lexema[0] #regresamos el lexema
    
    def getThisLexema(self):
        lexema=self.Lista_Lexemas[self.sub_indice-1]
        return lexema[0] #regresamos el lexema
    
    def undoToken(self):
        self.sub_indice-=1
        print("decremento a:",self.sub_indice)