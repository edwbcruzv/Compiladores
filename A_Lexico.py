from AFNe.AFNe import AFN_e,convertAFD

class A_Lexico:

    def __init__(self,nombre,afn):
        self.Nombre_A_Lexico=nombre
        
        self.afd=convertAFD(afn).afd
        self.afd.mostrarAutomata()
        self.afdTransiciones=self.afd.getTransiciones()


    def analizarCadena(self,cadena):
        list_cadena=list(cadena)

        Lista_Lexemas=[]
        Lexema_temp=[]

        tam_cadena=len(list_cadena)
        #inicio del algoritmo
        #posicion del estado del afn
        Estado_Actual=self.afd.getEdoInicial()
        #nos indicara si pasamos por un estado de aceptacion
        Bandera_Edo_Acept=False 
        cursor_cadena=0 
        
        #mientras que no sea el fin de la cadena
        while cursor_cadena==tam_cadena:
            simbolo=list_cadena[cursor_cadena]

            #ver si existe una transicion  del estado actual con el simbolo de la cadena actual
            Estado_Destino,boleano=self.__existeTransicion(Estado_Actual,simbolo)
            #si boolean el False hay un error
            if boleano:
                Lexema_temp.append(simbolo)
                #si estado actual es un estado de aceptacion
                if Estado_Actual.getToken>0:
                    #print(Estado_Actual.getToken())
                    Bandera_Edo_Acept=True
                else:#no es estado de aceptacion
                    Bandera_Edo_Acept=False 
                #seguimos sin pasar por estado de aceptacion
                Estado_Actual=Estado_Destino
                cursor_cadena=cursor_cadena+1
                

            #no esiste ninguna transicion entonces hay un error
            else:
                #checar si se paso por un estado de aceptacion
                if Bandera_Edo_Acept:
                    #se descarga el lexema actual
                    Lista_Lexemas.append(self.__nuevoLexema(Lexema_temp,Estado_Actual.token()))
                    Lexema_temp=[]
                    #posicion del estado del afd
                    Estado_Actual=self.afd.getEdoInicial()
                    
                #no se ha pasado por ningun estado de aceptacion
                else:
                    #posicion del estado del afd
                    Estado_Actual=self.afd.getEdoInicial()
                    #se descarta el lexema
                    Lexema_temp=[]
                    
        return Lista_Lexemas

    def __nuevoLexema(self,Lexema_lista,token):
        return ["".join(Lexema_lista),token]            
            
        #se Busca si existe una transicion en el afd 
    def __existeTransicion(self,Estado_Actual,Simbolo):
        
        for T in self.afdTransiciones:
            if T[0]==Estado_Actual and T[2]==Simbolo:
                return T[1],True #si existe
        #no existe
        return [],False

    def __lt__(self,a_lexico):
        return self.Nombre_A_Lexico<a_lexico.Nombre_A_Lexico

    def __le__(self,a_lexico):
        return self.Nombre_A_Lexico<=a_lexico.Nombre_A_Lexico

    def __eq__(self,a_lexico):
        return self.Nombre_A_Lexico==a_lexico.Nombre_A_Lexico

    def tablaAFD(self):
        pass