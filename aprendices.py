import json
from os import system
from colorama import Fore, init
import tabulate
import fichas

init(autoreset=True)

# Menu de opciones
def menu():
    
    print("\nMenu de opciones\n")
    print("A. Crear ficha")
    print("B. Eliminar ficha")
    print("C. Agregar aprendiz")
    print("D. Eliminar aprendiz")
    print("E. Actualizar aprendiz")
    print("F. Visualizar aprendiz")
    print("G. Listar aprendices por ficha")
    print("H. Salir del menu\n")

    opcion = input("Mi opcion es: ").strip().upper()

    if opcion.isalpha() and opcion in ('A','B','C','D','E','F','G','H'):
        return opcion
    
    else:
        print(f"{Fore.RED}Opcion incorrecta del menu!")
        control_flujo()
        return menu()


# limpiar la pantalla
def control_flujo():
    input("Presione Enter para continuar...")
    system('cls')


# Comprueba si hay algun aprendiz en la lista de diccionarios de las identificaciones
def comprobacion_aprendices(identificacion, numeros_identificaciones):
        identificacion_switche = True
        for diccionario in numeros_identificaciones:
            if diccionario['identificacion'] == identificacion:
                identificacion_switche = False
                break
        return identificacion_switche


# Abro y cargo los diccionarios del json de identificaciones
def abrir_json_aprendices():
        global numeros_identificaciones
        try:
            with open('identificaciones.json','r') as archivo_json:
                numeros_identificaciones = json.load(archivo_json)
        except FileNotFoundError:
            numeros_identificaciones = []
        return numeros_identificaciones


# Actualizacion del json de las identificaciones de los aprendices
def actualizar_json_aprendices(numeros_identificaciones):
    with open('identificaciones.json', 'w') as archivo_json:
        json.dump(numeros_identificaciones, archivo_json)


# Eliminar aprendices de alguna ficha
def eliminar_aprendices_ficha(ficha_eliminar):
    numeros_identificaciones_viejas = abrir_json_aprendices()

    numeros_identificaciones = [diccionario for diccionario in numeros_identificaciones_viejas if diccionario['numero_ficha'] != ficha_eliminar]

    actualizar_json_aprendices(numeros_identificaciones)


# Agregar aprendiz a una ficha
def agregar_aprendiz(cursor, conexion):
    print(f"\n{Fore.MAGENTA}Agregar un aprendiz\n")
    numeros_fichas = fichas.abrir_json_fichas()
    ficha = int(input("Ingrese la ficha: "))
    ficha_switch = fichas.comprobacion_ficha(ficha, numeros_fichas)
    if not ficha_switch:
        identificacion = int(input("Ingrese la identificación: "))
        numeros_identificaciones = abrir_json_aprendices()
        
        identificacion_switche = comprobacion_aprendices(identificacion, numeros_identificaciones)
        if identificacion_switche:
            nombre = input("Ingrese el nombre: ")
            apellido = input("Ingrese el apellido: ")
            edad = int(input("Ingrese la edad: "))
            telefono = int(input("Ingrese la teléfono: "))
            correo = input("Ingrese el correo: ")
            sql_aprendices = "INSERT INTO aprendices(id_aprendiz, nombre, apellido, edad, telefono, correo, programa_formacion, numero_ficha) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
            valores = [identificacion, nombre, apellido, edad, telefono, correo,"", ficha]
            cursor.execute(sql_aprendices, valores)
            conexion.commit()
            numeros_identificaciones.append({'identificacion':identificacion, 'numero_ficha': ficha})
            actualizar_json_aprendices(numeros_identificaciones)
            sql = """UPDATE aprendices
                    JOIN fichas	ON aprendices.numero_ficha = fichas.numero_ficha
                    SET aprendices.programa_formacion = fichas.programa_formacion"""
            cursor.execute(sql)
            conexion.commit()

            print(f"\n{Fore.GREEN}El aprendiz fue agregado correctamente!\n")
        else:
            print(f"{Fore.RED}El aprendiz ya esta registrada en alguna ficha!")
    
    else:
        print(f"{Fore.RED}Ficha no existente!")


# Funcion que elimina un aprendiz de la base de datos y la identificacion del JSON
def eliminar_aprendices(cursor, conexion):
    print(f"\n{Fore.MAGENTA}Eliminar algun aprendiz!\n")
    numeros_identificaciones = abrir_json_aprendices()
    identificacion = int(input("Ingrese la identificacion del aprendiz a eliminar: "))

    eliminar_switch = comprobacion_aprendices(identificacion, numeros_identificaciones)


    if not eliminar_switch:
        sql = f"DELETE FROM aprendices WHERE id_aprendiz = {identificacion}"
        cursor.execute(sql)
        conexion.commit()

        for indice,diccionario in enumerate(numeros_identificaciones):
            if diccionario['identificacion'] == identificacion:
                numeros_identificaciones.pop(indice)
                break

        actualizar_json_aprendices(numeros_identificaciones)
        print(f"\n{Fore.GREEN}Aprendiz eliminado correctamente!\n")
    else:
        print(f"{Fore.RED}Aprendiz no existente!")


# Funcion para actualizar datos de aprendices
def actualizar_aprendices(cursor, conexion):
    print(f"\n{Fore.MAGENTA}Actualización de datos de algun aprendiz!\n")
    numeros_identificaciones = abrir_json_aprendices()
    identificacion = int(input("Ingrese la identificacion del aprendiz: "))

    actualizar_switch = comprobacion_aprendices(identificacion, numeros_identificaciones)

    if not actualizar_switch:
        sql = "UPDATE aprendices SET edad = %s, telefono = %s, correo = %s WHERE id_aprendiz = %s"
        edad = int(input("Ingrese la edad: "))
        telefono = int(input("Ingrese la teléfono: "))
        correo = input("Ingrese el correo: ")
        valores = (edad, telefono, correo, identificacion)
        cursor.execute(sql, valores)
        conexion.commit()

        print(f"\n{Fore.GREEN}Datos actualizados correctamente!\n")
    else:
        print(f"{Fore.RED}Aprendiz no existente!")


# Funcion para visualizar los datos de un aprendiz
def visualizar_aprendices(cursor, conexion):
    print(f"\n{Fore.MAGENTA}Visualización de datos del algún aprendiz!\n")
    numeros_identificaciones = abrir_json_aprendices()
    identificacion = int(input("Ingrese la identificación: "))

    visualizar_switch = comprobacion_aprendices(identificacion, numeros_identificaciones)

    if not visualizar_switch:
        sql = f"SELECT * FROM aprendices WHERE id_aprendiz = {identificacion}"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print()
        print(tabulate.tabulate(datos, ("Identificacion", "Nombre", "Apellido", "Edad", "Teléfono", "Correo", "Programa", "# ficha"), tablefmt='fancy_grid'))
        print()
    else:
        print(f"{Fore.RED}Aprendiz no existente!")
        