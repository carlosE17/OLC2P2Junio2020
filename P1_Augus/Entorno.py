from CError import CError

class Entorno:
    
    def __init__(self):
        self.tabla={}
        self.etiquetas={}
    
    def actualizar(self,nombre,simbolo):
        self.tabla[str(nombre)]=simbolo
    
    def buscar(self,n,columna,linea,ast):
        if str(n) in self.tabla:
            return self.tabla[str(n)]
        else:
            ast.Lerrores.append(CError('Semantico','No se encontro la variable \''+str(n)+'\' probablemente no esta declarada',columna,linea))
            return None
    
    def getPosEtiqueta(self, nombre,columna,linea,ast):
        if str(nombre) in self.etiquetas:
            return int(self.etiquetas[str(nombre)])
        else:
            ast.Lerrores.append(CError('Semantico','No se encontro la Etiqueta \''+str(nombre)+'\' probablemente no esta declarada',columna,linea))
            return None  
    
    def addEtiqueta(self,nombre,i):
        self.etiquetas[str(nombre)]=int(i)
    