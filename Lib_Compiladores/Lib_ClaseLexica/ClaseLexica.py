from Lib_Compiladores.Lib_AFN_e import AFN_e
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
        self.__AFN=copy.copy(AFN)
        #el toquen no puede ser <= 0
        if Token>0:
            self.__definirToken(Token)

    def __definirToken(self,Token):
        #se le define un unico estado de aceptacion al automata
        self.getAFN().agregarEstadoFinal()
        #a su estado de aceptacion se le da valor al token
        self.getAFN().getEstadoAceptacion()[0].setToken(Token)
    

    def getNombreClaseLexica(self):
        return self.__Nombre_Clase_Lexica

    def getToken(self):
        return self.__Token

    def getAFN(self):
        return self.__AFN

    def getEstadoAceptacion(self):
        return self.__AFN.getEstadoAceptacion()[0]

    def toDataBase():
        nombre,token,estado_acept=self.__str__()
        return "%s__%s__%s__%s" %(nombre,token,estado_acept,self.getAFN().toDataBase())

    def mostrarClaseLexica(self):
        nombre,token,estado_acept=self.__str__()
        print("Nombre Clase Lexica:",nombre)

        print("Token:",token)

        print("Estado de Aceptacion",estado_acept)

    def __str__(self):

        return self.getNombreClaseLexica(),str(self.getToken()),self.getEstadoAceptacion().__str__()
