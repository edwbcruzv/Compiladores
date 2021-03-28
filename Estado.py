
class Estado():
    #elem puede ser lista o string ya que esta sobrecargado
    def __init__(self,elem,Token=0):
        #Nombre del Estado
        if list==type(elem):
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

    def __lt__(self,estado):
        return self.Nombre<estado.getNombre()

    def __le__(self,estado):
        return self.Nombre<=estado.getNombre()

    def __eq__(self,estado):
        return self.Nombre==estado.getNombre()

    def __str__(self):
        #en el caso de ser un estado de aceptacion tambien se mostrara su token
        if self.Token:
            return "%s [shape=doublecircle] [token=%d]" %(
                self.Nombre,self.Token)
        else: #como no es estado de aceptacion solo se mostrara su nombre
            return self.Nombre