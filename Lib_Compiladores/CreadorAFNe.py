from Lib_Compiladores.Lib_AFN_e.AFN_e import AFN_e

#Esta clase se encargara de validar los datos santes de crear un automata
class CreadorAFNe:
    #solo se crea el objeto
    def __init__(self):
        pass

    #los parametros recibidos son puras cadenas con un formato especifico
    def CrearAutomataAFN(self,nombre_AFN,num_estados,str_lenguaje,str_estado_inicial,str_estados_aceptacion,str_transiciones):
        
        #se valida el nombre
        if not(str==type(nombre_AFN) and len(nombre_AFN)>4):
            return None,"Error en el nombre o nombre muy corto"
        #num_estados puede ser un str o int
        if not(int==type(num_estados)) :
            #al no ser int se verifica si es str
            if str==type(num_estados):
                #al ser str se hace el prse a int
                num_estados=int(num_estados)
            else: #es un tipo desconocido no valido
                return None,"Error en el parametro del numero de estados"
        #se verifica que el resto sean str
        if not(str==type(str_lenguaje)):
            return None,"Error en el parametro de lenguaje"
        if not(str==type(str_estados_aceptacion)):
            return None,"Error en el parametro de estados de aceptacion"
        if not(str==type(str_transiciones)):
            return None,"Error en el parametro de transiciones"
        # FORMATO QUE SE LE PIDE AL USUARIO Y QUE SE DEBE DE VALIDAR

        # nombre_AFN: "nombreAFN"
        # num_estados: num  (es un int)
        # str_lenguaje: "simbolo1,simbolo2,simbolo3"
        # str_estado_inicial: "edo"
        # str_estados_aceptacion: "edo1-edo2-edo3" o "[edo1,token]-[edo2,token]-[edo3,token]"
        # str_transiciones:"[edo,edo,simbolo]-[edo,edo,simbolo]-[edo,edo,simbolo]"


        #FORMATO QUE DEBE SE CUMPLIR PARA QUE SE CREE EL OBJETO AFN_e
        # Nombre_AFN:"nombre del automata"

        # K_list:["estado1","estado2","estado3",.....]
        K_list=[]

        # Sigma_list:["a","b","c",.....]
        Sigma_list=[]
        
        # S:"nombre estado"
        S_str=str_estado_inicial   # "edo"

        # Z_list: ["estado1","estado2","estado3",.....]  #cuando es un AFN
        # Z_list: [[sublista1],[sublista2],[sublista3],....] #cuando es un AFD
        #        sublista:["estado",Token]    token es un int
        Z_list=[]   #Lista sobrecargada

        # M_list: [[sublista1],[sublista2],[sublista3],....]
        #        sublista:["estado1","estado2","Simbolos"]
        M_list=[]

        

        #si las funciones regresan una lista vacia se significa que hay un error en esa parte   
        K_list = self.__ValidaEstados(num_estados)
        if K_list==None:
            return None,"Error en el numero de estados"
    
        Sigma_list = self.__ValidaLenguaje(str_lenguaje)
        if Sigma_list==None:
            return None,"Error al definir el lenguaje"

        Z_list = self.__ValidaEstadosAceptacion(str_estados_aceptacion)
        if Z_list == None:
            return None, "Error en Los estados de aceptacion "

        M_list = self.__ValidaTransiciones(str_transiciones)
        if M_list==None:
            return None,"Error en las transiciones"
        
        # print("Nombre:",nombre_AFN)
        # print("Estados:",K_list)
        # print("Lenguaje",Sigma_list)
        # print("Estado inicial:",S_str)
        # print("Estados Aceptacion:",Z_list)
        # print("Transiciones:",M_list)

        automata=AFN_e(nombre_AFN,K_list,Sigma_list,S_str,Z_list,M_list)
        
        return automata,"Automata creado con exito" 

    # num_estados: num  (es un int)
    def __ValidaEstados(self,num_estados):#terminado
        # 0 hasta n
        lista_estados=[]
        for i in range(num_estados+1):
            
            lista_estados.append(str(i))
        #print(lista_estados)
        return lista_estados # :["estado1","estado2","estado3",.....]

    # str_lenguaje: "simbolo1,simbolo2,simbolo3"
    def __ValidaLenguaje(self,str_lenguaje): #terminado
        list_aux1=str_lenguaje.split(',')
        lista_retorno=[]
        for s in list_aux1:
            if len(s)==1:
                lista_retorno.append(s)
            elif "[" in s and "-" in s and "]" in s :
                #print("procesando rango")
                str_aux=s[1:len(s)]
                str_aux=str_aux[0:len(str_aux)-1]
                #print(str_aux)

                for n in range(ord(str_aux[0]),ord(str_aux[2])+1):
                    lista_retorno.append(chr(n))
                
            else:
                return None
        #print(list_aux1)
        return lista_retorno #:["a","b","c",.....]

    # str_estados_aceptacion: "edo1-edo2-edo3" o "[edo1,token]-[edo2,token]-[edo3,token]"
    def __ValidaEstadosAceptacion(self,str_estados_aceptacion):#terminardo

        list_aux1=str_estados_aceptacion.split('-')

        lista_retorno=[]
        for elem in list_aux1:

            if "[" in elem and "," in elem and "]" in elem :
                #cuando exista un token
                str_aux1="".join(elem.split('['))
                str_aux2="".join(str_aux1.split(']'))
                sublista=str_aux2.split(',')
                lista_retorno.append(sublista)
            #sin token
            lista_retorno.append(elem)

        #print(lista_retorno)
        # : ["estado1","estado2","estado3",.....]  #cuando es un AFN
        # : [sublista1,sublista2,sublista3,....] #cuando es un AFD
        #        sublista:["estado",Token]    token es un int
        return lista_retorno
        
    # str_transiciones:"[edo,edo,simbolo]-[edo,edo,simbolo]-[edo,edo,simbolo]"
    def __ValidaTransiciones(self,str_transiciones):#terminados

        list_aux1=str_transiciones.split("]-[")
        tam_list=len(list_aux1)
        tam=len(list_aux1[0])
        list_aux1[0]=list_aux1[0][1:tam]
        tam=len(list_aux1[tam_list-1])
        list_aux1[tam_list-1]=list_aux1[tam_list-1][0:tam-1]
        
        #print(list_aux1)
        
        lista_retorno=[]
        for l in list_aux1:
            sub_list=l.split(',')

            if "[" in sub_list[2] and "-" in sub_list[2] and "]" in sub_list[2] :
                #print("procesando rango")
                s=sub_list[2]
                str_aux=s[1:len(s)]
                str_aux=str_aux[0:len(str_aux)-1]
                #print(str_aux)
                for n in range(ord(str_aux[0]),ord(str_aux[2])+1):
                    lista_retorno.append([sub_list[0],sub_list[1],chr(n)])
            else:
                lista_retorno.append(sub_list)


        for l in lista_retorno:
            if l == [] or l == [""]:
                lista_retorno.remove(l)
        return lista_retorno
        

       
