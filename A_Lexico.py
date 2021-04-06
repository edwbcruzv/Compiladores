from AFN_e import *


class A_Lexico:
    afd=object()

    def __init__(self,estados,alfabeto,estado_inicial,estados_aceptacion,transiciones):
        self.afd=AFN_e(estados,alfabeto,estado_inicial,estados_aceptacion,transiciones)

    def toAFD(self):
        pass

    def irA(self):
        pass

    def moverA(self):
        pass

    def tablaAFD(self):
        pass