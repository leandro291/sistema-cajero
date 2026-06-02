from pydantic import BaseModel, Field, field_validator, ValidationError

class Cuenta:
    def __init__(self, numero_cuenta: str, tipo_cuenta: str):
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.saldo = 0
        self.estado = True

    def _cambiar_estado(self) -> None:
        self.estado = not self.estado
    
    def _validar_estado(self) -> None:
        if not self.estado:
            raise ValueError("La cuenta se encuentra inactiva")
        
    def _validar_monto(self, monto: float) -> None:
        
        if monto <= 0:
            raise ValueError("El monto depositado no puede ser menor a 0")
    
    def depositar(self, monto: float) -> None:

        self._validar_estado()
        self._validar_monto()
        
        self.saldo += monto

    def retirar(self, monto: float) -> None:

        self._validar_estado()
        self._validar_monto()

        self.saldo -= monto

class CuentaSchema(BaseModel):
    
    numero_cuenta: str
    tipo_cuenta: str

def main():
    pass

if __name__ == "__main__":
    pass