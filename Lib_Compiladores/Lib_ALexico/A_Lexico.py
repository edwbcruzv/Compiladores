from Lib_Compiladores.Lib_ClaseLexica.ClaseLexica import ClaseLexica
from Lib_Compiladores.Lib_AFN_e.AFN_e import AFN_e
import time
import copy
class A_Lexico():

        # Nombre_A_Lexico:"NombreALexico"
        # AFD: en el caso de tener un AFD
    def __init__(self,Nombre_A_Lexico,AFD=None):
        #lista de subconjuntos dela convercion a AFD
        self.Conjunto_Epsilon_List=[]
        # __Nombre_A_Lexico:"nombreALexico"
        self.__Nombre_A_Lexico=Nombre_A_Lexico
        # __Clase_Lexica:ClaseLexica().objet
        self.Union_AFNs=None
        # __AFD: AFN_e().objet      tendra las propiedades de un AFD
        self.__AFD=None

        # en el caso existir el AFD se construye 
        if isinstance(AFD,AFN_e):
            #se declara el analizador lexico terminado
            self.__AFD=AFD
            return
        #de lo contrario solo se crea la instancia y despues se agregan las clases lexicas
    # se uniran los estados iniciales
    def addClaseLexica(self,clase_lexica):
        
        if type(self.Union_AFNs)==type(None):
            self.Union_AFNs = copy.deepcopy(clase_lexica.getAFN())
            #print("esto debe imprimirse una vez")
            return
        
        afn_temp = copy.deepcopy(clase_lexica.getAFN())
        self.Union_AFNs.unionEspecial(clase_lexica.getAFN())

    def getAFD(self):
        return self.__AFD

    def getUnionClasesLexicas(self):
        return self.Union_AFNs

    def getNombreALexico(self):
        return self.__Nombre_A_Lexico 

    def definirALexico(self):
        # a partir de aqui se crea el AFD con el que se trabajara
        
        if type(self.__AFD)==type(None):
            # Al no existir un AFD se debe de crear uno
        
            if type(self.Union_AFNs) == type(None):
                # Al no existir alguna union de clases lexicas no se puede analizar ninguna cadena
                return
            else:
                # Como existe la union entonces se crea el AFD
                
                self.__AFNtoAFD()
                # y se bloquea la union de clases lexicas
        else:
            #ya existe el AFD
            return
