from AFNe.AFNe import AFN_e,convertAFD
import copy

# Formado n
def ValidaEstados(num_estados):#terminado
    # 0 hasta n
    lista_estados=[]
    for i in range(num_estados+1):
        
        lista_estados.append(str(i))
    #print(lista_estados)

    return lista_estados

    #formato :["edo",token]-["edo",token]-["edo",token]
def ValidaEstadosAceptacion(str_estados_aceptacion):#terminardo
    lista_estados_aceptacion=[]
    
    str_aux1="".join(str_estados_aceptacion.split('['))
    #print(str_aux1)
    str_aux2="".join(str_aux1.split(']'))
    #print(str_aux2)
    lista_estados_aceptacion=str_aux2.split('-')
    lista_retorno=[]
    for l in lista_estados_aceptacion:
        lista_retorno.append(l.split(','))

    for l in lista_retorno:
        l[1]=int(l[1])
    #print(lista_retorno)
    return lista_retorno
    
 #Formato Ejemplo:simbolo,simbolo,simbolo,[simboloinicial-simbolofinal],simbolo
def ValidaLenguaje(str_lenguaje): #terminado
    str_aux1=str_lenguaje.split(',')
    # str_aux2="".join(str_aux1.split('['))
    # str_aux3="".join(str_aux2.split(']'))
    # str_aux4="".join(str_aux3.split('-'))
    #print(str_aux1)

    return str_aux1

    #Formato Ejemplo: [edo,edo,simbolo]-[edo,edo,simbolo-[edo,edo,simbolo]
def ValidaTransiciones(str_transiciones):#terminados
    str_aux1="".join(str_transiciones.split('-'))
    str_aux2="".join(str_aux1.split('['))
    str_aux3=str_aux2.split(']')
    
    lista_retorno=[]
    for l in str_aux3:
        lista_retorno.append(l.split(','))

    for l in lista_retorno:
        if l == [] or l == [""]:
            lista_retorno.remove(l)
    #print(lista_retorno)
    return lista_retorno
    

def CrearAutomataAFN(nombre_AFN,num_estados,str_estados_aceptacion,str_lenguaje,str_transiciones):

    #Conjunto de Estados(Objeto) no vacios
    K_list=[]  #K_list:Formato=["estado1","estado2","estado3",.....]

    #Alfabeto que acepta el automata
    Sigma_list=[] #Sigma_list:Formato=['a','b','c',.....]

    #Estado de inicio del automata
    S_str="0" #S:Formato= "nombre estado" pero despues sera un objeto estado

    #Conjunto de Estados(Objeto) de aceptacion
    Z_list=[] #Z_list:Formato= ["estado1","estado2","estado3",.....]

    #Conjunto de Transiciones(Objeto)
    M_list=[] #M_list:Formato= [[sublista1],[sublista2],[sublista3],....]
        #        sublista: Formato=["estado1","estado2","Simbolos"]

    #si las funciones regresan una lista vacia se significa que hay un error en esa parte 
    
    #print("num estados:")
    K_list=ValidaEstados(num_estados)
    #print("edos aceptacion:")
    Z_list=ValidaEstadosAceptacion(str_estados_aceptacion) 
    #print("lenguaje:")
    Sigma_list=ValidaLenguaje(str_lenguaje) 
    #print("edos transicion:")
    M_list=ValidaTransiciones(str_transiciones)
    
    
    if K_list==[]:
        return "Error en el numero de estados"

    if Z_list==[]:
        return "Error en Los estados de aceptacion "

    if Sigma_list==[]:
        return "Error en el lenguaje"

    if M_list==[]:
        return "Error en las transiciones"

    automata=AFN_e(nombre_AFN,K_list,Sigma_list,S_str,Z_list,M_list)

    return automata    

def ConvierteAClaseLexica(nombre_clase_lexica,afn,token):
    #se creara una compia y ase trabajara sobre ella
    afn_copia=copy.copy(afn)
    #garantizamos tener solo un estado de aceptacion
    afn_copia.agregarEdoFinal()
    #ahota todos los tokens de los estados seran 0
    for T in afn_copia.getTransiciones():
        T[2]=0

    #el estado final le agregamos el token

    edo_final_temp=afn_copia.getEstadosAceptacion()[0]
    edo_final_temp.setToken(token)

    return afn_copia




