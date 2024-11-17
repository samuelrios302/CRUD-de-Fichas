from os import system
import conexion_basedatos
import fichas
import aprendices
from mysql.connector import Error

numeros_fichas = []   
numeros_identificaciones = []

try:
    conexion = conexion_basedatos.conexion_base_datos()
    conexion_basedatos.verificar_conexion(conexion)
    cursor = conexion.cursor()
    while True:
        aprendices.control_flujo()
        opcion = aprendices.menu()

        if opcion == 'A':

            system('cls')
            fichas.crear_ficha(cursor, conexion)

        elif opcion == 'B':

            system('cls')
            fichas.eliminar_ficha(cursor, conexion)

        elif opcion == 'C':

            system('cls')
            aprendices.agregar_aprendiz(cursor, conexion)
        
        elif opcion == 'D':

            system('cls')
            aprendices.eliminar_aprendices(cursor, conexion)

        elif opcion == 'E':

            system('cls')
            aprendices.actualizar_aprendices(cursor, conexion)


        elif opcion == 'F':

            system('cls')
            aprendices.visualizar_aprendices(cursor, conexion)


        elif opcion == 'G':
            system('cls')
            print("Saliendo del menú...")
            input()
            exit()
    
except Error as e:
    print(f"Ha ocurrido un error: {e}")