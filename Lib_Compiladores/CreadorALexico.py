from Lib_Compiladores.Lib_ALexico import A_Lexico


class CreadorALexico:
    
    #solo se crea el objeto
    def __init__(self):
        pass

    def CrearA_Lexico(self,str_nombre_a_lexico,clase_lexica_objec):

        if not(str==type(str_nombre_a_lexico) and len(str_nombre_a_lexico)>5):
            return "Error en el nombre, deben se mas caracteres"

        if not(isinstance(clase_lexica_objec,A_Lexico)):
            return "Error en el automata, no es A_Lexico"

        # __Nombre_A_Lexico:"nombreALexico"
        Nombre_A_Lexico=str_nombre_a_lexico
        # __Clase_Lexica:ClaseLexica().objet
        Clase_Lexica=clase_lexica_objec

        return A_Lexico(Nombre_A_Lexico,Clase_Lexica)

