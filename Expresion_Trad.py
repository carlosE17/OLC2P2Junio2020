from TipoTrad import *
from CError import CError
from tkinter import *
import sys

class primitivo:
    def __init__(self,t,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST(v,n)
        self.valor=str(v)
        self.tipo=t
        self.gramm='\n<tr><td>EXP::= '+str(v)+' </td><td> EXP= primitivo('+str(v)+');  </td></tr>'
    def getvalor(self,entorno,estat):
        v=str(self.valor)
        if self.tipo.tipo==tipoPrimitivo.Cadena or self.tipo.tipo==tipoPrimitivo.caracter: v='\"'+v.replace('\\n','\\\\n').replace('\\t','\\\\t')+"\""
        return nodoC3d(v,self.tipo,'',[],[],self.valor)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class id_:
    def __init__(self,d,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST(d,n)
        self.variable=d
        # self.tipo=tipoPrimitivo.variable
        self.gramm='\n<tr><td>EXP::= ID </td><td> EXP= ID;  </td></tr>'
        self.gramm+='\n<tr><td>ID::= '+str(d)+' </td><td> ID= id_('+str(d)+');  </td></tr>'
    def getvalor(self,entorno,estat):
        temp=entorno.buscar(self.variable,self.columna,self.linea,estat)
        if temp!=None:
            return nodoC3d(temp.temporal,temp.tipo,'',[],[],temp.valor)
        else:
            return nodoC3d('0',newtipo(tipoPrimitivo.Error,''),'',[],[],'0')
    
    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newSuma:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('+',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 + EXP2 </td><td> EXP= newSuma(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' + '+der.temporal+';\n'
                v=izq.temporal+' + '+der.temporal
                # print('c:\n'+c+'\n'+'der:\n'+str(der.valor)+'\n''type:\n'+str(type(der.valor))+'\n')
                if der.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor
                elif izq.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=der.temporal
                    v=der.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' + '+der.temporal+';\n'
                v=izq.temporal+' + '+der.temporal
                
                if izq.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=der.temporal
                    v=der.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' + '+t+';\n'
                v=izq.temporal+' + '+der.temporal

                if izq.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                    t2=t
                    v=der.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' + '+der.temporal+';\n'
                v=izq.temporal+' + '+der.temporal
                
                if der.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' + '+der.temporal+';\n'
                v=izq.temporal+' + '+der.temporal

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' + '+t2+';\n'
                v=izq.temporal+' + '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' + '+t+';\n'
                v=izq.temporal+' + '+der.temporal

                if der.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                    t2=t
                    v=izq.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)


        
        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en suma',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'+'+der.temporal+';\n'
        v=izq.temporal+' + '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)



class newResta:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('-',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 - EXP2 </td><td> EXP= newResta(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' - '+der.temporal+';\n'
                v=izq.temporal+' - '+der.temporal
                
                if der.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor
                elif izq.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=der.temporal
                    v=der.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' - '+der.temporal+';\n'
                v=izq.temporal+' - '+der.temporal
                
                if izq.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=der.temporal
                    v=der.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' - '+t+';\n'
                v=izq.temporal+' - '+der.temporal

                if izq.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                    t2=t
                    v=der.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' - '+der.temporal+';\n'
                v=izq.temporal+' - '+der.temporal
                
                if der.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' - '+der.temporal+';\n'
                v=izq.temporal+' - '+der.temporal

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' - '+t2+';\n'
                v=izq.temporal+' - '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' - '+t+';\n'
                v=izq.temporal+' - '+der.temporal

                if der.temporal=='0':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                    t2=t
                    v=izq.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)


        
        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en -',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'-'+der.temporal+';\n'
        v=izq.temporal+' - '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newMultiplicacion:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('*',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 * EXP2 </td><td> EXP= newMultiplicacion(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' * '+der.temporal+';\n'
                v=izq.temporal+' * '+der.temporal
                
                if der.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor
                elif izq.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=der.temporal
                    v=der.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' * '+der.temporal+';\n'
                v=izq.temporal+' * '+der.temporal
                
                if izq.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=der.temporal
                    v=der.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' * '+t+';\n'
                v=izq.temporal+' * '+der.temporal

                if izq.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                    t2=t
                    v=der.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' * '+der.temporal+';\n'
                v=izq.temporal+' * '+der.temporal
                
                if der.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' * '+der.temporal+';\n'
                v=izq.temporal+' * '+der.temporal
                # ----------------------------------------------------------------------------------------------------
                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' * '+t2+';\n'
                v=izq.temporal+' * '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' * '+t+';\n'
                v=izq.temporal+' * '+der.temporal

                if der.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                    t2=t
                    v=der.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)


        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en *',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'*'+der.temporal+';\n'
        v=izq.temporal+' * '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newDivision:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('/',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 / EXP2 </td><td> EXP= newDivision(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' / '+der.temporal+';\n'
                v=izq.temporal+' / '+der.temporal
                
                if der.temporal=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'
                    t=izq.temporal
                    v=izq.valor
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' / '+der.temporal+';\n'
                v=izq.temporal+' / '+der.temporal
                
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' / '+t+';\n'
                v=izq.temporal+' / '+der.temporal

                

                return nodoC3d(t2,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' / '+der.temporal+';\n'
                v=izq.temporal+' / '+der.temporal
                


                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' / '+der.temporal+';\n'
                v=izq.temporal+' / '+der.temporal
                # ----------------------------------------------------------------------------------------------------
                return nodoC3d(t,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' / '+t2+';\n'
                v=izq.temporal+' / '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' / '+t+';\n'
                v=izq.temporal+' / '+der.temporal

                if der.valor=='1':
                    c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                    t2=t
                    v=izq.valor

                return nodoC3d(t2,newtipo(tipoPrimitivo.Doble,''),c,[],[],v)


        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en /',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'/'+der.temporal+';\n'
        v=izq.temporal+' / '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newModulo:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('/',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 % _Exp2 </td><td> EXP= newModulo(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' % '+der.temporal+';\n'
                v=izq.temporal+' % '+der.temporal
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' % '+der.temporal+';\n'
                v=izq.temporal+' % '+der.temporal


                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' % '+t+';\n'
                v=izq.temporal+' % '+der.temporal


                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' % '+der.temporal+';\n'
                v=izq.temporal+' % '+der.temporal
                
 

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' % '+der.temporal+';\n'
                v=izq.temporal+' % '+der.temporal
                # ----------------------------------------------------------------------------------------------------
                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' % '+t2+';\n'
                v=izq.temporal+' % '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' % '+t+';\n'
                v=izq.temporal+' % '+der.temporal


                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)


        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en %',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'%'+der.temporal+';\n'
        v=izq.temporal+' % '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)


    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newAnd:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('&&',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= exp and and exp2 </td><td> EXP= newAnd(exp,exp2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' && '+der.temporal+';\n'
                v=izq.temporal+' && '+der.temporal

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' && '+der.temporal+';\n'
                v=izq.temporal+' && '+der.temporal
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' && '+t+';\n'
                v=izq.temporal+' && '+der.temporal

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' && '+der.temporal+';\n'
                v=izq.temporal+' && '+der.temporal
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' && '+der.temporal+';\n'
                v=izq.temporal+' && '+der.temporal
                # ----------------------------------------------------------------------------------------------------
                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' && '+t2+';\n'
                v=izq.temporal+' && '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' && '+t+';\n'
                v=izq.temporal+' && '+der.temporal

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en &&',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'&&'+der.temporal+';\n'
        v=izq.temporal+' && '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)


    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newOr:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('||',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 or or EXP2 </td><td> EXP= newOr(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        der=self.hijoDer.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Entero:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' || '+der.temporal+';\n'
                v=izq.temporal+' || '+der.temporal

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' || '+der.temporal+';\n'
                v=izq.temporal+' || '+der.temporal
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.caracter:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = '+izq.temporal+' || '+t+';\n'
                v=izq.temporal+' || '+der.temporal

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.Doble:
            if der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' || '+der.temporal+';\n'
                v=izq.temporal+' || '+der.temporal
                

                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Doble:
                t=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = '+izq.temporal+' || '+der.temporal+';\n'
                v=izq.temporal+' || '+der.temporal
                # ----------------------------------------------------------------------------------------------------
                return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        elif izq.tipo.tipo==tipoPrimitivo.caracter:
            if der.tipo.tipo==tipoPrimitivo.caracter:

                t=estat.newTemp()
                t2=estat.newTemp()
                t3=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+der.temporal+';\n'
                c+=t2+' = (int) '+izq.temporal+';\n'+t3+' = '+t+' || '+t2+';\n'
                v=izq.temporal+' || '+der.temporal


                return nodoC3d(t3,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

            elif der.tipo.tipo==tipoPrimitivo.Entero:
                t=estat.newTemp()
                t2=estat.newTemp()
                c=izq.c3d+'\n'+der.c3d+'\n'+t+' = (int) '+izq.temporal+';\n'
                c+=t2+' = '+der.temporal+' || '+t+';\n'
                v=izq.temporal+' || '+der.temporal

                return nodoC3d(t2,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

        if der.tipo.tipo == tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:        
            estat.Lerrores.append(CError('Semantico','Error en ||',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+'='+izq.temporal+'||'+der.temporal+';\n'
        v=izq.temporal+' || '+der.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)
            

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newNot:
    def __init__(self,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Not',n)
        self.vNodo.hijos.append(nodoAST('!',n+1))
        self.vNodo.hijos.append(der.vNodo)
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= !EXP </td><td> EXP= newNot(EXP);  </td></tr>'
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en !',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=der.c3d+'\n'+t+' = !'+der.temporal+';\n'
        v='!'+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newEqual:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('==',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 == EXP2 </td><td> EXP= newEqual(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en ==',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'=='+der.temporal+';\n'
        v=izq.temporal+'=='+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)
     
class newNotEqual:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('!=',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 != EXP2 </td><td> EXP= newNotEqual(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en !=',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'!='+der.temporal+';\n'
        v=izq.temporal+'!='+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newMenorq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\<',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 menorQue EXP2 </td><td> EXP= newMenorq(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en menor que',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'<'+der.temporal+';\n'
        v=izq.temporal+'<'+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newMayorq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\>',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 mayorQue EXP2 </td><td> EXP= newMayorq(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en mayor que',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'>'+der.temporal+';\n'
        v=izq.temporal+'>'+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newMenorIgualq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\<=',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 menorIgualQue EXP2 </td><td> EXP= newMenorIgualq(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en Menor Igual',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'<='+der.temporal+';\n'
        v=izq.temporal+'<='+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newMayorIgualq:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\>=',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 mayorIgualQue EXP2 </td><td> EXP= newMayorIgualq(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en Mayor Igual',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'>='+der.temporal+';\n'
        v=izq.temporal+'>='+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newAndBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('&',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 and EXP2 </td><td> EXP= newAndBtb(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en &',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'&'+der.temporal+';\n'
        v=izq.temporal+'&'+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newOrBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('|',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 or EXP2 </td><td> EXP= newOrBtb(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en |',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+' | '+der.temporal+';\n'
        v=izq.temporal+' | '+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newXorBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('^',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 ^ EXP2 </td><td> EXP= newXorBtb(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en ^',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'^'+der.temporal+';\n'
        v=izq.temporal+'^'+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newNotBtb:
    def __init__(self,izq,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('~',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.hijoIzq=izq
        self.gramm='\n<tr><td>EXP::= ~ EXP1 </td><td> EXP= newNotBtb(EXP1);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        izq=self.hijoIzq.getvalor(entorno,estat)
        if izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en ~ ',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+t+' = ~'+izq.temporal+';\n'
        v='~'+izq.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newDespIzqBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\< \<',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 despIzq EXP2 </td><td> EXP= newDespIzqBtb(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en Desplazo izq',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'<<'+der.temporal+';\n'
        v=izq.temporal+' << '+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

class newDespDerBtb:
    def __init__(self,izq,der,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('\> \>',n)
        self.vNodo.hijos.append(izq.vNodo)
        self.vNodo.hijos.append(der.vNodo)
        self.hijoIzq=izq
        self.hijoDer=der
        self.gramm='\n<tr><td>EXP::= EXP1 despDer EXP2 </td><td> EXP= newDespDerBtb(EXP1,EXP2);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)
        self.gramm+='\n'+str(der.gramm)

    
    def getvalor(self,entorno,estat):
        der=self.hijoDer.getvalor(entorno,estat)
        izq=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en Desplazamiento derecho',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=izq.c3d+'\n'+der.c3d+'\n'+t+' ='+izq.temporal+'>>'+der.temporal+';\n'
        v=izq.temporal+'>>'+der.temporal
        return nodoC3d(t,newtipo(tipoPrimitivo.Entero,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newNegacion:
    def __init__(self,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('-',n)
        self.vNodo.hijos.append(v.vNodo)
        self.exp=v
        self.gramm='\n<tr><td>EXP::= - EXP  </td><td> EXP= newNegacion(EXP);  </td></tr>'
        self.gramm+='\n'+str(v.gramm)

    
    def getvalor(self,entorno,estat):
        der=self.exp.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en -exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=der.c3d+'\n'+t+' = -'+der.temporal+';\n'
        v='-'+der.temporal
        return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newPuntero:
    def __init__(self,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('puntero',n)
        self.vNodo.hijos.append(nodoAST('&',n+1))
        self.vNodo.hijos.append(v.vNodo)
        self.exp=v
        self.tipo=tipoPrimitivo.puntero
        self.gramm='\n<tr><td>EXP::= and EXP1  </td><td> EXP= newPuntero(EXP1);  </td></tr>'
        self.gramm+='\n'+str(v.gramm)


    def getvalor(self,entorno,estat):
        der=self.exp.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en &exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=der.c3d+'\n'+t+' = &'+der.temporal+';\n'
        v='-'+der.temporal
        return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


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
        self.gramm='\n<tr><td>EXP::= (int) EXP1  </td><td> EXP= newCasteoInt(EXP1);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en (int)exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=der.c3d+'\n'+t+' = (int)'+der.temporal+';\n'
        v='(int)'+der.temporal
        return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

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
        self.gramm='\n<tr><td>EXP::= (float) EXP  </td><td> EXP= newCasteoFloat(EXP);  </td></tr>'
        self.gramm+='\n'+str(izq.gramm)

    def getvalor(self,entorno,estat):
        der=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en (float)exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=der.c3d+'\n'+t+' = (float)'+der.temporal+';\n'
        v='(float)'+der.temporal
        return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

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
        der=self.hijoIzq.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en (char)exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        t=estat.newTemp()
        c=der.c3d+'\n'+t+' = (char)'+der.temporal+';\n'
        v='(char)'+der.temporal
        return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

        
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
        t=estat.newTemp()
        c='\n'+t+'= array();\n'
        v='Array()'
        n=0
        prof=0
        for i in self.arreglo:
            e=i.getvalor(entorno,estat)
            if e.tipo.tipo==tipoPrimitivo.Error:
                estat.Lerrores.append(CError('Semantico','Error al crear el arreglo',self.columna,self.linea))
                return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
            c+=e.c3d+'\n'+t+'['+str(n)+']'+'='+e.temporal+';\n'
            if n==0:
                prof=e.profundidad
            n+=1 
        f=nodoC3d(t,newtipo(tipoPrimitivo.Arreglo,''),c,[],[],v)
        if len(self.arreglo)>0:
            f.profundidad+=prof
        return f

    
    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)
                


class newAccesoArr:
    def __init__(self,var,Li,c,l,n):
        self.columna=c
        self.linea=l
        self.indice=Li
        self.variable=var
        self.vNodo=nodoAST('acceso',n)
        self.vNodo.hijos.append(var.vNodo)
        self.vNodo.hijos.append(nodoAST('[Indices]',n+1))
        self.vNodo.hijos[1].hijos.append(Li.vNodo)
        self.gramm='\n<tr><td>EXP::= EXP1 [ EXP2 ] </td><td> EXP= newAccesoArr(EXP1,EXP2);  </td></tr>'
        self.gramm+=var.gramm
        self.gramm+=Li.gramm


    def getvalor(self,entorno,estat):
        izq=self.variable.getvalor(entorno,estat)
        i=self.indice.getvalor(entorno,estat)
        if i.tipo.tipo==tipoPrimitivo.Error or izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error al realizar acceso',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
        
        t=izq.temporal+'['+i.temporal+']'
        c=izq.c3d+'\n'+i.c3d+'\n'
        v=t
        return nodoC3d(t,newtipo(tipoPrimitivo.acceso,''),c,[],[],v)
        

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)

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
        izq=self.variable.getvalor(entorno,estat)
        i=self.indice
        if izq.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error al realizar acceso',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
        
        t=izq.temporal+'[\''+i+'\']'
        c=izq.c3d+'\n'
        v=t
        return nodoC3d(t,newtipo(tipoPrimitivo.acceso,''),c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)



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
        der=self.variable.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en ++exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        if self.tinc==1:
            c=der.c3d+'\n'+der.temporal+' ='+der.temporal+'+1;\n'
            v='++'+der.temporal
            return nodoC3d(der.temporal,der.tipo,c,[],[],v)
        else:
            t=estat.newTemp()
            c=der.c3d+'\n'+t+' ='+der.temporal+';\n'
            c+=der.temporal+' ='+der.temporal+'+1;\n'
            v='++'+der.temporal
            return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)
    
class newDecremento:
    def __init__(self,var,t,c,l,n):
        self.columna=c
        self.linea=l
        self.variable=var
        self.tdec=t
        self.vNodo=nodoAST('--',n)
        self.vNodo.hijos.append(nodoAST(str(var),n+1))
        self.gramm='\n<tr><td>EXP::= ID -- </td><td> EXP= newDecremento(ID);  </td></tr>'

    def getvalor(self,entorno,estat):
        der=self.variable.getvalor(entorno,estat)
        if der.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error en --exp',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')            
        if self.tdec==1:
            c=der.c3d+'\n'+der.temporal+' ='+der.temporal+'-1;\n'
            v='--'+der.temporal
            return nodoC3d(der.temporal,der.tipo,c,[],[],v)
        else:
            t=estat.newTemp()
            c=der.c3d+'\n'+t+' ='+der.temporal+';\n'
            c+=der.temporal+' ='+der.temporal+'-1;\n'
            v='--'+der.temporal
            return nodoC3d(t,der.tipo,c,[],[],v)

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)


class newTernaria:
    def __init__(self,v1,v2,v3,c,l,n):
        self.columna=c
        self.linea=l
        self.exp1=v1
        self.exp2=v2
        self.exp3=v3
        self.vNodo=nodoAST('TERNARIA',n)
        self.vNodo.hijos.append(v1.vNodo)
        self.vNodo.hijos.append(v2.vNodo)
        self.vNodo.hijos.append(v3.vNodo)
        self.gramm='\n<tr><td>EXP::= EXP1 ? EXP2 : EXP3  </td><td> EXP= newTernaria(EXP1,EXP2,EXP3);  </td></tr>'

    def getvalor(self,entorno,estat):
        e1=self.exp1.getvalor(entorno,estat)
        e2=self.exp2.getvalor(entorno,estat)
        e3=self.exp3.getvalor(entorno,estat)

        if e1.tipo.tipo==tipoPrimitivo.Error or e2.tipo.tipo==tipoPrimitivo.Error or e3.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','Error al realizar acceso',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')         

        t=estat.newTemp()
        l1=estat.newetiquetaL()
        c=e1.c3d+'\n'+e2.c3d+'\n'+e3.c3d
        c+='\n'+t+'='+e2.temporal+';'
        c+='\nif('+e1.temporal+') goto '+l1+';'
        c+='\n'+t+'='+e3.temporal+';'
        c+='\n'+l1+':\n'

        v=e1.temporal+'?'+e2.temporal+':'+e3.temporal

        return nodoC3d(t,newtipo(tipoPrimitivo.acceso,''),c,[],[],v)
        
        

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)





