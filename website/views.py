import re
from flask import Blueprint, render_template, request

views = Blueprint('views', __name__)

def analizar_codigo(codigo):
    reservadas = ["programa", "int", "read", "printf", "end"]
    operadores = ["+", "-", "*", "/"]
    parentesis_abre = ["(", "{", "["]
    parentesis_cierra = [")", "}", "]"]
    punto_coma = [";"]
    coma = [","]
    errores = []
    tokens_totales = []
    lineas = codigo.split("\n")

    for i, linea in enumerate(lineas, start=1):  
        # Inicia el contador de líneas en 1
        linea_tokens = []

        # Buscar palabras reservadas
        for token in reservadas:
            matches = re.findall(r"\b{}\b".format(token), linea)
            for match in matches:
                linea_tokens.append((i, match, "Reservada", "", ""))

        # Buscar operadores
        for token in operadores:
            matches = linea.count(token)
            for _ in range(matches):
                linea_tokens.append((i, token, "Operador", "", ""))

        # Buscar paréntesis de apertura
        for token in parentesis_abre:
            matches = linea.count(token)
            for _ in range(matches):
                linea_tokens.append((i, token, "Paréntesis", "", ""))

        # Buscar paréntesis de cierre
        for token in parentesis_cierra:
            matches = linea.count(token)
            for _ in range(matches):
                linea_tokens.append((i, token, "Paréntesis", "", ""))

        # Buscar punto y coma
        for token in punto_coma:
            matches = linea.count(token)
            for _ in range(matches):
                linea_tokens.append((i, token, "Punto y coma", "", ""))

        # Buscar coma
        for token in coma:
            matches = linea.count(token)
            for _ in range(matches):
                linea_tokens.append((i, token, "Coma", "", ""))

        # Buscar identificadores
        identificadores = re.findall(r"\b[a-zA-Z][a-zA-Z0-9_]*\b", linea)
        for identificador in identificadores:
            print("Identificador encontrado:", identificador.lower())
            for keyword in ["suma", "resta", "multiplicacion", "division"]:
                if keyword.startswith(identificador.lower()):
                    if identificador.lower() != keyword:
                        print("Palabra clave incompleta encontrada:", identificador.lower())
                        errores.append((i, identificador, "Error", "Palabra incorrecta", ""))
                        break  # Salir del bucle for keyword
                    else:
                        print("Palabra clave encontrada:", identificador.lower())
                        linea_tokens.append((i, identificador, "Identificador", "", ""))
                        break  # Salir del bucle for keyword
            else:
                linea_tokens.append((i, identificador, "Identificador", "", ""))

        tokens_totales.extend(linea_tokens)

    # Análisis sintáctico
    errores_sintacticos = analizar_sintaxis(lineas)

    return tokens_totales, errores, errores_sintacticos

def analizar_sintaxis(lineas):
    errores_sintacticos = []
    pila_llaves = []

    for i, linea in enumerate(lineas, start=1):
        # Verificar la estructura de system.out.print
        if 'system.out.print' in linea:
            if not re.match(r'.*system\.out\.print\s*\(.*\)\s*;', linea):
                errores_sintacticos.append((i, linea, "Error Sintáctico", "Estructura de system.out.print incorrecta"))
        else:
            if 'print' in linea or 'println' in linea:
                errores_sintacticos.append((i, linea, "Error Sintáctico", "Debe usar únicamente 'system.out.print'"))

        # Verificar si falta ';'
        if not linea.strip().endswith(';') and not linea.strip().endswith('{') and not linea.strip().endswith('}') and 'for' not in linea:
            errores_sintacticos.append((i, linea, "Error Sintáctico", "Falta ';'"))

        # Verificar llaves '{' y '}'
        for char in linea:
            if char == '{':
                pila_llaves.append('{')
            elif char == '}':
                if pila_llaves and pila_llaves[-1] == '{':
                    pila_llaves.pop()
                else:
                    errores_sintacticos.append((i, linea, "Error Sintáctico", "Llave de cierre '}' sin llave de apertura correspondiente"))

    if pila_llaves:
        for j in range(len(pila_llaves)):
            errores_sintacticos.append((i, "Llave de apertura '{' sin llave de cierre correspondiente"))

    return errores_sintacticos

@views.route('/', methods=['GET', 'POST'])
def index():
    codigo = ""
    if request.method == 'POST':
        codigo = request.form['codigo']
        tokens_totales, errores, errores_sintacticos = analizar_codigo(codigo)

        # Validar si hay tokens para evitar errores de suma
        if not tokens_totales:
            return render_template('home.html', error="No se encontraron tokens en el código", codigo=codigo)

        # Inicializar los totales
        total_reservadas = 0
        total_identificadores = 0
        total_simbolos = 0
        total_operadores = 0

        # Calcular los totales
        for token in tokens_totales:
            if token[2] == "Reservada":
                total_reservadas += 1
            elif token[2] == "Identificador":
                total_identificadores += 1
            elif token[2] == "Paréntesis" or token[2] == "Punto y coma" or token[2] == "Coma":
                total_simbolos += 1
            elif token[2] == "Operador":
                total_operadores += 1

        # Total de tokens
        total_tokens = len(tokens_totales)

        if errores or errores_sintacticos:
            return render_template('home.html', errores=errores, errores_sintacticos=errores_sintacticos, codigo=codigo)

        return render_template('home.html', tokens=tokens_totales, total_reservadas=total_reservadas, total_identificadores=total_identificadores, total_simbolos=total_simbolos, total_operadores=total_operadores, total_tokens=total_tokens, codigo=codigo)
    
    return render_template('home.html', codigo=codigo)