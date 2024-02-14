from tkinter import *
from tkinter import ttk
import ply.lex as lex

rlexema = list()

reservada = ('FOR', 'DO', 'WHILE', 'IF', 'ELSE', 'STATIC', 'INT', 'FLOAT', 'VOID', 'CHAR', 'PUBLIC')

tokens = reservada + ('VARIABLE', 'NUMEROE', 'NUMEROD', 'DELIMITADOR', 'OPERADOR','PUNTOCOM',)

def t_OPERADOR(t):
    r'[\+\*-/=]'
    global valor
    valor = "OPERADOR"
    return t

def t_DELIMITADOR(t):
    r'[\(\)\[\]\{\}]'
    global valor
    valor = "SIMBOLO"
    return t

def t_VARIABLE(t):
    r'[A-Za-z_][A-Za-z_]*'
    global valor
    if t.value.upper() in reservada:
        valor = "RESERVADA"
    else:
        valor = "IDENTIFICADOR"
    return t

def t_NUMEROD(t):
    r'[0-9]+\.[0-9]+'
    global valor
    valor = "NUMERO"
    return t

def t_NUMEROE(t):
    r'[0-9]+'
    global valor
    valor = "NUMERO"
    return t

def t_PUNTOCOM(t):
    r';'
    global valor
    valor ="PUNTO"
    return t

t_ignore =" \t "

def t_error(t):
    global rlexema
    estado = {"token":"No Identificado","lexema":str(t.value),"linea":str(t.lineno)}
    rlexema.append(estado)
    t.lexer.skip(1)

def analizar(data):
    global rlexema
    global valor
    rlexema.clear()
    analizador = lex.lex() 
    salto = data.split("\n")
    for valoresAux in salto:
        analizador.input(valoresAux)
        while True:
            token = analizador.token()
            if not token:
                break
            estado = {"token":valor,"lexema":str(token.value),"linea":str(token.lineno)}
            rlexema.append(estado)

def run():
    global rlexema
    index = 0
    entrada = text1.get("1.0", END)
    analizar(entrada)
    for resultado in rlexema:
        if resultado.get('token') == "IDENTIFICADOR":
            tabla.insert(parent='',index='end',iid=index,text='',
            values=(resultado.get('lexema'),"","X","","",""))    
        elif resultado.get('token') == "RESERVADA":
            tabla.insert(parent='',index='end',iid=index,text='',
            values=(resultado.get('lexema'),"X","","","",""))
        elif resultado.get('token') == "OPERADOR":
            tabla.insert(parent='',index='end',iid=index,text='',
            values=(resultado.get('lexema'),"","","X","",""))
        elif resultado.get('token') == "NUMERO":
            tabla.insert(parent='',index='end',iid=index,text='',
            values=(resultado.get('lexema'),"","","","X",""))
        elif resultado.get('token') == "SIMBOLO":
            tabla.insert(parent='',index='end',iid=index,text='',
            values=(resultado.get('lexema'),"","","","","X"))
        index = index +1
# Limpiar tabla
def limpiar():
    text1.delete("1.0", END)
    for valor in tabla.get_children():
        tabla.delete(valor)

ventana = Tk()
ventana.geometry("1020x800")
text1 = Text(ventana)
tabla = ttk.Treeview(ventana)
#colores y texto
boton1 = Button(ventana, text='Run', command=run)
boton2 = Button(ventana, text='Limpiar', command=limpiar)
###################################################################
text1.place(x=10, y=50, height=300, width=1000)
tabla['columns']= ('token','reservada','identificador','operador','numero','simbolo')
#tamaño y colocacion de los botones
boton1.place(x=10, y=10, width=90, height=30)
boton2.place(x=10, y=360, width=90, height=30)
##############################################
tabla.column("#0", width=0, stretch=NO)
tabla.column("token", anchor=CENTER, width=50)
tabla.column("reservada", anchor=CENTER, width=50)
tabla.column("identificador", anchor=CENTER, width=50)
tabla.column("operador", anchor=CENTER, width=50)
tabla.column("numero", anchor=CENTER, width=50)
tabla.column("simbolo", anchor=CENTER, width=50)
tabla.heading("#0", text="", anchor=CENTER)
tabla.heading("token", text="Token", anchor=CENTER)
tabla.heading("reservada", text="Reservada", anchor=CENTER)
tabla.heading("identificador", text="Identificador", anchor=CENTER)
tabla.heading("operador", text="Operador", anchor=CENTER)
tabla.heading("numero", text="Numero", anchor=CENTER)
tabla.heading("simbolo", text="Simbolo", anchor=CENTER)
tabla.place(x=10, y=400, height=350, width=1000)


ventana.mainloop()