##------INICIO DEL ALGORITMO DE ANALISIS DE UNA CADENA USANDO UN AFD----------
    def yylex(self,cadena):
        
        list_cadena=list(cadena)
        Lista_Lexemas=[]
        subcadena_lexema=[]

        tam_cadena=len(list_cadena)
        #inicio del algoritmo 
        #posicion del estado del afn
        Estado_Actual = self.getAFD().getEstadoInicial()
        #nos indicara si pasamos por un estado de aceptacion
        Bandera_Edo_Acept=False 
        cursor_cadena=0 
        
        #mientras que no sea el fin de la cadena
        while not(cursor_cadena==tam_cadena):
            simbolo=list_cadena[cursor_cadena]

            #ver si existe una transicion  del estado actual con el simbolo de la cadena actual
            Estado_Destino,boleano=self.__existeTransicion(Estado_Actual,simbolo)
            #si boolean el False hay un error
            print("δ(", Estado_Actual.getNombre(),
                  ",", simbolo, ")", end="=>")
            if boleano==True:
                #se agrega el simbolo a la lista en caso de ser parte d eun lexema
                subcadena_lexema.append(simbolo)
                print(Estado_Destino.getNombre(),end="  ")
                #si estado actual es un estado de aceptacion
                if Estado_Destino.getToken() > 0:
                    print("Token:", Estado_Destino.getToken())
                    Bandera_Edo_Acept=True
                    if cursor_cadena == tam_cadena-1:
                        lex_temp = self.__nuevoLexema(
                            subcadena_lexema, Estado_Destino.getToken())
                        print(lex_temp)
                        Lista_Lexemas.append(lex_temp)
                else:#no es estado de aceptacion
                    print(" vacio")
                    Bandera_Edo_Acept=False 
                    #seguimos sin pasar por estado de aceptacion

                #pasamos al estado destino de la transicion analizada
                Estado_Actual=Estado_Destino
                #pasamos a siguiente caracter de la casena
                cursor_cadena+=1
                
            #no esiste ninguna transicion entonces hay un error
            elif boleano == False:
                print("Error")
                #checar si anteriormente se paso por un estado de aceptacion
                if Bandera_Edo_Acept:
                    #se carga el lexema actual
                    
                    lex_temp=self.__nuevoLexema(
                        subcadena_lexema, Estado_Actual.getToken())
                    print(lex_temp)
                    Lista_Lexemas.append(lex_temp)
                    subcadena_lexema=[]
                    #posicion del estado del afd
                    Estado_Actual = self.getAFD().getEstadoInicial()
                    print("se ha reiniciado el automata,")
                    Bandera_Edo_Acept = False
                    
                    
                #no se ha pasado por ningun estado de aceptacion se trata de un error y es
                #una cadena lexicamente incorrecta
                else:
                    print("cadena lexicamente incorrecta")
                    return None#duda
                    #posicion del estado del afd
                    #Estado_Actual = self.getAFD().getEstadoInicial()
                    #se descarta el lexema
                    #subcadena_lexema=[]
                
                #al existir un error y al procesarlo nos mantenemos
                #en el caracter actual de la cadena
        Lista_Lexemas.append(["$", -1])           
        return Lista_Lexemas

    def __nuevoLexema(self,Lexema_lista,token):
        return ["".join(Lexema_lista),token]            
            
        #se Busca si existe una transicion en el afd 
    def __existeTransicion(self,Estado_Actual,Simbolo):
        
        for T in self.getAFD().getTransiciones():
            if T.getEstadoPrincipal()== Estado_Actual and T.getSimbolo() == Simbolo:
                return T.getEstadoDestino(),True #si existe
        #no existe
        return None,False

    def __lt__(self,a_lexico):
        return self.getNombreALexico() < a_lexico.getNombreALexico()

    def __le__(self,a_lexico):
        return self.getNombreALexico() <= a_lexico.getNombreALexico()

    def __eq__(self,a_lexico):
        return self.getNombreALexico() == a_lexico.getNombreALexico()

    def tablaAFD(self):
        pass

    def toDataBase(self):
        return "|||||%s%s" % (self.getNombreALexico(), self.getAFD().toDataBase())

    def __str__(self):
        nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones = self.getAFD().__str__()
        return self.getNombreALexico(), nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones


