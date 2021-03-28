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
        #primero se empieza a definir y a crear los estados de aceptacion, ya que
        #para los demas atributos necesitaremos la lista de todos los estados
        self.__ListEstadosObjs(K_list)

        #se defina el arlfabeto que aceptara el automata
        self.__ListAlfabeto(Sigma_list)

        #se definira el estado inicial
        self.__EstadoInicial(S)

        #se definiran los estados de aceptacion
        self.__ListEstadosAceptObjs(Z_list)

        #se definira las transiciones
        self.__ListTransicionesObjs(M_list)


    def unirCon(self,automata2):
        #se crea el nuevo estado inicial
        nuevo_edo_inicial='1000'
        #se crea el nuevo estado final
        nuevo_edo_final='100'

        #si este automata tiene mas estados finales
        #todos estos se unical al nuevo estado final
        tam1=len(self.getEstadosAceptacion())
        for i in range(tam1):
            edo_final1=self.getEstadosAceptacion()[i]
            [edo_final1,nuevo_edo_final,"£"]

        #si el 'automata2' tiene mas estados finales
        #todos estos se unical al nuevo estado final
        tam2=len(automata2.getEstadosAceptacion())
        for i in range(tam2):
            edo_final2=automata2.getEstadosAceptacion()[i]
            [edo_final2,nuevo_edo_final,"£"]
        
        #ahora se unira el nuevo estado inicial
        #con el estado inicial de este automata
        edo_init1=self.getEdoInicial()
        [nuevo_edo_inicial,edo_final1,"£"]
        
        #ahora se unira el nuevo estado inicial
        #con el estado inicial de 'automata2'
        edo_init2=automata2.getEdoInicial()
        [nuevo_edo_inicial,edo_final2,"£"]


    def concatCon(self,automata2):
        #si este automata tiene mas estados finales
        #todos estos se uniran al estado inicial de
        # 'automata2'
        tam1=len(self.getEstadosAceptacion())
        for i in range(tam1):
            edo_final=self.getEstadosAceptacion()[i]
            [edo_final,automata2.getEdoInicial(),"£"]

    def cerraduraPositiva(self,estado):
        pass

    def cerraduraKleene(self):
        pass

    def opcion(self):
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




#-------------METODOS AL INICIAR LA CONSTRUCCION DE UN AUTOMATA----------------------
    #Formato del parametro ["estado1","estado2","estado3",.....]
    def __ListEstadosObjs(self,lista):
        for nombre_edo in lista:
            self.K.append(Estado(nombre_edo))
        self.K.sort()

    def __ListAlfabeto(self,lista):
        self.Sigma=lista
        self.Sigma.sort()

    #Formato de parametro "nombre estado"
    def __EstadoInicial(self,nombre_edo):
        temp_edo=Estado(nombre_edo)
        #se busca el estado en la lista de estado para ver si existe
        #y se agregara a la transicion, pero tomando el estado de la lista
        for e in self.K:
            if e==temp_edo:    
                self.S=e
        #En caso de no existir un estado que viene en las transiciones no se agregara
        #no se ordena al ser estado unico


    #Formato del parametro ["estado1","estado2","esato3",.....]
    def __ListEstadosAceptObjs(self,lista):
        # sublista= ["nombre_edo_acept",num_token]
        for sublista in lista:
            temp_edo=Estado(sublista[0])
            #se busca el estado en la lista de estado para ver si existe
            #y se agregara a la transicion, pero tomando el estado de la lista
            for e in self.K:
                if e==temp_edo:    
                    e.setToken(sublista[1])
                    self.Z.append(e)
            #En caso de no existir un estado que viene en las transiciones no se agregara
        
        self.Z.sort()

    #Formato del parametro [[sublista1],[sublista2],[sublista3],....]
    def __ListTransicionesObjs(self,lista):
        #Formato de la sublista [EstadoPrincipal,EstadoDestino,Simbolos]
        for sublista in lista:
            temp_edo1=Estado(sublista[0]) #estado principal temporal
            temp_edo2=Estado(sublista[1]) #estado destino temporal
            simb=sublista[2]

            #se busca el estado en la lista de estado para ver si existe
            #y se agregara a la transicion, pero tomando el estado de la lista
            for e1 in self.K:
                if e1==temp_edo1:
                    
                    for e2 in self.K:
                        if e2==temp_edo2:
    
                            self.M.append(Transicion(e1,e2,simb))
            #En caso de no existir un estado que viene en las transiciones no se agregara

        #se ordenan las transiciones por medio del estado principal
        self.M.sort()


            
        
    def mostrarAutomata(self):
        
        print("Conjunto de Estados(Objeto) no vacios")
        for e in self.K:
           print(e.__str__())

        print("Alfabeto que acepta el automata")
        print(self.Sigma)

        print("Estado de inicio del automata")
        print(self.S.__str__())

        print("Conjunto de Estados(Objeto) de aceptacion")
        for e in self.Z:
            print(e.__str__())

        print("Conjunto de Transiciones(Objeto)")
        for e in self.M:
            print(e.__str__())
