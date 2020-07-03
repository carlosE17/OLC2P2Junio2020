from tkinter import *
import tkinter.scrolledtext as scrolledtext
import tkinter.ttk as ttk
import tkinter.messagebox
from tkinter import filedialog
import AST_Trad as AST_C3d
import Entorno_Trad as Entorno_C3d
import TipoTrad as tipo_C3d
from graphviz import Source
import Instruccion_Trad as InstrminorC
import gAscendente as agus
import Gramatica as g1
from CError import CError
import Simbolo_Trad as s_C3d
from PIL import ImageTk, Image
import os

# -------------------------------augus---------------------------
import Tipo as TipoAugus
import Entorno as EntornoAugus
import AST as ASTaugus
import Simbolo as SimboloAugus
import Instruccion as InstruccionAugus


# --------------------------------augus-------------------------

rutas = []
c3dPAraDebug=''

def traducir(Linstr,c,Le,tabs):
    LErr=Le
    ast=AST_C3d.Estaticos(LErr)
    entornoG=Entorno_C3d.Entorno(None)
    c3dPerFuncion={}
    c3dVarGlobales='$s0=array();\n$s1=array();\n$sp=-1;\n$ra=-1;\n$s1[$ra]=0;\n'


    try:
        i=0
        while i<len(Linstr):
            if isinstance(Linstr[i],InstrminorC.newDecFuncion):
                ast.addFun(Linstr[i].nombre,Linstr[i])                    
            i+=1
    except Exception as e:
        print('veentana[46]'+str(e))


    with open('reporteOptimizacion_minorC.dot', "w") as f:
        f.write('digraph {\n'+"node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Antes</td><td>Despues</td><td>Linea</td></tr>\n")


    try:
        i=0
        while i<len(Linstr):
            cTemp=Linstr[i].ejecutar(entornoG,ast)
            if isinstance(Linstr[i],InstrminorC.newAsignacion) or isinstance(Linstr[i],InstrminorC.newDeclaracion):
                c3dVarGlobales+=cTemp.c3d+''
            elif isinstance(Linstr[i],InstrminorC.newDecFuncion):
                c3dPerFuncion[Linstr[i].nombre]=cTemp.c3d                     
            i+=1
    except Exception as e:
        print('veentana[58]'+str(e))

    # i=0
    # while i<len(Linstr):
    #     cTemp=Linstr[i].ejecutar(entornoG,ast)
    #     if isinstance(Linstr[i],InstrminorC.newAsignacion) or isinstance(Linstr[i],InstrminorC.newDeclaracion):
    #         c3dVarGlobales+=cTemp.c3d+''
    #     elif isinstance(Linstr[i],InstrminorC.newDecFuncion):
    #         c3dPerFuncion[Linstr[i].nombre]=cTemp.c3d                     
    #     i+=1

    with open('reporteOptimizacion_minorC.dot', "a") as f:
        f.write( "    </table>\n" + ">];}")


    c3dOptimizado='main:\n'+c3dVarGlobales+'\n'
    for k,v in c3dPerFuncion.items():
        if k.lower()=='main': c3dOptimizado+=v+'\n'
    c3dOptimizado+='return:\n'+ast.retornos+'\nexit; \n'

    for k,v in c3dPerFuncion.items():
        if k.lower()!='main': c3dOptimizado+=k+':#-----------------------Funcion-------------------------\n'+v+'\n'
    


    editor = scrolledtext.ScrolledText(
            undo=True, width=80, height=10, wrap=WORD)
    editor['font'] = ('consolas', 12)
    editor.focus()
    t0 = 'C3d_Optimizado'
    editor.insert(INSERT,c3dOptimizado )
    tabs.add(editor, text=t0, padding=10)
    rutas.append(t0+'.txt')

    # print(c3dOptimizado)

    correrAugus(c3dOptimizado,c)
    global c3dPAraDebug
    c3dPAraDebug=c3dOptimizado

    gReporteErrTraduccion(ast.Lerrores)
    gReporteTsTraduccion(entornoG.tabla.items(),ast.C3dFunciones.items())
    graphASTtraduccion(Linstr)

def gReporteErrTraduccion(L):
    if len(L)>0:
        texto='digraph {\n'
        t=''
        repL=''
        repS=''
        repSem=''
        for i in L:
            t+=i.getTexto()
            if i.tipo=='Lexico': repL+=i.getTexto()
            elif i.tipo=='Sintactico': repS+=i.getTexto()
            else: repSem+=i.getTexto()
        texto += "node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ t+ "    </table>\n" + ">];}"
        with open('reporteErrores_minorC.dot', "w") as f:
                f.write(texto)
        texto = "digraph {\n node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ repL+ "    </table>\n" + ">];}"
        with open('reporteErroresLexicos_minorC.dot', "w") as f:
                f.write(texto)
        texto = "digraph {\n node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ repS+ "    </table>\n" + ">];}"
        with open('reporteErroresSintacticos_minorC.dot', "w") as f:
                f.write(texto)
        texto = "digraph {\n node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ repSem+ "    </table>\n" + ">];}"
        with open('reporteErroresSemanticos_minorC.dot', "w") as f:
                f.write(texto)
    else:
        t='digraph G {\"No hay errores\"}'
        with open('reporteErrores_minorC.dot', "w") as f:
                f.write(t)
        with open('reporteErroresLexicos_minorC.dot', "w") as f:
                f.write(t)
        with open('reporteErroresSintacticos_minorC.dot', "w") as f:
                f.write(t)
        with open('reporteErroresSemanticos_minorC.dot', "w") as f:
                f.write(t)

