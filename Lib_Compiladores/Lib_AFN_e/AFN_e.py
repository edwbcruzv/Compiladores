from Lib_Compiladores.Lib_AFN_e.Estado import Estado
from Lib_Compiladores.Lib_AFN_e.Transicion import Transicion
import copy

class AFN_e():
    
    #Formato de entrada
    # Nombre_AFN:"nombre del automata"

    # K_list:["estado1","estado2","estado3",.....]
    # Sigma_list:["a","b","c",.....]
    # S:"nombre estado"

    # Z_list: ["estado1","estado2","estado3",.....]  #cuando es un AFN

    # Z_list: [[sublista1],[sublista2],[sublista3],....] #cuando es un AFD
    #        sublista:["estado",Token]    token es un int

    # M_list: [[sublista1],[sublista2],[sublista3],....]
    #        sublista:["estado1","estado2","Simbolos"]
    def __init__(self,Nombre_AFN,K_list=None,Sigma_list=None,S=None,Z_list=None,M_list=None):

        #Nombre que recibe el automata para identificarlo
        self.__Nombre_AFN=Nombre_AFN 

        #Lista de Estados(Objeto) no vacios
        #K: [Estados("estado1"),Estados("estado2"),Estados("estado3"),.....]
        self.__K=[]  

        #Alfabeto que acepta el automata
        #Sigma_list:[Estados("estado1"),Estados("estado2"),Estados("estado3"),.....]
        self.__Sigma=[] 

        #Estado de inicio del automata
        #S:Estados("estado")
        self.__S=object() 

        #Lista de Estados(Objeto) de aceptacion
        #Z_list:[Estados("estado1"),Estados("estado2"),.....]
        #   Estados:["estado",numero_token]
        self.__Z=[] 

        #Lista de Transicion(Objeto)
        #M_list:[Transicion(sublista),Transicion(sublista),Transicion,....]
        #       sublista:["edo_origen","edo_destino","Simbolo"]
        self.__M=[] 


        if K_list==None and Sigma_list==None and S==None and Z_list==None and M_list==None:
            return
    
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

