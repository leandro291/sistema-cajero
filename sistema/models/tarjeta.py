from utils import limpiar_strings
from random import randint
from pydantic import BaseModel, field_validator, Field
from bcrypt import gensalt, hashpw, checkpw

class Tarjeta:

    def __init__(self, pin: str, numero_cuenta: str):
        self.estado = True
        self.intentos: int = 0
        self.numero_cuenta = numero_cuenta
        self.numero_tarjeta: str = self._generar_tarjeta()
        self.pin = self._hash_pin(pin=pin)

    def _cambiar_estado(self) -> None:
        self.estado = not self.estado
    
    def _validar_estado(self) -> None:
        if not self.estado:
            raise ValueError("La tarjeta se encuentra bloqueada o inactiva")
        
    def _hash_pin(self, pin: str) -> str:
        bytes_pin =  pin.encode('utf-8')
        salt = gensalt()
        hashed_pin = hashpw(password=bytes_pin, salt=salt)
        return hashed_pin.decode('utf-8')

    def _generar_tarjeta(self) -> str:
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


    def validar_pin(self, pin_ingresado: str) -> bool:
        self._validar_estado()
            
        pin_ingresado_bytes = pin_ingresado.encode('utf-8')
        hash_guardado = self.pin.encode('utf-8')
            
        if checkpw(password=pin_ingresado_bytes, hashed_password=hash_guardado):
            self.intentos = 0
            return True

        self.intentos += 1
        if self.intentos >= 3:
            self.estado = False
            raise ValueError("PIN incorrecto. Su tarjeta ha sido bloqueada por seguridad.")
        
        return False

    def __str__(self):
        return str({
            "numero_tarjeta" : self.numero_tarjeta,
            "pin" : self.pin,
            "estado" : "Activo" if self.estado else "Inactivo"
        })

class TarjetaSchema(BaseModel):

    pin: str
    numero_cuenta: str 

    @field_validator('pin')
    @classmethod
    def validate_pin(cls, valor: str):

        valor_limpio = limpiar_strings(valor)

        if not valor_limpio.isdigit():
            raise ValueError("El numero ingresado debe tener solo digitos")
        
        if len(valor_limpio) != 6:
            raise ValueError("El pin debe estar formado de 6 caracteres")
        
        return valor_limpio




    