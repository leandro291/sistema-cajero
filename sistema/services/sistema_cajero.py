from typing import Dict, List
from pydantic import ValidationError
from models import Cuenta, CuentaSchema, Usuario, UsuarioSchema, Tarjeta, TarjetaSchema, Cajero, CajeroSchema, Transaccion, TransaccionSchema
from random import random, choices, randint

class SistemaCajero:
    def __init__(self):
        self.usuarios: Dict[str, "Usuario"]  = {}
        self.cuentas: Dict[str, "Cuenta"] = {}
        self.transacciones: Dict[str, "Transaccion"] = {}
        self.tarjetas: Dict[str, "Tarjeta"] = {}
        self.cajero_principal = Cajero(numero_cajero="ATM-001", dinero_disponible=50000.0)

        self._contador_trx = 1

    def obtener_nombre_por_cuenta(self, numero_cuenta) -> str:
        
        cuenta = self.cuentas.get(numero_cuenta)

        if not cuenta:
            raise ValueError("La cuenta ingresada no existe")
        
        usuario = self.usuarios.get(cuenta.dni_usuario)

        if not usuario:
            raise ValueError("El usuario ingresado no existe")
        
        return usuario.nombre

    def obtener_historial_transacciones(self) -> Dict[str, "Transaccion"]:

        if len(self.transacciones) == 0:
            raise ValueError("El sistema no cuenta con transacciones registradas")
        
        return self.transacciones

    def _listar_usuarios(self) -> Dict[str, "Usuario"]:

        if len(self.usuarios) == 0:
            raise ValueError(f"No existen usuarios registradas en el sistema")

        return self.usuarios

    def _listar_cuentas_por_usuario(self, dni: str ) -> List["Cuenta"]:
        
        if len(self.cuentas) == 0:
            raise ValueError("No existen cuentas bancarias registradas en el sistema")
        
        usuario = self.usuarios.get(dni)

        if not usuario:
            raise ValueError("El DNI ingresado no se encuentra registrado")
        
        return usuario.cuentas

    def _listar_tarjetas_por_cuenta(self, numero_cuenta: str) -> List["Tarjeta"]:
        
        if len(self.cuentas) == 0:
            raise ValueError("No existen cuentas bancarias registradas en el sistema")
        
        cuenta = self.cuentas.get(numero_cuenta)

        return cuenta.tarjetas

    def crear_usuario(self, nombre: str, dni: str, saldo: float) -> str:

        if dni in self.usuarios:
            raise ValueError("El DNI registrado ya se encuentra en el sistema")
        
        validacion_usuario = UsuarioSchema(
            nombre=nombre,
            dni=dni,
            saldo=saldo
        )

        usuario = Usuario(
            nombre=validacion_usuario.nombre,
            dni=validacion_usuario.dni,
            saldo=validacion_usuario.saldo
        )

        self.usuarios[usuario.dni] = usuario
        return dni

    def crear_y_vincular_cuenta(self, dni_usuario: str, tipo_cuenta: str) -> str:

        if len(self.usuarios) == 0:
            raise ValueError(f"No existen usuarios registradas en el sistema")
        
        usuario = self.usuarios.get(dni_usuario)

        if not usuario:
            raise ValueError("El DNI ingresado no se encuentra registrado")
        
        while True:
            numero_aleatorio = "".join(choices("0123456789", k=3))
            numero_cuenta_generado = f"VISA-{numero_aleatorio}"

            if numero_cuenta_generado not in self.cuentas:
                break

        validacion_cuenta = CuentaSchema(
            numero_cuenta=numero_cuenta_generado,
            tipo_cuenta=tipo_cuenta,
            dni_usuario=dni_usuario
        )

        cuenta = Cuenta(
            numero_cuenta=validacion_cuenta.numero_cuenta,
            tipo_cuenta=validacion_cuenta.tipo_cuenta,
            dni_usuario=validacion_cuenta.dni_usuario
        )

        self.cuentas[cuenta.numero_cuenta] = cuenta
        usuario.vincular_cuenta(cuenta.numero_cuenta)

        return cuenta.numero_cuenta

    def crear_y_vincular_tarjeta(self, dni_usuario: str, numero_cuenta: str, pin: str) -> str:    

        if len(self.usuarios) == 0:
            raise ValueError(f"No existen usuarios registradas en el sistema")
        
        if len(self.cuentas) == 0:
            raise ValueError("No existen cuentas bancarias registradas en el sistema para vincular una tarjeta.")

        usuario = self.usuarios.get(dni_usuario)

        if not usuario:
            raise ValueError("El DNI ingresado no se encuentra registrado.")

        if len(usuario.cuentas) == 0:
            raise ValueError(f"{usuario.nombre} no tiene cuentas registradas")
        
        cuenta = self.cuentas.get(numero_cuenta)
        
        if not cuenta:
            raise ValueError("La cuenta ingresada no se encuentra registrado")
        
        if len(pin) != 6 or not pin.isdigit():
            raise ValueError("El PIN debe contener exactamente 6 dígitos numéricos.")
        
        while True:

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
            
            creacion_tarjeta = prefijo + str(digito_control)

            if creacion_tarjeta not in self.tarjetas:
                break
        
        validacion_tarjeta = TarjetaSchema(
            numero_tarjeta=creacion_tarjeta,
            pin=pin,
            numero_cuenta=numero_cuenta
        )

        tarjeta = Tarjeta(
            numero_tarjeta=validacion_tarjeta.numero_tarjeta,
            pin=validacion_tarjeta.pin,
            numero_cuenta= validacion_tarjeta.numero_cuenta
        )

        self.tarjetas[tarjeta.numero_tarjeta] = tarjeta
        cuenta.vincular_tarjeta(tarjeta.numero_tarjeta)
        
        return tarjeta.numero_tarjeta

    def depositar_fondos_cuenta(self, dni_usuario: str, numero_cuenta: str, monto: float) -> tuple:

        if len(self.usuarios) == 0:
            raise ValueError(f"No existen usuarios registradas en el sistema")
        
        if len(self.cuentas) == 0:
            raise ValueError("No existen cuentas bancarias registradas en el sistema para vincular una tarjeta")
            
        if monto <= 0:
            raise ValueError("El monto a depositar debe ser mayor a cero")

        usuario= self.usuarios.get(dni_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado en el sistema")
                
        cuenta = self.cuentas.get(numero_cuenta)
        if not cuenta:
            raise ValueError("Cuenta no encontrada en el Usuario asignado")
        
        if cuenta.dni_usuario != usuario.dni:
            raise ValueError("Esta cuenta no le pertenece a este usuario")
        
        if  monto > usuario.saldo:
            raise ValueError("El usuario no tiene suficiente dinero en efectivo para este depósito")

        cuenta.acreditar(monto)
        usuario.restar_dinero(monto)

        return usuario.saldo, cuenta.saldo

    def _autenticar_usuario(self, numero_tarjeta: str,pin_ingresado: str) -> "Cuenta":

        tarjeta = self.tarjetas.get(numero_tarjeta)

        if not tarjeta:
            raise ValueError("Tarjeta no reconocida")
        
        if not tarjeta.estado:
            raise ValueError("Esta tarjeta se encuentra bloqueada por seguridad")
        
        if len(pin_ingresado) != 6 or not pin_ingresado.isdigit():
            raise ValueError("El PIN debe estar formado exactamente por 6 dígitos numericos")

        if not tarjeta.validar_pin(pin_ingresado):
            restantes = 3 - tarjeta.intentos
            raise ValueError(f"PIN incorrecto. Le quedan {restantes} intentos")
            
        cuenta = self.cuentas.get(tarjeta.numero_cuenta)
        if not cuenta:
            raise ValueError("Error de sistema: Tarjeta sin cuenta vinculada")
    
        return cuenta 

    def retirar_dinero_cajero(self, cuenta: "Cuenta", monto: float) -> tuple["Transaccion", "Usuario", "Cuenta"]:

        usuario = self.usuarios.get(cuenta.dni_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado en el sistema")
        
        if monto <= 0:
            raise ValueError("Debe ingresar un monto mayor a cero.")
            
        if monto > cuenta.saldo:
            raise ValueError("Fondos insuficientes para realizar este retiro.")
            
        cuenta.debitar(monto)
        self.cajero_principal.dispensar_efectivo(monto)
        usuario.sumar_dinero(monto)

        nuevo_id = f"TRX-{self._contador_trx:03d}"

        validar_transaccion = TransaccionSchema(
            numero_transaccion=nuevo_id,
            numero_cajero="ATM-001",
            numero_cuenta=cuenta.numero_cuenta,
            monto=monto,
            tipo="Retiro"
        )

        transaccion = Transaccion(
            numero_transaccion=validar_transaccion.numero_transaccion,
            numero_cajero=validar_transaccion.numero_cajero,
            numero_cuenta=validar_transaccion.numero_cuenta,
            monto=validar_transaccion.monto,
            tipo=validar_transaccion.tipo
        )


        self.transacciones[transaccion.numero_transaccion] = transaccion
        cuenta.vincular_transaccion(transaccion.numero_transaccion)

        self._contador_trx += 1

        return transaccion, usuario, cuenta
        
    def transaccion_por_cuenta(self, cuenta: "Cuenta") -> List["Transaccion"]:
        
        if len(cuenta.historia_transacciones) == 0:
            raise ValueError("No hay transacciones registradas para esta cuenta")
        
        transacciones_cuenta = []

        for numero_transaccion in cuenta.historia_transacciones:
            
            transaccion = self.transacciones.get(numero_transaccion)

            if transaccion:
                transacciones_cuenta.append(transaccion)

        return transacciones_cuenta
            





