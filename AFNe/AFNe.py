
class Estado:
    #elem puede ser lista o string ya que esta sobrecargado
    def __init__(self,elem,Token=0):
        
        if list==type(elem):
            self.Nombre=elem[0]
            self.Token=elem[1]
        elif str==type(elem):
            self.Nombre=elem
            self.Token=Token
        

    def setNombre(self,Nombre):
        self.Nombre=Nombre

    #Al ser estado de aceptacion se requerira su token
    def setToken(self,Token):
        self.Token=Token

    def getNombre(self):
        return self.Nombre

    def getToken(self):
        return self.Token

    def __lt__(self,estado):
        return self.getNombre()<estado.getNombre()

    def __le__(self,estado):
        return self.getNombre()<=estado.getNombre()

    def __eq__(self,estado):
        return self.getNombre()==estado.getNombre()

    def __str__(self):
        #en el caso de ser un estado de aceptacion tambien se mostrara su token
        if self.Token:
            return "%s [shape=doublecircle]" %(
                self.Nombre)
        else: #como no es estado de aceptacion solo se mostrara su nombre
            return self.Nombre


class Transicion:
    
    def __init__(self,EdoPrincipal,NomEdoDestino,Simbolo):
        
        #Estado(Objeto) Principal
        self.EstadoPrincipal=EdoPrincipal
        #Estado(Objeto) Destino
        self.EstadoDestino=NomEdoDestino
        #Simbolo de transicion
        self.Simbolo=Simbolo
        

    def setEstadoPrincipal(self,estado):
        self.EstadoPrincipal=estado

    def setEstadoDestino(self,estado):
        self.EstadoDestino=estado

    def setSimbolo(self,simbolo):
        self.Simbolo=simbolo

    def getEstadoPrincipal(self):
        return self.EstadoPrincipal

    def getEstadoDestino(self):
        return self.EstadoDestino

    def getSimbolo(self):
        return self.Simbolo
    
    def __lt__(self,transicion):
        return self.EstadoPrincipal<transicion.getEstadoPrincipal()

    def __le__(self,transicion):
        return self.EstadoPrincipal<=transicion.getEstadoPrincipal()

    def __str__(self):

        return "s%s -> s%s [label=\"%s\"] " %(
            self.EstadoPrincipal.getNombre(),self.EstadoDestino.getNombre(),self.Simbolo.__str__())


