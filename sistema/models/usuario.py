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
        self.estado: bool = True

    def _cambiar_estado(self) -> None:
        
        self.estado = not self.estado

    def _validar_estado(self) -> None:
        
        if not self.estado:
            raise ValueError("El usuario se encuentra inactivo")

    def crear_cuenta(self, cuenta: Cuenta) -> None:
        
        self._validar_estado()
        self.cuentas[cuenta.numero_cuenta] = cuenta

    def __str__(self):
        return str({
            "nombre" : self.nombre,
            "dni" : self.dni,
            "dinero_incial" : self.dinero_inicial,
            "estado" : "Activo" if self.estado else "Inactivo",
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
