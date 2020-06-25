from CError import CError

class Entorno:
    
    def __init__(self,ant):
        self.tabla={}
        self.anterior=ant
    
    def insertar(self,nombre,simbolo,c,l,ast):
        if str(nombre) in self.tabla:
            ast.Lerrores.append(CError('Semantico','En este entorno \''+str(nombre)+'\' ya esta declarada',c,l))
            return
        else:
            self.tabla[str(nombre)]=simbolo
    
    def buscar(self,n,columna,linea,ast):
        e=self
        while(e!=None):
            if str(n) in e.tabla:
                return e.tabla[str(n)]
            e=e.anterior    
        ast.Lerrores.append(CError('Semantico','No se encontro la variable \''+str(n)+'\' probablemente no esta declarada',columna,linea))
        return None
    
    def actualizar(self,nombre,simbolo,c,l,ast):
        e=self
        while(e!=None):
            if str(nombre) in e.tabla:
                e.tabla[str(nombre)]=simbolo
                return
            e=e.anterior 
        ast.Lerrores.append(CError('Semantico','No se encontro la variable \''+str(nombre)+'\' probablemente no esta declarada',c,l))
        return None   


    