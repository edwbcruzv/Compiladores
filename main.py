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
        super(Ventana,self).__init__(parent)
        self.ui=Ui_Form()
        self.ui.setupUi(self)

        #se crea y carga la base de datos
        self.db = BaseDatos()
        #se cargan los combobox a partirde los datos cargados
        self.__cargarComboBox()
        #se carga la tabla de clases lexicas en la pestaña de analisis lexico
        self.__mostrarListaClasesLexicas()
        
        #area de los AFN
        self.ui.pushButton_Unir.clicked.connect(self.unir)
        self.ui.pushButton_Concat.clicked.connect(self.concatenar)
        self.ui.pushButton_CerraduraPositiva.clicked.connect(self.cerradura_Positiva)
        self.ui.pushButton_CerraduraKleene.clicked.connect(self.cerradura_Kleene)
        self.ui.pushButton_Opcional.clicked.connect(self.opcional)

        self.ui.pushButton_Crear.clicked.connect(self.crearAutomataAFN)

        #Area de las clases lexicas
        self.ui.pushButton_CrearClaseLexica.clicked.connect(self.crearClaseLexica)

        #Area de los analizadores lexicos
        self.ui.pushButton_CrearAnalizador.clicked.connect(self.crearAnalizadorLexico)

        
        self.ui.pushButton_Mostrar.clicked.connect(self.mostrar)
        



    def crearAutomataAFN(self):
        print("Creando afn")
        nombreAFN=self.ui.lineEdit_NombreAFN.text()
        num_estados=str(self.ui.spinBox_num_Estados.value())
        str_lenguaje=self.ui.textEdit_Lenguale.toPlainText()
        str_estados_aceptacion=self.ui.textEdit_EstadosAceptacion.toPlainText()
        str_transiciones=self.ui.textEdit_Transiciones.toPlainText()

        # print(nombreAFN)
        # print(num_estados)
        # print(str_lenguaje)
        # print("0")
        # print(str_estados_aceptacion)
        # print(str_transiciones)

        #se valida el automata
                                                
        afn,respuesta=self.db.CrearAutomataAFN(nombreAFN,num_estados,str_lenguaje,"0",str_estados_aceptacion,str_transiciones)

        #Se manda un status a la interfaz grafica
        self.ui.label_StatusCrear.setText(respuesta)
        #su hubo un error se termina el proceso
        if not(isinstance(afn,AFN_e)):
            return        
        
        #se muestra el automata en consola
        # afn.mostrarAutomata()

        #print("DataBase:",afn.toDataBase())
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
        afn=self.db.obtenerAFN(nombre_afn)

        #se validan los datos para la nueva Clase Lexica
        clase_lexica,respuesta=self.db.CrearClaseLexica(nombre_clase_lexica,token,afn)    

        # status de la creacion de la clase lexica
        self.ui.label_StatusClaseLexica.setText(respuesta)

        if not(isinstance(clase_lexica,ClaseLexica)):
            return
        #se muestra el automata en consola
        clase_lexica.mostrarClaseLexica()
        #se agrega a los combobox de clase lexica
        self.ui.comboBox_ClasesLexicas.addItem(clase_lexica.getNombreClaseLexica())
        #se almacena en la base de datos
        self.db.agregarClaseLexica(clase_lexica)
        

    def crearAnalizadorLexico(self):

        #nombre del nuevo analizador lexico
        nombre_a_lexico=self.ui.lineEdit_AnalizadorNom.text()
        
        a_lexico,respuesta=self.db.CrearA_Lexico(nombre_a_lexico)

        tabla=self.ui.tableWidget_ClasesLexicas
        for i in range(len(self.db.Lista_De_Clases_Lexicas)):
            #0 si tabla.item(i,0).checkState() esta desmarcado
            #2 si tabla.item(i,0).checkState() esta marcado
            if tabla.item(i,0).checkState() == 2:
                print(tabla.item(i,0).text()," agregado") 
                #se busca la clase lexica
                clase_lexica=self.db.obtenerClaseLexica(tabla.item(i,0).text())

        if a_lexico==None:
            self.ui.label_StatusALexico.setText("No se creo el analizador lexico")
            return

        #se manda un status de creacion
        self.ui.label_StatusALexico.setText(respuesta)
        #se muestra el automata en consola
        
        #se agrega a el combobox del  lexicos
        self.ui.comboBox_Analizadores.addItem(a_lexico.getNombreALexico())
        #se almacena en la base de datos
        #self.db.agregarALexico(a_lexico)

    def __mostrarListaClasesLexicas(self):
        _translate = QtCore.QCoreApplication.translate
        
        #------------INICIO DE LA TABLA DE CLASES LEXICAS---------------
        total_clases_lexicas=len(self.db.Lista_De_Clases_Lexicas)
        # Definiendo la cabecera
        self.ui.tableWidget_ClasesLexicas.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem() 
        self.ui.tableWidget_ClasesLexicas.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_ClasesLexicas.setHorizontalHeaderItem(1, item)

        #definiendo las filas
        self.ui.tableWidget_ClasesLexicas.setRowCount(total_clases_lexicas)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_ClasesLexicas.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ui.tableWidget_ClasesLexicas.setVerticalHeaderItem(1, item)

        
        # Definiendo la matriz
        for f in range(total_clases_lexicas):
            # Definiendo la columna con los checked
            item = QtWidgets.QTableWidgetItem()
            item.setCheckState(QtCore.Qt.Unchecked)
            self.ui.tableWidget_ClasesLexicas.setItem(f, 0, item)

            # Definiendo la columna faltante
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_ClasesLexicas.setItem(f, 1, item)
        

        item = self.ui.tableWidget_ClasesLexicas.verticalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.ui.tableWidget_ClasesLexicas.verticalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.ui.tableWidget_ClasesLexicas.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Clase Lexica"))
        item = self.ui.tableWidget_ClasesLexicas.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Token"))

        __sortingEnabled = self.ui.tableWidget_ClasesLexicas.isSortingEnabled()
        self.ui.tableWidget_ClasesLexicas.setSortingEnabled(False)
        
        f = 0
        for elem in self.db.Lista_De_Clases_Lexicas:
            #nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones
            list_aux = [elem.getNombreClaseLexica(),str(elem.getToken())]
            #print(list_aux)
            c = 0
            for dato in list_aux:
                item = self.ui.tableWidget_ClasesLexicas.item(f, c)
                item.setText(_translate("Form", dato))
                c += 1

            f += 1

        self.ui.tableWidget_ClasesLexicas.setSortingEnabled(__sortingEnabled)
        #------------FIN DE LA TABLA DE CLASES LEXICAS---------------

