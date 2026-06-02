from typing import Dict
from cuenta import Cuenta
from utils.utils import limpiar_strings
from pydantic import BaseModel, Field, field_validator, ValidationError

class Usuario:
    def __init__(self, nombre: str, dni: str):
        self.nombre = nombre
        self.dni = dni
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

    try:
        validador_usuario = UsuarioSchema(nombre="Leandro", dni="60746986")
        usuario1 = Usuario(nombre=validador_usuario.nombre, dni=validador_usuario.dni)

        print(usuario1.nombre)
        print(usuario1.dni)

    except ValidationError as e:
        print(f"Error: {e}")

    pass

if __name__ == "__main__":
    main()