from Lib_Compiladores.Lib_ClaseLexica import ClaseLexica

class CreadorClaseLexica:
    
    #solo se crea el objeto
    def __init__(self):
        pass

    #los parametros recibidos son puras cadenas con un formato especifico
    def CrearClaseLexica(self,str_nombre_clase_lexica,token,AFN_objet):

        if not(str==type(str_nombre_clase_lexica) and len(str_nombre_clase_lexica)>5):
            return "Error en el nombre, deben se mas caracteres"
        
        # token puede ser un str o int
        if not(int==type(token)) :
            #al no ser int se verifica si es str
            if str==type(token):
                #al ser str se hace el prse a int
                token=int(token)
            else: #es un tipo desconocido no valido
                return "Error en el parametro del numero de estados"
        
        
        if not(isinstance(AFN_objet,AFN_e)):
            return "Error en el automata, no es AFN_e"

        # FORMATO QUE SE LE PIDE AL USUARIO Y QUE SE DEBE DE VALIDAR
        # Nombre_Clase_Lexica:"NombreClaseLexica"
        # str_nombre_clase_lexica :"NombreClaseLexica"
        # AFN_objet : AFN().objet 
        # token (int o str)

        #FORMATO QUE DEBE SE CUMPLIR PARA QUE SE CREE EL OBJETO ClaseLexica

        # Nombre_Clase_Lexica:"NombreClaseLexica"
        Nombre_Clase_Lexica=str_nombre_clase_lexica
        # AFN: AFN().objet 
        AFN=AFN_objet
        # Token: int
        Token=token

        return ClaseLexica(self,Nombre_Clase_Lexica,Token,AFN)

