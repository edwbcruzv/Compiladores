from Lib_Compiladores.CreadorAFNe import *
from Lib_Compiladores.CreadorALexico import *
from Lib_Compiladores.CreadorClaseLexica import *
import os


class BaseDatos(CreadorAFNe,CreadorClaseLexica,CreadorALexico):

    def __init__(self):
        # Definiendo las carpetas de trabajo
        self.__CarpetaAFNs="Datos/CarpetaAFNs/"
        self.__CarpetaClasesLexicas="Datos/CarpetaClasesLexicas/"
        self.__CarpetaALexicos="Datos/CarpetaALexicos/"
        # Definiendo Los Creadores

        # Definiendo las listas donde se almacenaran cada tipo de automatas
        self.Lista_De_AFN=[]
        self.Lista_De_Clases_Lexicas=[]
        self.Lista_De_A_Lexicos=[]

        self.cargarAFNs()
        self.cargarClasesLexicas()
        self.cargarALexicos()
        

##******************FUNCIONES PARA CARGAR ARCHIVOS EXISTENTES***************
    def cargarAFNs(self):
        archivos=os.listdir(self.__CarpetaAFNs)

        for nombre_archivo in archivos:
            archivo = open(self.__CarpetaAFNs+nombre_archivo, "r")
            cadena=archivo.read()
            #print(cadena)
            str_aux="".join(cadena.split("|||"))
            list_aux=str_aux.split("__")
            #print(list_aux)

            #CrearAutomataAFN(nombreAFN,num_estados,str_lenguaje,str_edo_inicial,str_estados_aceptacion,str_transiciones)
            afn,respuesta=self.CrearAutomataAFN(list_aux[0], list_aux[1], list_aux[2], list_aux[3], list_aux[4], list_aux[5])
            #print(respuesta)
            if not(isinstance(afn,AFN_e)):
                print(respuesta)
                return
            self.Lista_De_AFN.append(afn)

    def cargarClasesLexicas(self):
        archivos=os.listdir(self.__CarpetaClasesLexicas)

        for nombre_archivo in archivos:
            archivo = open(self.__CarpetaClasesLexicas+nombre_archivo, "r")
            cadena = archivo.read()
            #print(cadena)
            str_aux1 = "".join(cadena.split("||||"))
            list_aux = str_aux1.split("|||")
            # informacion de la clase lexica
            clase_lexica = list_aux[0].split("__")
            # informacion del AFN asociado
            afn = list_aux[1].split("__")  
            #print("Clase Lexica:",clase_lexica)
            #print("AFN:",afn)

            AFN, respuesta = self.CrearAutomataAFN(afn[0], afn[1], afn[2], afn[3], afn[4], afn[5])
            #print(respuesta)
            Clase_Lexica,respuesta = self.CrearClaseLexica(clase_lexica[0], clase_lexica[1], AFN)
            #print(respuesta)
            if not(isinstance(AFN, AFN_e)) and not(isinstance(Clase_Lexica, ClaseLexica)):
                print(respuesta)
                return

            self.Lista_De_Clases_Lexicas.append(Clase_Lexica)

    def cargarALexicos(self):
        archivos=os.listdir(self.__CarpetaALexicos)

        for nombre_archivo in archivos:
            archivo = open(self.__CarpetaALexicos+nombre_archivo, "r")
            cadena = archivo.read()
            #print(cadena)
            str_aux1 = "".join(cadena.split("|||||"))
            list_aux = str_aux1.split("|||")
            # informacion del analizador lexico
            nombre_a_lexico = list_aux[0]
            # informacion del AFN(AFD) asociado
            afn = list_aux[1].split("__")
            #print("Analizador Lexico:",nombre_a_lexico)
            #print("AFN:", afn)
            AFN, respuesta = self.CrearAutomataAFN(
                afn[0], afn[1], afn[2], afn[3], afn[4], afn[5])
            #print(respuesta)

            a_lexico, respuesta=self.CrearA_Lexico(nombre_a_lexico,AFN)
            #print(respuesta)
            self.Lista_De_A_Lexicos.append(a_lexico)
#***************************************************************************

#*****************Manejo de las listas*******************
    def obtenerAFN(self,nombre_AFN):
        temp_A=AFN_e(nombre_AFN)
        
        afn=self.Lista_De_AFN[self.Lista_De_AFN.index(temp_A)]
        return afn

    def obtenerClaseLexica(self,nombre_clase_lexica):
        temp_clase_lexica=ClaseLexica(nombre_clase_lexica)
        clase_lexica=self.Lista_De_Clases_Lexicas[self.Lista_De_Clases_Lexicas.index(temp_clase_lexica)]
        return clase_lexica

    def obtenerALexico(self,nombre_a_lexico):
        temp_a_lexico=A_Lexico(nombre_a_lexico)
        a_lexico=self.Lista_De_A_Lexicos[self.Lista_De_A_Lexicos.index(temp_a_lexico)]
        return a_lexico
#********************************************************

##*****************MANEJO DE LAS CARPETAS********************
    #-----------------------------AFN_E
    def agregarAFN(self,AFN_e_obj):
        # se agrega a la carpeta
        nombre_archivo=AFN_e_obj.getNombreAFN()

        archivo=open(self.__CarpetaAFNs+nombre_archivo+".afn","w")
        archivo.write(AFN_e_obj.toDataBase())
        archivo.close()

        if AFN_e_obj in self.Lista_De_AFN:
            return

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
        archivo.write(Clase_Lexica_obj.toDataBase())
        archivo.close()

        if Clase_Lexica_obj in self.Lista_De_Clases_Lexicas:
            return
        self.Lista_De_Clases_Lexicas.append(Clase_Lexica_obj)
        self.Lista_De_Clases_Lexicas.sort()

    def quitarClaseLexica(self,nombre_archivo):
        # se quita de la carpeta
        os.remove(self.__CarpetaClasesLexicas+nombre_archivo)

        self.Lista_De_Clases_Lexicas.remove(object)
    #-----------------------------A_Lexico
    def agregarALexico(self,A_Lexico_obj):
        # se agrega a la carpeta
        nombre_archivo=A_Lexico_obj.getNombreALexico()
        archivo=open(self.__CarpetaALexicos+nombre_archivo+".alx","w")
        archivo.write(A_Lexico_obj.toDataBase())
        #print(A_Lexico_obj.toDataBase())
        archivo.close()
        self.Lista_De_A_Lexicos.append(A_Lexico_obj)
        self.Lista_De_A_Lexicos.sort()

    def quitarALexico(self,nombre_archivo):
        # se quita de la carpeta
        os.remove(self.__CarpetaALexicos+nombre_archivo)

        self.Lista_De_A_Lexicos.remove(object)
#************************************************************

