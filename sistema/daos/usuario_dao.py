from config.database import ConexionDB
from models.usuario import Usuario

class UsuarioDao:
    def __init__(self):
        self.db = ConexionDB()
        self.conexion = self.db.obtener_conexion()

    def registrar_usuario(self, usuario: "Usuario"):

        cursor = self.conexion.cursor()
        try:

            sql = "INSERT INTO usuarios VALUES (%s, %s, %s)"
            valores = (usuario.dni, usuario.nombre, usuario.saldo)

            cursor.execute(sql, valores)
            self.conexion.commit()
            return True

        except Exception as e:
            self.conexion.rollback()
            print(f"Error en el DAO a la hora de registrar: {e}")
            return False
        finally:
            cursor.close()

    