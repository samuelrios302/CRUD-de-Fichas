import json
import fichas as fichas

def abrir_json_fichas():
    global numeros_fichas
    try:
        with open('numeros_fichas.dat', 'r') as archivo_json:
            numeros_fichas = json.load(archivo_json)
    except FileNotFoundError:
        numeros_fichas = []
    return numeros_fichas


def actualizar_json_fichas():
    with open('numeros_fichas.dat', 'w') as archivo_json:
        json.dump(numeros_fichas, archivo_json)


def comprobacion_ficha(numero_ficha, numeros_fichas):
        ficha_switch = True
        for diccionario in numeros_fichas:
            if diccionario['numero_ficha'] == numero_ficha:
                ficha_switch = False
                break
        return ficha_switch


def crear_ficha(cursor, conexion):
        numeros_fichas = abrir_json_fichas()

        numero_ficha = int(input("Ingrese el numero de ficha: "))

        ficha_switch = fichas.comprobacion_ficha(numero_ficha, numeros_fichas) 

        if ficha_switch:

            sql = """INSERT INTO fichas(numero_ficha, programa_formacion, modalidad) VALUES (%s,%s,%s)"""
            programa_formacion = input("Ingrese el nombre del progama de formación: ")
            modalidad = input("Ingrese la modalidad: ")
            valores = [numero_ficha, programa_formacion, modalidad]
            cursor.execute(sql,valores)
            conexion.commit()

            numeros_fichas.append(
                {'numero_ficha':numero_ficha}
                )

            actualizar_json_fichas()
        else:
            print("Ficha ya existente!")


def eliminar_ficha(cursor, conexion):
        numeros_fichas = fichas.abrir_json_fichas()
        ficha_eliminar = int(input("Ingrese el numero de la ficha a eliminar: "))

        ficha_switch = True
        for indice,diccionario in enumerate(numeros_fichas):
            if diccionario['numero_ficha'] == ficha_eliminar:
                ficha_switch = False
                numeros_fichas.pop(indice)
                break
        
        if not ficha_switch:
            sql_estudiantes = f"""DELETE FROM aprendices WHERE numero_ficha = {ficha_eliminar}"""
            sql_ficha = f"""DELETE FROM fichas WHERE numero_ficha = {ficha_eliminar}"""

            cursor.execute(sql_estudiantes)
            conexion.commit()
            cursor.execute(sql_ficha)
            conexion.commit()

            fichas.actualizar_json_fichas()
        else:
            print("Ficha no encontrada!")