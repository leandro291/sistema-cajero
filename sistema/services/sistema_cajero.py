from typing import Dict
from pydantic import ValidationError
from models import Cuenta, CuentaSchema, Usuario, UsuarioSchema, Tarjeta, TarjetaSchema, Cajero, CajeroSchema
from random import random, choices, randint

class SistemaCajero:
    def __init__(self):
        self.usuarios: Dict[str, "Usuario"]  = {}
        self.cuentas: Dict[str, "Cuenta"] = {}
        self.tarjetas: Dict[str, "Tarjeta"] = {}
        self.cajeros: Dict[str, "Cajero"] = {}

    #No deben devolver prints aca
    def _listar_usuarios(self) -> None:

        if len(self.usuarios) == 0:
            raise ValueError(f"No existen usuarios registradas en el sistema")

        print("\n----- LISTA DE USUARIOS -----")
        for key, values in self.usuarios.items():
            print(f"{key} -> {values}")

    def _listar_cuentas_por_usuario(self, dni: str) -> None:
        
        if len(self.cuentas) == 0:
            raise ValueError("No existen cuentas bancarias registradas en el sistema")
        
        usuario = self.usuarios.get(dni)

        if not usuario:
            raise ValueError("El DNI ingresado no se encuentra registrado")
        
        print(f"\n------  CUENTAS DISPONIBLES DE {usuario.nombre.upper()} ------ ")
        for cuenta in usuario.cuentas:
            print(f"- {cuenta}")

    def _listar_tarjeas_por_cuenta(self, numero_cuenta: str) -> None:
        pass

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
            raise ValueError("No existen cuentas bancarias registradas en el sistema para vincular una tarjeta.")
            
        if monto <= 0:
            raise ValueError("El DNI ingresado no se encuentra registrado")

        usuario= self.usuarios.get(dni_usuario)
        if not usuario:
            raise ValueError("Usuario no encontrado en el sistema")
                
        cuenta = self.cuentas.get(numero_cuenta)
        if not cuenta:
            raise ValueError("Cuenta no encontrada en el Usuario asignado")
        
        if cuenta.dni_usuario != usuario.dni:
            raise ValueError("Esta cuenta no le pertenece a este usuario")
        
        if  monto > usuario.saldo:
            raise ValueError("El usuario no tiene suficiente dinero en efectivo para este depósito.")

        cuenta.acreditar(monto)
        usuario.sumar_dinero(monto)

        return usuario.saldo, cuenta.saldo

    def _autenticar_usuario(self) -> "Cuenta":
        
        print("\n" + "="*40)
        print(" 🏧 INGRESO AL CAJERO AUTOMÁTICO ")
        print("="*40)

        numero_tarjeta = input("Inserte el numero de su tarjeta: ").strip()
        tarjeta = self.tarjetas.get(numero_tarjeta)

        if not tarjeta:
            raise ValueError("Tarjeta no reconocida")
        
        if not tarjeta.estado:
            raise ValueError("Esta tarjeta se encuentra bloqueada por seguridad")
        
        while True:
            pin_ingresado = input("Ingrese su PIN de 6 digitos: ").strip()

            if len(pin_ingresado) != 6 or not pin_ingresado.isdigit():
                print("❌ El PIN debe estar formado de 6 digitos numericos")
                continue

            if tarjeta.validar_pin(pin_ingresado):
                
                break
            else:
                restantes = 3 - tarjeta.intentos
                print(f"❌ PIN incorrecto. Le quedan {restantes} intentos")
                

        
        cuenta = self.cuentas.get(tarjeta.numero_cuenta)
        if not cuenta:
            raise ValueError("Error de sistema: Tarjeta sin cuenta vinculada.")
            
        print("\n✅ Autenticación exitosa.")
        return cuenta 

    def retirar_dinero_cajero(self) -> None:
        
        try:

            cuenta_validada = self._autenticar_usuario()
            
            
            print("\n" + "-"*30)
            print(" 🏧 RETIRO DE EFECTIVO ")
            print("-" * 30)
            
            print(f"[INFO] Saldo disponible: S/. {cuenta_validada.saldo:.2f}")
            monto_str = input("Ingrese el monto que desea retirar: S/. ").strip()
            
            if not monto_str.replace('.', '', 1).isdigit():
                raise ValueError("El monto ingresado debe ser un valor numérico.")
                
            monto = float(monto_str)
            
            if monto <= 0:
                raise ValueError("Debe ingresar un monto mayor a cero.")
                
            if monto > cuenta_validada.saldo:
                raise ValueError("Fondos insuficientes para realizar este retiro.")
                
            cuenta_validada.debitar(monto) 
            
            print(f"\nTransacción aprobada")
            print(f"Por favor, retire sus S/. {monto:.2f} de la bandeja.")
            print(f"Su nuevo saldo es: S/. {cuenta_validada.saldo:.2f}")
            print("Retirando tarjeta... Gracias por usar nuestro ATM.")
            
        except ValueError as e:
            print(f"\nOperación rechazada: {e}")
            print("Terminando sesión del ATM...")
        except Exception as e:
            print(f"\nError inesperado en el cajero: {e}")





