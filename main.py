from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import QtWidgets
import sys

class Lexico(object):
    # Constructor de la clase
    def __init__(self, cadena, id, tipo):
        self.cadena = cadena
        self.token = id
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

    # Retorna la descripcion
    def obtenerdescripcion(self):
        return self.tipo

class Sintactico(object):
    def __init__(self, listaLexico):
        self.listaLexico = listaLexico
        self.posicion = 0
        self.error = False

    def analizar(self):
        self.declaracion_variable()

    def avanzar(self):
        self.posicion += 1
        if self.posicion >= len(self.listaLexico):
            self.posicion = len(self.listaLexico) - 1

    def emparejar(self, token_esperado):
        if self.listaLexico[self.posicion].obtenertoken() == token_esperado:
            self.avanzar()
        else:
            self.error = True
            valor_esperado = ""
            if token_esperado == 1:
                valor_esperado = "ID"
            elif token_esperado == 2:
                valor_esperado = ";"
            
            row = 0
            #self.tablaResultados.setItem(row, 0, QtWidgets.QTableWidgetItem(str("Hello")))
            print(f"Error de sintaxis. Se esperaba '{valor_esperado}' en lugar de '{self.listaLexico[self.posicion].obtenercadena()}'")

    def declaracion_variable(self):
        if self.listaLexico[self.posicion].obtenercadena() in ["int", "float", "char", "void"]:
            self.avanzar()
            self.emparejar(1) # "ID"
            self.emparejar(2) # ";"
        else:
            self.error = True
            print("Error de sintaxis. Declaración de variable inválida.")

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

        self.tablaResultados.setColumnWidth(0, 451)
        self.tablaResultados.setColumnWidth(1, 89)
        self.tablaResultados.setColumnWidth(2, 360)
        self.tablaResultados.setGeometry(QRect(20, 300, 940, 340))

        self.inputTexto = QTextEdit(self)
        self.inputTexto.setGeometry(QRect(40, 20, 380, 250))

        font = QFont()
        font.setPointSize(15)
        self.inputTexto.setFont(font)

        self.boton = QPushButton("VALIDAR", self)
        self.boton.setGeometry(QRect(440, 125, 100, 50))

        """
        self.inputTexto_2 = QTextEdit(self)
        self.inputTexto_2.setGeometry(QRect(560, 20, 380, 250))
        font = QFont()
        font.setPointSize(15)
        self.inputTexto_2.setFont(font)
        """
        self.boton.clicked.connect(self.analizar)

    def analizar(self):
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
        analizador_sintactico.analizar()

        if not analizador_sintactico.error:
            print("Análisis sintáctico completado sin errores.")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    app.exec()
