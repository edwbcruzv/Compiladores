
# Formado n
def ValidaEstados(num_estados):
    # 0 hasta n
    lista_estados=[]
    for i in range(num_estados+1):
        lista_estados.append(str(i))

    return True
    #formato :[edo,token]-[edo,token]-[edo,token]
def ValidaEstadosAceptacion(str_estados_aceptacion):
    lista_estados_aceptacion=[]
    
    lista_aux1=str_estados_aceptacion.split('[')
    lista_aux2=lista_aux1.split(']')
    lista_aux3=lista_aux2.split('-')
    print(lista_aux3)
    
 #Formato Ejemplo:simbolo,simbolo,simbolo,[simboloinicial-simbolofinal],simbolo
def ValidaLenguaje(str_lenguaje):
    lista_aux1=str_lenguaje.split(',')
    lista_aux2=lista_aux1.split('[')
    lista_aux3=lista_aux2.split(']')
    lista_aux4=lista_aux3.split('-')
    print(lista_aux1)
    print(lista_aux4)
    #Formato Ejemplo: [edo,edo,simbolo]-[edo,edo,simbolo-[edo,edo,simbolo]
def ValidaTransiciones(str_transiciones):
    lista_aux1=str_transiciones.split('[')
    lista_aux2=lista_aux1.split(']')
    lista_aux3=lista_aux2.split('-')
    lista_aux4=lista_aux3.split(',')
    print(lista_aux4)
    

def CrearAutomataAFN():

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
    

    K_list=ValidaEstados(num_estados)
    Z_list=ValidaEstadosAceptacion(str_estados_aceptacion) 
    Sigma_list=ValidaLenguaje(str_lenguaje) 
    M_list=ValidaTransiciones(str_transiciones)
    
    if K_list==[]:
        return "Error en el numero de estados"

    if Z_list==[]:
        return "Error en Los estados de aceptacion "

    if Sigma_list==[]:
        return "Error en el lenguaje"

    if M_list==[]:
        return "Error en las transiciones"

    automata=AFN_e(K_list,Sigma_list,S_str,Z_list,M_list)

