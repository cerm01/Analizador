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
        self.errores = [];
    
    def agregar_error(self, mensaje):
        self.errores.append(mensaje)

    def analizar(self):
        while self.posicion < len(self.listaLexico):
            print(f"Sintatico: {self.listaLexico[self.posicion].obtenercadena(), self.listaLexico[self.posicion].obtenertoken()}")
            print(f"Posicion: {self.posicion}")
            print(f"TOtal: {len(self.listaLexico)}")

            if self.error:
                return
            
            if self.listaLexico[self.posicion].obtenercadena() in ["int", "float", "char", "void"]:
                self.declaracion_variable()
            elif self.listaLexico[self.posicion].obtenercadena() == "if":
                self.analizar_condicional()
            elif self.listaLexico[self.posicion].obtenercadena() == "while":
                self.analizar_bucle()
            elif self.listaLexico[self.posicion].obtenertoken() == 1:  # ID
                self.analizar_expresion()
            elif (self.listaLexico[self.posicion].obtenertoken() == 2 and self.posicion == len(self.listaLexico) - 1):  # ";" (fin de instrucción)
                print("Análisis sintáctico completado sin errores.")
                self.agregar_error("Análisis sintáctico completado sin errores.")
                return
            else:
                self.error = True
                print("Error de sintaxis. Se esperaba una declaración, una expresión o una estructura de control.")
                self.agregar_error("Error de sintaxis. Se esperaba una declaración, una expresión o una estructura de control.")

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
            print(f"Error de sintaxis. Se esperaba '{valor_esperado}' en lugar de '{self.listaLexico[self.posicion].obtenercadena()}'")
            self.agregar_error(f"Error de sintaxis. Se esperaba '{valor_esperado}' en lugar de '{self.listaLexico[self.posicion].obtenercadena()}'")

    def declaracion_variable(self):
        tipo_dato = self.listaLexico[self.posicion].obtenercadena()
        self.avanzar()
        nombre_variable = self.listaLexico[self.posicion].obtenercadena()
        self.emparejar(1)  # "ID"

        if self.listaLexico[self.posicion].obtenertoken() == 8:  # "="
            self.avanzar()
            valor = self.analizar_expresion()
            self.emparejar(2)  # ";"
            if valor is not None:
                print(f"Declaración de variable con inicialización válida: {tipo_dato} {nombre_variable} = {valor};")
                self.agregar_error(f"Declaración de variable con inicialización válida: {tipo_dato} {nombre_variable} = {valor};")
        else:
            self.emparejar(2)  # ";"
            print(f"Declaración de variable sin inicialización válida: {tipo_dato} {nombre_variable};")
            self.agregar_error(f"Declaración de variable sin inicialización válida: {tipo_dato} {nombre_variable};")

    def analizar_expresion(self):
        pila_operadores = []
        pila_operandos = []
        operador = ""
        operand1 = ""
        operand2 = ""

        while self.posicion < len(self.listaLexico):
            if self.listaLexico[self.posicion].obtenertoken() == 1:  # ID
                pila_operandos.append(self.listaLexico[self.posicion].obtenercadena())
                self.avanzar()
            elif self.listaLexico[self.posicion].obtenertoken() == 13:  # Constante
                pila_operandos.append(self.listaLexico[self.posicion].obtenercadena())
                self.avanzar()
            elif self.listaLexico[self.posicion].obtenertoken() in [14, 16]:  # Operadores de suma o multiplicación
                while pila_operadores and pila_operadores[-1] in ['+', '-', '*', '/'] and self.precedencia(
                        self.listaLexico[self.posicion].obtenercadena()) <= self.precedencia(pila_operadores[-1]):
                    operador = pila_operadores.pop()
                    operand2 = pila_operandos.pop()
                    operand1 = pila_operandos.pop()
                    pila_operandos.append(f"({operand1} {operador} {operand2})")
                pila_operadores.append(self.listaLexico[self.posicion].obtenercadena())
                self.avanzar()
            elif self.listaLexico[self.posicion].obtenertoken() == 4:  # "("
                pila_operadores.append(self.listaLexico[self.posicion].obtenercadena())
                self.avanzar()
            elif self.listaLexico[self.posicion].obtenertoken() == 5:  # ")"
                while pila_operadores and pila_operadores[-1] != '(':
                    operador = pila_operadores.pop()
                    operand2 = pila_operandos.pop()
                    operand1 = pila_operandos.pop()
                    pila_operandos.append(f"({operand1} {operador} {operand2})")
                if pila_operadores and pila_operadores[-1] == '(':
                    pila_operadores.pop()
                self.avanzar()
            elif self.listaLexico[self.posicion].obtenertoken() == 2:  # ";"
                while pila_operadores:
                    operador = pila_operadores.pop()
                    operand2 = pila_operandos.pop()
                    operand1 = pila_operandos.pop()
                    pila_operandos.append(f"({operand1} {operador} {operand2})")
                if len(pila_operandos) == 1:
                    resultado = pila_operandos[0]
                    print(f"Expresión matemática válida: {resultado};")
                    return resultado
                else:
                    self.error = True
                    print("Error de sintaxis en la expresión matemática.")
                    self.agregar_error(f"Error de sintaxis en la expresión matemática. {operand1} {operador} {operand2}; " )
                    return None
            else:
                self.error = True
                print("Error de sintaxis en la expresión matemática.")
                self.agregar_error("Error de sintaxis en la expresión matemática.")
                return None

    def precedencia(self, operador):
        if operador in ['+', '-']:
            return 1
        elif operador in ['*', '/']:
            return 2
        return 0

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


