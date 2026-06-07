from typing import List
from pydantic import BaseModel, field_validator
class Cuenta:
    
    def __init__(self, numero_cuenta: str, tipo_cuenta: str, dni_usuario: str):
        self.numero_cuenta = numero_cuenta 
        self.tipo_cuenta = tipo_cuenta
        self.saldo: float = 0.0
        self.dni_usuario = dni_usuario
        self.tarjetas: List[str] = [] 
        self.historia_transacciones: List[str] = [] 

    def _validar_monto(self, monto: float) -> float:
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un valor numerico")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return monto

    def vincular_tarjeta(self, numero_tarjeta: str) -> None:
        self.tarjetas.append(numero_tarjeta)

    def vincular_transaccion(self, numero_transaccion: str) -> None:
        self.historia_transacciones.append(numero_transaccion)
            
    def acreditar(self, monto: float) -> None:
        monto_validado = self._validar_monto(monto)
        self.saldo += monto_validado

    def debitar(self, monto: float) -> None:
        monto_validado = self._validar_monto(monto)
        if monto_validado > self.saldo:
            raise ValueError("Fondos insuficientes para realizar la operacion")
        self.saldo -= monto_validado

    def __str__(self) -> str:
        return f"Cuenta(numero='{self.numero_cuenta}', tipo='{self.tipo_cuenta}', saldo={self.saldo})"
class CuentaSchema(BaseModel):
    
    numero_cuenta: str
    tipo_cuenta: str
    dni_usuario: str 

    @field_validator('dni_usuario')
    @classmethod
    def validate_dni(cls, valor: str) -> str:

        if len(valor) != 8 or not valor.isdigit():
            raise ValueError(f"El DNI {valor} debe estar formado de 8 digitos")
        
        return valor