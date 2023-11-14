from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys

class Lexico(object):
    # Constructor de la clase
    def __init__(self, cadena, token, tipo):
        self.cadena = cadena
        self.token = token
        self.tipo = tipo

    # Retorna la cadena y el token
    def __str__(self):
        return "%s  %s" % (self.cadena, self.token)

    # Retorna la cadena
    def obtenercadena(self):
        return self.cadena

    # Retorna el token
    def obtenertoken(self):
        return self.token

    # Retorna la descripción
    def obtenerdescripcion(self):
        return self.tipo


class Sintactico(object):
    def __init__(self, listaLexico):
        self.listaLexico = listaLexico
        self.posicion = 0
        self.error = False
        self.errores = []

    def agregar_error(self, mensaje):
        self.errores.append(mensaje)

    def avanzar(self):
        self.posicion += 1
        if self.posicion >= len(self.listaLexico):
            self.posicion = len(self.listaLexico) - 1

    def emparejar(self, token_esperado):
        if self.listaLexico[self.posicion].obtenertoken() == token_esperado:
            self.avanzar()
        else:
            self.error = True
            valor_esperado = "Palabra reservada" if token_esperado == 0 else "ID"
            mensaje_error = f"Error de sintaxis. Se esperaba '{valor_esperado}' en lugar de '{self.listaLexico[self.posicion].obtenercadena()}'"
            print(mensaje_error)
            self.agregar_error(mensaje_error)

    def analizar_expresion(self):
        try:
            resultado = self.expresion_matematica()
            if resultado is not None:
                return resultado
            else:
                raise Exception("Error en la expresión matemática.")
        except Exception as e:
            self.error = True
            mensaje_error = f"Error en la expresión matemática: {str(e)}"
            print(mensaje_error)
            self.agregar_error(mensaje_error)
            return None

    def factor(self):
        if self.listaLexico[self.posicion].obtenertoken() == 1 or self.listaLexico[self.posicion].obtenertoken() == 0:  # ID o palabra reservada
            resultado = self.listaLexico[self.posicion].obtenercadena()
            self.avanzar()
            return resultado
        elif self.listaLexico[self.posicion].obtenertoken() == 13:  # Constante
            resultado = self.listaLexico[self.posicion].obtenercadena()
            self.avanzar()
            return resultado
        elif self.listaLexico[self.posicion].obtenertoken() == 4:  # "("
            self.avanzar()
            expresion = self.expresion_matematica()
            self.emparejar(5)  # ")"
            return expresion
        else:
            # Avanzar la posición en caso de otro token no esperado
            self.avanzar()
            return None



    def termino(self):
        factor1 = self.factor()
        while self.listaLexico[self.posicion].obtenertoken() in [14, 16]:  # Operadores de multiplicación o división
            operador = self.listaLexico[self.posicion].obtenercadena()
            self.avanzar()
            factor2 = self.factor()
            factor1 = f"({factor1} {operador} {factor2})"
        return factor1

    def expresion_matematica(self):
        termino1 = self.termino()
        while self.listaLexico[self.posicion].obtenertoken() in [14, 16]:  # Operadores de suma o resta
            operador = self.listaLexico[self.posicion].obtenercadena()
            self.avanzar()
            termino2 = self.termino()
            termino1 = f"({termino1} {operador} {termino2})"
        return termino1

    def precedencia(self, operador):
        if operador in ['+', '-']:
            return 1
        elif operador in ['*', '/']:
            return 2
        return 0

    def declaracion_variable(self):
        tipo_dato = self.listaLexico[self.posicion].obtenercadena()
        self.avanzar()
        nombre_variable = self.listaLexico[self.posicion].obtenercadena()
        self.emparejar(1)  # "ID"

        if self.listaLexico[self.posicion].obtenertoken() == 8:  # "="
            self.avanzar()
            print("2-----------Análisis de expresión matemática.", self.listaLexico[self.posicion].obtenercadena())
            valor = self.analizar_expresion()
            self.emparejar(2)  # ";"
            if valor is not None:
                print(f"Declaración de variable con inicialización válida: {tipo_dato} {nombre_variable} = {valor};")
                self.agregar_error(f"Declaración de variable con inicialización válida: {tipo_dato} {nombre_variable} = {valor};")
        else:
            self.emparejar(2)  # ";"
            print(f"Declaración de variable sin inicialización válida: {tipo_dato} {nombre_variable};")
            self.agregar_error(f"Declaración de variable sin inicialización válida: {tipo_dato} {nombre_variable};")

    def analizar_condicional(self):
        self.emparejar(9)  # "if"
        self.emparejar(4)  # "("
        self.analizar_expresion()
        self.emparejar(5)  # ")"
        print("Análisis de estructura condicional.")
        # Implementa el análisis del bloque de código dentro del if

    def analizar_bucle(self):
        self.emparejar(10)  # "while"
        self.emparejar(4)  # "("
        self.analizar_expresion()
        self.emparejar(5)  # ")"
        print("Análisis de estructura de bucle.")
        # Implementa el análisis del bloque de código dentro del while


