from Lib_Compiladores.Lib_ALexico.A_Lexico import A_Lexico
from Lib_Compiladores.Lib_ClaseLexica.ClaseLexica import ClaseLexica
from Lib_Compiladores.Lib_AFN_e.AFN_e import AFN_e


class CreadorALexico:
    
    #solo se crea el objeto
    def __init__(self):
        pass

    def CrearA_Lexico(self,str_nombre_a_lexico,arg=None):

        if not(str==type(str_nombre_a_lexico) and len(str_nombre_a_lexico)>5):
            return None,"Error en el nombre, deben se mas caracteres"
        # __Nombre_A_Lexico:"nombreALexico"
        Nombre_A_Lexico=str_nombre_a_lexico

        a_lexico = A_Lexico(Nombre_A_Lexico)
        return a_lexico, "Analizador Lexico Creado"
