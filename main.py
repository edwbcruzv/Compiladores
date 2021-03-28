from AFN_e import *


def main():
    

    estados=["0","1","2","3","4","5","6","7","8","9","10"]
    alfabeto=['a','b','c']
    estado_inicial='0'
    estados_aceptacion=[["10",45]]

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

    transiciones=[t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14]

    a=AFN_e(estados,alfabeto,estado_inicial,estados_aceptacion,transiciones)

    a.mostrarAutomata()








if __name__=="__main__":
    main()