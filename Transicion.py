

class Transicion():
    
    def __init__(self,lista=None,EstadoPrincipal=None,EstadoDestino=None,Simbolos=None):
        
        if lista==None:
            #Estado(Objeto) Principal
            self.EstadoPrincipal=EstadoPrincipal
            #Estado(Objeto) Destino
            self.EstadoDestino=EstadoDestino
            #Lista de Simbolos de transicion
            self.Simbolos=Simbolos
        else:   #creacion deo objeto usando solo el primer argumento
            #Estado(Objeto) Principal
            self.EstadoPrincipal=lista[0]
            #Estado(Objeto) Destino
            self.EstadoDestino=lista[1]
            #Lista de Simbolos de transicion
            self.Simbolos=lista[2]

    def setEstadoPrincipal(self,EstadoPrincipal):
        self.EstadoPrincipal=EstadoPrincipal

    def setEstadoDestino(self,EstadoDestino):
        self.EstadoDestino=EstadoDestino

    def setSimbolos(self,Simbolos):
        self.Simbolos=Simbolos

    def getEstadoPrincipal(self):
        return self.EstadoPrincipal

    def getEstadoDestino(self):
        return self.EstadoDestino

    def getSimbolos(self):
        return self.Simbolos

    def __str__(self):

        return "%s -> %s [label=%s] " %(
            self.EstadoPrincipal,self.EstadoDestino,self.Simbolos)
