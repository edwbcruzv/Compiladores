from AFNe import *


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

        #inicio del proceso
        self.__analisisDe()
 

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
        #igualdad = False
        #se dara por hecho que por defecto todos los conjuntos estan ordenado
        #sino aplicar un sort()
        subindice_conjunto=0
        for C in self.conjuntos_list:
            #se da por hecho que los conjuntos son diferentes
            #igualdad = False
            # La unica forma de que sean iguales es:
            if len(C)==len(conjunto): #que sean del mismo tamano y todos los elementos iguales
                #igualdad = True #por ahora son iguales por tamano
                tam=len(C)
                for i in range(tam):
                    if not(C[i]==conjunto[i]): #si uno es diferente, entonces no solo iguales
                        #igualdad=False 
                        break #se rompe el ciclo de analisis y se continua con otro conjunto
                #si no se rompe el ciclo entonces el conjunto se repite y se regresa el subinice
                #de la lista de conjuntos 
                return subindice_conjunto

            #se aumenta el subindice ya que pasamos al siguiente conjunto de la lista
            subindice_conjunto=subindice_conjunto+1

        #se a verificado con todos y al terminar se da por hecho que no se repite 
        #se agrega al la lista de conjuntos
        self.conjuntos_list.append(conjunto)
        # y se regresa el subindice de la lista
        return subindice_conjunto-1


        
    #Regresara un nuevo conjunto o nada si es un estado final
    #Puede regresar un conjunto repetido
    def __irA(self,conjunto,simbolo):

        estados=self.__mover(conjunto,simbolo)
        conj_return=[]

        for e in estados:
            conj_temp=self.__creaConjuntoEpsilon(e)
            conj_return.extend(conj_temp)
        conj_return.sort()   

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
                #se imprime el cunjunto que est esta revisando
                print("Conjunto:",i,"Simbolos:",s)
                for e in self.conjuntos_list[i]:
                    print(e.__str__())
                indice_conj=self.__irA(self.conjuntos_list[i],s)

                #ya que termino el proceso de la funcion irA()
                #se empieza con la contruccion del AFD

                #se define la transicion actual creada
                #el subindice del conjunto que se analiza nos define el nombre del estado origen
                #el subindice del conjunto que da como resultado nos define el nombre del estado destino
                #el simbolo con el que se analiza la transicion sera el simbolo de la transicion
                transicion_temp=[str(i),indice_conj,s]
                #se agrega la transicion creada
                afd_M.append(transicion_temp)

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
                            nuevo_edo_final=[j,edo_afn.getToken()]
                            # y se agregara a la lista de estados finales del afd
                            afd_Z.append(nuevo_edo_final)
                    #en caso de no encontrar en el conj_temp[j] se va con el que sigue
                    j=j+1


        #se crea el automata con las propiedadesya creadas
        self.afd=AFN_e(afd_K,afd_Sigma,afd_S,afd_Z,afd_M)

        
