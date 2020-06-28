from TipoTrad import *
from CError import CError
from Simbolo_Trad import Simbolo
from tkinter import *
from Entorno_Trad import Entorno


class newDecStruct:
    def __init__(self,name,Latrib,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('STRUCT',n)
        self.nombre=name
        self.propiedades=Latrib
        self.vNodo.hijos.append(nodoAST(str(name),n+1))
        self.gramm='<tr><td>GLOBALES::= STRUCT ID { INSTRUCT }: </td><td> GLOBALES=newDecStruct(ID,INSTRUCT); </td></tr>'
        self.gramm+='\n<tr><td>ID::= '+str(name)+' : </td><td> ID='+str(name)+';  </td></tr>'
        for i in Latrib:
            self.vNodo.hijos.append(i.vNodo)
            self.gramm+=i.gramm
    
    def ejecutar(self,entorno,estat):
        estat.structs[self.nombre]=self.propiedades
        return nodoC3d('',newtipo(tipoPrimitivo.structura,''),'',[],[],self.nombre)

class newDecParam:
    def __init__(self,t,name,arr,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('PARAMETRO',n)
        self.nombre=name
        self.tipo=t
        self.dim=arr
        self.vNodo.hijos.append(nodoAST(str(t.tipo.name),n+1))
        self.vNodo.hijos.append(nodoAST(str(name),n+2))
        if arr!='':self.vNodo.hijos.append(arr.vNodo)
        self.gramm='<tr><td>PARAMETRO::= TIPO ID [] </td><td> PARAMETRO=newDecParam(TIPO,ID); </td></tr>'
        self.gramm+='\n<tr><td>ID::= '+str(name)+'  </td><td> ID='+str(name)+';  </td></tr>'
        self.gramm+='\n<tr><td>TIPO::= '+str(t.tipo.name)+'  </td><td> TIPO='+str(t.tipo.name)+';  </td></tr>'
    
    def ejecutar(self,entorno,estat):
        return

class newDecFuncion:
    def __init__(self,t,no,p,Linst,c,l,n):
        self.tipo=t
        self.nombre=no
        self.parametros=p
        self.Linstrucciones=Linst
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('FUNCION',n)
        self.vNodo.hijos.append(nodoAST(str(t.tipo.name),n+1))
        self.vNodo.hijos.append(nodoAST(str(no),n+2))
        self.vNodo.hijos.append(nodoAST('( PARAMETROS )',n+3))
        self.gramm='<tr><td>GLOBALES::= TIPO ID (PARAMETROS) { INSTRUCCIONES } </td><td> GLOBALES=newDecFuncion(TIPO,ID,PARAMETROS,INSTRUCCIONES); </td></tr>'
        self.gramm+='\n<tr><td>ID::= '+str(no)+'  </td><td> ID='+str(no)+';  </td></tr>'
        self.gramm+='\n<tr><td>TIPO::= '+str(t.tipo.name)+'  </td><td> TIPO='+str(t.tipo.name)+';  </td></tr>'
        for i in p:
            self.vNodo.hijos[2].hijos.append(i.vNodo)
            self.gramm+=i.gramm
        self.vNodo.hijos.append(nodoAST('{ INSTRUCCIONES }',n+4))
        for i in Linst:
            self.vNodo.hijos[3].hijos.append(i.vNodo)
    
    def ejecutar(self,entorno,estat):
        return nodoC3d('',self.tipo,'',[],[],'')

class newDecla:
    def __init__(self,name,dim,e,c,l,n):
        self.nombre=name
        self.dimensiones=dim
        self.exp=e
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Decla',n)
        self.vNodo.hijos.append(nodoAST(str(name),n+1))
        self.vNodo.hijos.append(nodoAST('DIMENSIONES',n+2))
        self.gramm='<tr><td>DECLA::= ID POSC POSEXP </td><td> PARAMETRO=newDecla(ID, POSC, POSEXP); </td></tr>'
        self.gramm+='\n<tr><td>ID::= '+str(name)+'  </td><td> ID='+str(name)+';  </td></tr>'

        if e!='':
            self.vNodo.hijos.append(nodoAST('=',n+3))
            self.vNodo.hijos.append(e.vNodo)
            self.gramm+=e.gramm
        if dim!='':
            self.gramm+='\n<tr><td>INDICES::= INDICES1 [ EXP ] : </td><td> INDICES=INDICES1; INDICES.append(EXP);  </td></tr>'
            self.gramm+='\n<tr><td>INDICES::= [EXP] : </td><td> INDICES=[]; INDICES.append(EXP);  </td></tr>'    
            for i in dim:
                self.vNodo.hijos[1].hijos.append(i.vNodo)
    
    def ejecutar(self,entorno,estat):
        return
        
class newDeclaracion:
    def __init__(self,t,Ldec,c,l,n):
        self.columna=c
        self.linea=l
        self.tipo=t
        self.vNodo=nodoAST('DECLARACION',n)
        self.gramm='<tr><td>DECLARACION::= TIPO LDECLA ;  </td><td> PARAMETRO=newDeclaracion(TIPO,LDECLA); </td></tr>'
        self.gramm+='<tr><td>LDECLA::= LDECLA DECLA ;  </td><td> LDECLA.append(DECLA); </td></tr>'
        self.declaraciones=Ldec
        for i in Ldec:
            self.vNodo.hijos.append(i.vNodo)
            self.gramm+=i.gramm

    def ejecutar(self,entorno,estat):

        predVal='0'
        c=''
        if self.tipo.tipo==tipoPrimitivo.Doble: predVal='0.0'
        elif self.tipo.tipo==tipoPrimitivo.caracter: predVal='\' \''
        elif self.tipo.tipo==tipoPrimitivo.structura:
            if self.tipo.v in estat.structs:
                predVal='array()'
            else:
                estat.Lerrores.append(CError('Semantico','Error no se ha declarado el struct\''+self.tipo.v+'\'',self.columna,self.linea))
                return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
        elif self.tipo.tipo==tipoPrimitivo.void:
            estat.Lerrores.append(CError('Semantico','Error no se pueden declarar variables tipo void',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')

        for i in self.declaraciones:
            v=predVal
            var=i.nombre
            t=estat.newTemp()
            tip=self.tipo
            if i.dimensiones!='':v='array()'
            if i.exp!='':
                temp=i.exp.getvalor(entorno,estat)
                if temp.tipo.tipo==tipoPrimitivo.Error:
                    estat.Lerrores.append(CError('Semantico','Error no se puede asignar un error',self.columna,self.linea))
                    continue

                v=temp.temporal
                c+=temp.c3d+'\n'
                tip=temp.tipo
            c+=t+' = '+v+';\n'
            entorno.insertar(var,Simbolo(tip,v,t,self.linea),self.columna,self.linea,estat)


        return nodoC3d('',self.tipo,c,[],[],'')



# ------------------------------------------------------------------------------------------------------------------------------
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
        return nodoC3d('',self.tipo,self.label_+':\n',[],[],'')

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
       return nodoC3d('',self.tipo,'goto '+self.label_+';\n',[],[],'')

class newAsignacion:
    def __init__(self,id,Li,v,tig,c,l,n):
        self.id=id
        self.accesos=Li
        self.valor=v
        self.columna=c
        self.linea=l
        self.operand=tig
        self.vNodo=nodoAST('ASIGNACION',n)
        self.vNodo.hijos.append(nodoAST(self.id,n+1))
        self.vNodo.hijos.append(nodoAST('accesos',n+2))
        self.gramm='<tr><td>INSTRUCCION::= VARIABLE INDICES = EXP ; </td><td> INSTRUCCION=newAsignacion(VARIABLE,INDICES,EXP); </td></tr>'
        self.gramm+='\n<tr><td>VARIABLE::= '+str(id)+' : </td><td> VARIABLE='+str(id)+';  </td></tr>'
        self.gramm+='\n<tr><td>INDICES::= INDICES1 [ EXP ] : </td><td> INDICES=INDICES1; INDICES.append(EXP);  </td></tr>'
        self.gramm+='\n<tr><td>INDICES::= [EXP] : </td><td> INDICES=[]; INDICES.append(EXP);  </td></tr>'
        for i in Li:
            if not isinstance(i,str):
                self.vNodo.hijos[1].hijos.append(i.vNodo)
                self.gramm+=str(i.gramm)
        self.vNodo.hijos.append(nodoAST(str('='),n+3))
        self.vNodo.hijos.append(v.vNodo)
        self.gramm+=str(v.gramm)

    def ejecutar(self,entorno,estat):
        t=entorno.buscar(self.id,self.columna,self.linea,estat)
        if t==None:
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
        tempo=t.temporal
        c=''
        for i in self.accesos:
            if isinstance(i,str):
                tempo+='[\''+i+'\']'
            else:
                tmp=i.getvalor(entorno,estat)
                if tmp.tipo.tipo!=tipoPrimitivo.Error:
                    tempo+='['+tmp.temporal+']'
                    c+=tmp.c3d+'\n'
        resultado=self.valor.getvalor(entorno,estat)
        if resultado.tipo.tipo==tipoPrimitivo.Error:
            estat.Lerrores.append(CError('Semantico','No se puede asignar un error',self.columna,self.linea))
            return nodoC3d('',newtipo(tipoPrimitivo.Error,''),'',[],[],'')
        c+=resultado.c3d+'\n'
        if self.operand=='=': c+=tempo+' = '+resultado.temporal+';\n'
        elif self.operand=='+=': c+=tempo+' = '+tempo+' + '+resultado.temporal+';\n'
        elif self.operand=='-=': c+=tempo+' = '+tempo+' - '+resultado.temporal+';\n'
        elif self.operand=='*=': c+=tempo+' = '+tempo+' * '+resultado.temporal+';\n'
        elif self.operand=='/=': c+=tempo+' = '+tempo+' / '+resultado.temporal+';\n'
        elif self.operand=='%=': c+=tempo+' = '+tempo+' % '+resultado.temporal+';\n'
        elif self.operand=='<<=': c+=tempo+' = '+tempo+' << '+resultado.temporal+';\n'
        elif self.operand=='>>=': c+=tempo+' = '+tempo+' >> '+resultado.temporal+';\n'
        elif self.operand=='&=': c+=tempo+' = '+tempo+' & '+resultado.temporal+';\n'
        elif self.operand=='|=': c+=tempo+' = '+tempo+' | '+resultado.temporal+';\n'
        elif self.operand=='^=': c+=tempo+' = '+tempo+' ^ '+resultado.temporal+';\n'



        return nodoC3d('',resultado.tipo,c,[],[],'')

class newLlamadaInstr:
    def __init__(self,id,p,c,l,n):
        self.columna=c
        self.linea=l
        self.nombre=id
        self.parametros=p
        self.vNodo=nodoAST('Llamada',n)
        self.vNodo.hijos.append(nodoAST(str(id),n+1))
        self.vNodo.hijos.append(nodoAST('parametros',n+2))
        self.gramm='<tr><td>EXP::= ID (PARAMETROS)  </td><td> EXP=newLlamadaInstr(ID,PARAMETRO); </td></tr>'
        for i in p:
            self.vNodo.hijos[1].hijos.append(i.vNodo)
        
    def getvalor(self,entorno,estat):
        return self

    def ejecutar(self,entorno,estat):
        return self.getvalor(entorno,estat)




class newIF:
    def __init__(self,Lsubif,els_,c,l,n):
        self.columna=c
        self.linea=l
        self.subifs=Lsubif
        self.else_=els_
        self.vNodo=nodoAST('IF',n)
        self.gramm='<tr><td>INSTRUCCION::=LSUBIF POSELSE  </td><td> INSTRUCCION=newIF(LSUBIF, POSELSE); </td></tr>'
        for i in Lsubif:
            self.vNodo.hijos.append(i.vNodo)
            self.gramm+=i.gramm
        if len(els_)>0:
            self.vNodo.hijos.append(nodoAST('else',n+1)) 

    def ejecutar(self,entorno,estat):
        c=''
        salidas=[]
        breaks=[]
        continues=[]
        for i in self.subifs:
            actual=Entorno(entorno)
            sub=i.ejecutar(actual,estat)
            c+=sub.c3d
            salidas=salidas+sub.EtiquetasdeSalida
            breaks=breaks+sub.EtiquetasBreak
            continues=continues+sub.EtiquetasContinue
        actual=Entorno(entorno)
        for i in self.else_:
            temp=i.ejecutar(actual,estat)
            breaks=breaks+temp.EtiquetasBreak
            continues=continues+temp.EtiquetasContinue
            c+=temp.c3d
        for i in salidas:
            c+=i+':\n'

        nodoResultante=nodoC3d('',newtipo(tipoPrimitivo.void,''),c,[],continues,'')
        nodoResultante.EtiquetasBreak=breaks

        return nodoResultante

class newSubIF:
    def __init__(self,cond,instr,c,l,n):
        self.columna=c
        self.linea=l
        self.condicion=cond
        self.Linstr=instr
        self.vNodo=nodoAST('SUBIF',n)
        self.vNodo.hijos.append(cond.vNodo)
        self.vNodo.hijos.append(nodoAST('INSTRUCCIONES',n+1))
        self.gramm='<tr><td>LSUBIF::= ELSE? IF (EXP) { INSTRUCCIONES }   </td><td> INSTRUCCION=newSubIF(EXP, INSTRUCCIONES); </td></tr>'
        for i in instr:
            self.vNodo.hijos[1].hijos.append(i.vNodo)
            self.gramm+=i.gramm
# etiquetas de salida, etiqueta de break y continue
    def ejecutar(self,entorno,estat):
        c=''
        resultado=self.condicion.getvalor(entorno,estat)
        if resultado.tipo.tipo==tipoPrimitivo.Error: 
            return nodoC3d('',resultado.tipo,'',[],[],'')
        L1=estat.newetiquetaL()
        L2=estat.newetiquetaL()
        L3=estat.newetiquetaL()
        breaks=[]
        continues=[]
        c+=resultado.c3d+'\n'
        c+='if('+resultado.temporal+') goto '+L1+';\n goto '+L2+';\n'+L1+':\n'
        for i in self.Linstr:
            temp=i.ejecutar(entorno,estat)
            breaks=breaks+temp.EtiquetasBreak
            continues=continues+temp.EtiquetasContinue
            c+=temp.c3d
        c+='goto '+L3+';\n'+L2+':\n'

        nodoResultante=nodoC3d('',resultado.tipo,c,[L3],continues,'')
        nodoResultante.EtiquetasBreak=breaks

        return nodoResultante
        

class newWhile:
    def __init__(self,cond,instr,c,l,n):
        self.columna=c
        self.linea=l
        self.condicion=cond
        self.Linstr=instr
        self.vNodo=nodoAST('WHILE',n)
        self.vNodo.hijos.append(cond.vNodo)
        self.vNodo.hijos.append(nodoAST('{ INSTRUCCIONES }',n+1))
        self.gramm='<tr><td>INSTRUCCION::= WHILE (EXP) { INSTRUCCIONES }   </td><td> INSTRUCCION=newWhile(EXP, INSTRUCCIONES); </td></tr>'
        for i in instr:
            self.vNodo.hijos[1].hijos.append(i.vNodo)
            self.gramm+=i.gramm

    def ejecutar(self,entorno,estat):
        cond=self.condicion.getvalor(entorno,estat)
        if cond.tipo.tipo==tipoPrimitivo.Error:
            return nodoC3d('',cond.tipo,'',[],[],'')

        c=''
        inwhile=''
        breaks=[]
        continues=[]
        Evaluar=estat.newetiquetaL()
        inicio=estat.newetiquetaL()
        salir=estat.newetiquetaL()
        actual=Entorno(entorno)
        for i in self.Linstr:
            temp=i.ejecutar(actual,estat)
            inwhile+=temp.c3d
            breaks=breaks+temp.EtiquetasBreak
            continues=continues+temp.EtiquetasContinue

        c+=Evaluar+':\n'
        
        for i in continues:
            c+=i+':\n'
        c+=cond.c3d
        c+='if ('+cond.temporal+') goto '+inicio+';\ngoto '+salir+';\n'+inicio+':\n'
        c+=inwhile
        c+='goto '+Evaluar+';\n'
        c+=salir+':\n'
        for i in breaks:
            c+=i+':\n'

        return nodoC3d('',cond.tipo,c,[],[],'')

class newDo:
    def __init__(self,cond,instr,c,l,n):
        self.columna=c
        self.linea=l
        self.condicion=cond
        self.Linstr=instr
        self.vNodo=nodoAST('DO',n)
        self.vNodo.hijos.append(nodoAST('{ INSTRUCCIONES }',n+1))
        self.vNodo.hijos.append(cond.vNodo)  
        self.gramm='<tr><td>INSTRUCCION::= DO { INSTRUCCIONES } WHILE (EXP);   </td><td> INSTRUCCION=newDo(EXP, INSTRUCCIONES); </td></tr>'
        for i in instr:
            self.vNodo.hijos[0].hijos.append(i.vNodo)
            self.gramm+=i.gramm

    def ejecutar(self,entorno,estat):
        cond=self.condicion.getvalor(entorno,estat)
        if cond.tipo.tipo==tipoPrimitivo.Error:
            return nodoC3d('',cond.tipo,'',[],[],'')

        c=''
        inwhile=''
        breaks=[]
        continues=[]
        Evaluar=estat.newetiquetaL()
        inicio=estat.newetiquetaL()
        salir=estat.newetiquetaL()
        actual=Entorno(entorno)
        for i in self.Linstr:
            temp=i.ejecutar(actual,estat)
            inwhile+=temp.c3d
            breaks=breaks+temp.EtiquetasBreak
            continues=continues+temp.EtiquetasContinue

        
        c+='goto '+inicio+';\n'
        c+=Evaluar+':\n'
        
        for i in continues:
            c+=i+':\n'
        c+=cond.c3d
        c+='if ('+cond.temporal+') goto '+inicio+';\ngoto '+salir+';\n'+inicio+':\n'
        c+=inwhile
        c+='goto '+Evaluar+';\n'
        c+=salir+':\n'
        for i in breaks:
            c+=i+':\n'

        return nodoC3d('',cond.tipo,c,[],[],'')


class newFor:
    def __init__(self,i1,cond,i2,instr,c,l,n):
        self.columna=c
        self.linea=l
        self.condicion=cond
        self.Linstr=instr
        self.ins1=i1
        self.ins2=i2
        self.vNodo=nodoAST('FOR',n)
        self.vNodo.hijos.append(i1.vNodo)
        self.vNodo.hijos.append(cond.vNodo)
        self.vNodo.hijos.append(i2.vNodo)
        self.gramm='<tr><td>INSTRUCCION::= FOR( F1 ; EXP ; ASIGNA|EXP ) { INSTRUCCIONES }  </td><td> INSTRUCCION=newFor(F1,EXP, F2); </td></tr>'
        self.gramm+='<tr><td>F1::= DECLA|ASIGNA </td><td> F1=(DECLA|ASIGNA); </td></tr>'
        self.gramm+='<tr><td>F2::= EXP|ASIGNA </td><td> F1=(EXP|ASIGNA); </td></tr>'
        self.vNodo.hijos.append(nodoAST('{ INSTRUCCIONES }',n+1))
        for i in instr:
            self.vNodo.hijos[3].hijos.append(i.vNodo)
            self.gramm+=i.gramm
        
    def ejecutar(self,entorno,estat):
        cond=self.condicion.getvalor(entorno,estat)
        if cond.tipo.tipo==tipoPrimitivo.Error:
            return nodoC3d('',cond.tipo,'',[],[],'')

        c=''
        inwhile=''
        breaks=[]
        continues=[]
        Evaluar=estat.newetiquetaL()
        incremento=estat.newetiquetaL()
        inicio=estat.newetiquetaL()
        salir=estat.newetiquetaL()
        actual=Entorno(entorno)
        for1=self.ins1.ejecutar(actual,estat)
        for3=self.ins2.ejecutar(actual,estat)

        for i in self.Linstr:
            temp=i.ejecutar(actual,estat)
            inwhile+=temp.c3d
            breaks=breaks+temp.EtiquetasBreak
            continues=continues+temp.EtiquetasContinue

        c+=for1.c3d
        c+='goto '+Evaluar+';'
        c+=incremento+':\n'
        for i in continues:
            c+=i+':\n'
        c+=for3.c3d
        c+=Evaluar+':\n'
        c+=cond.c3d
        c+='if ('+cond.temporal+') goto '+inicio+';\ngoto '+salir+';\n'+inicio+':\n'
        c+=inwhile
        c+='goto '+incremento+';\n'
        c+=salir+':\n'
        for i in breaks:
            c+=i+':\n'

        return nodoC3d('',cond.tipo,c,[],[],'')


class newSwitch:
    def __init__(self,cond,lcasos,c,l,n):
        self.columna=c
        self.linea=l
        self.condicion=cond
        self.casos=lcasos
        self.vNodo=nodoAST('SWITCH',n)
        self.vNodo.hijos.append(cond.vNodo)
        self.gramm='<tr><td>INSTRUCCION::= SWITCH( EXP ) { LCASOS }  </td><td> INSTRUCCION=newSwitch(EXP, LCASOS); </td></tr>'
        self.gramm+=cond.gramm
        for i in lcasos:
            self.vNodo.hijos.append(i.vNodo)
            self.gramm+=i.gramm
        
    def ejecutar(self,entorno,estat):
        return

class newCaso:
    def __init__(self,val,instr,esdef,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('CASO',n)
        self.valor=val
        self.Linstr=instr
        self.esDefault=esdef
        self.gramm='<tr><td>LCASOS::= CASE EXP : INSTRUCCIONES  </td><td> LCASOS=newCaso(EXP, INSTRUCCIONES); </td></tr>'
        if not esdef:
            self.vNodo.hijos.append(val.vNodo)
            self.gramm+=val.gramm
        else:
            self.vNodo.hijos.append(nodoAST('DEFAULT',n+1))
        self.vNodo.hijos.append(nodoAST('INSTRUCCIONES',n+2))
        for i in instr:
            self.vNodo.hijos[1].hijos.append(i.vNodo)
            self.gramm+=i.gramm
    
    def ejecutar(self,entorno,estat):
        return

class newRetorno:
    def __init__(self,v,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('RETORNO',n)
        self.valor=v
        self.gramm='<tr><td>INSTRUCCION::= RETORNO EXP;  </td><td> LCASOS=newRetorno(EXP); </td></tr>'
        if not v=='':
            self.vNodo.hijos.append(v.vNodo)
            self.gramm+=v.gramm
    
    def ejecutar(self,entorno,estat):
        return

class newBreak:
    def __init__(self,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('BREAK',n)
        self.gramm='<tr><td>INSTRUCCION::= BREAK;  </td><td> INSTRUCCION=newBreak(); </td></tr>'
    
    def ejecutar(self,entorno,estat):
        t=estat.newetiquetaL()
        v=nodoC3d('',newtipo(tipoPrimitivo.void,''),'goto '+t+';\n',[],[],'')
        v.EtiquetasBreak.append(t)
        return v


class newContinue:
    def __init__(self,c,l,n):
        self.columna=c
        self.linea=l
        self.vNodo=nodoAST('Continue',n)
        self.gramm='<tr><td>INSTRUCCION::= CONTINUE;  </td><td> INSTRUCCION=newContinue(); </td></tr>'
    
    def ejecutar(self,entorno,estat):
        t=estat.newetiquetaL()
        return nodoC3d('',newtipo(tipoPrimitivo.void,''),'goto '+t+';\n',[],[t],'')
        

        

