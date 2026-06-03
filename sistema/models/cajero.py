from pydantic import BaseModel, field_validator

class Cajero:
    
    def __init__(self, dinero_disponible: float):
        self.dinero_disponible = float

class CajeroSchema(BaseModel):

    dinero_disponible : float

    @field_validator('dinero_disponible')
    @classmethod
    def validation_dinero_disponible(cls, valor: float):

        if not isinstance(valor, (float)):
            raise TypeError("El monto ingresado no es valido")
        
        if valor <= 0:
            raise ValueError("El monto no puede ser menor igual a 0")
    