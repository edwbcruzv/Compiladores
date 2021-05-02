

class Transicion:
    
    def __init__(self,EdoPrincipal,NomEdoDestino,Simbolo):
        
        #Estado(Objeto) Principal
        self.EstadoPrincipal=EdoPrincipal
        #Estado(Objeto) Destino
        self.EstadoDestino=NomEdoDestino
        #Simbolo de transicion
        self.Simbolo=Simbolo
        

    def setEstadoPrincipal(self,estado):
        self.EstadoPrincipal=estado

    def setEstadoDestino(self,estado):
        self.EstadoDestino=estado

    def setSimbolo(self,simbolo):
        self.Simbolo=simbolo

    def getEstadoPrincipal(self):
        return self.EstadoPrincipal

    def getEstadoDestino(self):
        return self.EstadoDestino

    def getSimbolo(self):
        return self.Simbolo
    
    def __lt__(self,transicion):
        return self.EstadoPrincipal<transicion.getEstadoPrincipal()

    def __le__(self,transicion):
        return self.EstadoPrincipal<=transicion.getEstadoPrincipal()

    def __eq__(self,transicion):
        return (self.EstadoPrincipal<=transicion.getEstadoPrincipal() 
                and self.EstadoDestino<=transicion.getEstadoDestino()
                and self.Simbolo<=transicion.getSimbolo())

    def __str__(self):

        return "s%s -> s%s [label=\"%s\"] " %(
            self.EstadoPrincipal.getNombre(),self.EstadoDestino.getNombre(),self.Simbolo.__str__())
            