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

            fichas.crear_ficha(cursor, conexion)

        elif opcion == 'B':

            fichas.eliminar_ficha(cursor, conexion)

        elif opcion == 'C':

            aprendices.agregar_aprendiz(cursor, conexion)
        
        elif opcion == 'D':

            aprendices.eliminar_aprendices(cursor, conexion)

        elif opcion == 'E':

            aprendices.actualizar_aprendices(cursor, conexion)


        elif opcion == 'F':
            aprendices.visualizar_aprendices(cursor, conexion)


        elif opcion == 'G':
            print("Saliendo del menú...")
            input()
    
except Error as e:
    print(f"Ha ocurrido un error: {e}")