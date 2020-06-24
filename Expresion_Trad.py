from TipoTrad import *
from CError import CError
from tkinter import *
import sys

class primitivo:
    def __init__(self,t,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST(v,n)
        self.valor=v
        self.tipo=t
        self.gramm='\n<tr><td>PRIMITIVO::= '+str(v)+' </td><td> PRIMITIVO= primitivo('+str(v)+');  </td></tr>'
    def getvalor(self,entorno,estat):
        return self

class id_:
    def __init__(self,d,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST(d,n)
        self.variable=d
        # self.tipo=tipoPrimitivo.variable
        self.gramm='\n<tr><td>PRIMITIVO::= ID </td><td> PRIMITIVO= ID;  </td></tr>'
        self.gramm+='\n<tr><td>ID::= '+str(d)+' </td><td> ID= id_('+str(d)+');  </td></tr>'
    def getvalor(self,entorno,estat):
        temp=entorno.buscar(self.variable,self.columna,self.linea,estat)
        if temp!=None:
            return temp.valor.getvalor(entorno,estat)
        else:
            return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newSuma:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('+',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 + PRIMITIVO2 </td><td> EXP= newSuma(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(izq.valor)+int(der.valor),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)+float(der.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)+int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)+float(der.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Cadena:
            if der.tipo==tipoPrimitivo.Cadena:
                return primitivo(tipoPrimitivo.Cadena,str(izq.valor)+str(der.valor),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar la SUMA',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newResta:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('-',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 - PRIMITIVO2 </td><td> EXP= newResta(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(izq.valor)-int(der.valor),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)-float(der.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)-int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)-float(der.valor)),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar la RESTA',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newMultiplicacion:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('*',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 * PRIMITIVO2 </td><td> EXP= newMultiplicacion(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(izq.valor)*int(der.valor),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)*float(der.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)*int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)*float(der.valor)),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar la MULTIPLICACION',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newDivision:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('/',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 / PRIMITIVO2 </td><td> EXP= newDivision(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)/int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)/float(der.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)/int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)/float(der.valor)),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar la DIVISION',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newModulo:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('/',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 % PRIMITIVO2 </td><td> EXP= newModulo(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)%int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(int(izq.valor)%float(der.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)%int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                if float(der.valor)==0:
                    estat.Lerrores.append(CError('Semantico','No se puede dividir dentro de 0',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                return primitivo(tipoPrimitivo.Doble,float(float(izq.valor)%float(der.valor)),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar MODULO',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newAnd:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('&&',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 and and PRIMITIVO2 </td><td> EXP= newAnd(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                if(int(izq.valor)!=0):
                    izq=1
                else:
                    izq=0
                if(int(der.valor)!=0):
                    der=1
                else:
                    der=0
                return primitivo(tipoPrimitivo.Entero,izq and der,self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar And',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newOr:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('||',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 or or PRIMITIVO2 </td><td> EXP= newOr(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                if(int(izq.valor)!=0):
                    izq=1
                else:
                    izq=0
                if(int(der.valor)!=0):
                    der=1
                else:
                    der=0
                return primitivo(tipoPrimitivo.Entero,izq or der,self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar Or',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newNot:
    def __init__(self,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Not',n)
        self.vNodo.hijos.append(nodoAST('!',n+1))
        self.vNodo.hijos.append(der.vNodo)
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= !PRIMITIVO </td><td> EXP= newNot(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        if der.tipo==tipoPrimitivo.Entero:
            if(int(der.valor)!=0):
                der=1
            else:
                der=0
            return primitivo(tipoPrimitivo.Entero,int(not der),self.columna,self.linea,0)
        else:
            estat.Lerrores.append(CError('Semantico','Error al realizar Xor',self.columna,self.linea))
            return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newEqual:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('==',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 == PRIMITIVO2 </td><td> EXP= newEqual(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(int(izq.valor)==int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(int(izq.valor)==float(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Cadena:
                if str(der.valor).lstrip('-').replace('.','',1).isdigit():
                    return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)==float(der.valor)),self.columna,self.linea,0)
                else:
                    return primitivo(tipoPrimitivo.Entero,0,self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)==int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)==float(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Cadena:
                if str(der.valor).lstrip('-').replace('.','',1).isdigit():
                    return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)==float(der.valor)),self.columna,self.linea,0)
                else:
                    return primitivo(tipoPrimitivo.Entero,0,self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Cadena:
            if der.tipo==tipoPrimitivo.Cadena:
                return primitivo(tipoPrimitivo.Entero,int(str(izq.valor)==str(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Entero or der.tipo==tipoPrimitivo.Doble:
                if str(izq.valor).lstrip('-').replace('.','',1).isdigit():
                    return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)==float(der.valor)),self.columna,self.linea,0)
                return primitivo(tipoPrimitivo.Entero,0,self.columna,self.linea,0)

        
        estat.Lerrores.append(CError('Semantico','Error al realizar la Igualacion',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newNotEqual:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('!=',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 != PRIMITIVO2 </td><td> EXP= newNotEqual(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(int(izq.valor)!=int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(int(izq.valor)!=float(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Cadena:
                if str(der.valor).lstrip('-').replace('.','',1).isdigit():
                    return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)!=float(der.valor)),self.columna,self.linea,0)
                else:
                    return primitivo(tipoPrimitivo.Entero,1,self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)!=int(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)!=float(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Cadena:
                if str(der.valor).lstrip('-').replace('.','',1).isdigit():
                    return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)!=float(der.valor)),self.columna,self.linea,0)
                else:
                    return primitivo(tipoPrimitivo.Entero,1,self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Cadena:
            if der.tipo==tipoPrimitivo.Cadena:
                return primitivo(tipoPrimitivo.Entero,int(str(izq.valor)!=str(der.valor)),self.columna,self.linea,0)
            elif der.tipo==tipoPrimitivo.Entero or der.tipo==tipoPrimitivo.Doble:
                if str(izq.valor).lstrip('-').replace('.','',1).isdigit():
                    return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)!=float(der.valor)),self.columna,self.linea,0)
                return primitivo(tipoPrimitivo.Entero,1,self.columna,self.linea,0)

        
        estat.Lerrores.append(CError('Semantico','Error al realizar la Diferencia',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newMenorq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\<',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 menorQue PRIMITIVO2 </td><td> EXP= newMenorq(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero or izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero or der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)<float(der.valor)),self.columna,self.linea,0)

        estat.Lerrores.append(CError('Semantico','Error al realizar Menor Que',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newMayorq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\>',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 mayorQue PRIMITIVO2 </td><td> EXP= newMayorq(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero or izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero or der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)>float(der.valor)),self.columna,self.linea,0)

        estat.Lerrores.append(CError('Semantico','Error al realizar Mayor Que',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newMenorIgualq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\<=',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 menorIgualQue PRIMITIVO2 </td><td> EXP= newMenorIgualq(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero or izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero or der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)<=float(der.valor)),self.columna,self.linea,0)

        estat.Lerrores.append(CError('Semantico','Error al realizar Menor igual Que',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newMayorIgualq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\>=',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 mayorIgualQue PRIMITIVO2 </td><td> EXP= newMayorIgualq(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero or izq.tipo==tipoPrimitivo.Doble:
            if der.tipo==tipoPrimitivo.Entero or der.tipo==tipoPrimitivo.Doble:
                return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)>=float(der.valor)),self.columna,self.linea,0)

        estat.Lerrores.append(CError('Semantico','Error al realizar Mayor Igual Que',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newAndBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('&',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 and PRIMITIVO2 </td><td> EXP= newAndBtb(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                bizq=bin(int(izq.valor)).replace("b","").replace('-','')
                bder=bin(int(der.valor)).replace("b","").replace('-','')
                while(len(bizq)<len(bder)):
                    bizq='0'+bizq
                while(len(bder)<len(bizq)):
                    bder='0'+bder
                res='0'
                pos=0
                while pos<len(bizq):
                    res+=str(int(bizq[pos]) and int(bder[pos]))
                    pos+=1
                
                return primitivo(tipoPrimitivo.Entero,int(res,2),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar And bit a bit',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newOrBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('|',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 or PRIMITIVO2 </td><td> EXP= newOrBtb(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                bizq=bin(int(izq.valor)).replace("b","").replace('-','')
                bder=bin(int(der.valor)).replace("b","").replace('-','')
                while(len(bizq)<len(bder)):
                    bizq='0'+bizq
                while(len(bder)<len(bizq)):
                    bder='0'+bder
                res='0'
                pos=0
                while pos<len(bizq):
                    res+=str(int(bizq[pos]) or int(bder[pos]))
                    pos+=1
                
                return primitivo(tipoPrimitivo.Entero,int(res,2),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar OR bit a bit',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newXorBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('^',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 ^ PRIMITIVO2 </td><td> EXP= newXorBtb(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                bizq=bin(int(izq.valor)).replace("b","").replace('-','')
                bder=bin(int(der.valor)).replace("b","").replace('-','')
                while(len(bizq)<len(bder)):
                    bizq='0'+bizq
                while(len(bder)<len(bizq)):
                    bder='0'+bder
                res='0'
                pos=0
                while pos<len(bizq):
                    res+=str(int(bizq[pos]) ^ int(bder[pos]))
                    pos+=1
                
                return primitivo(tipoPrimitivo.Entero,int(res,2),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar XOR bit a bit',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newNotBtb:
    def __init__(self,izq,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('~',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.hijoIzq=izq
        self.gramm='\n<tr><td>EXP::= ~ PRIMITIVO </td><td> EXP= newNotBtb(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            bizq=bin(int(izq.valor)).replace("b","").replace('-','')
            res='0'
            pos=1
            while pos<len(bizq):
                res+=str(int(not int(bizq[pos])))
                pos+=1    
            return primitivo(tipoPrimitivo.Entero,int(res,2),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar Not bit a bit',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newDespIzqBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\< \<',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 despIzq PRIMITIVO2 </td><td> EXP= newDespIzqBtb(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                bizq=bin(int(izq.valor)).replace("b","").replace('-','')
                pos=int(der.valor)
                if pos<0:
                    estat.Lerrores.append(CError('Semantico','Error al realizar XOR bit a bit',self.columna,self.linea))
                    return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

                res=str(bizq)
                for i in range(pos):
                    res+='0'

                return primitivo(tipoPrimitivo.Entero,int(res,2),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar Desplazamiento izquierdo bit a bit',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newDespDerBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\> \>',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= PRIMITIVO1 despDer PRIMITIVO2 </td><td> EXP= newDespDerBtb(PRIMITIVO1,PRIMITIVO2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            if der.tipo==tipoPrimitivo.Entero:
                bizq=bin(int(izq.valor)).replace("b","").replace('-','')
                pos=0
                cond=len(bizq)-int(der.valor)
                if cond<=0:
                    res='0'
                else:
                    res=''
                    while pos<cond:
                        res+=str(int(bizq[pos]))
                        pos+=1
                
                return primitivo(tipoPrimitivo.Entero,int(res,2),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar Desplazamiento derecha bit a bit',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)


class newNegacion:
    def __init__(self,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('-',n)
        self.vNodo.hijos.append(v.vNodo)
        self.exp=v
        self.gramm='\n<tr><td>EXP::= - PRIMITIVO  </td><td> EXP= newNegacion(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(v.gramm)

    def getvalor(self,entorno,estat):
        temp=self.exp.getvalor(entorno,estat)
        if temp.tipo==tipoPrimitivo.Entero:
            return primitivo(tipoPrimitivo.Entero,int(int(temp.valor)*-1),self.columna,self.linea,0)
        elif temp.tipo==tipoPrimitivo.Doble:
            return primitivo(tipoPrimitivo.Doble,float(float(temp.valor)*-1),self.columna,self.linea,0)
        
        estat.Lerrores.append(CError('Semantico','Error al realizar Negacion numerica',self.columna,self.linea))
        return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0) 

class newPuntero:
    def __init__(self,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('puntero',n)
        self.vNodo.hijos.append(nodoAST('&',n+1))
        self.vNodo.hijos.append(v.vNodo)
        self.exp=v
        self.tipo=tipoPrimitivo.puntero
        self.gramm='\n<tr><td>EXP::= and PRIMITIVO  </td><td> EXP= newPuntero(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(v.gramm)

    def getvalor(self,entorno,estat):
        if(isinstance(self.exp,id_)):
            temp=entorno.buscar(self.exp.variable,self.columna,self.linea,estat)
            if temp!=None:
                return temp.valor
            else:
                return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)
        else:
            t=self.exp.getvalor(entorno,estat)
            if t.tipo==tipoPrimitivo.Error:
                return t
            return self.exp
            

class newCasteoInt:
    def __init__(self,izq,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Casteo',n)
        self.vNodo.hijos.append(nodoAST('(',n+1))
        self.vNodo.hijos.append(nodoAST('int',n+2))
        self.vNodo.hijos.append(nodoAST('(',n+3))
        self.vNodo.hijos.append(izq.vNodo)
        self.hijoIzq=izq
        self.gramm='\n<tr><td>EXP::= (int) PRIMITIVO  </td><td> EXP= newCasteoInt(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            return primitivo(tipoPrimitivo.Entero,int(float(izq.valor)),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Cadena:
            return primitivo(tipoPrimitivo.Entero,ord(str(izq.valor)[0]),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Arreglo:
            if len(izq.arreglo)==0:
                estat.Lerrores.append(CError('Semantico','Error al realizar casteo a Int',self.columna,self.linea))
                return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

            return newCasteoInt(izq.arreglo[list(izq.arreglo.keys())[0]],self.columna,self.linea,0).getvalor(entorno,estat)
        else:
            estat.Lerrores.append(CError('Semantico','Error al realizar casteo a Int',self.columna,self.linea))
            return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newCasteoFloat:
    def __init__(self,izq,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Casteo',n)
        self.vNodo.hijos.append(nodoAST('(',n+1))
        self.vNodo.hijos.append(nodoAST('float',n+2))
        self.vNodo.hijos.append(nodoAST('(',n+3))
        self.vNodo.hijos.append(izq.vNodo)
        self.hijoIzq=izq
        self.gramm='\n<tr><td>EXP::= (float) PRIMITIVO  </td><td> EXP= newCasteoFloat(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero:
            return primitivo(tipoPrimitivo.Entero,float(izq.valor),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Doble:
            return primitivo(tipoPrimitivo.Entero,float(izq.valor),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Cadena:
            return primitivo(tipoPrimitivo.Entero,float(ord(str(izq.valor)[0])),self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Arreglo:
            if len(izq.arreglo)==0:
                estat.Lerrores.append(CError('Semantico','Error al realizar casteo a Float',self.columna,self.linea))
                return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)
                
            return newCasteoFloat(izq.arreglo[list(izq.arreglo.keys())[0]],self.columna,self.linea,0).getvalor(entorno,estat)
        else:
            estat.Lerrores.append(CError('Semantico','Error al realizar casteo a Float',self.columna,self.linea))
            return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

class newCasteoChar:
    def __init__(self,izq,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Casteo',n)
        self.vNodo.hijos.append(nodoAST('(',n+1))
        self.vNodo.hijos.append(nodoAST('char',n+2))
        self.vNodo.hijos.append(nodoAST('(',n+3))
        self.vNodo.hijos.append(izq.vNodo)
        self.hijoIzq=izq
        self.gramm='\n<tr><td>EXP::= (char) PRIMITIVO  </td><td> EXP= newCasteoChar(PRIMITIVO);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        if izq.tipo==tipoPrimitivo.Entero or izq.tipo==tipoPrimitivo.Doble:
            temp=int(float(izq.valor))
            if(temp>255):
                temp=temp%256            
            return primitivo(tipoPrimitivo.Cadena,chr(int(temp)),self.columna,self.linea,0)        
        elif izq.tipo==tipoPrimitivo.Cadena:
            return primitivo(tipoPrimitivo.Cadena,str(izq.valor)[0],self.columna,self.linea,0)
        elif izq.tipo==tipoPrimitivo.Arreglo:
            if len(izq.arreglo)==0:
                estat.Lerrores.append(CError('Semantico','Error al realizar casteo a Char',self.columna,self.linea))
                return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)
                
            return newCasteoChar(izq.arreglo[list(izq.arreglo.keys())[0]],self.columna,self.linea,0).getvalor(entorno,estat)
        else:
            estat.Lerrores.append(CError('Semantico','Error al realizar casteo a Char',self.columna,self.linea))
            return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

        
class newArreglo:
    def __init__(self,Le,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('{ ARREGLO }',n)
        self.arreglo=Le
        self.tipo=tipoPrimitivo.Arreglo
        self.gramm='\n<tr><td>EXP::= { LEXP } </td><td> EXP= newArreglo(LEXP);  </td></tr>'
        for i in Le:
            self.vNodo.hijos.append(i.vNodo)
            self.gramm+=i.gramm
        
    def getvalor(self,entorno,estat):
        # actualizar valor en caso se imprima arreglo
        return self
                


class newAccesoArr:
    def __init__(self,var,Li,c,l,n):
        self.columna=c
        self.linea=l
        self.indice=Li
        self.variable=var
        self.vNodo=nodoAST('acceso',n)
        self.vNodo.hijos.append(var.vNodo)
        self.vNodo.hijos.append(nodoAST('[Indices]',n+1))
        self.vNodo.hijos[1].append(Li.vNodo)
        self.gramm='\n<tr><td>EXP::= EXP1 [ EXP2 ] </td><td> EXP= newAccesoArr(EXP1,EXP2);  </td></tr>'
        self.gramm+=var.gramm
        self.gramm+=Li.gramm


    def getvalor(self,entorno,estat):
        return


class newAccesoStr:
    def __init__(self,var,Li,c,l,n):
        self.columna=c
        self.linea=l
        self.indice=Li
        self.variable=var
        self.vNodo=nodoAST('PUNTO',n)
        self.vNodo.hijos.append(var.vNodo)
        self.vNodo.hijos.append(nodoAST(str(Li),n+1))
        self.gramm='\n<tr><td>EXP::= EXP1 PUNTO ID </td><td> EXP= newAccesoStr(EXP1,ID);  </td></tr>'
        self.gramm+=var.gramm

    def getvalor(self,entorno,estat):
        return

class newIncremento:
    def __init__(self,var,t,c,l,n):
        self.columna=c
        self.linea=l
        self.variable=var
        self.tinc=t
        self.vNodo=nodoAST('++',n)
        self.vNodo.hijos.append(nodoAST(str(var),n+1))
        self.gramm='\n<tr><td>EXP::= ID ++ </td><td> EXP= newIncremento(ID);  </td></tr>'

    def getvalor(self,entorno,estat):
        return

    
class newDecremento:
    def __init__(self,var,t,c,l,n):
        self.columna=c
        self.linea=l
        self.variable=var
        self.tinc=t
        self.vNodo=nodoAST('--',n)
        self.vNodo.hijos.append(nodoAST(str(var),n+1))
        self.gramm='\n<tr><td>EXP::= ID -- </td><td> EXP= newIncremento(ID);  </td></tr>'

    def getvalor(self,entorno,estat):
        return