# Ejemplo de uso
lexico1 = Lexico("int", 0, "Palabra reservada")
lexico2 = Lexico("x", 1, "ID")
lexico3 = Lexico("=", 8, "Operador de asignación")
lexico4 = Lexico("4", 13, "Constante")
lexico5 = Lexico(";", 2, "Punto y coma")

lista_lexico = [lexico1, lexico2, lexico3, lexico4, lexico5]

analizador_sintactico = Sintactico(lista_lexico)
analizador_sintactico.analizar_expresion()




class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setFixedSize(1200, 650)
        self.setWindowTitle("Analizador léxico y sintáctico")

        self.tablaResultados = QTableWidget(self)

        if self.tablaResultados.columnCount() < 3:
            self.tablaResultados.setColumnCount(3)

        __qtablewidgetitem = QTableWidgetItem("TOKEN")
        self.tablaResultados.setHorizontalHeaderItem(1, __qtablewidgetitem)
        __qtablewidgetitem = QTableWidgetItem("CADENA")
        self.tablaResultados.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem = QTableWidgetItem("DESCRIPCIÓN")
        self.tablaResultados.setHorizontalHeaderItem(2, __qtablewidgetitem)

        self.tablaResultados.setColumnWidth(0, 165)
        self.tablaResultados.setColumnWidth(1, 165)
        self.tablaResultados.setColumnWidth(2, 180)
        self.tablaResultados.setGeometry(QRect(20, 310, 560, 300))
        # ---------------------------------------------------------------
        self.inputTexto = QTextEdit(self)
        self.inputTexto.setGeometry(QRect(20, 20, 560, 200))
        font = QFont()
        font.setPointSize(15)
        self.inputTexto.setFont(font)
        #----------------------------------------------------------------
        self.inputTexto_3 = QTextEdit(self)
        self.inputTexto_3.setGeometry(QRect(610, 20, 560, 200))
        font = QFont()
        font.setPointSize(15)
        #----------------------------------------------------------------
        self.boton = QPushButton("VALIDAR", self)
        self.boton.setGeometry(QRect(550, 240, 100, 50))
        #----------------------------------------------------------------
        self.boton_Abrir = QPushButton("ABRIR", self)
        self.boton_Abrir.setGeometry(QRect(20, 240, 100, 50))
        #----------------------------------------------------------------      
        #Genera un cuadro en el punto 600, 310 con un tamaño de 570, 300 para salida de texto
        self.inputTexto_2 = QTextEdit(self)
        self.inputTexto_2.setGeometry(QRect(610, 310, 560, 300))
        font = QFont()
        font.setPointSize(15)
        self.inputTexto_2.setFont(font)
        self.inputTexto_2.setReadOnly(True)

        self.boton.clicked.connect(self.analizar)

    def analizar(self):
        # Prueba para imprimir
        #self.inputTexto_2.setText("Error de sintaxis. Declaración de variable inválida.")
        cadena = str(self.inputTexto.toPlainText())
        listaLexico = list()
        i = 0
        size = len(cadena)
        cadena = cadena + " "
        cadenaTemp = ""
        
        while i < size:
            cadenaTemp = ""
            # Si es una letra
            if cadena[i].isalpha() == True:
                # Ciclo que recorre la cadena
                while cadena[i].isalpha() == True or cadena[i].isdigit() == True: # Si es una letra o un digito
                    # Si es una letra
                    if cadena[i] == " ":
                        break
                    cadenaTemp = cadenaTemp + cadena[i]
                    i = i+1
                    if i==size:
                        break
                # Si la cadena es una palabra reservada
                if cadenaTemp == "if": # Si es if
                    tiposDeDato = Lexico(cadenaTemp, 9, "IF")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "while": # Si es while
                    tiposDeDato = Lexico(cadenaTemp, 10, "WHILE")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "return": # Si es return
                    tiposDeDato = Lexico(cadenaTemp, 11, "RETURN")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "else": # Si es else
                    tiposDeDato = Lexico(cadenaTemp, 12, "ELSE")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "int":  # Si es int
                    tiposDeDato = Lexico(cadenaTemp, 0, "Tipo de dato")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "float": # Si es float
                    tiposDeDato = Lexico(cadenaTemp, 0, "Tipo de dato")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "char": # Si es char
                    tiposDeDato = Lexico(cadenaTemp, 0, "Tipo de dato")
                    listaLexico.append(tiposDeDato)
                elif cadenaTemp == "void": # Si es void
                    tiposDeDato = Lexico(cadenaTemp, 0, "Tipo de dato")
                    listaLexico.append(tiposDeDato)
                else:
                    tiposDeDato = Lexico(cadenaTemp, 1, "ID")
                    listaLexico.append(tiposDeDato)
            # Si es un digito
            elif cadena[i].isdigit() == True:
                while cadena[i].isdigit() == True:
                    cadenaTemp = cadenaTemp + cadena[i]
                    i = i+1
                    if i==size:
                        break
                tiposDeDato = Lexico(cadenaTemp, 13, "Constante")
                listaLexico.append(tiposDeDato)
            # Si es un caracter de tipo operarador logico    
            elif (cadena[i] == "|" and cadena[i+1] == "|") or (cadena[i] == "&" and cadena[i+1] == "&"):
               cadenaTemp = cadena[i] + cadena[i+1]
               tiposDeDato = Lexico(cadenaTemp, 15, "Operador logico")
               listaLexico.append(tiposDeDato)
               i = i +2
            # Si es un caracter de tipo operador suma
            elif cadena[i] == "+" or cadena[i] == "-":
                cadenaTemp = cadena[i]
                tiposDeDato = Lexico(cadenaTemp, 14, "Operador suma")
                listaLexico.append(tiposDeDato)
                i = i +1
            
            # Si es un caracter de tipo operador multiplicacion
            elif cadena[i] == "*" or cadena[i] == "/":
                cadenaTemp = cadena[i]
                tiposDeDato = Lexico(cadenaTemp,16, "Operador multiplicación ")
                listaLexico.append(tiposDeDato)
                i = i +1
            # Si es un caracter de tipo operador relacional
            elif (cadena[i] == "=" and cadena[i+1] == "=") or (cadena[i] == "<" and cadena[i+1] == "=") or (cadena[i] == ">" and cadena[i+1] == "=") or (cadena[i] == "!" and cadena[i+1] == "="):
                cadenaTemp = cadena[i] + cadena[i+1]
                tiposDeDato = Lexico(cadenaTemp, 17, "Operador relacional")
                listaLexico.append(tiposDeDato)
                i = i +2
            # Si es un caracter de tipo operador relacional
            elif cadena[i] == "<" or cadena[i] == ">":
                cadenaTemp = cadena[i]
                tiposDeDato = Lexico(cadenaTemp, 17, "Operador relacional ")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Sie es un $
            elif cadena[i] == "$":
                cadenaTemp = "$"
                tiposDeDato = Lexico(cadenaTemp, 18, "$")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un ;
            elif cadena[i] == ";":
                cadenaTemp = ";"
                tiposDeDato = Lexico(cadenaTemp, 2, "Punto y coma")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es una ,
            elif cadena[i] == ",":
                cadenaTemp = ","
                tiposDeDato = Lexico(cadenaTemp, 3, "Coma")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un (
            elif cadena[i] == "(":
                cadenaTemp = "("
                tiposDeDato = Lexico(cadenaTemp, 4, "Parentesis izquierdo")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un )
            elif cadena[i] == ")":
                cadenaTemp = ")"
                tiposDeDato = Lexico(cadenaTemp, 5, "Parentesis derecho")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un {
            elif cadena[i] == "{":
                cadenaTemp = "{"
                tiposDeDato = Lexico(cadenaTemp, 6, "Llave izquierda")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un }
            elif cadena[i] == "}":
                cadenaTemp = "}"
                tiposDeDato = Lexico(cadenaTemp, 7, "Llave derecha")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un =
            elif cadena[i] == "=":
                cadenaTemp = "="
                tiposDeDato = Lexico(cadenaTemp, 8, "Igual")
                listaLexico.append(tiposDeDato)
                i = i + 1
            # Si es un espacio
            elif cadena[i] == " ":
                i = i + 1
            # Si es un caracter invalido
            else:
                i = i+1

        row = 0
        self.tablaResultados.setRowCount(len(listaLexico))
        for tiposDeDato in listaLexico:
            aux = tiposDeDato.obtenercadena()
            aux2 = tiposDeDato.obtenertoken()
            aux3 = tiposDeDato.obtenerdescripcion()
            self.tablaResultados.setItem(row, 0, QtWidgets.QTableWidgetItem(str(aux)))
            self.tablaResultados.setItem(row, 1, QtWidgets.QTableWidgetItem(str(aux2)))
            self.tablaResultados.setItem(row, 2, QtWidgets.QTableWidgetItem(str(aux3)))
            row = row + 1

        # Luego, iniciamos el análisis sintáctico
        analizador_sintactico = Sintactico(listaLexico)
        print("Iniciando análisis sintáctico...") 
        analizador_sintactico.analizar_expresion()

        if not analizador_sintactico.error:
            print("Análisis sintáctico completado sin errores.")

        self.inputTexto_2.clear()
        print("Errores sintácticos:")
        for error in analizador_sintactico.errores:
            print(error)
            self.inputTexto_2.append(error)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    app.exec()

x = 4;
y = 0; 
x + 3; 
x + y;
printf(x);
