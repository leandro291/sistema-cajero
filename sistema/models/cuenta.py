from pydantic import BaseModel, Field, field_validator, ValidationError

class Cuenta:
    def __init__(self, numero_cuenta: str, tipo_cuenta: str):
        self.numero_cuenta = numero_cuenta
        self.tipo_cuenta = tipo_cuenta
        self.saldo = 0
        self.estado = True

class CuentaSchema(BaseModel):
    
    numero_cuenta: str
    tipo_cuenta: str

def main():
    pass

if __name__ == "__main__":
    pass