def gReporteTsTraduccion(L,L2):
    texto='digraph {\n'
    t=''
    for k,v in L:
        t+="<tr> <td> " + str(k) + "</td><td> " + str(v.tipo.tipo.name) + " </td><td> " + v.temporal + " </td><td> " + v.valor + " </td><td> "+ v.linea + "</td> </tr>"
    for k,v in L2:
        t+="<tr> <td> " + str(k) + "</td><td> " + 'funcion '+str(v.tipo.tipo.name) + " </td><td> " + '---' + " </td><td> " + '---' + " </td><td> "+str(v.linea)  + "</td> </tr>"


    texto += "node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>ID</td><td>Tipo</td><td>Temporal</td><td>valor</td><td>Linea</td></tr>\n"+ t+ "    </table>\n" + ">];}"
    with open('reporteTs_minorC.dot', "w") as f:
        f.write(texto)

        
def graphASTtraduccion(L):
    if len(L)!=0:
        t='digraph Q { \n  node [shape=record];\n'
        for i in L:
            t+='node'+i.vNodo.nNodo+'[label=\"'+i.vNodo.vNodo+'\"];\n'
            t+='p_inicio ->'+'node'+i.vNodo.nNodo+';\n'
            t+=dibujo(i.vNodo)
        t+='\n}'
        with open('reporteAST_minorC.dot', "w") as f:
                f.write(t)
    else:
        with open('reporteAST_minorC.dot', "w") as f:
                f.write('digraph G {\"No hay instrucciones\"}')

def dibujo(n):
    t=''
    for i in n.hijos:
        t+='node'+i.nNodo+'[label=\"'+i.vNodo+'\"];\n'
        t+='node'+n.nNodo+' -> node'+i.nNodo+';\n'
        t+=dibujo(i)
    return t

def gramRepoTraduccion(L):
    texto='digraph {\n'
    t='<tr><td>INICIO::= INSTRUCCIONES </td><td> INICIO=INSTRUCCIONES; </td></tr>\n'

    for i in L:
        t+=i.gramm+'\n'
    texto += "node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>PRODUCCION</td><td>ACCIONES</td></tr>\n"+ t+ "    </table>\n" + ">];}"
    with open('reporteGramatical_minorC.dot', "w") as f:
        f.write(texto)

# --------------------------------------------------------------------integracion augus------------------------------------------

def correrAugus(texto,salida):
    agus.resetLerr()
    agus.resetNonodo()
    # print(texto)
    resultado=agus.parse(texto)

    salida.delete('1.0', END)
    salida.insert(INSERT, "Output:\n")

    Ejec(resultado,salida,agus.Lerr)
    gramRepo(resultado,1)
    if len(agus.Lerr)>0 :
        tkinter.messagebox.showerror(
            "Error", "Se encontraron errores al ejecutar")
        s = Source.from_file("reporteErrores.dot", format="pdf")
        s.view()

