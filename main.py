import sys
import os
from PyQt5 import *
from PyQt5.QtWidgets import *
from InterfazGrafica.Interfaz_Lexico import Ui_Form #>> pyuic5 -x Interfaz_Lexico.ui -o Interfaz_Lexico.py 
from PyQt5 import QtCore, QtGui, QtWidgets
from Lib_Compiladores.Lib_AFN_e.AFN_e import AFN_e
from Lib_Compiladores.Lib_ClaseLexica.ClaseLexica import ClaseLexica
from Lib_Compiladores.Lib_ALexico.A_Lexico import A_Lexico
from BaseDatos import BaseDatos
import copy

class Ventana(QtWidgets.QWidget):
    

    def __init__(self,parent=None):
        self.db=BaseDatos()

        super(Ventana,self).__init__(parent)
        self.ui=Ui_Form()
        self.ui.setupUi(self)
        

        self.ui.pushButton_Unir.clicked.connect(self.unir)
        self.ui.pushButton_Concat.clicked.connect(self.concatenar)
        self.ui.pushButton_CerraduraPositiva.clicked.connect(self.cerradura_Positiva)
        self.ui.pushButton_CerraduraKleene.clicked.connect(self.cerradura_Kleene)
        self.ui.pushButton_Opcional.clicked.connect(self.opcional)

        self.ui.pushButton_Crear.clicked.connect(self.crearAutomataAFN)
        self.ui.pushButton_CrearClaseLexica.clicked.connect(self.crearClaseLexica)
        self.ui.pushButton_CrearAnalizador.clicked.connect(self.crearAnalizadorLexico)

        self.ui.pushButton_Mostrar.clicked.connect(self.mostrar)


    def crearAutomataAFN(self):
        print("Creando afn")
        nombreAFN=self.ui.lineEdit_NombreAFN.text()
        num_estados=str(self.ui.spinBox_num_Estados.value())
        str_lenguaje=self.ui.textEdit_Lenguale.toPlainText()
        str_estados_aceptacion=self.ui.textEdit_EstadosAceptacion.toPlainText()
        str_transiciones=self.ui.textEdit_Transiciones.toPlainText()

        print(nombreAFN)
        print(num_estados)
        print(str_lenguaje)
        print("0")
        print(str_estados_aceptacion)
        print(str_transiciones)

        #se valida el automata
        afn,respuesta=self.db.CrearAutomataAFN(nombreAFN,num_estados,str_lenguaje,"0",str_estados_aceptacion,str_transiciones)

        #Se manda un status a la interfaz grafica
        self.ui.label_StatusCrear.setText(respuesta)
        #su hubo un error se termina el proceso
        if not(isinstance(afn,AFN_e)):
            return        
        
        #se muestra el automata en consola
        afn.mostrarAutomata()

        print("DataBase:",afn.toDataBase())
        #se agrega a los combobox
        self.__agregarAComboBox_Automatas(afn.getNombreAFN())
        #Se almacena el automata creado en la base de datos
        self.db.agregarAFN(afn)

    def crearClaseLexica(self):
        #nombre de la nueva clase lexica
        nombre_clase_lexica=self.ui.lineEdit_ClaseLexicaNom.text()
        #token de la calse lexica
        token=self.ui.spinBox_Token.value()
        #nombre de el automata 
        nombre_afn=self.ui.comboBox_AFN.currentText()
        #se busca el afn para la clase lexica
        afn=copy.copy(self.db.obtenerAFN(nombre_afn))

        #se validan los datos para la nueva Clase Lexica
        clase_lexica=self.db.CrearClaseLexica(nombre_clase_lexica,token,afn)    

        

        # status de la creacion de la clase lexica
        self.ui.label_StatusClaseLexica.setText("hecho")
        #se muestra el automata en consola
        afn.mostrarAutomata()
        #se agrega a los combobox de clase lexica
        self.ui.comboBox_ClasesLexicas.addItem(clase_lexico.getNombreALexico())
        #se almacena en la base de datos
        self.db.agregarClaseLexica(clase_lexica)
        

    def crearAnalizadorLexico(self):
        #nombre del nuevo analizador lexico
        nombre_a_lexico=self.ui.lineEdit_AnalizadorNom.text()
        #nombre de la clase lexica para el analizador lexico
        nombre_clase_lexica=self.ui.comboBox_AFN.currentText()
        #se busca la clase lexica
        clase_lexica=self.db.obtenerClaseLexica(self,nombre_clase_lexica)
        
        a_lexico=self.db.CrearA_Lexico()

        #se manda un status de creacion
        self.ui.label_StatusALexico.setText("hecho")
        #se muestra el automata en consola
        afn.mostrarAutomata()
        #se agrega a el combobox del analizadores
        self.ui.comboBox_Analizadores.addItem(a_lexico.getNombreALexico())
        #se almacena en la base de datos
        self.db.agregarALexico(a_lexico)
    

