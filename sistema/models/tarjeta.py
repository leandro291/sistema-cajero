from utils import limpiar_strings
from random import random, randint
from pydantic import BaseModel, field_validator, Field

class Tarjeta:
    def __init__(self, pin: str):
        self.estado = True
        self.numero_tarjeta = self.generar_tarjeta()
        self.pin = pin
        self.intentos = 0

    def _cambiar_estado(self) -> None:
        self.estado = not self.estado
    
    def _validar_estado(self) -> None:

        if not self.estado:
            raise ValueError("La cuenta se encuentra inactiva")

    def generar_tarjeta(self) -> str:

        self._validar_estado()

        prefijo = "4" + "".join(str(randint(0, 9)) for _ in range(14))
            
        suma = 0
        reverso = prefijo[::-1]
        
        for i, digito in enumerate(reverso):
            n = int(digito)
            if i % 2 == 0:
                n *= 2
                if n > 9:
                    n -= 9
            suma += n
            
        digito_control = (10 - (suma % 10)) % 10
        
        return prefijo + str(digito_control)

    def validar_pin(self, pin: str) -> bool:

        self._validar_estado()

        if self.intentos >= 3:
            self.estado = False
            return False
            
        if self.pin == pin:
            self.intentos = 0 
            return True
        else:
            self.intentos += 1  
            return False        


class TarjetaSchema(BaseModel):

    pin: str 

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, valor: str):

        valor_limpio = limpiar_strings(valor)

        if not valor_limpio.isdigit():
            raise ValueError("El numero ingresado debe tener solo digitos")
        
        if len(valor_limpio) != 6:
            raise ValueError("El pin debe estar formado de 6 caracteres")
        
        return valor_limpio




    