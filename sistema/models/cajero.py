from pydantic import BaseModel, Field
class Cajero:
    
    def __init__(self, numero_cajero: str, dinero_disponible: float):
        self.numero_cajero = numero_cajero
        self.dinero_disponible = dinero_disponible

    def _validar_monto(self, monto: float) -> float:
        if not isinstance(monto, (int, float)):
            raise TypeError("El monto debe ser un valor numerico")
        if monto <= 0:
            raise ValueError("El monto debe ser mayor a 0")
        return monto
        
    def dispensar_efectivo(self, monto: float) -> None:

        monto_validado = self._validar_monto(monto)
        
        if monto_validado > self.dinero_disponible:
            raise ValueError("El cajero físico no cuenta con los billetes suficientes para esta transaccion")
            
        self.dinero_disponible -= monto_validado

    def __str__(self) -> str:
        return f"Cajero(numero='{self.numero_cajero}', disponible=S/. {self.dinero_disponible})"


class CajeroSchema(BaseModel):

    numero_cajero: str
    dinero_disponible : float = Field(gt=0.0)