#------------------------OPERACIONES DE LOS AUTOMATAS-------------------
    #La funcion regresara un nuevo estado inicial en base a los estados ya existente
    #y asi evitar nombres de estados repetidos
    def nuevoEdo(self):
        #el nuevo estado se nombrara en base
        #al tamanio actual del conjunto de estados
        len_edos=len(self.getEstados())
        temp=Estado(str(len_edos))

        #el nuevo estado se agrega al final de la lista
        self.getEstados().append(temp)

        #pasando la referencia del nuevo estado en base
        #al conjunto de estados
        #se atualiza el tamano
        len_edos=len(self.getEstados())
        return self.getEstados()[len_edos-1]

    def agregarEstadoFinal(self):
        
        nuevo_edo_final=self.nuevoEdo()

        #si el AFN tiene mas de un estado final
        #todos estos se inicial al nuevo estado final
        for edo_final in self.getEstadosAceptacion():
            self.__ListTransicionesObjs([[edo_final.getNombre(),nuevo_edo_final.getNombre(),"E"]])

        #redefiniendo los nuevos estados finales creados
        self.setEstadosAceptacion([nuevo_edo_final])

    #se unen los automatas a partir de sus estados iniciales
    def unionEspecial(self,AFN):
        automata2=copy.deepcopy(AFN)

        #antes de hacer la union se debe de renombrar todos los estados del automata2
        self_tam=len(self.getEstados()) #cantidad de estados que tiene este automata
        a2_tam=len(automata2.getEstados()) #cantidad de estadoa del automata2
        
        for i in  range(a2_tam):
            automata2.getEstados()[i].setNombre(str(i+self_tam)) #se continuara la numeracion de cada estado
        
        #Los estados de automata2 se unen con la lista de estados de este automata
        self.getEstados().extend(automata2.getEstados())
        #ahora las transiciones de automata2 de uniran con este automata
        self.getTransiciones().extend(automata2.getTransiciones())
        #ahora se unen los afabetos evitando que se repitan
        for i in automata2.getAlfabeto():
            if i not in self.getAlfabeto():
                self.getAlfabeto().append(i)

        
        #se une el estado inicial de este automata con el automata2
        edo_init=self.getEstadoInicial()
        edo_init_2=automata2.getEstadoInicial()
        self.__ListTransicionesObjs([[edo_init.getNombre(),edo_init_2.getNombre(),"E"]])

        #se agrega el estado de aceptacion del automata2 a la lista de este automata
        self.getEstadosAceptacion().extend(automata2.getEstadosAceptacion())
        

    #Nos permite unir el automata actual con otro automata que se reciba como parametro
    def unirCon(self,AFN):
        automata2=copy.deepcopy(AFN)

        #se crea el nuevo estado inicial
        nuevo_edo_inicial=self.nuevoEdo()
        
        #antes de hacer la union se debe de renombrar todos los estados del automata2
        self_tam=len(self.getEstados()) #cantidad de estados que tiene este automata
        a2_tam=len(automata2.getEstados()) #cantidad de estadoa del automata2
        
        for i in  range(a2_tam):
            automata2.getEstados()[i].setNombre(str(i+self_tam)) #se continuara la numeracion de cada estado

        #Los estados de automata2 se unen con la lista de estados de este automata
        self.getEstados().extend(automata2.getEstados())
        #ahora las transiciones de automata2 de uniran con este automata
        self.getTransiciones().extend(automata2.getTransiciones())
        #ahora se unen los afabetos evitando que se repitan
        for i in automata2.getAlfabeto():
            if i not in self.getAlfabeto():
                self.getAlfabeto().append(i)

        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        #si este automata tiene mas estados finales
        #todos estos se unical al nuevo estado final
        tam1=len(self.getEstadosAceptacion())
        for i in range(tam1):
            edo_final1=self.getEstadosAceptacion()[i]
            self.__ListTransicionesObjs([[edo_final1.getNombre(),nuevo_edo_final.getNombre(),"E"]])

        #si el 'automata2' tiene mas estados finales
        #todos estos se unical al nuevo estado final
        tam2=len(automata2.getEstadosAceptacion())
        for i in range(tam2):
            edo_final2=automata2.getEstadosAceptacion()[i]
            self.__ListTransicionesObjs([[edo_final2.getNombre(),nuevo_edo_final.getNombre(),"E"]])
        
        #ahora se unira el nuevo estado inicial
        #con el estado inicial de este automata
        edo_init1=self.getEstadoInicial()
        self.__ListTransicionesObjs([[nuevo_edo_inicial.getNombre(),edo_init1.getNombre(),"E"]])
        
        #ahora se unira el nuevo estado inicial
        #con el estado inicial de 'automata2'
        edo_init2=automata2.getEstadoInicial()
        self.__ListTransicionesObjs([[nuevo_edo_inicial.getNombre(),edo_init2.getNombre(),"E"]])

        #redefiniendo los nuevos estados iniciales creados
        #redefiniendo los nuevos estados finales creados
        self.setEstadoInicial(nuevo_edo_inicial)
        self.setEstadosAceptacion([nuevo_edo_final])

    def concatCon(self,AFN):
        automata2=copy.deepcopy(AFN)

        #antes de hacer la concatenacion  se debe de renombrar todos los estados edel automata2
        self_tam=len(self.getEstados()) #cantidad de estados que tiene este automata
        a2_tam=len(automata2.getEstados()) #cantidad de estadoa del automata2
        
        for i in  range(a2_tam):
            automata2.getEstados()[i].setNombre(str(i+self_tam)) #se continuara la numeracion de cada estado

        #Los estados de automata2 se unen con la lista de estados de este automata
        self.getEstados().extend(automata2.getEstados())
        #ahora las transiciones de automata2 de uniran con este automata
        self.getTransiciones().extend(automata2.getTransiciones())
        #ahora se unen los afabetos evitando que se repitan
        for i in automata2.getAlfabeto():
            if i not in self.getAlfabeto():
                self.getAlfabeto().append(i)

        #si este automata tiene mas estados finales
        #todos estos se uniran al estado inicial de
        # 'automata2'
        for e in self.getEstadosAceptacion():
            self.__ListTransicionesObjs([[e.getNombre(),automata2.getEstadoInicial().getNombre(),"E"]])

        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        print("-----------------Nuevo estado final agregado :",nuevo_edo_final.__str__())


        #si el 'automata2' tiene mas estados finales
        #todos estos se inicial al nuevo estado final
        for e in automata2.getEstadosAceptacion():
            self.__ListTransicionesObjs([[e.getNombre(),nuevo_edo_final.getNombre(),"E"]])

        #redefiniendo los nuevos estados finales creados
        self.setEstadosAceptacion([nuevo_edo_final])


    def cerraduraPositiva(self):
        #se crea el nuevo estado inicial
        nuevo_edo_inicial=self.nuevoEdo()
        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        #si este automata tiene mas estados finales
        #todos estos se uniran al nuevo estado final
        tam=len(self.getEstadosAceptacion())
        for i in range(tam):
            edo_final1=self.getEstadosAceptacion()[i]
            t=[edo_final1.getNombre(),nuevo_edo_final.getNombre(),"E"]
            self.__ListTransicionesObjs([t])
        
        #se crea la transicion que retrocede al estado inicial
        t=[nuevo_edo_final.getNombre(),self.getEstadoInicial().getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        #ahora se unira el nuevo estado inicial
        #con el estado inicial de este automata
        edo_init1=self.getEstadoInicial()
        t=[nuevo_edo_inicial.getNombre(),edo_init1.getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        #redefiniendo los nuevos estados iniciales creados
        #redefiniendo los nuevos estados finales creados
        self.setEstadoInicial(nuevo_edo_inicial)
        self.setEstadosAceptacion([nuevo_edo_final])

    def cerraduraKleene(self):
        #Despues de esta funcion solo existira
        #un estado inicial y uno final
        self.cerraduraPositiva()

        #ahora solo quedara unir el inicial con el final ya existentes
        edo_init=self.getEstadoInicial()
        edo_final=self.getEstadosAceptacion()[0]
        t=[edo_init.getNombre(),edo_final.getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        #redefiniendo los nuevos estados iniciales creados
        #redefiniendo los nuevos estados finales creados
        # self.setEstadoInicial(edo_init)
        # self.setEstadosAceptacion([edo_final])

    def opcion(self):
        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        #si este automata tiene mas estados finales
        #todos estos se uniran al nuevo estado final
        tam=len(self.getEstadosAceptacion())
        for i in range(tam):
            edo_final=self.getEstadosAceptacion()[i]
            t=[edo_final.getNombre(),nuevo_edo_final.getNombre(),"E"]
            self.__ListTransicionesObjs([t])

        #se crea la transicion del estado inicial al final
        t=[self.getEstadoInicial().getNombre(),nuevo_edo_final.getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        #solo se redefine el estado final 
        self.setEstadosAceptacion([nuevo_edo_final])

#-------------------------SET'S Y GET'S--------------------------
    def setNombreAFN(self,Nombre_AFN):
        self.__Nombre_AFN=Nombre_AFN

    def setEstados(self,K):
        self.__K=K

    def setAlfabeto(self,Sigma):
        self.__Sigma=Sigma

    def setEstadoInicial(self,S):
        self.__S=S

    def setEstadosAceptacion(self,Z):
        self.__Z=Z

    def setTransiciones(self,M):
        self.__M=M
##**********************************************
    def getNombreAFN(self):
        return self.__Nombre_AFN

    def getEstados(self):
        return self.__K

    def getAlfabeto(self):
        return self.__Sigma

    def getEstadoInicial(self):
        return self.__S

    def getEstadosAceptacion(self):
        return self.__Z

    def getTransiciones(self):
        return self.__M
##***********************************************************
    def __lt__(self,automata):
        return self.getNombreAFN()<automata.getNombreAFN()

    def __le__(self,automata):
        return self.getNombreAFN()<=automata.getNombreAFN()

    def __eq__(self,automata):
        return self.getNombreAFN()==automata.getNombreAFN()

#-----------------------------------------------------------------
#-------------METODOS AL INICIAR LA CONSTRUCCION DE UN AUTOMATA----------------------

    # K_list:["estado1","estado2","estado3",.....]
    def __ListEstadosObjs(self,K_list):
        for nombre_edo in K_list:
            self.getEstados().append(Estado(nombre_edo))
        self.getEstados().sort()
    # Sigma_list:["a","b","c",.....]
    def __ListAlfabeto(self,Sigma_list):
        #ahora se unen los afabetos evitando que se repitan
        lista_aux=[]
        for i in Sigma_list:
            if i not in lista_aux:
                lista_aux.append(i)
        self.setAlfabeto(lista_aux)
        self.getAlfabeto().sort()

    # S:"nombre estado"
    def __EstadoInicial(self,S):
        temp_edo=Estado(S)
        #se busca el estado en la lista de estado para ver si existe
        #y se agregara a la transicion, pero tomando el estado de la lista
        for e in self.getEstados():
            if e==temp_edo:    
                self.setEstadoInicial(e)
        #En caso de no existir un estado que viene en las transiciones no se agregara
        #no se ordena al ser estado unico

    # Z_list: ["estado1","estado2","estado3",.....]  #cuando es un AFN

    # Z_list: [[sublista1],[sublista2],[sublista3],....] #cuando es un AFD
    #        sublista:["estado",Token]    token es un int
    def __ListEstadosAceptObjs(self,Z_list):
        #elem puede ser un dtr o una lista
        
        for elem in Z_list:
            edo_temp=Estado(elem) #en caso de haber token aqui se almacena
            #se busca el estado en la lista de estado para ver si existe
            #y se agregara a la transicion, pero tomando el estado de la lista
            
            for e in self.getEstados():
                if e==edo_temp:    
                    self.getEstadosAceptacion().append(e)
                    e.setToken(edo_temp.getToken())
            #En caso de no existir un estado que viene en las transiciones no se agregara
            
        self.getEstadosAceptacion().sort()

    # M_list: [[sublista1],[sublista2],[sublista3],....]
    #        sublista:["estado1","estado2","Simbolos"]
    def __ListTransicionesObjs(self,M_list):
        #Formato de la sublista ["EstadoPrincipal","EstadoDestino","Simbolos"]
        for sublista in M_list:
            temp_edo1=Estado(sublista[0]) #estado principal temporal
            temp_edo2=Estado(sublista[1]) #estado destino temporal
            simb=sublista[2]

            #se busca el estado en la lista de estado para ver si existe
            #y se agregara a la transicion, pero tomando el estado de la lista
            for e1 in self.getEstados():
                if e1==temp_edo1:
                    for e2 in self.getEstados():
                        if e2==temp_edo2:
                            self.getTransiciones().append(Transicion(e1,e2,simb))
            #En caso de no existir un estado que viene en las transiciones no se agregara

        #se ordenan las transiciones por medio del estado principal
        self.getTransiciones().sort()
#------------------------------------------------------------------------------
    def toDataBase(self):
        nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones = self.__str__()
        return "|||%s__%s__%s__%s__%s__%s" % (nombre_AFN, num_estados, str_lenguaje, 
        str_edo_inicial, str_estados_aceptacion, str_transiciones)

    def mostrarAutomata(self):
        nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones = self.__str__()
        print("Nombre de AFN :",nombre_AFN)

        print("Conjunto de Estados(Objeto) no vacios :", num_estados)
        for e in self.getEstados():
           print(e.__str__())

        print("Alfabeto que acepta el automata")
        print(str_lenguaje)

        print("Estado de inicio del automata")
        print(str_edo_inicial)

        print("Conjunto de Estados(Objeto) de aceptacion")
        print(str_estados_aceptacion)

        print("Conjunto de Transiciones(Objeto)")
        print(str_transiciones)


        # print("Alfabeto que acepta el automata")
        # print(self.getAlfabeto())
        # print("Estado de inicio del automata")
        # print(self.getEstadoInicial().__str__())
        # print("Conjunto de Estados(Objeto) no vacios")
        # for e in self.getEstados():
        #    print(e.__str__())
        # print("Conjunto de Estados(Objeto) de aceptacion")
        # for e in self.getEstadosAceptacion():
        #     print(e.__str__())

        # print("Conjunto de Transiciones(Objeto)")
        # for e in self.getTransiciones():
        #     print(e.__str__()) 
            

    def __str__(self):
        #FORMATO EN EL QUE NOS BASAREMOS 

        # nombre_AFN: "nombreAFN"
        # num_estados: num  (es un int)
        # str_lenguaje: "simbolo1,simbolo2,simbolo3"
        # str_edo_inicial: "edo"
        # str_estados_aceptacion: "edo1-edo2-edo3" o "[edo1,token]-[edo2,token]-[edo3,token]"
        # str_transiciones:"[edo,edo,simbolo]-[edo,edo,simbolo]-[edo,edo,simbolo]"
        
        nombre_AFN=self.getNombreAFN()

        num_estados=str(len(self.getEstados())-1)

        str_lenguaje=""
        i=1
        for s in self.getAlfabeto():
            str_lenguaje+=s
            if i==len(self.getAlfabeto()):
                break
            str_lenguaje+=","
            i+=1

        str_edo_inicial=self.getEstadoInicial().__str__()

        str_estados_aceptacion=""
        i=1
        for e in self.getEstadosAceptacion():
            
            str_estados_aceptacion+=e.__str__()
            if i==len(self.getEstadosAceptacion()):
                break
            str_estados_aceptacion+="-"
            i+=1
        
        str_transiciones=""
        i=1
        for t in self.getTransiciones():
            str_transiciones+=t.__str__()
            if i==len(self.getTransiciones()):
                break
            str_transiciones+="-"
            i+=1

        return nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones
