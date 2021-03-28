
class Estado():
    #elem puede ser lista o string ya que esta sobrecargado
    def __init__(self,elem=None,Token=0):
        #Nombre del Estado
        if elem==type(list):
            self.Nombre=elem[0]
            self.Token=elem[1]
        else:
            self.Nombre=elem
            self.Token=Token
            

    def setNombre(self,Nombre):
        self.Nombre=Nombre

    #Al ser estado de aceptacion se requerira su token
    def setToken(self,Token):
        self.Token=Token

    def getNombre(self):
        return self.Nombre

    def getToken(self):
        return self.Token

    def __str__(self):
        #en el caso de ser un estado de aceptacion tambien se mostrara su token
        if self.Token:
            return "%s [shape=doublecircle] [token=%s]" %(
                self.Nombre,self.Token)
        else: #como no es estado de aceptacion solo se mostrara su nombre
            return self.Nombre