import mysql.connector

# Conexion entre python y mysql
def conexion_base_datos():
    conexion = mysql.connector.connect(
        host = "localhost",
        username = "Samuel",
        password = "1234",
        port = "3306",
        database = "sena")
    
    return conexion


# Verificar si la conexion ha sido creada corretamente
def verificar_conexion(conexion):
    if conexion.is_connected():
        print("Conexion exitosa a la base de datos")