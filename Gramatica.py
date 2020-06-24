reservadas = {
    'goto' : 'RGOTO',
    'break' : 'BREAK',
    'continue' : 'CONTINUE',
    'if' : 'IF',
    'else' : 'ELSE',
    'case' : 'CASE',
    'int' : 'TINT',
    'float': 'TFLOAT',
    'char' : 'TCHAR',
    'double' : 'TDOBLE',
    'void' : 'TVOID',
    'return' : 'RETORNO',
    'for' : 'FOR',
    'struct' : 'STRUCT',
    'switch' : 'SWITCH',
    'while' : 'WHILE',
    'do' : 'DO',
    'default' : 'DEFAULT'
}

tokens  = [
    'PTCOMA',
    'DOSPTS',
    'PUNTO',
    'COMA',
    'PREGUNTA',
    'CORCHA',
    'CORCHC',
    'PARA',
    'PARC',
    'LLAVEA',
    'LLAVEC',
    'IGUAL',
    'MAS',
    'MENOS',
    'POR',
    'DIVIDIDO',
    'MODULO',
    'NOT',
    'AND',
    'OR',
    'CEJA',
    'MENORQ',
    'MAYORQ',
    'DOBIGUAL',
    'DOBAND',
    'DOBOR',
    'NOIGUAL',
    'MAYORIGUALQ',
    'MENORIGUALQ',
    'POTENC',
    'ROTIZQ',
    'ROTDER',
    'MASIGUAL',
    'MENOSIGUAL',
    'PORIGUAL',
    'DIVIGUAL',
    'ORIGUAL',
    'MODIGUAL',
    'LEFTIGUAL',
    'RIGHTIGUAL',
    'ANDIGUAL',
    'XORIGUAL',
    'MASMAS',
    'MENOSMENOS',
    'FLECHA',
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'CARACTER',
    'ID'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_DOSPTS    = r':'
t_PUNTO    = r'\.'
t_COMA    = r','
t_PREGUNTA    = r'\?'
t_CORCHA   = r'\['
t_CORCHC   = r'\]'
t_PARA    = r'\('
t_PARC    = r'\)'
t_LLAVEA    = r'{'
t_LLAVEC    = r'}'
t_IGUAL     = r'='
t_MAS       = r'\+'
t_MENOS     = r'-'
t_POR       = r'\*'
t_DIVIDIDO  = r'/'
t_MODULO    = r'%'
t_NOT       = r'!'
t_AND       = r'&'
t_OR        = r'\|'
t_CEJA      = r'~'
t_MENORQ    = r'<'
t_MAYORQ    = r'>'
t_DOBIGUAL  = r'=='
t_DOBAND    = r'&&'
t_DOBOR     = r'\|\|'
t_NOIGUAL   = r'!='
t_MAYORIGUALQ = r'>='
t_MENORIGUALQ = r'<='
t_POTENC    = r'\^'
t_ROTIZQ    = r'<<'
t_ROTDER    = r'>>'
t_MASIGUAL   = r'\+='
t_MENOSIGUAL   = r'-='
t_PORIGUAL   = r'\*='
t_DIVIGUAL   = r'/='
t_ORIGUAL   = r'\|='
t_MODIGUAL   = r'%='
t_LEFTIGUAL   = r'<<='
t_RIGHTIGUAL   = r'>>='
t_ANDIGUAL   = r'&='
t_XORIGUAL   = r'\^='
t_MASMAS   = r'\+\+'
t_MENOSMENOS   = r'--'
t_FLECHA   = r'->'

Lerr=[]
noNodo=0
from CError import CError
def t_DECIMAL(t):
    r'\d+\.\d+'
    try:
        t.value = float(t.value)
    except ValueError:
        print("Float value too large %d", t.value)
        global Lerr
        Lerr.append(CError('Lexico','Error en el valor float',0,t.lexer.lineno))
        t.value = 0
    return t

def t_ENTERO(t):
    r'\d+'
    try:
        t.value = int(t.value)
    except ValueError:
        print("Integer value too large %d", t.value)
        global Lerr
        Lerr.append(CError('Lexico','Error en el valor entero',0,t.lexer.lineno))
        t.value = 0
    return t

def t_CADENA(t):
    r'\".*?\"'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_CARACTER(t):
    r'\'.?\''
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_ID(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'ID')    # Check for reserved words
     return t

# Comentario de múltiples líneas /* .. */
def t_COMENTARIO_MULTILINEA(t):
    r'/\*(.|\n)*?\*/'
    t.lexer.lineno += t.value.count('\n')

# Comentario simple // ...
def t_COMENTARIO_SIMPLE(t):
    r'\#.*\n'
    t.lexer.lineno += 1

# Caracteres ignorados
t_ignore = " \t"

def t_newline(t):
    r'\n+'
    t.lexer.lineno += t.value.count("\n")

def find_column(input,token):
    last_cr = input.rfind('\n',0,token.lexpos)
    if last_cr < 0:
        last_cr = 0
    column = (token.lexpos - last_cr) + 1
    return column
    
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    global Lerr
    Lerr.append(CError('Lexico','Caracter invalido \''+t.value[0]+'\'',0,t.lexer.lineno))
    t.lexer.skip(1)

# Construyendo el analizador léxico
import ply.lex as lex
lexer = lex.lex()


# Asociación de operadores y precedencia
precedence = (
    ('left','COMA'),
    ('right','IGUAL','MASIGUAL','MENOSIGUAL','PORIGUAL','DIVIGUAL','MODIGUAL','ORIGUAL','LEFTIGUAL','RIGHTIGUAL','ANDIGUAL','XORIGUAL'),
    ('right','DOSPTS','PREGUNTA'),
    ('left','DOBOR'),
    ('left','DOBAND'),
    ('left','OR'),
    ('left','POTENC'),
    ('left','AND'),
    ('left','DOBIGUAL','NOIGUAL'),
    ('left','MENORQ','MAYORQ','MENORIGUALQ','MAYORIGUALQ'),
    ('left','ROTIZQ','ROTDER'),
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO','MODULO'),
    ('right','UMENOS'),
    ('left','PUNTO','FLECHA','PARA','PARC','CORCHA','CORCHC'),
    )

# Definición de la gramática

from Expresion_Trad import *
from Instruccion_Trad import *



def p_init(t) :
    'init            : posglobales'
    t[0] = t[1]

def p_posglob(t) :
    'posglobales    : globales'
    t[0] = t[1]

def p_posglobEmpt(t) :
    'posglobales    : '
    t[0] = []

def p_globales(t) :
    'globales    : globales global'
    t[1].append(t[2])
    t[0] = t[1]

def p_globales_(t) :
    'globales    : global'
    t[0] = [t[1]]

def p_global(t) :
    '''global      : strucs_
                        | funcion_
                        | asignacion
                        | declaracion'''
    t[0] = t[1]

def p_struct(t) :
    'strucs_    : STRUCT ID LLAVEA instruct LLAVEC '
    global noNodo
    t[0] = newDecStruct(t[2],t[4],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=2

def p_inStruct(t):
    'instruct   : instruct declaracion '
    t[1].append(t[2])
    t[0] = t[1]

def p_inStruct1(t):
    'instruct   : declaracion '
    t[0] = [t[1]]

def p_funcion_(t):
    'funcion_   : tipo ID PARA posparams PARC LLAVEA posinstr LLAVEC'
    global noNodo
    t[0] = newDecFuncion(t[1],t[2],t[4],t[7],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_posparam_(t):
    'posparams  :  params'
    t[0] = t[1]

def p_posparams_(t):
    'posparams  : '
    t[0] = []

def p_params_(t):
    'params  : params COMA tipo ID opc'
    global noNodo
    t[1].append(newDecParam(t[3],t[4],t[5],t.lexpos(1),t.lineno(1),noNodo))
    t[0] = t[1]
    noNodo+=3

def p_params1_(t):
    'params  :  tipo ID opc'
    global noNodo
    t[0] = [newDecParam(t[1],t[2],t[3],t.lexpos(1),t.lineno(1),noNodo)]
    noNodo+=3

def p_opc1_(t):
    'opc  : CORCHA pose CORCHC '
    t[0] = t[2]
    

def p_opc2_(t):
    'opc  : '
    t[0] = ''
    
def p_pose1_(t):
    'pose  : exp '
    t[0] = t[1]

def p_pose2_(t):
    'pose  : '
    t[0] = ''

def p_posinst1_(t):
    'posinstr  : instrucciones'
    t[0] = t[1]

def p_posinst2_(t):
    'posinstr  : '
    t[0] =[]

def p_tipos_(t):
    '''tipo : TINT
            | TFLOAT
            | TCHAR
            | TDOBLE
            | TVOID
            | STRUCT ID'''
    if t[1].lower() == 'int'  : t[0] = newtipo(tipoPrimitivo.Entero,'')
    elif t[1].lower() == 'float': t[0] = t[0] = newtipo(tipoPrimitivo.Doble,'')
    elif t[1].lower() == 'char': t[0] = t[0] = newtipo(tipoPrimitivo.caracter,'')
    elif t[1].lower() == 'double': t[0] = t[0] = newtipo(tipoPrimitivo.Doble,'')
    elif t[1].lower() == 'void': t[0] = t[0] = newtipo(tipoPrimitivo.void,'')
    elif t[1].lower() == 'struct': t[0] = t[0] = newtipo(tipoPrimitivo.structura,t[2])


def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : etiqueta
                        | salto PTCOMA
                        | declaracion
                        | asignacion PTCOMA
                        | exp PTCOMA
                        | if_
                        | while_
                        | do_
                        | for_
                        | switch_
                        | retorno_
                        | brek_ PTCOMA
                        | cont_ PTCOMA '''
    t[0] = t[1]

def p_etiqueta_instr(t) :
    'etiqueta     : ID DOSPTS'
    global noNodo
    t[0] =newEtiqueta(t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=2
    
def p_salto_instr(t) :
    'salto   : RGOTO ID'
    global noNodo
    t[0] =newSalto(t[2],t.lexpos(2),t.lineno(2),noNodo)
    noNodo+=3

def p_declaracion_instr(t) :
    'declaracion   : tipo ldecla_ PTCOMA'
    global noNodo
    
    noNodo+=3

def p_Ldecla(t) :
    'ldecla_   : ldecla_ COMA decla'
    t[1].append(t[3])
    t[0]=t[1]

def p_Ldecla2(t) :
    'ldecla_   :  decla'
    t[0]=[t[1]]

def p_decla(t) :
    'decla   :  ID posdecla posdecasig'
    global noNodo
    t[0]=newDecla(t[1],t[2],t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=4

def p_declaexp(t) :
    'posdecasig   :  IGUAL exp'
    t[0]=t[2]

def p_declaexp2(t) :
    'posdecasig   :  '
    t[0]=''

def p_posdecla(t) :
    '''posdecla   : indices
                    | dimvacios  '''
    t[0]=t[1]

def p_posdecla2(t) :
    '''posdecla   :   '''
    t[0]=''

def p_dimvacios_L(t):
    'dimvacios   : dimvacios CORCHA  CORCHC'
    t[0]=t[1]+1

def p_dimvacios(t):
    'dimvacios   : CORCHA CORCHC'
    t[0]=0


def p_asignaciona_instr(t) :
    'asignacion   : ID indicess1 igualess exp '
    global noNodo
    t[0]=newAsignacion(t[1],t[2],t[4],t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=4


def p_igualess(t):
    '''igualess  : IGUAL
                | MASIGUAL
                | MENOSIGUAL
                | PORIGUAL
                | DIVIGUAL
                | ORIGUAL
                | MODIGUAL
                | LEFTIGUAL
                | RIGHTIGUAL
                | ANDIGUAL
                | XORIGUAL'''
    t[0]=t[1]


def p_indicess_L(t):
    'indicess1   : indicess'
    t[0]=t[1]

def p_indicess_empty(t):
    'indicess1   : '
    t[0]=[]

def p_indicess_L1(t):
    'indicess   : indicess CORCHA exp CORCHC'
    t[1].append(t[3])
    t[0]=t[1]

def p_indicess_(t):
    'indicess   : indicess PUNTO ID'
    t[1].append(t[3])
    t[0]=t[1]

def p_indicess_L1s(t):
    'indicess   : CORCHA exp CORCHC'
    t[0]=[t[2]]

def p_indicess_s(t):
    'indicess   : PUNTO ID'
    t[0]=[t[2]]


def p_indices_L(t):
    'indices   : indices CORCHA exp CORCHC'
    t[1].append(t[3])
    t[0]=t[1]

def p_indice(t):
    'indices   : CORCHA exp CORCHC'
    t[0]=[t[2]]

# HACER LLAMADA, EXP
# 1 SAVE ALL FUNCTIONS, 2 GLOBALS, 3 MAIN, 4 ALL OTHER METHODS---------------------------------------------

def p_llamadaf_instr(t):
    'llamadafuncion   : ID PARA poslexp PARC  '
    global noNodo
    t[0]=newLlamadaInstr(t[1],t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=6

def p_plexp(t):
    'poslexp   : lexp '
    t[0]=t[1]

def p_plexp_(t):
    'poslexp   : '
    t[0]=[]

def p_lexp_(t):
    'lexp   : lexp COMA exp'
    t[1].append(t[3])
    t[0]=t[1]

def p_lexp(t):
    'lexp   : exp'
    t[0]=[t[1]]

def p_if_instr(t):
    'if_   : lsubif poselse'
    global noNodo
    t[0]=newIF(t[1],t[2],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=6

def p_poselse(t):
    'poselse  : ELSE LLAVEA posinstr LLAVEC'
    t[0]=t[3]

def p_poselse1(t):
    'poselse  : '
    t[0]=[]
    

def p_subif_instr(t):
    'lsubif  : lsubif ELSE IF PARA exp PARC LLAVEA posinstr LLAVEC'
    global noNodo
    t[1].append(newSubIF(t[5],t[8],t.lexpos(2),t.lineno(2),noNodo))
    t[0]=t[1]
    noNodo+=6

def p_subif2_instr(t):
    'lsubif  : IF PARA exp PARC LLAVEA posinstr LLAVEC'
    global noNodo
    t[0]=[newSubIF(t[3],t[6],t.lexpos(1),t.lineno(1),noNodo)]
    noNodo+=6

def p_while_instr(t):
    'while_  : WHILE PARA exp PARC LLAVEA posinstr LLAVEC'
    global noNodo
    t[0]=newWhile(t[3],t[6],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_do_instr(t):
    'do_  : DO LLAVEA posinstr LLAVEC WHILE PARA exp PARC PTCOMA '
    global noNodo
    t[0]=newDo(t[7],t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5


def p_for_instr(t):
    'for_  : FOR PARA inifor_ exp PTCOMA finfor_ PARC LLAVEA posinstr LLAVEC '
    global noNodo
    t[0]=newFor(t[3],t[4],t[6],t[9],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_for1_instr(t):
    '''inifor_  : declaracion
                | asignacion PTCOMA
                | exp PTCOMA '''
    t[0]=t[1]

def p_for3_instr(t):
    '''finfor_  : asignacion
                | exp '''
    t[0]=t[1]

def p_switch_instr(t):
    'switch_  : SWITCH PARA exp PARC LLAVEA plcasos LLAVEC '
    global noNodo
    t[0]=newSwitch(t[3],t[6],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_switch1_instr(t):
    'plcasos  : lcasos '
    t[0]=t[1]

def p_switch2_instr(t):
    'plcasos  : '
    t[0]=[]

def p_switch3_instr(t):
    '''lcasos  : lcasos CASE exp DOSPTS posinstr 
                | lcasos DEFAULT DOSPTS posinstr  '''
    global noNodo
    if t[2].lower() == 'case'  : t[1].append(newCaso(t[3],t[5],False,t.lexpos(2),t.lineno(2),noNodo))
    else:  t[1].append(newCaso('',t[4],True,t.lexpos(2),t.lineno(2),noNodo))
    t[0]=t[1]
    noNodo+=5

def p_switch4_instr(t):
    '''lcasos  : CASE exp DOSPTS posinstr 
                | DEFAULT DOSPTS posinstr  '''
    global noNodo
    if t[1].lower() == 'case'  : t[0]=[newCaso(t[2],t[4],False,t.lexpos(1),t.lineno(1),noNodo)]
    else:  t[0]=[newCaso('',t[3],True,t.lexpos(1),t.lineno(1),noNodo)]
    noNodo+=5

# cont_

def p_retorno_instr(t):
    'retorno_  : RETORNO posret'
    t[0]=t[2]

def p_retorno2_instr(t):
    'posret : exp PTCOMA '
    global noNodo
    t[0]=newRetorno(t[1],t.lexpos(2),t.lineno(2),noNodo)
    noNodo+=5

def p_retorno3_instr(t):
    'posret : PTCOMA '
    global noNodo
    t[0]=newRetorno('',t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_break_instr(t):
    'brek_  : BREAK'
    global noNodo
    t[0]=newBreak(t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_continue_instr(t):
    'cont_  : CONTINUE'
    global noNodo
    t[0]=newContinue(t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5


def p_expresion_binaria(t):
    '''exp : exp MAS exp
            | exp MENOS exp
            | exp POR exp
            | exp DIVIDIDO exp
            | exp MODULO exp
            | exp AND exp
            | exp DOBAND exp
            | exp OR exp
            | exp DOBOR exp
            | exp POTENC exp
            | exp ROTIZQ exp
            | exp ROTDER exp
            | exp DOBIGUAL exp
            | exp NOIGUAL exp
            | exp MENORQ exp
            | exp MAYORQ exp
            | exp MAYORIGUALQ exp
            | exp MENORIGUALQ exp'''

    global noNodo
    if t[2] == '+'  : t[0] = newSuma(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '-': t[0] = newResta(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '*': t[0] = newMultiplicacion(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '/': t[0] = newDivision(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '%': t[0] = newModulo(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '&': t[0] = newAndBtb(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '&&': t[0] = newAnd(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '|': t[0] = newOrBtb(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '||': t[0] = newOr(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '^': t[0] = newXorBtb(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '<<': t[0] = newDespIzqBtb(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '>>': t[0] = newDespDerBtb(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '==': t[0] = newEqual(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '!=': t[0] = newNotEqual(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '<': t[0] = newMenorq(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '>': t[0] = newMayorq(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '<=': t[0] = newMenorIgualq(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
    elif t[2] == '>=': t[0] = newMayorIgualq(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)

    
    noNodo+=1

def p_expresion_unaria(t):
    '''exp : MENOS exp %prec UMENOS
            | AND exp %prec UMENOS
            | NOT exp %prec UMENOS
            | CEJA exp %prec UMENOS'''
    global noNodo
    if t[1] == '-'  : t[0] = newNegacion(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1]== '&' : t[0] = newPuntero(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1]== '!' : t[0] = newNot(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1]== '~' : t[0] = newNotBtb(t[2],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_expresion_casteo(t):
    '''exp : PARA TINT PARC exp
            | PARA TFLOAT PARC exp
            | PARA TCHAR PARC exp
            | PARA TDOBLE PARC exp
            | PARA exp PARC'''
    global noNodo
    if t[2].lower()== 'int' : t[0]=newCasteoInt(t[4],t.lexpos(1),t.lineno(1),noNodo)
    elif t[2].lower()== 'float' : t[0]=newCasteoFloat(t[4],t.lexpos(1),t.lineno(1),noNodo)
    elif t[2].lower()== 'char' : t[0]=newCasteoChar(t[4],t.lexpos(1),t.lineno(1),noNodo)
    elif t[2].lower()== 'double' : t[0]=newCasteoFloat(t[4],t.lexpos(1),t.lineno(1),noNodo)
    else: t[0]=t[2]

    noNodo+=5


def p_exp_entero(t):
    'exp : ENTERO'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.Entero,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_decimal(t):
    'exp : DECIMAL'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.Doble,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_cadena(t):
    'exp : CADENA'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.Cadena,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_caracter(t):
    'exp : CARACTER'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.caracter,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_id(t):
    'exp : ID'
    global noNodo
    t[0] = id_(t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_acceso(t):
    'exp : exp CORCHA exp CORCHC'
    global noNodo
    t[0] = newAccesoArr(t[1],t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_exp_acceso_struct(t):
    'exp : exp PUNTO ID'
    global noNodo
    t[0] = newAccesoStr(t[1],t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_exp_fcall(t):
    'exp : llamadafuncion'
    t[0]=t[1]

def p_exp_arreglo(t):
    'exp : LLAVEA lexp LLAVEC'
    global noNodo
    t[0]=newArreglo(t[2],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5



def p_error(t):
    global Lerr
    Lerr.append(CError('Sintactico','Se encontro \''+str(t.value)+'\'',str(t.lexpos),str(t.lineno)))
    print("Error sintáctico en '%s'" % t.value)
    while True:
        tok = parser.token()             # Get the next token  
        if not tok or tok.type == 'PTCOMA': 
            break
    # t.lexer.skip(1)
    tok = parser.token()
    parser.errok()
    return tok 

import ply.yacc as yacc
parser = yacc.yacc()


def parse(input) :
    return parser.parse(input)

def getLerr():
    global Lerr
    return Lerr

def resetLerr():
    global Lerr
    Lerr=[]

def resetNonodo():
    global noNodo
    noNodo=0