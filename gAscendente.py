reservadas = {
    'goto' : 'RGOTO',
    'unset' : 'RUNSET',
    'print' : 'IMPRIMIR',
    'if' : 'IF',
    'exit' : 'SALIR',
    'read' : 'LEER',
    'int' : 'TINT',
    'float': 'TFLOAT',
    'char' : 'TCHAR',
    'abs' : 'VABSOL',
    'array' : 'ARREGLO',
    'xor' : 'XOR'
}

tokens  = [
    'PTCOMA',
    'DOSPTS',
    'CORCHA',
    'CORCHC',
    'PARA',
    'PARC',
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
    'DECIMAL',
    'ENTERO',
    'CADENA',
    'LABEL',
    'VARIABLE'
] + list(reservadas.values())

# Tokens
t_PTCOMA    = r';'
t_DOSPTS    = r':'
t_CORCHA   = r'\['
t_CORCHC   = r'\]'
t_PARA    = r'\('
t_PARC    = r'\)'
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
    r'(\".*?\")|(\'.*?\')'
    t.value = t.value[1:-1] # remuevo las comillas
    return t 

def t_LABEL(t):
     r'[a-zA-Z_][a-zA-Z_0-9]*'
     t.type = reservadas.get(t.value.lower(),'LABEL')    # Check for reserved words
     return t

def t_VARIABLE(t):
     r'\$(([tavs][0-9]+)|ra|sp)'
     t.type = reservadas.get(t.value.lower(),'VARIABLE')    # Check for reserved words
     return t

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
    ('left','MAS','MENOS'),
    ('left','POR','DIVIDIDO'),
    )

# Definición de la gramática

from Expresion import *
from Instruccion import *



def p_init(t) :
    'init            : instrucciones'
    t[0] = t[1]

def p_instrucciones_lista(t) :
    'instrucciones    : instrucciones instruccion'
    t[1].append(t[2])
    t[0] = t[1]


def p_instrucciones_instruccion(t) :
    'instrucciones    : instruccion '
    t[0] = [t[1]]

def p_instruccion(t) :
    '''instruccion      : etiqueta
                        | salto
                        | asignacion
                        | unset
                        | imprimir_
                        | exit_
                        | if_'''
    t[0] = t[1]

def p_etiqueta_instr(t) :
    'etiqueta     : LABEL DOSPTS'
    global noNodo
    t[0] =newEtiqueta(t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=2
    
def p_salto_instr(t) :
    'salto   : RGOTO LABEL PTCOMA'
    global noNodo
    t[0] =newSalto(t[2],t.lexpos(2),t.lineno(2),noNodo)
    noNodo+=3


# def p_asignacions_instr(t) :
#     'asignacion   : VARIABLE IGUAL exp PTCOMA'
#     global noNodo
#     t[0] =newAsignacion(t[1],[],t[3],t.lexpos(1),t.lineno(1),noNodo)
#     noNodo+=4

def p_asignaciona_instr(t) :
    'asignacion   : VARIABLE indicess IGUAL exp PTCOMA'
    global noNodo
    t[0]=newAsignacion(t[1],t[2],t[4],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=4

def p_indicess_L(t):
    'indicess   : indices'
    t[0]=t[1]

def p_indicess_empty(t):
    'indicess   : '
    t[0]=[]

def p_indices_L(t):
    'indices   : indices CORCHA primitivo CORCHC'
    t[1].append(t[3])
    t[0]=t[1]

def p_indice(t):
    'indices   : CORCHA primitivo CORCHC'
    t[0]=[t[2]]

def p_unset_instr(t):
    'unset   : RUNSET PARA vars PARC PTCOMA'
    global noNodo
    t[0]=newUnset(t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=4

def p_imprimir_instr(t):
    'imprimir_   : IMPRIMIR PARA primitivo PARC PTCOMA'
    global noNodo
    t[0]=newImprimir(t[3],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=4

def p_salir_instr(t):
    'exit_   : SALIR PTCOMA'
    global noNodo
    t[0]=newSalir(t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_if_instr(t):
    'if_   : IF PARA exp PARC RGOTO LABEL PTCOMA'
    global noNodo
    t[0]=newIF(t[3],t[6],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=6


def p_expresion_binaria(t):
    '''exp : primitivo MAS primitivo
            | primitivo MENOS primitivo
            | primitivo POR primitivo
            | primitivo DIVIDIDO primitivo
            | primitivo MODULO primitivo
            | primitivo AND primitivo
            | primitivo DOBAND primitivo
            | primitivo OR primitivo
            | primitivo DOBOR primitivo
            | primitivo POTENC primitivo
            | primitivo XOR primitivo
            | primitivo ROTIZQ primitivo
            | primitivo ROTDER primitivo
            | primitivo DOBIGUAL primitivo
            | primitivo NOIGUAL primitivo
            | primitivo MENORQ primitivo
            | primitivo MAYORQ primitivo
            | primitivo MAYORIGUALQ primitivo
            | primitivo MENORIGUALQ primitivo'''
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
    elif t[2].lower() == 'xor': t[0] = newXor(t[1],t[3],t.lexpos(2),t.lineno(2),noNodo)
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
    '''exp : MENOS primitivo
            | AND vars
            | LEER PARA PARC
            | VABSOL PARA primitivo PARC
            | NOT primitivo
            | CEJA primitivo
            | ARREGLO PARA PARC'''
    global noNodo
    if t[1] == '-'  : t[0] = newNegacion(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1]== '&' : t[0] = newPuntero(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1].lower()== 'read' : t[0] = newLeer(t.lexpos(1),t.lineno(1),noNodo)
    elif t[1].lower()== 'abs' : t[0] = newAbsoluto(t[3],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1]== '!' : t[0] = newNot(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1]== '~' : t[0] = newNotBtb(t[2],t.lexpos(1),t.lineno(1),noNodo)
    elif t[1].lower()== 'array': t[0]=newArreglo(t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=5

def p_expresion_casteo(t):
    '''exp : PARA TINT PARC primitivo
            | PARA TFLOAT PARC primitivo
            | PARA TCHAR PARC primitivo'''
    global noNodo
    if t[2].lower()== 'int' : t[0]=newCasteoInt(t[4],t.lexpos(1),t.lineno(1),noNodo)
    elif t[2].lower()== 'float' : t[0]=newCasteoFloat(t[4],t.lexpos(1),t.lineno(1),noNodo)
    elif t[2].lower()== 'char' : t[0]=newCasteoChar(t[4],t.lexpos(1),t.lineno(1),noNodo)


    noNodo+=5

def p_exp_primitivo(t):
    'exp : primitivo'
    t[0]=t[1]

def p_exp_entero(t):
    'primitivo : ENTERO'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.Entero,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_decimal(t):
    'primitivo : DECIMAL'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.Doble,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_cadena(t):
    'primitivo : CADENA'
    global noNodo
    t[0] = primitivo(tipoPrimitivo.Cadena,t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_variables(t):
    'primitivo : vars'
    t[0] = t[1]

def p_exp_id(t):
    'vars : VARIABLE'
    global noNodo
    t[0] = id_(t[1],t.lexpos(1),t.lineno(1),noNodo)
    noNodo+=1

def p_exp_acceso(t):
    'vars : VARIABLE indices'
    global noNodo
    t[0] = newAcceso(t[1],t[2],t.lexpos(1),t.lineno(1),noNodo)
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