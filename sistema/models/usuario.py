from typing import List
from .cuenta import Cuenta
from utils import limpiar_strings
from pydantic import BaseModel, Field, field_validator, ValidationError

class Usuario:
    
    def __init__(self, nombre: str, dni: str, dinero_incial: float):
        self.nombre = nombre
        self.dni = dni
        self.dinero_inicial = dinero_incial
        self.cuentas: List[str] = []

    def _validar_dinero(self, monto: float) -> float:
        if not isinstance(monto, (float, int)):
            raise TypeError("El monto debe ser un valor numerico")        
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        
        return monto
    
    def _validar_pertenencia(self, cuenta: "Cuenta") -> None:
        if cuenta.dni_usuario != self.dni:
            raise ValueError("La cuenta no pertenece a este usuario")
        
    def _validar_pre_transaccion(self, cuenta: "Cuenta", monto: float) -> float:
        monto_validado = self._validar_dinero(monto)
        self._validar_pertenencia(cuenta)
        return monto_validado

    def vincular_cuenta(self, numero_cuenta: str):
        self.cuentas.append(numero_cuenta)

    def retirar(self, cuenta: "Cuenta", monto: float) -> None:
        monto_validado = self._validar_pre_transaccion(cuenta, monto)

        cuenta.debitar(monto_validado)
        
        self.dinero_inicial += monto_validado

    def depositar(self, cuenta: "Cuenta", monto: float) -> None:
        
        monto_validado = self._validar_pre_transaccion(cuenta, monto)
        if monto > self.dinero_inicial:
            raise ValueError("Fondos insuficientes para realizar la operacion")

        cuenta.acreditar(monto_validado)

        self.dinero_inicial -= monto_validado

    def __str__(self) -> str:
        return f"Usuario(nombre='{self.nombre}', dni='{self.dni}', fondos={self.dinero_inicial})"
class UsuarioSchema(BaseModel):
    
    nombre: str = Field(min_length=1, max_length=60)
    dni: str = Field(min_length=8)
    dinero_inicial: float = Field(default=0.0, ge=0.0)

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
