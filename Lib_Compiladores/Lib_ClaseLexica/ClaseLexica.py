from Lib_Compiladores.Lib_AFN_e.AFN_e import AFN_e
import copy

class ClaseLexica():
        
        # Nombre_Clase_Lexica:"NombreClaseLexica"
        # AFN: AFN().objet
        # Arg_AFN_List: [Nombre_AFN,K_list,Sigma_list,S,Z_list,M_list]
     
    def __init__(self,Nombre_Clase_Lexica,Token=None,AFN=None):
        # __Nombre_Clase_Lexica:"NombreClaseLexica"
        self.__Nombre_Clase_Lexica=Nombre_Clase_Lexica
        # __AFN: AFN().objet 
        self.__AFN=object() 
        # __Token: int
        self.__Token=0

        #solo se crea la instancia para fines de busqueda 
        if Token==None and AFN==None:
            return
        
        #en el caso de no ser un AFN_e
        if not(isinstance(AFN,AFN_e)):
            return
        self.__AFN=copy.deepcopy(AFN)
        self.__Token=Token
        #el toquen no puede ser <= 0
        if self.__Token>0:
            self.__definirToken(Token)

    def __definirToken(self,Token):
        #se le define un unico estado de aceptacion al automata
        self.getAFN().agregarEstadoFinal()
        #a su estado de aceptacion se le da valor al token
        self.getEstadoAceptacion().setToken(Token)
    

    def getNombreClaseLexica(self):
        return self.__Nombre_Clase_Lexica

    def getToken(self):
        return self.__Token

    def getAFN(self):
        return self.__AFN

    def getEstadoAceptacion(self):
        return self.__AFN.getEstadosAceptacion()[0]

##***********************************************************
    def __lt__(self, clase_lexica):
        return self.getNombreClaseLexica() < clase_lexica.getNombreClaseLexica()

    def __le__(self, clase_lexica):
        return self.getNombreClaseLexica() <= clase_lexica.getNombreClaseLexica()

    def __eq__(self, clase_lexica):
        return self.getNombreClaseLexica() == clase_lexica.getNombreClaseLexica()
##************************************************************
    def toDataBase(self):
        nombre=self.getNombreClaseLexica()
        token=self.getToken()
        return "||||%s__%s__%s" %(nombre,token,self.getAFN().toDataBase())

    def mostrarClaseLexica(self):
        nombre=self.getNombreClaseLexica()
        token=self.getToken()
        print("Nombre Clase Lexica:",nombre)

        print("Token:",token)

        print("AFN asociado:")
        self.getAFN().mostrarAutomata()

    def __str__(self):
        nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones = self.getAFN().__str__()
        return self.getNombreClaseLexica(), str(self.getToken()), nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones
