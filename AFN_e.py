from PySimpleAutomata import DFA,automata_IO
from Estado import *
from Transicion import *


class AFN_e:
    #Conjunto de Estados(Objeto) no vacios
    K=[]  #K_list:Formato=["estado1","estado2","estado3",.....]

    #Alfabeto que acepta el automata
    Sigma=[] #Sigma_list:Formato=['a','b','c',.....]

    #Estado de inicio del automata
    S=object() #S:Formato= "nombre estado"

    #Conjunto de Estados(Objeto) de aceptacion
    Z=[] #Z_list:Formato= [[sublista1],[sublista2],[sublista3],....]
        # sublista= ["nombre_edo_acept",num_token]

    #Conjunto de Transiciones(Objeto)
    M=[] #M_list:Formato= [[sublista1],[sublista2],[sublista3],....]
        #        sublista: Formato=[EstadoPrincipal,EstadoDestino,Simbolos]

    def __init__(self,K_list,Sigma_list,S,Z_list,M_list):
        self.__ListEstadosObjs(K_list)
        self.Sigma=Sigma_list
        self.__EstadoInicial(S)
        self.__ListEstadosAceptObjs(Z_list)
        self.__ListTransicionesObjs(M_list)

    def unirCon(self,automata2):

        #si el 'automata2' tiene mas estados finales
        if len(automata2.getEstadosAceptacion())>1:
            pass
        #si este automata tiene mas estados finales
        if len(self.getEstadosAceptacion())>1:
            pass

        #se toman el estado inicial y final del segundo automata
        edo_init2=automata2.getEdoInicial()
        edo_final2=automata2.getEstadosAceptacion()[0]
        #este automata tiene si y solo si 1 estado final
            
        #se toman el estado inicial y final de este estado
        edo_init1=self.getEdoInicial()
        edo_final1=self.getEstadosAceptacion()[0]
        #se va a sobreescribir el estado inicial y final
        #  este automata con el automata2
        #  y se mezclaran las transiciones
        # para evitar estados y transisiones repetidos se agregara un caracter
        # inicial al nombre de cada estado



        self.__juntartransiciones(automata2.getTransiciones())

    # Juntas las transiciones de los dos automatas
    def __juntartransiciones(self,transiciones2):
        trs1=self.getTransiciones();
        trs2=transiciones2
        


    def concatCon(self,estado):
        pass

    def cerraduraPositiva(self,estado):
        pass

    def opcion(self):
        
        pass

    def cerraduraKleene(self):
        pass

    def setEdoInicial(self,S):
        self.S=S

    def setEstadosAceptacion(self,Z):
        self.Z=Z

    def setTransicion(self,M):
        self.M=M

    def getEdoInicial(self):
        return self.S

    def getEstadosAceptacion(self):
        return self.Z

    def getTransiciones(self):
        return self.M

    #Formato del parametro ["estado1","estado2","estado3",.....]
    def __ListEstadosObjs(self,lista):
        for nombre_edo in lista:
            self.K.append(Estado(nombre_edo))
    #Formato de parametro "nombre estado"
    def __EstadoInicial(self,nombre_edo):
        self.S=Estado(nombre_edo)

    #Formato del parametro ["estado1","estado2","esato3",.....]
    def __ListEstadosAceptObjs(self,lista):
        # sublista= ["nombre_edo_acept",num_token]
        for sublista in lista:
            self.Z.append(Estado(sublista))

    #Formato del parametro [[sublista1],[sublista2],[sublista3],....]
    def __ListTransicionesObjs(self,lista):
        #Formato de la sublista [EstadoPrincipal,EstadoDestino,Simbolos]
        for sublista in lista:
            self.M.append(Transicion(sublista))

    def mostrarAutomata(self):
        
        print("Conjunto de Estados(Objeto) no vacios")
        for e in self.K:
           print(e.__str__())

        print("Alfabeto que acepta el automata")
        print(self.Sigma)

        print("Estado de inicio del automata")
        self.S.__str__()

        print("Conjunto de Estados(Objeto) de aceptacion")
        for e in self.Z:
            print(e.__str__())

        print("Conjunto de Transiciones(Objeto)")
        for e in self.M:
            print(e.__str__())
