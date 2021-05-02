from Lib_Compiladores.CreadorAFNe import *
from Lib_Compiladores.CreadorALexico import *
from Lib_Compiladores.CreadorClaseLexica import *
from pathlib import Path
import os


class BaseDatos(CreadorAFNe,CreadorClaseLexica,CreadorALexico):

    def __init__(self):
        # Definiendo las carpetas de trabajo
        self.__CarpetaAFNs=Path("Datos/CarpetaAFNs")
        self.__CarpetaClasesLexicas=Path("Datos/CarpetaClasesLexicas")
        self.__CarpetaALexicos=Path("Datos/CarpetaALexicos")
        # Definiendo Los Creadores

        # Definiendo las listas donde se almacenaran cada tipo de automatas
        self.Lista_De_AFN=[]
        self.Lista_De_Clases_Lexicas=[]
        self.Lista_De_A_Lexicos=[]

##******************FUNCIONES PARA CARGAR ARCHIVOS EXISTENTES***************
    def cargarAFNs(self):
        archivos=os.listdir(self.__CarpetaAFNs)

        for archivo in archivos:
            archivo
            self.Lista_De_AFN.append()

    def cargarClasesLexicas(self):
        archivos=os.listdir(self.__CarpetaClasesLexicas)

        for archivo in archivos:
            archivo
            self.Lista_De_Clases_Lexicas.append()

    def cargarALexicos(self):
        archivos=os.listdir(self.__CarpetaALexicos)

        for archivo in archivos:
            archivo
            self.Lista_De_A_Lexicos.append()
#***************************************************************************

#*****************Manejo de las listas*******************
    def obtenerAFN(self,nombre_AFN):
        temp_A=AFN_e(nombre_AFN)
        
        afn=self.Lista_De_Automatas[self.Lista_De_Automatas.index(temp_A)]
        return afn

    def obtenerClaseLexica(self,nombre_clase_lexica):
        temp_clase_lexica=ClaseLexica(nombre_clase_lexica)
        clase_lexica=self.Lista_De_Clases_Lexicas[self.Lista_De_Clases_Lexicas.index(temp_clase_lexica)]
        return clase_lexica

    def obtenerALexico(self,nombre_a_lexico):
        temp_a_lexico=A_Lexico(nombre_a_lexico)
        a_lexico=self.Lista_De_A_Lexicos[self.Lista_De_A_Lexicos.index(temp_a_lexico)]
        return a_lexic
#********************************************************

##*****************MANEJO DE LAS CARPETAS********************
    #-----------------------------AFN_E
    def agregarAFN(self,AFN_e_obj):
        # se agrega a la carpeta
        nombre_archivo=AFN_e_obj.getNombreAFN()
        archivo=open(self.__CarpetaAFNs+nombre_archivo+".afn","w")

        self.Lista_De_AFN.append(AFN_e_obj)
        self.Lista_De_AFN.sort()

    def quitarAFN(self,nombre_archivo):
        # se quita de la carpeta
        os.remove(self.__CarpetaAFNs+nombre_archivo)

        self.Lista_De_AFN.remove(object)
    #-----------------------------ClaseLexica
    def agregarClaseLexica(self,Clase_Lexica_obj):
        # se agrega a la carpeta
        nombre_archivo=Clase_Lexica_obj.getNombreClaseLexica()
        archivo=open(self.__CarpetaClasesLexicas+nombre_archivo+".clx","w")

        self.Lista_De_Clases_Lexicas.append(Clase_Lexica_obj)
        self.Lista_De_Clases_Lexicas.sort()

    def quitarClaseLexica(self,nombre_archivo):
        # se quita de la carpeta
        os.remove(self.__CarpetaClasesLexicas+nombre_archivo)

        self.Lista_De_Clases_Lexicas.remove(object)
    #-----------------------------A_Lexico
    def agregarALexico(self,A_Lexico_e_obj):
        # se agrega a la carpeta
        nombre_archivo=A_Lexico_e_obj.getNombreALexico()
        archivo=open(self.__CarpetaALexicos+nombre_archivo+".alx","w")

        self.Lista_De_A_Lexicos.append(A_Lexico_e_obj)
        self.Lista_De_A_Lexicos.sort()

    def quitarALexico(self,nombre_archivo):
        # se quita de la carpeta
        os.remove(self.__CarpetaALexicos+nombre_archivo)

        self.Lista_De_A_Lexicos.remove(object)
#************************************************************