##*****************************************Pestania de operaciones******
    def unir(self):
        nombre_union=self.ui.lineEdit_UnionNom.text()
        nombre_A1=self.ui.comboBox_A1Unir.currentText()
        nombre_A2=self.ui.comboBox_A2Unir.currentText()
        
        A1=self.db.obtenerAFN(nombre_A1)
        A2=self.db.obtenerAFN(nombre_A2)
        
        A1.unirCon(A2)
        # if not(nombre_union ==""):
        #     A1.Nombre_Automata=nombre_union
        A1.mostrarAutomata()

    def concatenar(self):
        nombre_concat=self.ui.lineEdit_ConcatNom.text()
        nombre_A1=self.ui.comboBox_A1Concat.currentText()
        nombre_A2=self.ui.comboBox_A2Concat.currentText()

        A1=self.db.obtenerAFN(nombre_A1)
        A2=self.db.obtenerAFN(nombre_A2)

        A1.concatCon(A2)
        # if not(nombre_concat ==""):
        #     A1.Nombre_Automata=nombre_concat

        A1.mostrarAutomata()

    def cerradura_Kleene(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()

        A=self.db.obtenerAFN(nombre_A)

        A.cerraduraKleene()
        A.mostrarAutomata()

    def cerradura_Positiva(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()

        A=self.db.obtenerAFN(nombre_A)
        
        A.cerraduraPositiva()
        A.mostrarAutomata()

    def opcional(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()

        A=self.db.obtenerAFN(nombre_A)

        A.opcion()
        A.mostrarAutomata()
##*************************************Fin de Pestania de operaciones******
##*****************************************Lista de AFNs*********

    def __eliminarAutomataLista(self,automata):
        
        #se eliminan de los combobox relacionados
        self.__eliminarAComboBox_Automatas(automata)

##*****************************************Lista de AFNs*********
##*****************************************Lista de Clases Lexicas******
        

    def __eliminarClaseLexicaLista(self,clase_lexico):
        
        #se procede a eliminar y ordanar para no tener problemas
        self.ui.comboBox_ClasesLexicas.removeItem(clase_lexico)
        
##*****************************************Lista de Clases Lexicas******

##*****************************************Lista de Analizadores Lexicos******
        
    def __eliminarALexicoLista(self,a_lexico):
        
        #se agrega a el combobox
        self.ui.comboBox_Analizadores.removeItem(a_lexico)
        
##*****************************************Lista de Analizadores Lexicos******


##*****************************************Combobox de AFN******
    def __agregarAComboBox_Automatas(self,nombre_afn):
        self.ui.comboBox_A1Unir.addItem(nombre_afn)
        self.ui.comboBox_A2Unir.addItem(nombre_afn)
        self.ui.comboBox_A1Concat.addItem(nombre_afn)
        self.ui.comboBox_A2Concat.addItem(nombre_afn)
        self.ui.comboBox_ACerradura.addItem(nombre_afn)

        self.ui.comboBox_AFN.addItem(nombre_afn)

    def __eliminarAComboBox_Automatas(self,nombre_afn):

        self.ui.comboBox_A1Unir.removeItem(self.ui.comboBox_A1Unir.findText(nombre_afn))
        self.ui.comboBox_A2Unir.removeItem(self.ui.comboBox_A2Unir.findText(nombre_afn))
        self.ui.comboBox_A1Concat.removeItem(self.ui.comboBox_A1Concat.findText(nombre_afn))
        self.ui.comboBox_A2Concat.removeItem(self.ui.comboBox_A2Concat.findText(nombre_afn))
        self.ui.comboBox_ACerradura.removeItem(self.ui.comboBox_ACerradura.findText(nombre_afn))
        
        self.ui.comboBox_AFN.removeItem(self.ui.comboBox_ACerradura.findText(nombre_afn))
##*****************************************Fin de Combobox de AFN******


##*************************************

    def mostrar(self):
        
        
        if self.ui.radioButton_AFNs.isChecked():
            try:
                self.__mostrarAutomata()
            except:
                print("No existen datos") 
        
        elif self.ui.radioButton_ClaseLexica.isChecked():
            try:
                self.__mostrarALexico()
            except:
                print("No existen datos")

        elif self.ui.radioButton_Analizador.isChecked():
            try:
                
                self.__mostrarClaseLexica()
            except:
                print("No existen datos")


    def __mostrarAutomata(self):
        _translate = QtCore.QCoreApplication.translate
        
        # definiendo numero de columnas
        self.ui.tableWidget_Mostrar.setColumnCount(6)
        # definiendo numero de filas (usando numero de automatas en la lista)
        total_automatas=6#len(self.Lista_De_Automatas)
        self.ui.tableWidget_Mostrar.setRowCount(total_automatas)



        #definiendo los numeros de las filas
        for f in range(total_automatas):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_Mostrar.setVerticalHeaderItem(f, item)

        #definiendo las columnas y la cabecera
        for c in range(6):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(c, item)
        

        ##definiendo los cuadros de las tabla (matriz)
        for f in range(total_automatas):
            for c in range(6):
                item = QtWidgets.QTableWidgetItem()
                self.ui.tableWidget_Mostrar.setItem(f, c, item)
        
        #etiquetas del numero de filas 
        for f in range(total_automatas):
            item = self.ui.tableWidget_Mostrar.verticalHeaderItem(f)
            item.setText(_translate("Form", str(f+1)))

        
        #etiquetas de la cabecera
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Nombre"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Lenguaje"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Estadi Inicial"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Estados"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Estados Finales"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Transiciones"))
        
        ##nombre e items
        __sortingEnabled = self.ui.tableWidget_Mostrar.isSortingEnabled()
        self.ui.tableWidget_Mostrar.setSortingEnabled(False)

        item = self.ui.tableWidget_Mostrar.item(0, 0)
        item.setText(_translate("Form", "texto1x1dnfbdfbdshfbdsbfhdbfhdsbfbdfbdsfbjdfgbfbvhjbf"))
        item = self.ui.tableWidget_Mostrar.item(0, 1)
        item.setText(_translate("Form", "texto1x2"))
        item = self.ui.tableWidget_Mostrar.item(0, 2)
        item.setText(_translate("Form", "texto1x3"))
        item = self.ui.tableWidget_Mostrar.item(0, 3)
        item.setText(_translate("Form", "texto1x4"))
        item = self.ui.tableWidget_Mostrar.item(0, 4)
        item.setText(_translate("Form", "texto1x5"))
        item = self.ui.tableWidget_Mostrar.item(0, 5)
        item.setText(_translate("Form", "texto1x6"))
        item = self.ui.tableWidget_Mostrar.item(1, 0)
        item.setText(_translate("Form", "texto2x1"))
        item = self.ui.tableWidget_Mostrar.item(1, 1)
        item.setText(_translate("Form", "texto2x2"))
        item = self.ui.tableWidget_Mostrar.item(1, 2)
        item.setText(_translate("Form", "texto2x3"))
        item = self.ui.tableWidget_Mostrar.item(1, 3)
        item.setText(_translate("Form", "texto2x4"))
        item = self.ui.tableWidget_Mostrar.item(1, 4)
        item.setText(_translate("Form", "texto2x5"))
        item = self.ui.tableWidget_Mostrar.item(1, 5)
        item.setText(_translate("Form", "texto2x6"))
        self.ui.tableWidget_Mostrar.setSortingEnabled(__sortingEnabled)


    def __mostrarClaseLexica(self):
        pass

    def __mostrarALexico(self):
        pass

    def Respaldo(self):
        _translate = QtCore.QCoreApplication.translate
        
        # definiendo numero de columnas
        self.ui.tableWidget_Mostrar.setColumnCount(6)
        # definiendo numero de filas (usando numero de automatas en la lista)

        self.ui.tableWidget_Mostrar.setRowCount(2)

        #definiendo los numeros de las filas
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setVerticalHeaderItem(1, item)
        #definiendo las caberera
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(5, item)

        ##definiendo los cuadros de las tabla
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(0, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(0, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(0, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(0, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(0, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(0, 5, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(1, 0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(1, 1, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(1, 2, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(1, 3, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(1, 4, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_Mostrar.setItem(1, 5, item)
        #etiquetas del numero de filas 
        item = self.ui.tableWidget_Mostrar.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.ui.tableWidget_Mostrar.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        #etiquetas de la cabecera
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Nombre"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Lenguaje"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Estadi Inicial"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Estados"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Estados Finales"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Transiciones"))
        ##nombre e items
        __sortingEnabled = self.ui.tableWidget_Mostrar.isSortingEnabled()
        self.ui.tableWidget_Mostrar.setSortingEnabled(False)
        item = self.ui.tableWidget_Mostrar.item(0, 0)
        item.setText(_translate("Form", "texto1x1dnfbdfbdshfbdsbfhdbfhdsbfbdfbdsfbjdfgbfbvhjbf"))
        item = self.ui.tableWidget_Mostrar.item(0, 1)
        item.setText(_translate("Form", "texto1x2"))
        item = self.ui.tableWidget_Mostrar.item(0, 2)
        item.setText(_translate("Form", "texto1x3"))
        item = self.ui.tableWidget_Mostrar.item(0, 3)
        item.setText(_translate("Form", "texto1x4"))
        item = self.ui.tableWidget_Mostrar.item(0, 4)
        item.setText(_translate("Form", "texto1x5"))
        item = self.ui.tableWidget_Mostrar.item(0, 5)
        item.setText(_translate("Form", "texto1x6"))
        item = self.ui.tableWidget_Mostrar.item(1, 0)
        item.setText(_translate("Form", "texto2x1"))
        item = self.ui.tableWidget_Mostrar.item(1, 1)
        item.setText(_translate("Form", "texto2x2"))
        item = self.ui.tableWidget_Mostrar.item(1, 2)
        item.setText(_translate("Form", "texto2x3"))
        item = self.ui.tableWidget_Mostrar.item(1, 3)
        item.setText(_translate("Form", "texto2x4"))
        item = self.ui.tableWidget_Mostrar.item(1, 4)
        item.setText(_translate("Form", "texto2x5"))
        item = self.ui.tableWidget_Mostrar.item(1, 5)
        item.setText(_translate("Form", "texto2x6"))
        self.ui.tableWidget_Mostrar.setSortingEnabled(__sortingEnabled)


##*****INICIO DE TODO EL PROGRAMA
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp=Ventana()
    myapp.show()
    sys.exit(app.exec_())
