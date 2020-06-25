from Tipo import *
from CError import CError
from Simbolo import Simbolo
from tkinter import *
from Expresion import newPuntero,newArreglo,primitivo
class newEtiqueta:
    def __init__(self,v,c,l,n):
        self.tipo=tipoInstruccion.etiqueta
        self.label_=v
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('LABEL',n)
        self.vNodo.hijos.append(nodoAST(v,n+1))
        self.gramm='<tr><td>INSTRUCCION::= LABEL : </td><td> INSTRUCCION=newEtiqueta(LABEL); </td></tr>'
        self.gramm+='\n<tr><td>LABEL::= '+str(v)+' : </td><td> LABEL='+str(v)+';  </td></tr>'
    
    def ejecutar(self,entorno,estat):
        return

class newSalto:
    def __init__(self,v,c,l,n):
        self.tipo=tipoInstruccion.salto
        self.label_=v
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('SALTO',n)
        self.vNodo.hijos.append(nodoAST('GOTO',n+1))
        self.vNodo.hijos.append(nodoAST(v,n+2))
        self.gramm='<tr><td>INSTRUCCION::= GOTO LABEL ; </td><td> INSTRUCCION=newSalto(LABEL); </td></tr>'
        self.gramm+='\n<tr><td>LABEL::= '+str(v)+' : </td><td> LABEL='+str(v)+';  </td></tr>'

    def ejecutar(self,entorno,estat):
        if self.label_ in entorno.etiquetas:
            estat.i=int(entorno.etiquetas[self.label_])
        else:
            estat.Lerrores.append(CError('Semantico','no se encontro la etiqueta \''+str(self.label_)+'\'',self.columna,self.linea))

class newAsignacion:
    def __init__(self,id,Li,v,c,l,n):
        self.id=id
        self.indices=Li
        self.valor=v
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('ASIGNACION',n)
        self.vNodo.hijos.append(nodoAST(self.id,n+1))
        self.vNodo.hijos.append(nodoAST('Indices',n+2))
        self.gramm='<tr><td>INSTRUCCION::= VARIABLE INDICES = EXP ; </td><td> INSTRUCCION=newAsignacion(VARIABLE,INDICES,EXP); </td></tr>'
        self.gramm+='\n<tr><td>VARIABLE::= '+str(id)+' : </td><td> VARIABLE='+str(id)+';  </td></tr>'
        self.gramm+='\n<tr><td>INDICES::= INDICES1 [ PRIMITIVO ] : </td><td> INDICES=INDICES1; INDICES.append(PRIMITIVO);  </td></tr>'
        self.gramm+='\n<tr><td>INDICES::= [PRIMITIVO] : </td><td> INDICES=[]; INDICES.append(PRIMITIVO);  </td></tr>'
        for i in Li:
            self.vNodo.hijos[1].hijos.append(i.vNodo)
            self.gramm+=str(i.gramm)
        self.vNodo.hijos.append(nodoAST('=',n+3))
        self.vNodo.hijos.append(v.vNodo)
        self.gramm+='\n<tr><td>EXP::= PRIMITIVO : </td><td> EXP= PRIMITIVO;  </td></tr>'
        self.gramm+=str(v.gramm)
        

    def getClave(self,v,entorno,estat):
        temp=v.getvalor(entorno,estat)
        if temp.tipo==tipoPrimitivo.Entero: return int(temp.valor)
        elif temp.tipo==tipoPrimitivo.Cadena: return str(temp.valor)
        elif temp.tipo==tipoPrimitivo.Doble: return float(temp.valor)
        else:
            estat.Lerrores.append(CError('Semantico','Se esperaba un Int, Float, o String como indice de acceso al struct/Arreglo',self.columna,self.linea))
            return primitivo(tipoPrimitivo.Error,'@error@',self.columna,self.linea,0)

    def ejecutar(self,entorno,estat):
        resultado=self.valor.getvalor(entorno,estat)
        if resultado.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','no se puede asignar error a la variable \''+str(self.id)+'\'',self.columna,self.linea))
            return
        temp=Simbolo(resultado.tipo,resultado)
        if isinstance(self.valor,newPuntero):
            temp=Simbolo(self.valor.tipo,self.valor)
        # -----------------------------------------------------------------
        if len(self.indices)==0:
            entorno.actualizar(self.id,temp)
        else:
            tmp=newArreglo(self.columna,self.linea,0)
            if self.id in entorno.tabla:
                tmp=entorno.buscar(self.id,self.columna,self.linea,estat).valor.getvalor(entorno,estat)
            else:
                entorno.actualizar(self.id,Simbolo(tmp.tipo,tmp))
                tmp=entorno.buscar(self.id,self.columna,self.linea,estat).valor.getvalor(entorno,estat)

            claves=[]
            for i in self.indices:
                k=self.getClave(i,entorno,estat)
                if isinstance(k,primitivo):
                    return
                claves.append(k)
            i=0
            while i<len(claves)-1:
                if tmp.tipo==tipoPrimitivo.Arreglo:
                    if claves[i] in tmp.arreglo:
                        tmp=tmp.arreglo[claves[i]].getvalor(entorno,estat)
                    else:
                        tmp.setPos(self.indices[i],newArreglo(self.columna,self.linea,0),entorno,estat)
                        tmp=tmp.arreglo[claves[i]]
                elif tmp.tipo==tipoPrimitivo.Cadena:
                    if isinstance(claves[i],int):
                        if claves[i]<len(tmp.valor):
                            tmp=primitivo(tipoPrimitivo.Cadena,tmp.valor[claves[i]],self.columna,self.linea,0)
                        else:
                            estat.Lerrores.append(CError('Semantico','Indice fuera de rango en String',self.columna,self.linea))
                            return
                    else:
                        estat.Lerrores.append(CError('Semantico','String solo acepta indices tipo Int',self.columna,self.linea))
                        return
                i+=1
            if tmp.tipo==tipoPrimitivo.Arreglo:
                tmp.setPos(self.indices[i],temp.valor,entorno,estat)
            elif tmp.tipo==tipoPrimitivo.Cadena:
                if isinstance(claves[i],int):
                    if claves[i]<len(tmp.valor):
                        t=list(tmp.valor)
                        t[claves[i]]=str(temp.valor.getvalor(entorno,estat).valor)
                        tmp.valor=''.join(t)
                    else:
                        t=list(tmp.valor)
                        t.append(str(temp.valor.getvalor(entorno,estat).valor))
                        tmp.valor=''.join(t)
                else:
                    estat.Lerrores.append(CError('Semantico','String solo acepta indices tipo Int',self.columna,self.linea))
                    return
            else:
                estat.Lerrores.append(CError('Semantico','Se esperaba string o Array',self.columna,self.linea))
                return

