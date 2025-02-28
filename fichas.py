import json
from colorama import Fore, init
from tabulate import tabulate
import fichas 
import aprendices

init(autoreset=True)

# Abre y carga los diccionarios de todas las fichas almacenadas en el JSON
def abrir_json_fichas():
    global numeros_fichas
    try:
        with open('numeros_fichas.json', 'r') as archivo_json:
            numeros_fichas = json.load(archivo_json)
    except FileNotFoundError:
        numeros_fichas = []
    return numeros_fichas

# Actualizar el JSON con los nueva ficha registrada
def actualizar_json_fichas():
    with open('numeros_fichas.json', 'w') as archivo_json:
        json.dump(numeros_fichas, archivo_json)


# Comprobacion de una ficha existente
def comprobacion_ficha(numero_ficha, numeros_fichas):
        ficha_switch = True
        for diccionario in numeros_fichas:
            if diccionario['numero_ficha'] == numero_ficha:
                ficha_switch = False
                break
        return ficha_switch

# Crear una ficha
def crear_ficha(cursor, conexion):
        
        print(f"\n{Fore.MAGENTA}Creacion de fichas!\n")

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

            print(f"\n{Fore.GREEN}Ficha {numero_ficha} creada exitosamente!\n")
        else:
            print(f"{Fore.RED}Ficha ya existente!")


# Eliminar alguna ficha
def eliminar_ficha(cursor, conexion):  
        print(f"\n{Fore.MAGENTA}Eliminacion de fichas!\n")
        numeros_fichas = fichas.abrir_json_fichas()
        ficha_eliminar = int(input("Ingrese el numero de la ficha a eliminar: "))

        ficha_switch = True
        for indice,diccionario in enumerate(numeros_fichas):
            if diccionario['numero_ficha'] == ficha_eliminar:
                ficha_switch = False
                numeros_fichas.pop(indice)
                break
        
        if not ficha_switch:
            
            print(f"\n¿Quieres {Fore.RED}eliminarla{Fore.RESET} por completo? puede contener aprendices!\n")
            print("A. Si, quiero eliminarla")
            print("B. No, prefiero preservarla\n")
            opcion_menu = input("Mi opción es: ").upper().strip()
            if opcion_menu == 'A':
                # Sentencia para eliminar los aprendices de la ficha a eliminar
                sql_estudiantes = f"""DELETE FROM aprendices WHERE numero_ficha = {ficha_eliminar}"""
                
                # Sentencia para eliminar la ficha de la tabla de fichas
                sql_ficha = f"""DELETE FROM fichas WHERE numero_ficha = {ficha_eliminar}"""
                cursor.execute(sql_estudiantes)
                conexion.commit()
                cursor.execute(sql_ficha)
                conexion.commit()
                fichas.actualizar_json_fichas()
                sql = f"DELETE FROM aprendices WHERE numero_ficha = {ficha_eliminar}"
                cursor.execute(sql)
                conexion.commit()
                aprendices.eliminar_aprendices_ficha(ficha_eliminar)
                print(f"\n{Fore.GREEN}Ficha {ficha_eliminar} eliminada exitosamente!\n")
            elif opcion_menu == 'B':
                print(f"{Fore.MAGENTA}Se cancelo la eliminacion de la ficha")
            else:
                print(f"{Fore.RED}Opcion incorrecta! no se eliminará la ficha!")


        else:
            print(f"{Fore.RED}Ficha no encontrada!")

# Visualizar todos los aprendices de una ficha
def visualizar_ficha(cursor):
    print(f"\n{Fore.MAGENTA}Listar aprendices por ficha!\n")
    numeros_fichas = abrir_json_fichas()
    ficha_listar = int(input("Ingrese la ficha: "))
    swicth_ficha = comprobacion_ficha(ficha_listar,numeros_fichas)

    if not swicth_ficha:
        sql = f"SELECT * FROM aprendices WHERE numero_ficha = {ficha_listar}"
        cursor.execute(sql)
        datos = cursor.fetchall()
        print("")
        print(tabulate(datos,("Identificación", "Nombre", "Apellido", "Edad","Teléfono","Correo","Programa de formación","Numero de Ficha"),tablefmt='fancy_grid'))
    else:
        print(f"{Fore.RED}Ficha no existente!")