def Ejec(Linstr,c,Le):
    LErr=Le
    ast=ASTaugus.Estaticos(c,LErr,len(Linstr))
    entornoG=EntornoAugus.Entorno()
    iEt=0
    try:
        while iEt<len(Linstr):
            if(isinstance(Linstr[iEt],InstruccionAugus.newEtiqueta)):
                if Linstr[iEt].label_ in entornoG.etiquetas:
                    ast.Lerrores.append(CError('Semantico','La etiqueta \''+Linstr[iEt].label_+'\' ya fue declarada',0,iEt+1))

                entornoG.addEtiqueta(Linstr[iEt].label_,iEt)
            iEt+=1
    except Exception as e:
        print('ventana[178] '+e)

    if isinstance(Linstr[0],InstruccionAugus.newEtiqueta):
        if str(Linstr[0].label_).lower()!='main':
            ast.Lerrores.append(CError('Semantico','no se encontro la etiqueta Main al inicio',0,1))
    else:
        ast.Lerrores.append(CError('Semantico','no se encontro la etiqueta Main al inicio',0,1))


    try:
        while ast.i<len(Linstr):
            Linstr[ast.i].ejecutar(entornoG,ast)
            ast.i+=1
    except Exception as e:
        print('veentana[192]'+str(e))
    # generar reportes de errores, y graficar el arbol---------------------------------------------------------------------
    try:
        i_0=0
        while i_0<len(Linstr):
            if isinstance(Linstr[i_0],InstruccionAugus.newEtiqueta):
                entornoG.actualizar(str(Linstr[i_0].label_),SimboloAugus.Simbolo(TipoAugus.tipoPrimitivo.labl,str(Linstr[i_0].label_)+':'))
            i_0+=1


        i_0=0
        while i_0<len(Linstr):
            tpo_=TipoAugus.tipoPrimitivo.labl

            if isinstance(Linstr[i_0],InstruccionAugus.newSalto):
                if i_0>0 and i_0<len(Linstr):
                    if isinstance(Linstr[i_0-1],InstruccionAugus.newAsignacion):
                        if '$a' in str(Linstr[i_0-1].id).lower():
                            tpo_=TipoAugus.tipoPrimitivo.met1
                        elif '$v' in str(Linstr[i_0-1].id).lower():
                            tpo_=TipoAugus.tipoPrimitivo.fun1
                entornoG.actualizar(str(Linstr[i_0].label_),SimboloAugus.Simbolo(tpo_,str(Linstr[i_0].label_)+':'))
            elif isinstance(Linstr[i_0],InstruccionAugus.newIF):
                if i_0>0 and i_0<len(Linstr):
                    if isinstance(Linstr[i_0-1],InstruccionAugus.newAsignacion):
                        if '$a' in str(Linstr[i_0-1].id).lower():
                            tpo_=TipoAugus.tipoPrimitivo.met1
                        elif '$v' in str(Linstr[i_0-1].id).lower():
                            tpo_=TipoAugus.tipoPrimitivo.fun1
                entornoG.actualizar(str(Linstr[i_0].label),SimboloAugus.Simbolo(tpo_,str(Linstr[i_0].label)+':'))

            i_0+=1
    except Exception as e:
        print('veentana[225]'+str(e))
    
    gReporteErr(ast.Lerrores)
    gReporteTs(entornoG.tabla.items(),entornoG.etiquetas)
    graphAST(Linstr)

def gReporteErr(L):
    if len(L)>0:
        texto='digraph {\n'
        t=''
        repL=''
        repS=''
        repSem=''
        for i in L:
            t+=i.getTexto()
            if i.tipo=='Lexico': repL+=i.getTexto()
            elif i.tipo=='Sintactico': repS+=i.getTexto()
            else: repSem+=i.getTexto()
        texto += "node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ t+ "    </table>\n" + ">];}"
        with open('reporteErrores.dot', "w") as f:
                f.write(texto)
        texto = "digraph {\n node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ repL+ "    </table>\n" + ">];}"
        with open('reporteErroresLexicos.dot', "w") as f:
                f.write(texto)
        texto = "digraph {\n node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ repS+ "    </table>\n" + ">];}"
        with open('reporteErroresSintacticos.dot', "w") as f:
                f.write(texto)
        texto = "digraph {\n node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>TIPO</td><td>Descripcion</td><td>Linea</td></tr>\n"+ repSem+ "    </table>\n" + ">];}"
        with open('reporteErroresSemanticos.dot', "w") as f:
                f.write(texto)
    else:
        t='digraph G {\"No hay errores\"}'
        with open('reporteErrores.dot', "w") as f:
                f.write(t)
        with open('reporteErroresLexicos.dot', "w") as f:
                f.write(t)
        with open('reporteErroresSintacticos.dot', "w") as f:
                f.write(t)
        with open('reporteErroresSemanticos.dot', "w") as f:
                f.write(t)

def gReporteTs(L,etiq):
    nTipos=['Int','String','Float','Array','error',' ',' ','puntero']
    texto='digraph {\n'
    t=''
    # print(L)
    # print(etiq)
    for k,v in L:
        
        if int(v.tipo.value)-1==7:
            t+="<tr> <td> " + str(k) + "</td><td> " + nTipos[int(v.tipo.value)-1] + " </td><td> " + str(v.valor.exp.variable) + " </td><td> "+'0' + " </td><td> " + str(v.valor.linea) + " </td><td> "+ str(v.valor.exp.variable) + "</td> </tr>"
        elif int(v.tipo.value)-1==3:
            t+="<tr> <td> " + str(k) + "</td><td> " + nTipos[int(v.tipo.value)-1] + " </td><td> " + str(v.valor.getTabla()) + " </td><td> "+str(v.valor.getProfundidad()) + " </td><td> " + str(v.valor.linea) + " </td><td> "+ '---' + "</td> </tr>"            
        elif int(v.tipo.value)==9:
            t+="<tr> <td> " + str(k) + "</td><td> " + 'Etiqueta' + " </td><td> " + str(v.valor) + " </td><td> "+'0' + " </td><td> " + str(etiq[str(k)]+1) + " </td><td> "+ '---' + "</td> </tr>"            
        elif int(v.tipo.value)==10:
            t+="<tr> <td> " + str(k) + "</td><td> " + 'Funcion' + " </td><td> " + str(v.valor) + " </td><td> "+'0' + " </td><td> " + str(etiq[str(k)]+1) + " </td><td> "+ '---' + "</td> </tr>"
        elif int(v.tipo.value)==11:
            t+="<tr> <td> " + str(k) + "</td><td> " + 'Metodo' + " </td><td> " + str(v.valor) + " </td><td> "+'0' + " </td><td> " + str(etiq[str(k)]+1) + " </td><td> "+ '---' + "</td> </tr>"                    
        else:                
            t+="<tr> <td> " + str(k) + "</td><td> " + nTipos[int(v.tipo.value)-1] + " </td><td> " + str(v.valor.valor) + " </td><td> "+'0' + " </td><td> " + str(v.valor.linea) + " </td><td> "+ '---' + "</td> </tr>"
    texto += "node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>ID</td><td>Tipo</td><td>Valor</td><td>Dimension</td><td>Linea</td><td>Referencia</td></tr>\n"+ t+ "    </table>\n" + ">];}"
    with open('reporteTs.dot', "w") as f:
        f.write(texto)
        