class AFN_e:
    

    def __init__(self,K_list,Sigma_list,S,Z_list,M_list):
        #Conjunto de Estados(Objeto) no vacios
        self.K=[]  #K_list:Formato=[estado1,estado2,estado3,.....]

        #Alfabeto que acepta el automata
        self.Sigma=[] #Sigma_list:Formato=['a','b','c',.....]

        #Estado de inicio del automata
        self.S=object() #S:Formato= "nombre estado"

        #Conjunto de Estados(Objeto) de aceptacion
        self.Z=[] #Z_list:Formato= [estado1,estado2,estado3,.....]

        #Conjunto de Transiciones(Objeto)
        self.M=[] #M_list:Formato= [[sublista1],[sublista2],[sublista3],....]
            #        sublista: Formato=[estado1,estado2,Simbolos]
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
        temp=Estado(str(len(self.K)))
        #el nuevo estado se agrega al final de la lista
        self.K.append(temp)
        #pasando la referencia del nuevo estado en base
        # al conjunto de estados
        return self.K[len(self.K)-1]

    def unirCon(self,automata2):
        #se crea el nuevo estado inicial
        nuevo_edo_inicial=self.nuevoEdo()
        
        #antes de hacer la union se debe de renombrar todos los estados edel automata2
        self_tam=len(self.K) #cantidad de estados que tiene este automata
        a2_tam=len(automata2.K) #cantidad de estadoa del automata2
        
        for i in  range(a2_tam):
            automata2.K[i].setNombre(str(i+self_tam)) #se continuara la numeracion de cada estado

        #Los estados de automata2 se unen con la lista de estados de este automata
        self.K.extend(automata2.K)
        #ahora las transiciones de automata2 de uniran con este automata
        self.M.extend(automata2.M)
        #ahora se unen los afabetos
        self.Sigma.extend(automata2.Sigma)

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
        edo_init1=self.getEdoInicial()
        self.__ListTransicionesObjs([[nuevo_edo_inicial.getNombre(),edo_init1.getNombre(),"E"]])
        
        #ahora se unira el nuevo estado inicial
        #con el estado inicial de 'automata2'
        edo_init2=automata2.getEdoInicial()
        self.__ListTransicionesObjs([[nuevo_edo_inicial.getNombre(),edo_init2.getNombre(),"E"]])

        self.S=nuevo_edo_inicial #redefiniendo los nuevos estados iniciales creados
        self.Z=[nuevo_edo_final] #redefiniendo los nuevos estados finales creados

    def concatCon(self,automata2):

        #antes de hacer la concatenacion  se debe de renombrar todos los estados edel automata2
        self_tam=len(self.K) #cantidad de estados que tiene este automata
        a2_tam=len(automata2.K) #cantidad de estadoa del automata2
        
        for i in  range(a2_tam):
            automata2.K[i].setNombre(str(i+self_tam)) #se continuara la numeracion de cada estado

        #Los estados de automata2 se unen con la lista de estados de este automata
        self.K.extend(automata2.K)
        #ahora las transiciones de automata2 de uniran con este automata
        self.M.extend(automata2.M)
        #ahora se unen los afabetos
        self.Sigma.extend(automata2.Sigma)

        #si este automata tiene mas estados finales
        #todos estos se uniran al estado inicial de
        # 'automata2'
        tam1=len(self.getEstadosAceptacion())
        for i in range(tam1):
            edo_final=self.getEstadosAceptacion()[i]
            self.__ListTransicionesObjs([[edo_final.getNombre(),automata2.getEdoInicial().getNombre(),"E"]])

        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        #si el 'automata2' tiene mas estados finales
        #todos estos se inicial al nuevo estado final
        tam2=len(automata2.getEstadosAceptacion())
        for i in range(tam2):
            edo_final2=automata2.getEstadosAceptacion()[i]
            self.__ListTransicionesObjs([[edo_final2.getNombre(),nuevo_edo_final.getNombre(),"E"]])

        # self.S=nuevo_edo_inicial #redefiniendo los nuevos estados iniciales creados
        self.Z=[nuevo_edo_final] #redefiniendo los nuevos estados finales creados

    def cerraduraPositiva(self):
        #se crea el nuevo estado inicial
        nuevo_edo_inicial=self.nuevoEdo()
        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        #si este automata tiene mas estados finales
        #todos estos se uniran al nuevo estado final
        tam=len(self.getEstadosAceptacion())
        for i in range(tam):
            edo_final1=self.Z[i]
            t=[edo_final1.getNombre(),nuevo_edo_final.getNombre(),"E"]
            self.__ListTransicionesObjs([t])
        
        #se crea la transicion que retrocede al estado inicial
        t=[nuevo_edo_final.getNombre(),self.getEdoInicial().getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        #ahora se unira el nuevo estado inicial
        #con el estado inicial de este automata
        edo_init1=self.getEdoInicial()
        t=[nuevo_edo_inicial.getNombre(),edo_init1.getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        self.S=nuevo_edo_inicial #redefiniendo los nuevos estados iniciales creados
        self.Z=[nuevo_edo_final] #redefiniendo los nuevos estados finales creados


    def cerraduraKleene(self):
        #Despues de esta funcion solo existira
        #un estado inicial y uno final
        self.cerraduraPositiva()

        #ahora solo quedara unir el inicial con el final ya existentes
        edo_init=self.getEdoInicial()
        edo_final=self.getEstadosAceptacion()[0]
        t=[edo_init.getNombre(),edo_final.getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        self.S=edo_init #redefiniendo los nuevos estados iniciales creados
        self.Z=[edo_final] #redefiniendo los nuevos estados finales creados


    def opcion(self):
        #se crea el nuevo estado final
        nuevo_edo_final=self.nuevoEdo()

        #si este automata tiene mas estados finales
        #todos estos se uniran al nuevo estado final
        tam=len(self.getEstadosAceptacion())
        for i in range(tam):
            edo_final=self.Z[i]
            t=[edo_final.getNombre(),nuevo_edo_final.getNombre(),"E"]
            self.__ListTransicionesObjs([t])

        #se crea la transicion del estado inicial al final
        t=[self.getEdoInicial().getNombre(),nuevo_edo_final.getNombre(),"E"]
        self.__ListTransicionesObjs([t])

        #solo se redefine el estado final 
        self.Z=[nuevo_edo_final] 

#-------------------------SET'S Y GET'S--------------------------

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



#-----------------------------------------------------------------
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
        #Formato de la sublista ["EstadoPrincipal","EstadoDestino","Simbolos"]
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
#------------------------------------------------------------------------------
#------------------ARMADO DEL DOCUMENTO DEL ARCHIVO .DOT-----------------------
            
        
    def mostrarAutomata(self):

        print("Alfabeto que acepta el automata")
        print(self.Sigma)

        print("Estado de inicio del automata")
        print(self.S.__str__())

        print("Conjunto de Estados(Objeto) no vacios")
        for e in self.K:
           print(e.__str__())

        print("Conjunto de Estados(Objeto) de aceptacion")
        for e in self.Z:
            print(e.__str__())

        print("Conjunto de Transiciones(Objeto)")
        for e in self.M:
            print(e.__str__())