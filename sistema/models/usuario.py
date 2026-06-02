from typing import Dict
from pydantic import BaseModel, Field, field_validator, ValidationError
from utils.utils import limpiar_strings

class Usuario:
    def __init__(self, nombre: str, dni: str):
        self.nombre = nombre
        self.dni = dni
        self.cuentas = {}
        self.estado = True

    def _cambiar_estado(self):
        pass

    def _validar_estado(self):
        pass

    def crear_cuenta(self):
        pass


class UsuarioSchema(BaseModel):
    nombre: str = Field(min_length=1, max_length=60)
    dni: str = Field(min_length=8)

    @field_validator('nombre')
    @classmethod
    def validate_nombre(cls, valor: str):

        valor_limpio = limpiar_strings(valor)

        if not valor_limpio.isalpha():
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

def main():
    pass

if __name__ == "__main__":
    main()