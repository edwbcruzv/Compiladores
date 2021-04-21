import sys
from Interfaz_Lexico import Ui_Form #>> pyuic5 -x Interfaz_Lexico.ui -o Interfaz_Lexico.py 
from PyQt5 import *
from PyQt5.QtWidgets import *
from AFNe.AFNe import AFN_e
from Crear import *
from A_Lexico import *



class Ventana(QtWidgets.QWidget):
    

    def __init__(self,parent=None):
        self.Lista_De_Automatas=[]
        self.Lista_De_Clases_Lexicas=[]
        self.Lista_De_A_Lexicos=[]

        super(Ventana,self).__init__(parent)
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        self.ui.pushButton_Crear.clicked.connect(self.CrearAutomataAFN)

        self.ui.pushButton_Unir.clicked.connect(self.unir)
        self.ui.pushButton_Concat.clicked.connect(self.concatenar)
        self.ui.pushButton_CerraduraPositiva.clicked.connect(self.cerradura_Positiva)
        self.ui.pushButton_CerraduraKleene.clicked.connect(self.cerradura_Kleene)
        self.ui.pushButton_Opcional.clicked.connect(self.opcional)

        self.ui.pushButton_CrearClaseLexica.clicked.connect(self.CrearClaseLexica)
        self.ui.pushButton_CrearAnalizador.clicked.connect(self.crearAnalizadorLexico)

        self.ui.pushButton_Mostrar.clicked.connect(self.mostrar)


    def CrearAutomataAFN(self):
        print("creando afn")
        nombreAFN=self.ui.lineEdit_NombreAFN.text()
        # num_estados=self.ui.spinBox_num_Estados.value()
        # str_lenguaje=self.ui.textEdit_Lenguale.toPlainText()
        # str_estados_aceptacion=self.ui.textEdit_EstadosAceptacion.toPlainText()
        # str_transiciones=self.ui.textEdit_Transiciones.toPlainText()

        num_estados=1
        str_lenguaje="d"
        str_estados_aceptacion="[1,10]"
        str_transiciones="[0,1,d]"
        afn=CrearAutomataAFN(nombreAFN,num_estados,str_estados_aceptacion,str_lenguaje,str_transiciones)
        #al crear el automata se agrega a una lista de automatas
        self.__agregarAutomataLista(afn)
        ##afn.mostrarAutomata()
        
        self.ui.label_StatusCrear.setText("Automata Creado")

    def CrearClaseLexica(self):
        nombre_clase_lexica=self.ui.lineEdit_ClaseLexicoNom.text()
        token=self.ui.spinBox_Token.value()
        nombre_afn=self.ui.comboBox_ALexicoAFN.currentText()

        temp_A=AFN_e(nombre_afn)
        afn=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A)]

        clase_lexica=ConvierteAClaseLexica(nombre_clase_lexica,afn,token)
        self.__agregarClaseLexicaLista(clase_lexica)
        self.ui.label_StatusCrearClaseLex.setText("hecho")

    def crearAnalizadorLexico(self):
        
        nombre_a_lexico=self.ui.lineEdit_AnalizadorNom.text()
        nombre_A=self.ui.comboBox_ClasesLexicas.currentText()

        temp_A=AFN_e(nombre_A)
        AFN=self.Lista_De_Clases_Lexicas[self.Lista_De_Clases_Lexicas.index(temp_A)]
        
        A_Lex=A_Lexico(nombre_a_lexico,AFN)
        self.__agregarALexicoLista(A_Lex)
        self.ui.label_StatusALexico.setText("hecho")

    