class newUnset:
    def __init__(self,id,c,l,n):
        self.id=id
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('UNSET',n)
        self.vNodo.hijos.append(nodoAST('unset',n+1))
        self.vNodo.hijos.append(nodoAST('(',n+2))
        self.vNodo.hijos.append(self.id.vNodo)
        self.vNodo.hijos.append(nodoAST(')',n+3))
        self.gramm='<tr><td>INSTRUCCION::= UNSET(VARIABLE) ; </td><td> INSTRUCCION=newUnset(VARIABLE); </td></tr>'
        self.gramm+='\n<tr><td>VARIABLE::= '+str(id.vNodo.vNodo)+' : </td><td> VARIABLE='+str(id.vNodo.vNodo)+';  </td></tr>'


    def ejecutar(self,entorno,estat):
        if self.id.tipo==tipoPrimitivo.variable:
            d=self.id.variable
            if(d in entorno.tabla):
                entorno.tabla.pop(d)
            else:
                estat.Lerrores.append(CError('Semantico','Error al aplicar unset(), No existe la variable \''+str(d)+'\'',self.columna,self.linea))
            return
        else:
            print('aun no hay arreglos xd')

class newImprimir:
    def __init__(self,v,c,l,n):
        self.v=v
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('PRINT',n)
        self.vNodo.hijos.append(nodoAST('print',n+1))
        self.vNodo.hijos.append(nodoAST('(',n+2))
        self.vNodo.hijos.append(v.vNodo)
        self.vNodo.hijos.append(nodoAST(')',n+3))
        self.gramm='<tr><td>INSTRUCCION::= PRINT (PRIMITIVO); </td><td> INSTRUCCION=newImprimir(PRIMITIVO); </td></tr>'
        self.gramm+=v.gramm

    def ejecutar(self,entorno,estat):
        temp=self.v.getvalor(entorno,estat)
        if temp.tipo!=tipoPrimitivo.Error and temp.tipo!=tipoPrimitivo.Arreglo:
            estat.consola.insert(INSERT, str(temp.valor).replace('\\n','\n').replace('\\t','\t')+"")
        else:
           estat.Lerrores.append(CError('Semantico','No se puede imprimir un error ni Arreglo',self.columna,self.linea))
 
class newSalir:
    def __init__(self,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('exit',n)
        self.gramm='<tr><td>INSTRUCCION::= EXIT ; </td><td> INSTRUCCION=newSalir(); </td></tr>'

    def ejecutar(self,entorno,estat):
        estat.i=estat.e

class newIF:
    def __init__(self,cond,label,c,l,n):
        self.columna=c
        self.linea=l
        self.condicion=cond
        self.label=label
        self.vNodo=nodoAST('IF',n)
        self.vNodo.hijos.append(nodoAST('if',n+1))
        self.vNodo.hijos.append(nodoAST('(',n+2))
        self.vNodo.hijos.append(cond.vNodo)
        self.vNodo.hijos.append(nodoAST(')',n+3))
        self.vNodo.hijos.append(nodoAST('goto',n+4))
        self.vNodo.hijos.append(nodoAST(label,n+5))
        self.gramm='<tr><td>INSTRUCCION::= IF(EXP) GOTO LABEL ; </td><td> INSTRUCCION=newIF(EXP,LABEL); </td></tr>'
        self.gramm+='\n<tr><td>LABEL::= '+str(label)+' : </td><td> LABEL='+str(label)+';  </td></tr>'
        self.gramm+='\n<tr><td>EXP::= PRIMITIVO : </td><td> EXP= PRIMITIVO;  </td></tr>'
        self.gramm+=str(cond.gramm)
    def ejecutar(self,entorno,estat):
        temp=self.condicion.getvalor(entorno,estat)
        if temp.tipo==tipoPrimitivo.Entero:
            valtemp=int(temp.valor)
            if valtemp!=0:
                if self.label in entorno.etiquetas:
                    estat.i=int(entorno.etiquetas[self.label])
                else:
                    estat.Lerrores.append(CError('Semantico','no se encontro la etiqueta \''+str(self.label)+'\'',self.columna,self.linea))
            else:
                return
        else:
            estat.Lerrores.append(CError('Semantico','Se esperaba expresion de tipo entero en el IF, pero se encontro tipo \''+temp.tipo.name+'\'',self.columna,self.linea))




        

