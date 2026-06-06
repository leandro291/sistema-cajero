from datetime import datetime
from pydantic import BaseModel

class Transaccion:
    def __init__(self, numero_transaccion: str, numero_cajero: str, numero_cuenta: str, monto: float, tipo: str):
        self.numero_transaccion = numero_transaccion 
        self.numero_cajero = numero_cajero 
        self.numero_cuenta = numero_cuenta 
        self.monto = monto
        self.tipo = tipo
        self.fecha = datetime.now()

    def __str__(self):
        fecha_str = self.fecha.strftime("%d/%m/%Y %H:%M:%S")
        return str({
            "Numero de Transaccion" : self.numero_transaccion,
            "Numero de Cajero" : self.numero_cajero,
            "Numero de Cuenta" : self.numero_cuenta,
            "Monto" : self.monto,
            "Tipo" : self.tipo,
            "Fecha" : fecha_str
        })
    
class TransaccionSchema(BaseModel):

    numero_transaccion: str
    numero_cajero: str
    numero_cuenta: str
    monto: float
    tipo: str

