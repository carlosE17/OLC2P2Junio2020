from CError import CError

class Estaticos:
    def __init__(self,Lerr):
        self.nL=0
        self.nT=0
        self.nA=0
        self.nV=0
        self.nS=2
        self.ra=1
        self.Lerrores=Lerr
        self.C3d=''
        self.globalesC3d=''
        self.mainC3d=''
        self.retornos=''
        self.C3dFunciones={}
        self.structs={}

    def addFun(self,n,funcion):
        if n in self.Lerrores:
            self.Lerrores.append(CError("Semantico","La funcion \'"+str(n)+'\' ya fue declarada',0,funcion.linea))
            return
        self.C3dFunciones[n]=funcion
    
    def newTemp(self):
        self.nT+=1
        return "$t"+str(self.nT)
    
    def newparamA(self):
        self.nA+=1
        return "$a"+str(self.nA)

    def newretornoV(self):
        self.nV+=1
        return "$v"+str(self.nV)

    def newpilaS(self):
        self.nS+=1
        return "$s"+str(self.nS)
    
    def newetiquetaL(self):
        self.nL+=1
        return "L"+str(self.nL)