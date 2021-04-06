from AFN_e import *


def main():
    
    #los estados unicamente seran numeros enteros
    #se tendra formato 's0','s1','s2','S3',......
    #pero este rubro se llena solo al construir el automata
    
    #estados=["0","1","2","3","4","5","6","7"]
    #alfabeto=['a','b','c']
    #el estado inicial solo sera un numero entero
    #estado_inicial='0'
    #los estados de aceptacion tambn seran 's10','s11','s12','S13',......
    #y los toquen seran entero sin formato de cadena 10,25,416,78,14,.........
    #estados_aceptacion=[["7",47],["10",45]]
    #Las transiciones se agregarar como sub listas
    #t1=["0","1","E"]
    # t10=["0","7","E"]
    # t2=["1","2","E"]
    # t3=["1","4","E"]
    # t4=["2","3","a"]
    # t5=["4","5","b"]
    # t6=["3","6","E"]
    # t7=["5","6","E"]
    # t8=["6","1","E"]
    # t9=["6","7","E"]
    # transiciones=[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10]

    estados=['0','1']
    alfabeto=['a']
    estado_inicial='0'
    estados_aceptacion=[["1",47]]
    t1=["0","1","a"]
    transiciones=[t1]
    a=AFN_e(estados,alfabeto,estado_inicial,estados_aceptacion,transiciones)
    a.cerraduraKleene()
    #a.cerraduraPositiva()
    #a.opcion()
    #a.ordenaEdos()
    a.mostrarAutomata()








if __name__=="__main__":
    main()