#---------INICIO DEL ALGORITMO Y FUNCIONES DE LA CONVERSION A AFD---------
    def __AFNtoAFD(self):
        # Formato de la lista de conjuntos epsilon 
        # Lista de conjuntos:[[sublista1],[sublista2],[sublista3],....]
        #           sublista:["Estado1","Estado2",...,"Estadon"]
        self.Conjunto_Epsilon_List=[]

        #inicio de la conversion a AFD
        self.__analisisDe()

    #conjunto de estados destino al tener un "E" RECURSIVO
    #los estados se agregan a la variable conjunto recibido
    def __cerraduraEpsilon(self,conjunto):
      
        # ahora se buscan las transiciones donde
        # el estado principal sea la variable estado,
        # el simbolo sea "E"
        # despues se toma el estado destino y se agrega al conjunto
        estado=conjunto[len(conjunto)-1]
        for T in self.Union_AFNs.getTransiciones():
            edo_prin=T.getEstadoPrincipal() #Estado Principal
            edo_dest=T.getEstadoDestino() #Estado Destino
            sim=T.getSimbolo() #Simbolo
            if edo_prin==estado and sim=="¢":
                #se evita que no se repitan estados en el conjunto
                for e in conjunto:
                    if e==edo_dest:
                        #retorna si se repite ϵ
                        return 
                #print(T.__str__())
                conjunto.append(edo_dest)
                self.__cerraduraEpsilon(conjunto)
        return

    # Se crea un Conjunto de cerradura epsilon a partir del estado que se envie
    def __creaConjuntoEpsilon(self,estado):
        conjunto=[]
        #por defecto el mismo estado se incluye en el conjunto
        conjunto.append(estado)
        self.__cerraduraEpsilon(conjunto)
        #se debe de ordenar para una comparacion futura correcta
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
            for T in self.Union_AFNs.getTransiciones():
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
    
    def __sonIguales(self,lista1,lista2):

        if len(lista1) == len(lista2):

            for i in range(len(lista1)):
                if not(lista1[i] == lista2[i]):
                
                    return False
                
            return True
        else:
            return False

    def __existeConjunto(self,conjunto):
        #se dara por hecho que por defecto todos los conjuntos estan ordenado
        #sino aplicar un sort()
        subindice_conjunto=0
        for C in self.Conjunto_Epsilon_List:
            #se da por hecho que los conjuntos son diferentes
            #se compara conjunto por conjunto
            if self.__sonIguales(C,conjunto):
                #son iguales:se regresa el subindice del sunconjunto examinado
                return subindice_conjunto
            else:
                #se aumenta el subindice ya que pasamos al siguiente conjunto de la lista
                subindice_conjunto += 1

        #este caso sera cuando ninguno de los subconjuntos sean iguales
        #se agrega al la lista de conjuntos
        self.Conjunto_Epsilon_List.append(conjunto)
        return subindice_conjunto

    #Regresara un nuevo conjunto o nada si es un estado final
    #Puede regresar un conjunto repetido
    def __irA(self,conjunto,simbolo):

        estados=self.__mover(conjunto,simbolo)
        print(end="C(")
        conj_return=[]

        for e in estados:
            print(e.__str__(), end=' ')
            conj_temp=self.__creaConjuntoEpsilon(e)
            conj_return.extend(conj_temp)
        conj_return.sort()   
        print(")==>{", end='')
        for e in conj_return:
            print(e.__str__(), end=' ')
        print(end="}")
        if conj_return == []:
            return None
        return self.__existeConjunto(conj_return)

    #esta es la funcion principal, la que se encarga del analisis del automata 
    def __analisisDe(self):     

        #se toma como inicio el estado inicial del automata afn
        c_temp = self.__creaConjuntoEpsilon(self.Union_AFNs.getEstadoInicial())
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
        afd_Sigma = self.Union_AFNs.getAlfabeto()

        #contador para los conjuntos creados
        i=0
        #se define el estado inicial del automata
        afd_S=str(i)

        while True:
            #inicio del analisis con cada simbolo del alfabeto del automata
            #tambien se agregan los nuevos estados al afd
            afd_K.append(str(i))
            print("\nTam lista conjuntos:",len(self.Conjunto_Epsilon_List))
            print("Conjunto:S",i,end="{")
            for e in self.Conjunto_Epsilon_List[i]:
                print(e.__str__(), end=' ')
            print(end="}")
            for s in self.Union_AFNs.getAlfabeto():
                #se imprime el cunjunto que est esta revisando
                print("\nirA(S", i, ",", s, ")=>", end='')

                indice_conj=self.__irA(self.Conjunto_Epsilon_List[i],s)

                if indice_conj==None:
                    continue
                print("==>S",indice_conj,end="")
                #ya que termino el proceso de la funcion irA()
                #se empieza con la contruccion del AFD

                #se define la transicion actual creada
                #el subindice del conjunto que se analiza nos define el nombre del estado origen
                #el subindice del conjunto que da como resultado nos define el nombre del estado destino
                #el simbolo con el que se analiza la transicion sera el simbolo de la transicion
                transicion_temp=[str(i),str(indice_conj),s]
                #se agrega la transicion creada
                afd_M.append(transicion_temp)

            i+=1
            #time.sleep(10)
            #para el caso de que ya no existas conjuntos por analizar se rompe el ciclo para terminar
            if i >= len(self.Conjunto_Epsilon_List):
                break
        #al terminar el analisis se definen los nuevos estados de aceptacion
        #de la lista de conjuntos, solo puede existir un estado de aceptacion
        #por lo cual debemos tabmn obtener su Token
        
        
        #Se identificaran como estados de aceptacion aquellos que tu token sean > 0

        for edo_afn in self.Union_AFNs.getEstados():  # estados del afn
            if edo_afn.getToken() > 0:
            #al encontrar un estado de aceptacion del afn, ahora se buscaran en el conjunto
                j=0 #subindice del conjunto
                for conj_temp in self.Conjunto_Epsilon_List:
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
    

        # print("\n\nConjunto de Estados(Objeto):")
        # print(afd_K)

        # print("Alfabeto que acepta el automata")
        # print(afd_Sigma)

        # print("Estado de inicio del automata")
        # print(afd_S)

        # print("Conjunto de Estados(Objeto) de aceptacion")
        # print(afd_Z)

        # print("Conjunto de Transiciones(Objeto)")
        # print(afd_M)
                    
        self.__AFD=AFN_e("AFD_"+self.getNombreALexico(),afd_K,afd_Sigma,afd_S,afd_Z,afd_M)
        return 
