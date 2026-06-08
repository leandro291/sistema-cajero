import psycopg2
from utils.logger import Logger
class ConexionDB:

    _instancia = None

    def __new__(cls, *args):

        if cls._instancia is None:
            cls._instancia = super().__new__(cls)
        
        return cls._instancia
    
    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self._conexion = None
            self._conectar()

            self.inicializado = True
    
    def _conectar(self):
        try:
            self._conexion = psycopg2.connect(
                dbname='cajerodb',
                user='postgres',
                password='root',
                host='localhost',
                port='5432'
            )
            Logger.add_to_log(f"info", "Base de datos: Conexion exitosa a la base de datos PostgreSQL")
        except Exception as e:
            Logger.add_to_log(f"error", "Base de datos: Error al conectarse a la base de datos: {e}")
    
    def obtener_conexion(self):
        return self._conexion
    
    def cerrar_conexion(self):
        if self._conexion:
            self._conexion.close()
            Logger.add_to_log(f"error", "Base de datos: Conexion cerrada de forma segura")

if __name__ == "__main__":
    
    db1 = ConexionDB()

    print(db1.obtener_conexion)
    db1.cerrar_conexion()