##*****************************************Pestania de operaciones******
    def unir(self):
        nombre_union=self.ui.lineEdit_UnionNom.text()
        nombre_A1=self.ui.comboBox_A1Unir.currentText()
        nombre_A2=self.ui.comboBox_A2Unir.currentText()

        temp_A1=AFN_e(nombre_A1)
        temp_A2=AFN_e(nombre_A2)
        
        A1=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A1)]
        A2=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A2)]
        
        A1.unirCon(A2)
        if not(nombre_union ==""):
            A1.Nombre_Automata=nombre_union
        self.__eliminarAutomataLista(A2)
        A1.mostrarAutomata()

    def concatenar(self):
        nombre_concat=self.ui.lineEdit_ConcatNom.text()
        nombre_A1=self.ui.comboBox_A1Concat.currentText()
        nombre_A2=self.ui.comboBox_A2Concat.currentText()
        temp_A1=AFN_e(nombre_A1)
        temp_A2=AFN_e(nombre_A2)
        
        A1=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A1)]
        A2=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A2)]

        A1.concatCon(A2)
        if not(nombre_concat ==""):
            A1.Nombre_Automata=nombre_concat
        self.__eliminarAutomataLista(A2)
        A1.mostrarAutomata()

    def cerradura_Kleene(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()
        temp_A=AFN_e(nombre_A)
        A=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A)]
        A.cerraduraKleene()
        A.mostrarAutomata()

    def cerradura_Positiva(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()
        temp_A=AFN_e(nombre_A)
        A=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A)]
        A.cerraduraPositiva()
        A.mostrarAutomata()

    def opcional(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()
        temp_A=AFN_e(nombre_A)
        A=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A)]
        A.opcion()
        A.mostrarAutomata()
##*************************************Fin de Pestania de operaciones******

##*****************************************Lista de Clases Lexicas******
    def __agregarClaseLexicaLista(self,clase_lexico):
        #al agregar el analizador a la lista 
        self.Lista_De_Clases_Lexicas.append(clase_lexico)
        #se procede a ordanar para no tener problemas
        self.ui.comboBox_ClasesLexicas.addItem(clase_lexico)
        # de los combobox
        self.Lista_De_Clases_Lexicas.sort()

    def __eliminarClaseLexicaLista(self,clase_lexico):
        #se elimina el analizador de la lista
        self.Lista_De_A_Lexicos.remove(clase_lexico)
        #se procede a eliminar y ordanar para no tener problemas
        self.ui.comboBox_ClasesLexicas.removeItem(clase_lexico)
        # de los combobox
        self.Lista_De_Clases_Lexicas.sort()
##*****************************************Lista de Clases Lexicas******

##*****************************************Lista de Analizadores Lexicos******
    def __agregarALexicoLista(self,a_lexico):
        #al agregar el analizador a la lista 
        self.Lista_De_A_Lexicos.append(a_lexico)
        #se agrega a el combobox
        self.ui.comboBox_Analizadores.addItem(a_lexico)
        # se ordena la lista
        self.Lista_De_A_Lexicos.sort()

    def __eliminarALexicoLista(self,a_lexico):
        #se elimina el analizador de la lista
        self.Lista_De_A_Lexicos.remove(a_lexico)
        #se agrega a el combobox
        self.ui.comboBox_Analizadores.removeItem(a_lexico)
        # se ordena la lista
        self.Lista_De_A_Lexicos.sort()
##*****************************************Lista de Analizadores Lexicos******


##*****************************************Combobox de AFN******
    def __agregarAComboBox_Automatas(self,automata):
        self.ui.comboBox_A1Unir.addItem(automata.Nombre_Automata)
        self.ui.comboBox_A2Unir.addItem(automata.Nombre_Automata)
        self.ui.comboBox_A1Concat.addItem(automata.Nombre_Automata)
        self.ui.comboBox_A2Concat.addItem(automata.Nombre_Automata)
        self.ui.comboBox_ACerradura.addItem(automata.Nombre_Automata)

        self.ui.comboBox_ALexicoAFN.addItem(automata.Nombre_Automata)

        self.ui.comboBox_AFNMostrar.addItem(automata.Nombre_Automata)

    def __eliminarAComboBox_Automatas(self,automata):

        self.ui.comboBox_A1Unir.removeItem(self.ui.comboBox_A1Unir.findText(automata.Nombre_Automata))
        self.ui.comboBox_A2Unir.removeItem(self.ui.comboBox_A2Unir.findText(automata.Nombre_Automata))
        self.ui.comboBox_A1Concat.removeItem(self.ui.comboBox_A1Concat.findText(automata.Nombre_Automata))
        self.ui.comboBox_A2Concat.removeItem(self.ui.comboBox_A2Concat.findText(automata.Nombre_Automata))
        self.ui.comboBox_ACerradura.removeItem(self.ui.comboBox_ACerradura.findText(automata.Nombre_Automata))
        
        self.ui.comboBox_ALexicoAFN.removeItem(self.ui.comboBox_ACerradura.findText(automata.Nombre_Automata))

        self.ui.comboBox_AFNMostrar.removeItem(self.ui.comboBox_ACerradura.findText(automata.Nombre_Automata))
