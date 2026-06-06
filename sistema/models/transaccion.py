from datetime import now
from pydantic import BaseModel

class Transaccion:
    def __init__(self, numero_transaccion: str, numero_cajero: str, numero_cuenta: str, monto: float, tipo: str):
        self.numero_transaccion = numero_transaccion 
        self.numero_cajero = numero_cajero 
        self.numero_cuenta = numero_cuenta 
        self.monto = monto
        self.tipo = tipo
        self.fecha = now().strftime("%Y-%m-%d %H:%M:%S")
    
class TransaccionSchema(BaseModel):

    numero_transaccion: str
    numero_cajero: str
    numero_cuenta: str
    monto: float
    tipo: str

