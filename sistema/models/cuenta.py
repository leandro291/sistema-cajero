from pydantic import BaseModel, Field, field_validator, ValidationError
from .tarjeta import Tarjeta

class Cuenta:
    def __init__(self, numero_cuenta: str, tipo_cuenta: str):
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.saldo = 0
        self.tarjetas = {}

    def _validar_monto(self, monto: float) -> None:
        
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un valor numerico")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

    def agregar_tarjeta(self, tarjeta: "Tarjeta"):

        if not isinstance(tarjeta, Tarjeta):
            raise ValueError("Debes agregar una tarjeta ")
        
        self.tarjetas[tarjeta.numero_tarjeta] = tarjeta
            
    def acreditar(self, monto: float) -> None:

        self._validar_monto(monto)
        self.saldo += monto

    def debitar(self, monto: float) -> None:

        self._validar_monto(monto)

        if monto > self.saldo:
            raise ValueError("Fondos insuficientes para realizar la operacion")

        self.saldo -= monto

    def __str__(self):
        return str({
            "numero_cuenta": self.numero_cuenta,
            "tipo": self.tipo_cuenta,
            "saldo": self.saldo,
        })

class CuentaSchema(BaseModel):
    
    numero_cuenta: str
    tipo_cuenta: str

def main():
    pass

if __name__ == "__main__":
    pass