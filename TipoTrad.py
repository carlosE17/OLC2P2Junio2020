import enum

class tipoPrimitivo(enum.Enum):
    Entero=1
    Cadena=2
    Doble=3
    Arreglo=4
    Error=5
    void=6
    acceso=7
    puntero=8
    caracter=9
    structura=10

class tipoInstruccion(enum.Enum):
    etiqueta=1
    asignacionT=2
    asignacionA=3
    asignacionV=4
    salto=5
    condicional=6

class newtipo:
    def __init__(self,t,v):
        self.tipo=t
        self.v=v

class nodoAST:
    def __init__(self,v,n):
        self.vNodo=str(v)
        self.nNodo=str(n)
        self.hijos=[]


