from AFNe.AFNe import AFN_e

def automata1():
    K_list1=['0','1']
    Sigma_list1=['h']
    S1='0'
    Z_list1=[['1',41]]
    T1=['0','1','h']
    M_list1=[T1]
    A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
    return A1

def automata2():
    K_list1=['0','1']
    Sigma_list1=['i']
    S1='0'
    Z_list1=[['1',42]]
    T1=['0','1','i']
    M_list1=[T1]
    A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
    return A1

def automata3():
    K_list1=['0','1']
    Sigma_list1=['j']
    S1='0'
    Z_list1=[['1',43]]
    T1=['0','1','j']
    M_list1=[T1]
    A1=AFN_e(K_list1,Sigma_list1,S1,Z_list1,M_list1)
    return A1

def main():
    print("------------------------------------automata1")
    A1=automata1()
    A1.mostrarAutomata()
    print("------------------------------------automata2")
    A2=automata2()
    A2.mostrarAutomata()
    print("------------------------------------automata3")
    A3=automata3()
    A3.mostrarAutomata()

    print("------------------------------------concat")
    A1.unirCon(A2)
    A1.unirCon(A3)
    A1.mostrarAutomata()





if __name__=="__main__":
    main()