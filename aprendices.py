import json
from os import system
from colorama import Fore, init
import tabulate
import fichas as fichas

init(autoreset=True)

def menu():
    
    print("\nMenu de opciones\n")
    print("A. Crear ficha")
    print("B. Eliminar ficha")
    print("C. Agregar aprendiz")
    print("D. Eliminar aprendiz")
    print("E. Actualizar aprendiz")
    print("F. Visualizar aprendiz")
    print("G. Salir del menu\n")

    opcion = input("Mi opcion es: ").strip().upper()

    if opcion.isalpha() and opcion in ('A','B','C','D','E','F','G'):
        return opcion
    
    else:
        print(f"{Fore.RED}Opcion incorrecta del menu!")
        return menu()

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
            with open('identificaciones.dat','r') as archivo_json:
                numeros_identificaciones = json.load(archivo_json)
        except FileNotFoundError:
            numeros_identificaciones = []
        return numeros_identificaciones
    

def actualizar_json_aprendices():
    with open('identificaciones.dat', 'w') as archivo_json:
        json.dump(numeros_identificaciones, archivo_json)


def agregar_aprendiz(cursor, conexion):
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
            numeros_identificaciones.append({'identificacion':identificacion})
            actualizar_json_aprendices()
            sql = """UPDATE aprendices
                    JOIN fichas	ON aprendices.numero_ficha = fichas.numero_ficha
                    SET aprendices.programa_formacion = fichas.programa_formacion"""
            cursor.execute(sql)
            conexion.commit()

            sql = ""
        else:
            print(f"{Fore.RED}El aprendiz ya esta registrada en alguna ficha!")
    
    else:
        print(f"{Fore.RED}Ficha no existente!")

# Funcion que elimina un aprendiz de la base de datos y la identificacion del JSON
def eliminar_aprendices(cursor, conexion):
    
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

        actualizar_json_aprendices()

    else:
        print(f"{Fore.RED}Aprendiz no existente!")


def actualizar_aprendices(cursor, conexion):
    numeros_identificaciones = abrir_json_aprendices()
    identificacion = int(input("Ingrese la identificacion del aprendiz que desea actualizarle los datos: "))

    actualizar_switch = comprobacion_aprendices(identificacion, numeros_identificaciones)

    if not actualizar_switch:
        print("\nActualización de datos!\n")
        sql = "UPDATE aprendices SET edad = %s, telefono = %s, correo = %s WHERE id_aprendiz = %s"
        edad = int(input("Ingrese la edad: "))
        telefono = int(input("Ingrese la teléfono: "))
        correo = input("Ingrese el correo: ")
        valores = (edad, telefono, correo, identificacion)
        cursor.execute(sql, valores)
        conexion.commit()
    else:
        print(f"{Fore.RED}Aprendiz no existente!")

def visualizar_aprendices(cursor, conexion):
    print("\nVisualización de datos del algún aprendiz!\n")
    numeros_identificaciones = abrir_json_aprendices()
    identificacion = int(input("Ingrese la identificación: "))

    visualizar_switch = comprobacion_aprendices(identificacion, numeros_identificaciones)

    if not visualizar_switch:
        sql = f"SELECT * FROM aprendices WHERE id_aprendiz = {identificacion}"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print(tabulate.tabulate(datos, ("Identificacion", "Nombre", "Apellido", "Edad", "Teléfono", "Correo", "Programa", "# ficha"), tablefmt='fancy_grid'))
    else:
        print(f"{Fore.RED}Aprendiz no existente!")
        