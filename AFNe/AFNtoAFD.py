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
        self.transiciones=self.afn.getTransiciones()

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
            edo_prin=T[0] #Estado Principal
            edo_dest=T[1] #Estado Destino
            sim=T[2] #Simbolo
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
                edo_prin=T[0] #Estado Principal
                edo_dest=T[1] #Estado Destino
                sim=T[2] #Simbolo
                if edo_prin==estado and sim==simbolo:
                    lista_edos.append(edo_dest)
        lista_edos.sort()
        return lista_edos

    def __existeConjunto(self,conjunto):
        bandera = True
        for C in self.conjuntos_list:
            #se dara por hecho que por defecto todos los conjuntos estan ordenado
            #sino aplicar un sort()
            if len(C)==len(conjunto): #son del mismo tamano
                tam=len(C)
                for i in range(tam):
                    if not(C[i]==conjunto[i]): #al detectar elementos direrentes
                        bandera=False #se activa la bandera
        if bandera==True:
            return True
        #se a verificado con todos y se llego a que existen repetidos
        return False


        
    #Regresara un nuevo conjunto o nada si es un estado final
    #Puede regresar un conjunto repetido
    def __irA(self,conjunto,simbolo):

        estados=self.__mover(conjunto,simbolo)
        conj_return=[]
        for e in estados:
            conj_temp=self.__creaConjuntoEpsilon(e)
            conj_return.extend(conj_temp)
        conj_return.sort()   
        
        #en caso de que exista el mismo ocnjunto se retornara un conjunto vacio
        if self.__existeConjunto(conjunto):
            conj_return=[]

        return conj_return

    #esta es la funcion principal, la que se encarga del analisis del automata 
    def __analisisDe(self):     

        #se toma como inicio el estado inicial del automata
        c_temp=self.__creaConjuntoEpsilon(self.afn.getEdoInicial())
        self.conjuntos_list.append(c_temp)
        #contador para los conjuntos creados
        i=0
        while True:
            #inicio del analisis con cada simbolo del alfabeto del automata
            for s in self.Sigma:
                c_temp=self.__irA(self.conjuntos_list[i],s)

                #condiciones en caso de conjuntos vacios no se agregan
                if not(c_temp==[]):
                     self.conjuntos_list.append(c_temp)
            i=i+1
            if i >= len(self.conjuntos_list):
                break
