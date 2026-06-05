from typing import List
from utils import limpiar_strings
from pydantic import BaseModel, Field, field_validator, ValidationError

class Usuario:
    
    def __init__(self, nombre: str, dni: str, saldo: float):
        self.nombre = nombre
        self.dni = dni
        self.saldo = saldo
        self.cuentas: List[str] = []

    def _validar_dinero(self, monto: float) -> float:
        if not isinstance(monto, (float, int)):
            raise TypeError("El monto debe ser un valor numerico")        
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        return monto

    def vincular_cuenta(self, numero_cuenta: str) -> None:
        self.cuentas.append(numero_cuenta)

    def sumar_dinero(self, monto: float) -> None:
        monto_validado = self._validar_dinero(monto)
        
        self.saldo += monto_validado

    def restar_dinero(self, monto: float) -> None:
        
        monto_validado = self._validar_dinero(monto)
        if monto > self.saldo:
            raise ValueError("Fondos insuficientes para realizar la operacion")
        
        self.saldo -= monto_validado

    def __str__(self) -> str:
        return f"Usuario(nombre='{self.nombre}', dni='{self.dni}', fondos={self.saldo})"
class UsuarioSchema(BaseModel):
    
    nombre: str = Field(min_length=1, max_length=60)
    dni: str = Field(min_length=8)
    saldo: float = Field(default=0.0, ge=0.0)

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, valor: str):
        valor_limpio = limpiar_strings(valor)
        if not valor_limpio.replace(" ", "").isalpha():
            raise ValueError("El nombre solo debe ser alfabetico")
        return valor_limpio

    @field_validator('dni')
    @classmethod
    def validate_dni(cls, valor: str) -> str:
        valor_limpio = limpiar_strings(valor)
        if not valor_limpio.isdigit():
            raise ValueError("El DNI solo debe contener numeros")
        if len(valor_limpio) != 8:
            raise ValueError("El DNI debe contar con 8 caracteres")
        return valor_limpio
