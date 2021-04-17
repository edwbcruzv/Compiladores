import sys
from Interfaz_Lexico import Ui_Form #>> pyuic5 -x Interfaz_Lexico.ui -o Interfaz_Lexico.py 
from PyQt5 import *
from PyQt5.QtWidgets import *
from AFNe.AFNe import AFN_e,convertAFD


# def automata1():
#     K_list1=['0','1']
#     Sigma_list1=['h']
#     S1='0'
#     Z_list1=[['1',41]]
#     T1=['0','1','h']
#     M_list1=[T1]
#     A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
#     return A1

# def automata2():
#     K_list1=['0','1']
#     Sigma_list1=['i']
#     S1='0'
#     Z_list1=[['1',42]]
#     T1=['0','1','i']
#     M_list1=[T1]
#     A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
#     return A1

# def automata3():
#     K_list1=['0','1']
#     Sigma_list1=['j']
#     S1='0'
#     Z_list1=[['1',43]]
#     T1=['0','1','j']
#     M_list1=[T1]
#     A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
#     return A1

# def automata4():
#     K_list1=['0','1']
#     Sigma_list1=['k']
#     S1='0'
#     Z_list1=[['1',44]]
#     T1=['0','1','k']
#     M_list1=[T1]
#     A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
#     return A1

# def main():
#     print("------------------------------------automata1")
#     A1=automata1()
#     A1.mostrarAutomata()
#     print("------------------------------------automata2")
#     A2=automata2()
#     A2.mostrarAutomata()
#     print("------------------------------------automata3")
#     A3=automata3()
#     A3.mostrarAutomata()
#     print("------------------------------------automata4")
#     A4=automata4()
#     A4.mostrarAutomata()

#     print("--------------concat o union")
#     A1.unirCon(A2)
#     A1.unirCon(A3)
#     A1.unirCon(A4)
#     A1.mostrarAutomata()

#     convertidor=convertAFD(A1)
#     afd=convertidor.getAFD()
#     afd.mostrarAutomata()

if __name__=="__main__":
    app=QtWidgets.QApplication(sys.argv)
    myapp=Ventana()
    myapp.show()
    sys.exit(app.exec_())

    #main()