##*****************************************Pestania de operaciones******
    def unir(self):
        nombre_union=self.ui.lineEdit_UnionNom.text()
        nombre_A1=self.ui.comboBox_A1Unir.currentText()
        nombre_A2=self.ui.comboBox_A2Unir.currentText()
        
        A1=self.db.obtenerAFN(nombre_A1)
        A2=self.db.obtenerAFN(nombre_A2)

        if nombre_union =="":
            self.ui.label_StatusUnir.setText("Ingrese un nombre a la union")
        
        A1.unirCon(A2)
        A1.setNombreAFN(nombre_union)
        A1.mostrarAutomata()
        self.ui.label_StatusUnir.setText("Hecho")
        #se agrega a los combobox
        self.__agregarAComboBox_Automatas(A1.getNombreAFN())
        #Se almacena el automata creado en la base de datos
        self.db.agregarAFN(A1)

    def concatenar(self):
        nombre_concat=self.ui.lineEdit_ConcatNom.text()
        nombre_A1=self.ui.comboBox_A1Concat.currentText()
        nombre_A2=self.ui.comboBox_A2Concat.currentText()

        A1=self.db.obtenerAFN(nombre_A1)
        A2=self.db.obtenerAFN(nombre_A2)

        if nombre_concat =="":
            
            self.ui.label_StatusConcat.setText("Ingrese un nombre a la concatenacion")

        A1.concatCon(A2)
        A1.setNombreAFN(nombre_concat)
        self.ui.label_StatusConcat.setText("Hecho")
        A1.mostrarAutomata()
        #se agrega a los combobox
        self.__agregarAComboBox_Automatas(A1.getNombreAFN())
        #Se almacena el automata creado en la base de datos
        self.db.agregarAFN(A1)

    def cerradura_Kleene(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()

        A=self.db.obtenerAFN(nombre_A)

        A.cerraduraKleene()
        A.mostrarAutomata()
        self.ui.label_StatusKleene.setText("Kleene Hecho")
        self.db.agregarAFN(A)

    def cerradura_Positiva(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()

        A=self.db.obtenerAFN(nombre_A)
        
        A.cerraduraPositiva()
        A.mostrarAutomata()
        self.ui.label_StatusPositiva.setText("Positiva Hecho")
        self.db.agregarAFN(A)

    def opcional(self):
        nombre_A=self.ui.comboBox_ACerradura.currentText()

        A=self.db.obtenerAFN(nombre_A)

        A.opcion()
        A.mostrarAutomata()
        self.ui.label_StatusOpcional.setText("Opcional Hecho")
        self.db.agregarAFN(A)
##*************************************Fin de Pestania de operaciones******

    def __cargarComboBox(self):

        for afn in self.db.Lista_De_AFN:
            self. __agregarAComboBox_Automatas(afn.getNombreAFN())

        for clase_lexica in self.db.Lista_De_Clases_Lexicas:
            self.ui.comboBox_ClasesLexicas.addItem(clase_lexica.getNombreClaseLexica())

        for a_lexico in self.db.Lista_De_A_Lexicos:
            self.ui.comboBox_Analizadores.addItem(a_lexico.getNombreALexico())
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
                self.__mostrarAFNs()
            except:
                print("No existen datos") 
        
        elif self.ui.radioButton_ClaseLexica.isChecked():
            #try:
            self.__mostrarClasesLexicas()
                
            #except:
            #    print("No existen datos")

        elif self.ui.radioButton_Analizador.isChecked():
            try:
                self.__mostrarALexicos()
            except:
                print("No existen datos")


    def __mostrarAFNs(self):
        _translate = QtCore.QCoreApplication.translate

        # definiendo numero de columnas
        self.ui.tableWidget_Mostrar.setColumnCount(6)
        # definiendo numero de filas (usando numero de automatas en la lista)
        total_automatas = len(self.db.Lista_De_AFN)
        print("Todal de automatas", total_automatas)
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
        item.setText(_translate("Form", "Estados"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Lenguaje"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Estado Inicial"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Estados De Aceptacion"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Transiciones"))

        ##nombre e items
        __sortingEnabled = self.ui.tableWidget_Mostrar.isSortingEnabled()
        self.ui.tableWidget_Mostrar.setSortingEnabled(False)

        f = 0
        for elem in self.db.Lista_De_AFN:
            #nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones
            list_aux = list(elem.__str__())
            #print(list_aux)
            c = 0
            for dato in list_aux:
                item = self.ui.tableWidget_Mostrar.item(f, c)
                item.setText(_translate("Form", dato))
                c += 1

            f += 1

        self.ui.tableWidget_Mostrar.setSortingEnabled(__sortingEnabled)


    def __mostrarClasesLexicas(self):
        

        _translate = QtCore.QCoreApplication.translate

        # definiendo numero de columnas
        self.ui.tableWidget_Mostrar.setColumnCount(8)
        # definiendo numero de filas (usando numero de clases lexicas en la lista)
        total_clases_lexicas = len(self.db.Lista_De_Clases_Lexicas)
        print("Todal de Clase lexicas", total_clases_lexicas)
        self.ui.tableWidget_Mostrar.setRowCount(total_clases_lexicas)

        #definiendo los numeros de las filas
        for f in range(total_clases_lexicas):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_Mostrar.setVerticalHeaderItem(f, item)

        #definiendo las columnas y la cabecera
        for c in range(8):
            item = QtWidgets.QTableWidgetItem()
            self.ui.tableWidget_Mostrar.setHorizontalHeaderItem(c, item)

        ##definiendo los cuadros de las tabla (matriz)
        for f in range(total_clases_lexicas):
            for c in range(8):
                item = QtWidgets.QTableWidgetItem()
                self.ui.tableWidget_Mostrar.setItem(f, c, item)
        
        #etiquetas del numero de filas
        for f in range(total_clases_lexicas):
            item = self.ui.tableWidget_Mostrar.verticalHeaderItem(f)
            item.setText(_translate("Form", str(f+1)))

        #etiquetas de la cabecera
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Nombre Clase Lexica"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Token"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Nombre AFN"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Estados"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Lenguaje"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Estado Inicial"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Estados De Aceptacion"))
        item = self.ui.tableWidget_Mostrar.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Transiciones"))

        ##nombre e items
        __sortingEnabled = self.ui.tableWidget_Mostrar.isSortingEnabled()
        self.ui.tableWidget_Mostrar.setSortingEnabled(False)

        f = 0
        for elem in self.db.Lista_De_Clases_Lexicas:
            #nombre_AFN, num_estados, str_lenguaje, str_edo_inicial, str_estados_aceptacion, str_transiciones
            list_aux = list(elem.__str__())
            #print(list_aux)
            c = 0
            for dato in list_aux:
                item = self.ui.tableWidget_Mostrar.item(f, c)
                item.setText(_translate("Form", dato))
                c += 1

            f += 1

        self.ui.tableWidget_Mostrar.setSortingEnabled(__sortingEnabled)

    def __mostrarALexicos(self):
        pass



##*****INICIO DE TODO EL PROGRAMA
if __name__=='__main__':
    app=QtWidgets.QApplication(sys.argv)
    myapp=Ventana()
    myapp.show()
    sys.exit(app.exec_())