##*****************************************Fin de Combobox de AFN******

##*****************************************Lista de AFNs*********
    def __agregarAutomataLista(self,automata):
        #se agrega  ala lista de automatas
        self.Lista_De_Automatas.append(automata)
        #se agrega a todas los combobox relacionados
        self.__agregarAComboBox_Automatas(automata)
        # se orden a lista
        self.Lista_De_Automatas.sort()

    def __eliminarAutomataLista(self,automata):
        #se elimina el automata de la lista
        self.Lista_De_Automatas.remove(automata)
        #se eliminan de los combobox relacionados
        self.__eliminarAComboBox_Automatas(automata)
        # se ordena la lista
        self.Lista_De_Automatas.sort()
##*****************************************Lista de AFNs*********

##*************************************

    def mostrar(self):

        
        if self.ui.radioButton_AFNs.isChecked():
            nombre_afn=self.ui.comboBox_AFNMostrar.currentText()
            temp_A=AFN_e(nombre_afn)
            automata=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A)]

            self.__mostrarAutomata(automata)
        
        elif self.ui.radioButton_ClaseLexica.isChecked():
            
            nombre_A=self.ui.comboBox_ClaseLexicaMostrar.currentText()
            temp_A=AFN_e(nombre_A)
            a_lexico=self.Lista_De_Clases_Lexicas[self.Lista_De_Clases_Lexicas.index(temp_A)]

            self.__mostrarALexico(a_lexico)

        # elif self.ui.radioButton_Analizador.isChecked():
        #     self.ui.comboBox_AnalizadorMostrar.currentText()
        #     self.__mostrarClaseLexica(clase_lexica)


    def __mostrarAutomata(self,automata):
        encabezado=("nombre","Lenguaje","Estado Inicial","Estados","Estados De Aceptacion","Transiciones")

        # self.ui.tableView_Mostrar.hideColumn(6)
        # self.ui.tableView_Mostrar.hideRow(0)
        
        # nombre=QtWidgets.QTableWidgetItem()
        # Lenguaje=QtWidgets.QTableWidgetItem()
        # Estado_Inicial=QtWidgets.QTableWidgetItem()
        # Estados=QtWidgets.QTableWidgetItem()
        # Estados_De_Aceptacion=QtWidgets.QTableWidgetItem()
        # Transiciones=QtWidgets.QTableWidgetItem()

        # self.ui.tableView_Mostrar.setHorizontalHeaderItem(0,nombre)
        # self.ui.tableView_Mostrar.setHorizontalHeaderItem(1,Lenguaje)
        # self.ui.tableView_Mostrar.setHorizontalHeaderItem(2,Estado_Inicial)
        # self.ui.tableView_Mostrar.setHorizontalHeaderItem(3,Estados)
        # self.ui.tableView_Mostrar.setHorizontalHeaderItem(4,Estados_De_Aceptacion)
        # self.ui.tableView_Mostrar.setHorizontalHeaderItem(5,Transiciones)

        automata.Nombre_Automata
        print(automata.Sigma)
        print(automata.S.__str__())
        for e in automata.K:
           print(e.__str__())
        for e in automata.Z:
            print(e.__str__())
        for e in automata.M:
            print(e.__str__())

    def __mostrarClaseLexica(self,clase_lexica):
        pass

    def __mostrarALexico(self,a_lexico):
        pass

##*****INICIO DE TODO EL PROGRAMA
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp=Ventana()
    myapp.show()
    sys.exit(app.exec_())
