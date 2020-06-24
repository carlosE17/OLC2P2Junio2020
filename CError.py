

class CError:
    def __init__(self,t,d,c,l):
        self.columna=str(c)
        self.linea=str(l)
        self.tipo=str(t)
        self.descripcion=str(d)
    def getTexto(self):
        return "<tr> <td> " + self.tipo + "</td><td> " + self.descripcion + " </td><td> " + self.linea + " </td> </tr>"