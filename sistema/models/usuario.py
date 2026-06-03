from typing import Dict
from .cuenta import Cuenta
from utils import limpiar_strings
from pydantic import BaseModel, Field, field_validator, ValidationError

class Usuario:
    def __init__(self, nombre: str, dni: str, dinero_incial: float):
        self.nombre = nombre
        self.dni = dni
        self.dinero_inicial = dinero_incial
        self.cuentas: Dict[str, Cuenta] = {}

    def _validar_dinero(self, monto: float):

        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un valor numerico")

        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")

    def crear_cuenta(self, cuenta: "Cuenta") -> None:

        if not isinstance(cuenta, Cuenta):
            raise ValueError("Debe agregar una cuenta existente")
        
        self.cuentas[cuenta.numero_cuenta] = cuenta

    def retirar(self, cuenta: "Cuenta", monto: float):

        self._validar_dinero(monto)
        self.dinero_inicial += monto
        cuenta.debitar(monto)

    def depositar(self, cuenta: "Cuenta", monto: float):
        
        self._validar_dinero(monto)
        
        if monto > self.dinero_inicial:
            raise ValueError("Fondos insuficientes para realizar la operacion")

        self.dinero_inicial -= monto
        cuenta.acreditar(monto)

    def __str__(self):
        return str({
            "nombre" : self.nombre,
            "dni" : self.dni,
            "dinero_incial" : self.dinero_inicial,
            "cuentas" : self.cuentas
        })
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
