from Lib_Compiladores.Lib_ClaseLexica import ClaseLexica


class A_Lexico():

        # Nombre_A_Lexico:"NombreALexico"
        # Clase_Lexica: [ClaseLexica1(),ClaseLexica2(),.....]
    def __init__(self,Nombre_A_Lexico,Clase_Lexica=None):
        # __Nombre_A_Lexico:"nombreALexico"
        self.__Nombre_A_Lexico=Nombre_A_Lexico
        # __Clase_Lexica:ClaseLexica().objet
        self.__Lista_Clases_Lexicas=[]
        # __AFD: AFN_e().objet      tendra las propiedades de un AFD
        self.__AFD=object()

        #solo se define un nombre para terminos de busqueda o definir
        if Clase_Lexica==None:
            return
        # se verifica que sea una instancia de ClaseLExica
        if not(isinstance(Clase_Lexica,ClaseLexica)):
            return
            
        self.__Clase_Lexica=Clase_Lexica
        #se llama a la funcion que se encarga de convertir el AFN a AFD

        #self.__AFNtoAFD()
    
    def getNombreALexico(self):
        return self.__Nombre_A_Lexico

    ##solo se uniran los estados iniciales
    def unionClasesLexicas(self,clase_lexica):
        pass   

##------INICIO DEL ALGORITMO DE ANALISIS DE UNA CADENA USANDO UN AFD----------
    def analizarCadena(self,cadena):
        list_cadena=list(cadena)

        Lista_Lexemas=[]
        Lexema_temp=[]

        tam_cadena=len(list_cadena)
        #inicio del algoritmo
        #posicion del estado del afn
        Estado_Actual=self.afd.getEdoInicial()
        #nos indicara si pasamos por un estado de aceptacion
        Bandera_Edo_Acept=False 
        cursor_cadena=0 
        
        #mientras que no sea el fin de la cadena
        while cursor_cadena==tam_cadena:
            simbolo=list_cadena[cursor_cadena]

            #ver si existe una transicion  del estado actual con el simbolo de la cadena actual
            Estado_Destino,boleano=self.__existeTransicion(Estado_Actual,simbolo)
            #si boolean el False hay un error
            if boleano:
                Lexema_temp.append(simbolo)
                #si estado actual es un estado de aceptacion
                if esestadoAceptacion(Estado_Actual):
                    #print(Estado_Actual.getToken())
                    Bandera_Edo_Acept=True
                else:#no es estado de aceptacion
                    Bandera_Edo_Acept=False 
                #seguimos sin pasar por estado de aceptacion
                Estado_Actual=Estado_Destino
                cursor_cadena=cursor_cadena+1
                

            #no esiste ninguna transicion entonces hay un error
            else:
                #checar si se paso por un estado de aceptacion
                if Bandera_Edo_Acept:
                    #se descarga el lexema actual
                    Lista_Lexemas.append(self.__nuevoLexema(Lexema_temp,Estado_Actual.token()))
                    Lexema_temp=[]
                    #posicion del estado del afd
                    Estado_Actual=self.afd.getEdoInicial()
                    
                #no se ha pasado por ningun estado de aceptacion
                else:
                    #posicion del estado del afd
                    Estado_Actual=self.afd.getEdoInicial()
                    #se descarta el lexema
                    Lexema_temp=[]
                    
        return Lista_Lexemas

    def __nuevoLexema(self,Lexema_lista,token):
        return ["".join(Lexema_lista),token]            
            
        #se Busca si existe una transicion en el afd 
    def __existeTransicion(self,Estado_Actual,Simbolo):
        
        for T in self.afdTransiciones:
            if T[0]==Estado_Actual and T[2]==Simbolo:
                return T[1],True #si existe
        #no existe
        return [],False

    def __lt__(self,a_lexico):
        return self.Nombre_A_Lexico<a_lexico.Nombre_A_Lexico

    def __le__(self,a_lexico):
        return self.Nombre_A_Lexico<=a_lexico.Nombre_A_Lexico

    def __eq__(self,a_lexico):
        return self.Nombre_A_Lexico==a_lexico.Nombre_A_Lexico

    def tablaAFD(self):
        pass



#---------INICIO DEL ALGORITMO Y FUNCIONES DE LA CONVERSION A AFD---------
    def __AFNtoAFD(self):
        # Formato de la lista de conjuntos epsilon 
        # Lista de conjuntos:[[sublista1],[sublista2],[sublista3],....]
        #           sublista:["Estado1","Estado2",...,"Estadon"]
        self.Conjunto_Epsilon_List=[]

        #inicio de la conversion a AFD
        self.AFD=self.__analisisDe()

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
        for C in self.Conjunto_Epsilon_List:
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
        self.Conjunto_Epsilon_List.append(conjunto)
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
        self.Conjunto_Epsilon_List.append(c_temp)

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
                for e in self.Conjunto_Epsilon_List[i]:
                    print(e.__str__())
                indice_conj=self.__irA(self.Conjunto_Epsilon_List[i],s)

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
            if i >= len(self.Conjunto_Epsilon_List):
                break
        #al terminar el analisis se definen los nuevos estados de aceptacion
        #de la lista de conjuntos, solo puede existir un estado de aceptacion
        #por lo cual debemos tabmn obtener su Token
        
        
        #Se identificaran como estados de aceptacion aquellos que tu token sean > 0

        for edo_afn in self.afn.K: #estados del afd
            if edo_afn.getToken() > 0:
            #al encontrar un estado de aceptacion del afn, ahora se buscaran en el conjunto
                j=0 #subindice del conjunto
                for conj_temp in self.Conjunto_Epsilon_List:
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
        return AFN_e("AFD",afd_K,afd_Sigma,afd_S,afd_Z,afd_M)
