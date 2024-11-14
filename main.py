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

    #fichas.crear_ficha(cursor, conexion)
    #fichas.eliminar_ficha(cursor, conexion)

    #aprendices.agregar_aprendiz(cursor, conexion)
    aprendices.eliminar_aprendices(cursor, conexion)
    
except Error as e:
    print(f"Ha ocurrido un error: {e}")