def graphAST(L):
    if len(L)!=0:
        t='digraph Q { \n  node [shape=record];\n'
        for i in L:
            t+='node'+i.vNodo.nNodo+'[label=\"'+i.vNodo.vNodo+'\"];\n'
            t+='p_inicio ->'+'node'+i.vNodo.nNodo+';\n'
            t+=dibujo(i.vNodo)
        t+='\n}'
        with open('reporteAST.dot', "w") as f:
                f.write(t)
    else:
        with open('reporteAST.dot', "w") as f:
                f.write('digraph G {\"No hay instrucciones\"}')

def gramRepo(L,s):
    texto='digraph {\n'
    t='<tr><td>INICIO::= INSTRUCCIONES </td><td> INICIO=INSTRUCCIONES; </td></tr>\n'
    if s==1:
        t+='<tr><td>INSTRUCCIONES::= INSTRUCCIONES1 INSTRUCCION </td><td> INSTRUCCIONES=INSTRUCCIONES1; INSTRUCCIONES.append(INSTRUCCION); </td></tr>\n'
        t+='<tr><td>INSTRUCCIONES::= INSTRUCCION </td><td> INSTRUCCIONES=[]; INSTRUCCIONES.append(INSTRUCCION); </td></tr>\n'
    else:
        t+='<tr><td>INSTRUCCIONES::=  INSTRUCCION INSTRUCCIONES1</td><td> INSTRUCCIONES=INSTRUCCIONES1; INSTRUCCIONES.append(INSTRUCCION); </td></tr>\n'
        t+='<tr><td>INSTRUCCIONES::=  </td><td> INSTRUCCIONES=[];  </td></tr>\n'

    for i in L:
        t+=i.gramm+'\n'
    texto += "node0" + " ["+ "    shape=plaintext\n"+ "    label=<\n"+ "\n" +"      <table cellspacing='0'>\n"+ "      <tr><td>PRODUCCION</td><td>ACCIONES</td></tr>\n"+ t+ "    </table>\n" + ">];}"
    with open('reporteGramatical.dot', "w") as f:
        f.write(texto)

    



# -------------------------------------------------------------------fin augus-----------------------------------------------------