class semantico(object):
    def __init__(self, listaLexico):
        self.listaLexico = listaLexico
        self.posicion = 0
        self.error = False
        self.errores = []
    
    def agregar_error(self, mensaje):
        self.errores.append(mensaje)

    def analizar(self):
        #Ids no declarados
        tipoDato = list()
        ids = list()
        declarados = list()
        utilizados = list()
        # Verficar si en la listaLexico exsite un token 0 (Tipo de dato)
        for i in range(len(self.listaLexico)):
            if self.listaLexico[i].obtenertoken() == 0:
                #Obtener la posicion del token 0 (Tipo de dato) sumar 1 y agregarlo a la lista cadena
                tipoDato.append(i+1)
        # Verficar si en la listaLexico exsite un token 1 (ID)
        for i in range(len(self.listaLexico)):
            if self.listaLexico[i].obtenertoken() == 1:
                #Obtener la posicion del token 1 (ID) y agregarlo a la lista ids
                ids.append(i)

        # Verificar si la lista cadena esta vacia y la de ids no
        if len(tipoDato) == 0 and len(ids) != 0:
            # Si es asi mostrar un mensaje de error
            self.agregar_error("Error semántico: No se ha declarado ninguna variable")
            self.error = True
        else:
            # Comparar la lista tipoDato con la lista ids, si la cadena de la lista ListaLexico en la posicion i de la lista tipoDato es igual a la cadena de la lista ListaLexico en la posicion i de la lista ids
            for i in range(len(tipoDato)):
                aux = self.listaLexico[tipoDato[i]].obtenercadena()
                declarados.append(aux)
            for i in range (len(ids)):
                aux2 = self.listaLexico[ids[i]].obtenercadena()
                utilizados.append(aux2)
                if aux2 not in declarados:
                    self.agregar_error("Error semántico: La variable " + aux2 + " no ha sido declarada") 
                    self.error = True

        # Ids declarados pero no usados
        for i in range(len(declarados)):
            aux = declarados[i]
            # Ver cauntas veces se repite la cadena aux en la lista utilizados
            contador = utilizados.count(aux)
            # Si el contador es menor a 2 mostrar un mensaje de error
            if contador < 2:
                self.agregar_error("Error semántico: La variable " + aux + " no ha sido usada")
                self.error = True

        


                    

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
        self.inputTexto_3.setFont(font)
        #----------------------------------------------------------------
        self.boton = QPushButton("VALIDAR", self)
        self.boton.setGeometry(QRect(550, 240, 100, 50))
        #----------------------------------------------------------------
        self.boton_Abrir = QPushButton("ABRIR", self)
        self.boton_Abrir.setGeometry(QRect(20, 240, 100, 50))
        #----------------------------------------------------------------
        self.boton_Guardar = QPushButton("GUARDAR", self)
        self.boton_Guardar.setGeometry(QRect(150, 240, 100, 50))
        #----------------------------------------------------------------      
        #Genera un cuadro en el punto 600, 310 con un tamaño de 570, 300 para salida de texto
        self.inputTexto_2 = QTextEdit(self)
        self.inputTexto_2.setGeometry(QRect(610, 310, 560, 300))
        font = QFont()
        font.setPointSize(15)
        self.inputTexto_2.setFont(font)
        self.inputTexto_2.setReadOnly(True)

        #----------------------------------------------------------------
        # Conectamos la señal del boton con el metodo analizar
        self.boton.clicked.connect(self.analizar)
        #----------------------------------------------------------------
        # Conectamos la señal del boton con el metodo abrirArchivo
        self.boton_Abrir.clicked.connect(self.abrirArchivo)
        #----------------------------------------------------------------
        # Conectamos la señal del boton con el metodo guardarArchivo
        self.boton_Guardar.clicked.connect(self.guardarArchivo)
        #----------------------------------------------------------------

    def guardarArchivo(self):
        # Si y solo si se abierto un archivo con el boton abrir se podra modificar el archivo y guardarlo con el boton guardar es decir como un sobre escribir  
        if self.inputTexto.toPlainText() != "":
            # Generar una exploración de archivos para guardar un archivo
            nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "", "All Files (*);;Python Files (*.py)")
            # Abrir el archivo en modo escritura
            archivo = open(nombreArchivo, "w")
            # Escribir el contenido del cuadro de texto en el archivo
            archivo.write(self.inputTexto.toPlainText())
            # Cerrar el archivo
            archivo.close()
        else:
            # Si no se ha abierto un archivo con el boton abrir se mostrara un mensaje de error
            QMessageBox.warning(self, "Error", "No se ha abierto un archivo", QMessageBox.Ok)


    def abrirArchivo(self):
        # Generar una exploración de archivos para abrir un archivo
        nombreArchivo, _ = QFileDialog.getOpenFileName(self, "Abrir Archivo", "", "All Files (*);;Python Files (*.py)")
        # Abrir el archivo en modo lectura
        archivo = open(nombreArchivo, "r")
        # Leer todo el contenido del archivo
        contenido = archivo.read()
        # Cerrar el archivo
        archivo.close()
        # Mostrar el contenido en el cuadro de texto
        self.inputTexto.setText(contenido)

    

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
                #Verifcar si este es de tipo entero o flotante
                while cadena[i].isdigit() == True:
                    cadenaTemp = cadenaTemp + cadena[i]
                    i = i+1
                    if i==size:
                        break
                if cadena[i] == ".":
                    cadenaTemp = cadenaTemp + cadena[i]
                    i = i+1
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

        #Imprimir en consola la listaLexico
        print("Lista de tokens:")
        for tiposDeDato in listaLexico:
            print(tiposDeDato)

        # Luego, iniciamos el análisis sintáctico
        analizador_sintactico = Sintactico(listaLexico)
        print("Iniciando análisis sintáctico...") 
        analizador_sintactico.analizar()

        if not analizador_sintactico.error:
            print("Análisis sintáctico completado sin errores.")

        self.inputTexto_2.clear()
        print("Errores sintácticos:")
        for error in analizador_sintactico.errores:
            print(error)
            self.inputTexto_2.append(error)

        # Luego, iniciamos el análisis semántico
        analizador_semantico = semantico(listaLexico)
        analizador_semantico.analizar()

        if not analizador_semantico.error:
            self.inputTexto_3.clear()
            self.inputTexto_3.append("Análisis semántico completado sin errores.")
        else:
            self.inputTexto_3.clear()
            for error in analizador_semantico.errores:
                self.inputTexto_3.append(error)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = MainWindow()
    ventana.show()
    app.exec()
