class Singleton:
    _instancias = {}

    def __new__(cls, *args, **kwargs):
        if cls not in cls._instancias:
            cls._instancias[cls] = super().__new__(cls)
        
        return cls._instancias[cls]
    
class ConexionBD(Singleton):
    
    def __init__(self):
        if not hasattr(self, 'inicializado'):
            self._conexion = None
            self._conectar()
            self.inicializado = True

    def _conectar(self):
        pass