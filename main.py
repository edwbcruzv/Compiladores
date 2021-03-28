from AFN_e import *


def main():
    
    #los estados unicamente seran numeros enteros
    #se tendra formato 's0','s1','s2','S3',......
    #pero este rubro se llena solo al construir el automata
    
    estados=["0","1","2","3","4","5","6","7","8","9","10"]
    alfabeto=['a','b','c']
    #el estado inicial solo sera un numero entero
    estado_inicial='0'
    #los estados de aceptacion tambn seran 's10','s11','s12','S13',......
    #y los toquen seran entero sin formato de cadena 10,25,416,78,14,.........
    estados_aceptacion=[["7",47],["10",45]]
    #Las transiciones se agregarar como sub listas
    t1=['0','1','£']
    t2=["1","2","£"]
    t3=["1","3","£"]
    t4=["2","3","a"]
    t5=["4","5","b"]
    t6=["3","6","£"]
    t7=["5","6","£"]
    t8=["6","1","£"]
    t9=["6","7","£"]
    t10=["7","8","£"]
    t11=["7","10","£"]
    t12=["8","9","c"]
    t13=["9","8","£"]
    t14=["9","10","£"]
    t15=["10","11","£"]

    transiciones=[t1,t2,t3,t13,t5,t6,t7,t8,t9,t10,t11,t4,t12,t14,t15]

    a=AFN_e(estados,alfabeto,estado_inicial,estados_aceptacion,transiciones)

    a.mostrarAutomata()








if __name__=="__main__":
    main()