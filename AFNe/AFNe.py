
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
            return "%s [shape=doublecircle] %d" %(
                self.Nombre,self.Token)
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
        self.S=object() #S:Formato= "nombre estado" pero despues sera un objeto estado

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

    def setTransiciones(self,M):
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


class convertAFD:

    def __init__(self,afn):
        # Formato de la lista de conjuntos epsilon 
        # Lista de conjuntos=[[sublista1],[sublista2],[sublista3],....]
        # sublista=["Estado1","Estado2",...,"Estadon"]
        self.conjuntos_list=[]

        self.afn=afn
        self.Sigma=afn.Sigma
        # Formato de la lista de transiciones 
        # M=[[sublista1],[sublista2],[sublista3],....]
        # sublista=["EstadoPrincipal","EstadoDestino","Simbolos"]
        self.transiciones=self.afn.M
        self.afd=object()
        #inicio del proceso
        self.__analisisDe()

    def getAFD(self):
        return self.afd
 

    #conjunto de estados destino al tener un "E" RECURSIVO
    #los estados se agregan a la variable conjunto recibido
    def __cerraduraEpsilon(self,conjunto):
      
        # ahora se buscan las transiciones donde
        # el estado principal sea la variable estado,
        # el simbolo sea "E"
        # despues se toma el estado destino y se agrega al conjunto
        estado=conjunto[len(conjunto)-1]
        for T in self.transiciones:
            edo_prin=T.getEstadoPrincipal() #Estado Principal
            edo_dest=T.getEstadoDestino() #Estado Destino
            sim=T.getSimbolo() #Simbolo
            if edo_prin==estado and sim=="E":
                #se evita que no se repitan estados en el conjunto
                for e in conjunto:
                    if e==edo_dest:
                        #retorna si se repite
                        return 
                conjunto.append(edo_dest)
                self.__cerraduraEpsilon(conjunto)
        return

    # Se crea un Conjunto de cerradura epsilon a partir del estado que se envie
    def __creaConjuntoEpsilon(self,estado):
        conjunto=[]
        #por defecto el mismo estado se incluye en el conjunto
        conjunto.append(estado)
        self.__cerraduraEpsilon(conjunto)
        conjunto.sort()
        return conjunto

    

    #regresa una lista de Estado destino de un conjunto de transiciones
    #en base al simbolo
    def __mover(self,conjunto,simbolo):
        lista_edos=[]
        for estado in conjunto:
        # ahora se buscan las transiciones donde
        # el estado principal sea la variable "estado",
        # el simbolo sea "simbolo"
        # despues se toma el estado destino y se agrega al conjunto
            for T in self.transiciones:
                edo_prin=T.getEstadoPrincipal() #Estado Principal
                edo_dest=T.getEstadoDestino() #Estado Destino
                sim=T.getSimbolo() #Simbolo
                if edo_prin==estado and sim==simbolo:
                    lista_edos.append(edo_dest)
        lista_edos.sort()
        return lista_edos

    #verifica que el conjunto que recibe como parametro exista
    #si existe regresa el subindice de la lista
    #si no existe lo agrega a la lista y regresa el subindice
    def __existeConjunto(self,conjunto):
        #se da por h
        igualdad = False
        #se dara por hecho que por defecto todos los conjuntos estan ordenado
        #sino aplicar un sort()
        subindice_conjunto=0
        for C in self.conjuntos_list:
            #se da por hecho que los conjuntos son diferentes
            igualdad = False
            # La unica forma de que sean iguales es:
            if len(C)==len(conjunto): #que sean del mismo tamano y todos los elementos iguales
                igualdad = True #por ahora son iguales por tamano
                tam=len(C)
                for i in range(tam):
                    if not(C[i]==conjunto[i]): #si uno es diferente, entonces no solo iguales
                        igualdad=False 
                        break #se rompe el ciclo de analisis y se continua con otro conjunto

                    #si un elemento es igual se coninua con el otro elemento

                # por ahora pudieron suceder dos cosas,
                if igualdad==False:
                    #se rompio el ciclo porque son elementos diferentes de dos conjuntos tamanios iguales
                    continue #se continua con otro conjunto
                # o los dos conjuntos si son iguales
                if igualdad==True:
                    #se regresa el subindice del conjunto repetido
                    return subindice_conjunto

            #se aumenta el subindice ya que pasamos al siguiente conjunto de la lista
            subindice_conjunto=subindice_conjunto+1

        #se a verificado con todos y al terminar se da por hecho que no se repite 
        #se agrega al la lista de conjuntos
        self.conjuntos_list.append(conjunto)
        # y se regresa el subindice de la lista
        return self.conjuntos_list.index(conjunto)


        
    #Regresara un nuevo conjunto o nada si es un estado final
    #Puede regresar un conjunto repetido
    def __irA(self,conjunto,simbolo):

        estados=self.__mover(conjunto,simbolo)
        conj_return=[]

        for e in estados:
            #print("Mover",e.__str__())
            conj_temp=self.__creaConjuntoEpsilon(e)
            conj_return.extend(conj_temp)
        conj_return.sort()

        if conj_return==[]:
            return False
        return self.__existeConjunto(conj_return)

    #esta es la funcion principal, la que se encarga del analisis del automata 
    def __analisisDe(self):     

        #se toma como inicio el estado inicial del automata afn
        c_temp=self.__creaConjuntoEpsilon(self.afn.getEdoInicial())
        self.conjuntos_list.append(c_temp)

        #se define las variables para el nuevo AFD
        #para ello se usa la clase AFN-e, pero tendra las propiedades
        #de un AFD
        #Conjunto de Estados(Objeto) no vacios
        afd_K=[]  #K_list:Formato=["estado1","estado2","estado3",.....] listo

        #Alfabeto que acepta el automata
        afd_Sigma=[] #Sigma_list:Formato=['a','b','c',.....] listo

        #Estado de inicio del automata
        afd_S='' #S:Formato= "nombre estado" listo

        #Conjunto de Estados(Objeto) de aceptacion
        afd_Z=[] #Z_list:Formato= [[sublista1],[sublista2],[sublista3],,.....]
            #        sublista: Formato=["estado",Token]

        #Conjunto de Transiciones(Objeto)
        afd_M=[] #M_list:Formato= [[sublista1],[sublista2],[sublista3],....] listo
            #        sublista: Formato=[estado1,estado2,Simbolos]
        

        #El alfabeto del afd sera el mismo que el afN
        afd_Sigma=self.afn.Sigma

        #contador para los conjuntos creados
        i=0
        #se define el estado inicial del automata
        afd_S=str(i)

        while True:
            #inicio del analisis con cada simbolo del alfabeto del automata
            #tambien se agregan los nuevos estados al afd
            afd_K.append(str(i))

            for s in self.Sigma:
                indice_conj=self.__irA(self.conjuntos_list[i],s)

                #se imprime el cunjunto que est esta revisando
                print("conjunto:",i,"indice:",indice_conj,"Simbolos:",s)
                for e in self.conjuntos_list[i]:
                    print(e.__str__())

                
                
                #si es False significa que es un jonunto vacion lo que se regresa
                if not(indice_conj==False):
                    #ya que termino el proceso de la funcion irA()
                    #se empieza con la contruccion del AFD

                    #se define la transicion actual creada
                    #el subindice del conjunto que se analiza nos define el nombre del estado origen
                    #el subindice del conjunto que da como resultado nos define el nombre del estado destino
                    #el simbolo con el que se analiza la transicion sera el simbolo de la transicion
                    transicion_temp=[str(i),str(indice_conj),s]
                    print(str(i),str(indice_conj),s)
                    #se agrega la transicion creada
                    afd_M.append(transicion_temp)
            #pasando al siguiente conjunto
            i=i+1
            #para el caso de que ya no existas conjuntos por analizar se rompe el ciclo para terminar
            if i >= len(self.conjuntos_list):
                break

            
        #al terminar el analisis se definen los nuevos estados de aceptacion
        #de la lista de conjuntos, solo puede existir un estado de aceptacion
        #por lo cual debemos tabmn obtener su Token
        
        
        #Se identificaran como estados de aceptacion aquellos que tu token sean > 0

        for edo_afn in self.afn.K: #estados del afd
            if edo_afn.getToken() > 0:
            #al encontrar un estado de aceptacion del afn, ahora se buscaran en el conjunto
                j=0 #subindice del conjunto
                for conj_temp in self.conjuntos_list:
                    # e es estado a partir del afn
                    for e in conj_temp:
                        #si e existe como estado de aceptacion en afn
                        if e == edo_afn: #estados del afd
                            #se agrega a la lista de estados de aceptacion definiendo el token del afn
                            nuevo_edo_final=[str(j),edo_afn.getToken()]
                            # y se agregara a la lista de estados finales del afd
                            afd_Z.append(nuevo_edo_final)
                    #en caso de no encontrar en el conj_temp[j] se va con el que sigue
                    j=j+1
        #todos los connjuntos que se analizaron
        # print("Todos los conjuntos que se analizaron")
        # k=0
        # for c in self.conjuntos_list:
        #     print("conjunto: ",k) 
        #     for e in c:
        #                 print(e.__str__())

        #     k=k+1

        #se crea el automata con las propiedadesya creadas
        self.afd=AFN_e(afd_K,afd_Sigma,afd_S,afd_Z,afd_M)

        