class Ventana:

    def __init__(self, master):
        self.nVentanas = 0
        # cuerpo general del frame----------------------------
        topFrame = Frame(master)
        topFrame.pack()
        bottomFrame = Frame(master)
        bottomFrame.pack(side=BOTTOM)
        # fin cuerpo general del frame------------------------
        # topFrame-----------------------------------------------------------------------------------------------
        # menu----------------------------
        barraMenu = Menu(master)
        master.config(menu=barraMenu)

        menuArchivos = Menu(barraMenu)
        menuColores = Menu(barraMenu)
        menuDebug = Menu(barraMenu)
        menuAyuda = Menu(barraMenu)
        menuReportesc3d=Menu(barraMenu)
        menuEditar=Menu(barraMenu)
        menuRepoImgc3d=Menu(barraMenu)

        menuReportes=Menu(barraMenu)
        menuRepoImg=Menu(barraMenu)

        barraMenu.add_cascade(label="Archivo", menu=menuArchivos)
        barraMenu.add_cascade(label="Colores", menu=menuColores)
        barraMenu.add_cascade(label="Debugger", menu=menuDebug)
        barraMenu.add_cascade(label="Reportes minorC PDF",menu=menuReportesc3d)
        barraMenu.add_cascade(label="Reportes minorC in App",menu=menuRepoImgc3d)
        barraMenu.add_cascade(label="Reportes PDF Augus",menu=menuReportes)
        barraMenu.add_cascade(label="Reportes in App Augus",menu=menuRepoImg)
        barraMenu.add_cascade(label='Editar',menu=menuEditar)
        barraMenu.add_cascade(label="Ayuda", menu=menuAyuda)
        

        menuArchivos.add_command(label="Nuevo", command=self.nuevo)
        menuArchivos.add_command(label="Abrir...", command=self.abrir)
        menuArchivos.add_command(label="Guardar", command=self.guardar)
        menuArchivos.add_command(label="Guardar como...", command=self.guardarComo)
        menuArchivos.add_separator()
        menuArchivos.add_command(label="Salir", command=self.salir)

        menuColores.add_command(label="original", command=self.color1)
        menuColores.add_command(label="negro", command=self.color2)
        menuColores.add_command(label="azul", command=self.color3)
        menuColores.add_command(label="morado", command=self.color4)

        menuDebug.add_command(label="debuggear", command=self.debugg)

        menuReportesc3d.add_command(label='Todos los Errores',command=self.repoErroresc3d)
        menuReportesc3d.add_separator()
        menuReportesc3d.add_command(label="Errores Lexicos", command=self.errLexc3d)
        menuReportesc3d.add_command(label="Errores Sintacticos", command=self.errSinc3d)
        menuReportesc3d.add_command(label="Errores Semanticos", command=self.errSemc3d)
        menuReportesc3d.add_separator()
        menuReportesc3d.add_command(label="Tabla de Simbolos", command=self.tbSimbc3d)
        menuReportesc3d.add_command(label="AST",command=self.astRepoc3d)
        menuReportesc3d.add_command(label="Reporte Gramatical", command=self.repoGramc3d)
        menuReportesc3d.add_command(label="Reporte Optimizacion", command=self.repoOptimizacion)
        # 0000 repoOptimizacion
        menuRepoImgc3d.add_command(label='Todos los Errores',command=self.repoErrores2c3d)
        menuRepoImgc3d.add_separator()
        menuRepoImgc3d.add_command(label="Errores Lexicos", command=self.errLex2c3d)
        menuRepoImgc3d.add_command(label="Errores Sintacticos", command=self.errSin2c3d)
        menuRepoImgc3d.add_command(label="Errores Semanticos", command=self.errSem2c3d)
        menuRepoImgc3d.add_separator()
        menuRepoImgc3d.add_command(label="Tabla de Simbolos", command=self.tbSimb2c3d)
        menuRepoImgc3d.add_command(label="AST",command=self.astRepo2c3d)
        menuRepoImgc3d.add_command(label="Reporte Gramatical", command=self.repoGram2c3d)
        menuRepoImgc3d.add_command(label="Reporte Optimizacion", command=self.repoOptimizacion2)
        
        # -------------------------------------------------------------------------------------------------augus------------

        menuReportes.add_command(label='Todos los Errores',command=self.repoErrores)
        menuReportes.add_separator()
        menuReportes.add_command(label="Errores Lexicos", command=self.errLex)
        menuReportes.add_command(label="Errores Sintacticos", command=self.errSin)
        menuReportes.add_command(label="Errores Semanticos", command=self.errSem)
        menuReportes.add_separator()
        menuReportes.add_command(label="Tabla de Simbolos", command=self.tbSimb)
        menuReportes.add_command(label="AST",command=self.astRepo)
        menuReportes.add_command(label="Reporte Gramatical", command=self.repoGram)
        # 0000
        menuRepoImg.add_command(label='Todos los Errores',command=self.repoErrores2)
        menuRepoImg.add_separator()
        menuRepoImg.add_command(label="Errores Lexicos", command=self.errLex2)
        menuRepoImg.add_command(label="Errores Sintacticos", command=self.errSin2)
        menuRepoImg.add_command(label="Errores Semanticos", command=self.errSem2)
        menuRepoImg.add_separator()
        menuRepoImg.add_command(label="Tabla de Simbolos", command=self.tbSimb2)
        menuRepoImg.add_command(label="AST",command=self.astRepo2)
        menuRepoImg.add_command(label="Reporte Gramatical", command=self.repoGram2)


        # -----------------------------------------------------------------augus-----------------------------------------------


        menuEditar.add_command(label='Copiar',command=self.copiartxt)
        menuEditar.add_command(label='Pegar',command=self.pegartxt)
        menuEditar.add_command(label='Buscar y Remplazar',command=self.buscYremp)
        self.txtCopiado=''

        menuAyuda.add_command(label="ayuda", command=self.ayuda)
        menuAyuda.add_command(label="Sobre nosotros", command=self.aboutus)

        # fin menu------------------------

        txtTitulo1 = Label(topFrame, text="Proyecto 2: MinorC")
        txtTitulo1.config(font=("Arial", 24))

        txtTitulo1.grid(row=2, columnspan=2)

        # editor-------------------
        # ventanas---
        self.ventanas = ttk.Notebook(topFrame)
        #self.ventanas.add(self.editor, text='ventana0', padding=10)
        self.ventanas.grid(row=3, columnspan=2, pady=10, padx=10)
        self.ventanas.focus()
        # boton tipo de analizador------------
       
        # fin topFrame-------------------------------------------------------------------------------------------

        # bottomFrame--------------------------------------------------------------------------------------------
        txtTitulo2 = Label(bottomFrame, text="Salida:")
        txtTitulo2.config(font=("Arial", 20))
        txtTitulo2.grid(row=0)

        # salida---------------------
        self.salida = scrolledtext.ScrolledText(bottomFrame, undo=True, width=80, height=10,
                                                wrap=WORD, bg="black",
                                                fg="light green",
                                                insertbackground='light green')

        # este tambien funciona como append
        self.salida.insert(INSERT, "Output:\n")
        self.salida['font'] = ('consolas', 12)
        self.salida.focus()
        self.salida.grid(row=2, columnspan=2, pady=10, padx=10)
        # salida.delete('1.0', END) # limpiar consola
        # finSalida------------------
        # botones etc-----------------------------------------------
        self.btnEjecutar = Button(topFrame, text="Ejecutar", bg="light sky blue", fg="black",
                                  font=("Arial", 12), command=self.ejecutar)
        self.btnEjecutar.grid(row=5, column=0)

        self.btnNext = Button(topFrame, text="Next", bg="light gray", fg="black",
                                  font=("Arial", 12),state=DISABLED,command=self.nextDebug)
        self.btnNext.grid(row=6, column=1)

    def getTextoActual(self):
        return self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index("current")]).winfo_children()[1].get(1.0, END)

    def ejecutar(self):
        if not (len(self.ventanas.tabs()) != 0 and len(rutas) > self.ventanas.index('current')):
            tkinter.messagebox.showerror(
                "Error", "No se encontro consola de entrada de texto")
            return

        txtEntrada = self.getTextoActual()
        if len(txtEntrada)<=1:
            return
        self.salida.delete('1.0', END)
        self.salida.insert(INSERT, "Output:\n")

       
        g1.resetLerr()
        g1.resetNonodo()
        resultado=g1.parse(txtEntrada)
        traducir(resultado,self.salida,g1.Lerr,self.ventanas)
        self.nVentanas+=1
        gramRepoTraduccion(resultado)
        if len(g1.Lerr)>0:
            tkinter.messagebox.showerror(
                "Error", "Se encontraron errores al ejecutar")
            s = Source.from_file("reporteErrores_minorC.dot", format="pdf")
            s.view()

    def nuevo(self):
        editor = scrolledtext.ScrolledText(
            undo=True, width=80, height=10, wrap=WORD)
        editor['font'] = ('consolas', 12)
        editor.focus()
        t0 = 'Nuevo'+str(self.nVentanas)
        self.ventanas.add(editor, text=t0, padding=10)
        self.nVentanas += 1
        rutas.append(t0+'.txt')

    def abrir(self):
        ftypes = [('All files', '*')]
        dlg = filedialog.Open(filetypes=ftypes)
        fl = dlg.show()
        if fl != '':
            with open(fl, "r") as f:
                text = f.read()
                editor = scrolledtext.ScrolledText(
                    undo=True, width=80, height=10, wrap=WORD)
                editor['font'] = ('consolas', 12)
                editor.insert(INSERT, text)
                editor.focus()
                self.ventanas.add(editor, text=fl, padding=10)
                self.nVentanas += 1
                rutas.append(fl)

    def guardar(self):
        if(len(self.ventanas.tabs()) != 0 and len(rutas) > self.ventanas.index('current')):
            with open(rutas[self.ventanas.index('current')], "w") as f:
                f.write(self.getTextoActual())
        else:
            tkinter.messagebox.showerror(
                "Error", "se encontro un error al guardar")

    def guardarComo(self):
        r=filedialog.asksaveasfilename()
        if r!="" and (len(self.ventanas.tabs()) != 0 and len(rutas) > self.ventanas.index('current')):
            with open(r, "w") as f:
                f.write(self.getTextoActual())
            rutas[self.ventanas.index('current')]=r
            self.ventanas.tab(self.ventanas.tabs()[self.ventanas.index("current")],text=r)
        else:
            tkinter.messagebox.showerror(
                "Error", "se encontro un error al guardar")

    def salir(self):
        ventana1.destroy()

    def color1(self):
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index(
            "current")]).winfo_children()[1].config(background="white")

    def color2(self):
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index(
            "current")]).winfo_children()[1].config(background="gray")

    def color3(self):
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index(
            "current")]).winfo_children()[1].config(background="RoyalBlue1")

    def color4(self):
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index(
            "current")]).winfo_children()[1].config(background="MediumPurple1")

    def ayuda(self):
        help = tkinter.messagebox.askyesno(
            message="Desea consultar los manuales?", title="ayuda")
        if help:
            print('abrir manuales')
        else:
            print("ok, tu puedes")

    def aboutus(self):
        tkinter.messagebox.showinfo(
            message="Carlos Rodrigo Estrada Najarro\nCarnet: 201700314", title="About Us")

    def debugg(self):

        global c3dPAraDebug
        if c3dPAraDebug=='':
            tkinter.messagebox.showerror(
                "Error", "No se encontro consola de entrada de texto")
            return

        txtEntrada = c3dPAraDebug
        if len(txtEntrada)==0:
            return
        self.salida.delete('1.0', END)
        self.salida.insert(INSERT, "Output:\n")
        agus.resetLerr()
        agus.resetNonodo()
        resultado=agus.parse(txtEntrada)
        self.astDebug=ASTaugus.Estaticos(self.salida,agus.Lerr,len(resultado))
        self.entornoDebug=EntornoAugus.Entorno()
        self.Ldebugger=resultado
        iEt=0
        try:
            while iEt<len(resultado):
                if(isinstance(resultado[iEt],InstruccionAugus.newEtiqueta)):
                    self.entornoDebug.addEtiqueta(resultado[iEt].label_,iEt)
                iEt+=1
        except Exception as e:
            print('ventana[292] '+e)

        self.btnNext.config(state=NORMAL)

    def errLexc3d(self):
        s = Source.from_file("reporteErroresLexicos_minorC.dot", format="pdf")
        s.view()
    def errSinc3d(self):
        s = Source.from_file("reporteErroresSintacticos_minorC.dot", format="pdf")
        s.view()
    def errSemc3d(self):
        s = Source.from_file("reporteErroresSemanticos_minorC.dot", format="pdf")
        s.view()
    def tbSimbc3d(self):
        s = Source.from_file("reporteTs_minorC.dot", format="pdf")
        s.view()
    def astRepoc3d(self):
        s = Source.from_file("reporteAST_minorC.dot", format="pdf")
        s.view()
    def repoGramc3d(self):
        s = Source.from_file("reporteGramatical_minorC.dot", format="pdf")
        s.view()
    def repoErroresc3d(self):
        s = Source.from_file("reporteErrores_minorC.dot", format="pdf")
        s.view()
        # -----------------------------------------
    def errLex2c3d(self):
        s = Source.from_file("reporteErroresLexicos_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErroresLexicos_minorC.dot.png')
        parent.wait_window(entrada.top)
    def errSin2c3d(self):
        s = Source.from_file("reporteErroresSintacticos_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErroresSintacticos_minorC.dot.png')
        parent.wait_window(entrada.top)
    def errSem2c3d(self):
        s = Source.from_file("reporteErroresSemanticos_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErroresSemanticos_minorC.dot.png')
        parent.wait_window(entrada.top)
    def tbSimb2c3d(self):
        s = Source.from_file("reporteTs_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteTs_minorC.dot.png')
        parent.wait_window(entrada.top)
    def astRepo2c3d(self):
        s = Source.from_file("reporteAST_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteAST_minorC.dot.png')
        parent.wait_window(entrada.top)
    def repoGram2c3d(self):
        s = Source.from_file("reporteGramatical_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteGramatical_minorC.dot.png')
        parent.wait_window(entrada.top)
    def repoErrores2c3d(self):
        s = Source.from_file("reporteErrores_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErrores_minorC.dot.png')
        parent.wait_window(entrada.top)
    
    # -----------------
    def errLex(self):
        s = Source.from_file("reporteErroresLexicos.dot", format="pdf")
        s.view()
    def errSin(self):
        s = Source.from_file("reporteErroresSintacticos.dot", format="pdf")
        s.view()
    def errSem(self):
        s = Source.from_file("reporteErroresSemanticos.dot", format="pdf")
        s.view()
    def tbSimb(self):
        s = Source.from_file("reporteTs.dot", format="pdf")
        s.view()
    def astRepo(self):
        s = Source.from_file("reporteAST.dot", format="pdf")
        s.view()
    def repoGram(self):
        s = Source.from_file("reporteGramatical.dot", format="pdf")
        s.view()
    def repoErrores(self):
        s = Source.from_file("reporteErrores.dot", format="pdf")
        s.view()
        # -----------------------------------------
    def errLex2(self):
        s = Source.from_file("reporteErroresLexicos.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErroresLexicos.dot.png')
        parent.wait_window(entrada.top)
    def errSin2(self):
        s = Source.from_file("reporteErroresSintacticos.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErroresSintacticos.dot.png')
        parent.wait_window(entrada.top)
    def errSem2(self):
        s = Source.from_file("reporteErroresSemanticos.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErroresSemanticos.dot.png')
        parent.wait_window(entrada.top)
    def tbSimb2(self):
        s = Source.from_file("reporteTs.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteTs.dot.png')
        parent.wait_window(entrada.top)
    def astRepo2(self):
        s = Source.from_file("reporteAST.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteAST.dot.png')
        parent.wait_window(entrada.top)
    def repoGram2(self):
        s = Source.from_file("reporteGramatical.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteGramatical.dot.png')
        parent.wait_window(entrada.top)
    def repoErrores2(self):
        s = Source.from_file("reporteErrores.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteErrores.dot.png')
        parent.wait_window(entrada.top)

    def repoOptimizacion(self):
        s = Source.from_file("reporteOptimizacion_minorC.dot", format="pdf")
        s.view()


    def repoOptimizacion2(self):
        s = Source.from_file("reporteOptimizacion_minorC.dot", format="png")
        s.render()
        parent = self.salida.master
        entrada=popupRepo(parent,'reporteOptimizacion_minorC.dot.png')
        parent.wait_window(entrada.top)


    def nextDebug(self):
        try:
            if self.astDebug.i<len(self.Ldebugger):
                self.Ldebugger[self.astDebug.i].ejecutar(self.entornoDebug,self.astDebug)
                self.astDebug.i+=1
            else:
                try:
                    i_0=0
                    while i_0<len(self.Ldebugger):
                        if isinstance(self.Ldebugger[i_0],InstruccionAugus.newEtiqueta):
                            self.entornoDebug.actualizar(str(self.Ldebugger[i_0].label_),SimboloAugus.Simbolo(TipoAugus.tipoPrimitivo.labl,str(self.Ldebugger[i_0].label_)+':'))
                        i_0+=1


                    i_0=0
                    while i_0<len(self.Ldebugger):
                        tpo_=TipoAugus.tipoPrimitivo.labl

                        if isinstance(self.Ldebugger[i_0],InstruccionAugus.newSalto):
                            if i_0>0 and i_0<len(self.Ldebugger):
                                if isinstance(self.Ldebugger[i_0-1],InstruccionAugus.newAsignacion):
                                    if '$a' in str(self.Ldebugger[i_0-1].id).lower():
                                        tpo_=TipoAugus.tipoPrimitivo.met1
                                    elif '$v' in str(self.Ldebugger[i_0-1].id).lower():
                                        tpo_=TipoAugus.tipoPrimitivo.fun1
                            self.entornoDebug.actualizar(str(self.Ldebugger[i_0].label_),SimboloAugus.Simbolo(tpo_,str(self.Ldebugger[i_0].label_)+':'))
                        elif isinstance(self.Ldebugger[i_0],InstruccionAugus.newIF):
                            if i_0>0 and i_0<len(self.Ldebugger):
                                if isinstance(self.Ldebugger[i_0-1],InstruccionAugus.newAsignacion):
                                    if '$a' in str(self.Ldebugger[i_0-1].id).lower():
                                        tpo_=TipoAugus.tipoPrimitivo.met1
                                    elif '$v' in str(self.Ldebugger[i_0-1].id).lower():
                                        tpo_=TipoAugus.tipoPrimitivo.fun1
                            self.entornoDebug.actualizar(str(self.Ldebugger[i_0].label),SimboloAugus.Simbolo(tpo_,str(self.Ldebugger[i_0].label)+':'))

                        i_0+=1
                except Exception as e:
                    print('veentana[466]'+str(e))
                self.btnNext.config(state=DISABLED)
                graphAST(self.Ldebugger)                
        except Exception as e:
            print(str(e)+'ventana[314]')
            self.astDebug.i+=1
        # generar reportes de errores, y graficar el arbol
        gReporteErr(self.astDebug.Lerrores)
        gReporteTs(self.entornoDebug.tabla.items(),self.entornoDebug.etiquetas)

    def copiartxt(self):
        if not (len(self.ventanas.tabs()) != 0 and len(rutas) > self.ventanas.index('current')):
            tkinter.messagebox.showerror(
                "Error", "No se encontro consola de entrada de texto")
            return
        self.txtCopiado=self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index("current")]).winfo_children()[1].selection_get()
    def pegartxt(self):
        if not (len(self.ventanas.tabs()) != 0 and len(rutas) > self.ventanas.index('current')):
            tkinter.messagebox.showerror(
                "Error", "No se encontro consola de entrada de texto")
            return
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index("current")]).winfo_children()[1].insert(INSERT,self.txtCopiado)
    def buscYremp(self):
        parent = self.salida.master
        entrada=popupSearch(parent)
        # parent.configure(state='disable')
        parent.wait_window(entrada.top)
        # parent.configure(state='enable')
        txtbuscar=str(entrada.buscar)
        txtremplazar=str(entrada.remplazar)
        newTxt=str(self.getTextoActual()).replace(txtbuscar,txtremplazar)
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index("current")]).winfo_children()[1].delete('1.0', END)
        self.ventanas._nametowidget(self.ventanas.tabs()[self.ventanas.index("current")]).winfo_children()[1].insert(INSERT,newTxt)

class popupSearch(object):
    def __init__(self,master):
        top=self.top=Toplevel(master)
        self.l=Label(top,text="Buscar")
        self.l.pack()
        self.e=Entry(top)
        self.e.pack()
        self.l2=Label(top,text="Remplazar")
        self.l2.pack()
        self.e2=Entry(top)
        self.e2.pack()
        self.b=Button(top,text='Ok',command=self.cleanup)
        self.b.pack()
        self.buscar=''
        self.remplazar=''
    def cleanup(self):
        self.buscar=self.e.get()
        self.remplazar=self.e2.get()
        self.top.destroy()

class popupRepo(object):
    def __init__(self,master,path):
        top=self.top=Toplevel(master) 
        img = ImageTk.PhotoImage(Image.open(path))
        panel = Label(top, image = img)
        panel.image=img
        #The Pack geometry manager packs widgets in rows or columns.
        panel.pack(side = "bottom", fill = "both", expand = "yes")

# loop------------------------------------------------
ventana1 = Tk()
ventana1.title('Proyecto1')
v0 = Ventana(ventana1)
ventana1.mainloop()
# endLoop---------------------------------------------
