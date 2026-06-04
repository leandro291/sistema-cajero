from .tarjeta import Tarjeta
from .cuenta import Cuenta
from utils import limpiar_strings
from pydantic import BaseModel, field_validator

class Cajero:
    
    def __init__(self, dinero_disponible: float):
        self.dinero_disponible = dinero_disponible

    def retirar_dinero(self, cuenta: "Cuenta", tarjeta: "Tarjeta", pin: str, monto: float) -> None:
        pin_limpio = limpiar_strings(pin)

        if not pin_limpio.isdigit():
            raise ValueError("El PIN solo debe contener valores numéricos.")
        
        if not isinstance(monto, float):
            raise TypeError("El monto ingresado no es válido.")
        
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0.")

        if tarjeta.validar_pin(pin_ingresado=pin_limpio):
            cuenta.debitar(monto=monto)
            self.dinero_disponible -= monto
        else:
            raise ValueError(f"PIN incorrecto. Le quedan {3 - tarjeta.intentos} intentos.")
    
    def __str__(self):
        return str({"dinero_disponible" : self.dinero_disponible})


class CajeroSchema(BaseModel):

    dinero_disponible : float

    @field_validator('dinero_disponible')
    @classmethod
    def validation_dinero_disponible(cls, valor: float):

        if not isinstance(valor, (float)):
            raise TypeError("El monto ingresado no es valido")
        
        if valor <= 0:
            raise ValueError("El monto no puede ser menor igual a 0")
    