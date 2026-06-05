from typing import Dict
from utils import limpiar_strings
from pydantic import ValidationError
from models import Cuenta, CuentaSchema, Usuario, UsuarioSchema, Tarjeta, TarjetaSchema, Cajero, CajeroSchema

class SistemaCajero:
    def __init__(self):
        self.usuarios: Dict[str, "Usuario"]  = {}
        self.cuentas: Dict[str, "Cuenta"] = {}
        self.tarjetas: Dict[str, "Tarjeta"] = {}
        self.cajeros: Dict[str, "Cajero"] = {}
        self.sesion_activa = None

    def _lista_de_usuarios(self) -> None:
        print("\n----- LISTA DE USUARIOS -----")
        for key, values in self.usuarios.items():
            print(f"{key} -> {values}")
    
    def crear_usuario(self) -> None:
        try:

            print(f"\n------ REGISTRO DE USUARIOS ------ ")
            nombre = input("Ingrese su nombre: ").title()
            dni = input("Ingrese su DNI: ")

            if dni in self.usuarios:
                raise ValueError("El DNI registrado ya se encuentra en el sistema")

            saldo = float(input("Ingrese dinero incial: "))
            
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
            print(f"\n{usuario.nombre} ha sido registrado con exito")

        except ValidationError as e:
            print("\nError en los datos ingresados:")
            for error in e.errors():
                print(f" - {error['msg']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def crear_y_vincular_cuenta(self) -> None:
        try:

            if len(self.usuarios) == 0:
                raise ValueError(f"No existen cuentas registradas en el sistema")
            
            print(f"\n------ VINCULACION DE CUENTAS ------ ")

            self._lista_de_usuarios()

            dni_usuario = limpiar_strings(input("Ingrese DNI del usuario: "))
            if dni_usuario not in self.usuarios:
                raise ValueError("El DNI ingresado no se encuentra registrado")
            
            print(f"\n------ CREACION DE CUENTA ------ ")
            numero_cuenta = limpiar_strings(input("Ingrese el numero de cuenta: "))
            if numero_cuenta in self.cuentas:
                raise ValueError("La cuenta seleccionada ya se encuentra vinculada")

            tipo_cuenta = limpiar_strings(input("Ingrese su tipo de cuenta: "))

            validacion_cuenta = CuentaSchema(
                numero_cuenta=numero_cuenta,
                tipo_cuenta=tipo_cuenta,
                dni_usuario=dni_usuario
            )

            cuenta = Cuenta(
                numero_cuenta=validacion_cuenta.numero_cuenta,
                tipo_cuenta=validacion_cuenta.tipo_cuenta,
                dni_usuario=validacion_cuenta.dni_usuario
            )

            self.cuentas[cuenta.numero_cuenta] = cuenta
            usuario: "Usuario" = self.usuarios.get(dni_usuario)
            usuario.vincular_cuenta(cuenta.numero_cuenta)
            print(f"\nLa cuenta {cuenta.numero_cuenta} ha sido vinculada correctamente hacia {usuario.nombre}")

        except ValidationError as e:
            print("\nError en los datos ingresados:")
            for error in e.errors():
                print(f" - {error['msg']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

    def crear_y_vincular_tarjeta(self) -> None:    
        try:

            if len(self.usuarios) == 0:
                raise ValueError(f"No existen cuentas registradas en el sistema")

            print(f"\n------  VINCULACION DE TARJETAS ------ ")
            self._lista_de_usuarios()

            dni_usuario = input("Ingrese DNI del usuario al que desea vincular: ").strip()
            if dni_usuario not in self.usuarios:
                raise ValueError("El DNI ingresado no se encuentra registrado")
            
            usuario: "Usuario" = self.usuarios.get(dni_usuario)
            print("\n------  CUENTAS DISPONIBLES ------ ")

            if len(usuario.cuentas) == 0:
                raise ValueError(f"{usuario.nombre} no tiene cuentas registradas")

            for cuenta in usuario.cuentas:
                print(f"- {cuenta}")

            numero_cuenta = input("Ingrese el numero de cuenta: ").strip()
            if numero_cuenta not in self.cuentas:
                raise ValueError("La cuenta ingresada no se encuentra registrado")
            
            print(f"\n------  CREACION DE TARJETA ------ ")

            pin = input("Ingrese el PIN para su tarjeta: ").strip()
            
            validacion_tarjeta = TarjetaSchema(
                pin=pin,
                numero_cuenta=numero_cuenta
            )

            tarjeta = Tarjeta(
                pin=validacion_tarjeta.pin,
                numero_cuenta= validacion_tarjeta.numero_cuenta
            )

            self.tarjetas[tarjeta.numero_tarjeta] = tarjeta
            cuenta : "Cuenta" = self.cuentas[numero_cuenta]
            cuenta.vincular_tarjeta(tarjeta.numero_tarjeta)
            print(f"La tarjeta {tarjeta.numero_tarjeta} ha sido vinculada exitosamente a la cuenta {cuenta.numero_cuenta}")

        except ValidationError as e:
            print("\nError en los datos ingresados:")
            for error in e.errors():
                print(f" - {error['msg']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")




    def depositar_fondos_cuenta(self) -> None:
        print(f"------  DEPOSITAR FONDO A CUENTA ------ ")
        self._lista_de_usuarios()

        dni_usuario = input("Ingrese DNI del usuario: ").strip()
        usuario: "Usuario" = self.usuarios.get(dni_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado en el sistema")

        print("------  CUENTAS DISPONIBLES ------ ")
        for cuenta in usuario.cuentas:
            print(f"- {cuenta}")

        numero_cuenta = input("Ingrese el numero de cuenta: ").strip()        
        cuenta: "Cuenta" = self.cuentas.get(numero_cuenta)

        if not cuenta:
            raise ValueError("Cuenta no encontrada en el Usuario asignado")
        
        if cuenta.dni_usuario != usuario.dni:
            raise ValueError("Esta cuenta no le pertenece a este usuario")

        print(f"{usuario.nombre} tiene un saldo disponible de S/. {usuario.saldo}")

        try:
            monto = float(input("Ingrese el monto que desea mover: "))
            usuario.restar_dinero(monto)
            cuenta.acreditar(monto)

            print(f"Transaccion realizada exitosamente: ")
            print(f"Nuevo saldo del Usuario: {usuario.nombre} -> S/. {usuario.saldo} ")
            print(f"Nuevo saldo en la Cuenta: {cuenta.numero_cuenta} -> S/. {cuenta.saldo} ")
        except ValueError as e:
            print(f"Error: {e}")

    def retirar_fondos_cuenta(self) -> None:
        print(f"------  RETIRAR FONDO A CUENTA ------ ")
        self._lista_de_usuarios()

        dni_usuario = input("Ingrese DNI del usuario: ").strip()
        usuario: "Usuario" = self.usuarios.get(dni_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado en el sistema")

        print("------  CUENTAS DISPONIBLES ------ ")
        for cuenta in usuario.cuentas:
            print(f"- {cuenta}")

        numero_cuenta = input("Ingrese el numero de cuenta: ").strip()        
        cuenta: "Cuenta" = self.cuentas.get(numero_cuenta)

        if not cuenta:
            raise ValueError("Cuenta no encontrada en el Usuario asignado")
        
        if cuenta.dni_usuario != usuario.dni:
            raise ValueError("Esta cuenta no le pertenece a este usuario")

        print(f"{usuario.nombre} tiene un saldo disponible de S/. {usuario.saldo}")

        try:
            monto = float(input("Ingrese el monto que desea mover: "))
            usuario.sumar_dinero(monto)
            cuenta.debitar(monto)

            print(f"Transaccion realizada exitosamente: ")
            print(f"Nuevo saldo del Usuario: {usuario.nombre} -> S/. {usuario.saldo} ")
            print(f"Nuevo saldo en la Cuenta: {cuenta.numero_cuenta} -> S/. {cuenta.saldo} ")
        except ValueError as e:
            print(f"Error: {e}")

    def retirar_del_cajero(self) -> None:
        print(f"------  RETIRAR DINERO DEL CAJERO ------ ")
        self._lista_de_usuarios()

        dni_usuario = input("Ingrese DNI del usuario: ").strip()
        usuario: "Usuario" = self.usuarios.get(dni_usuario)

        if not usuario:
            raise ValueError("Usuario no encontrado en el sistema")

        print("------  CUENTAS DISPONIBLES ------ ")
        for cuenta in usuario.cuentas:
            print(f"- {cuenta}")

        numero_cuenta = input("Ingrese el numero de cuenta: ").strip()        
        cuenta: "Cuenta" = self.cuentas.get(numero_cuenta)

        if not cuenta:
            raise ValueError("Cuenta no encontrada en el Usuario asignado")
        
        if cuenta.dni_usuario != usuario.dni:
            raise ValueError("Esta cuenta no le pertenece a este usuario")

        print(f"{cuenta.numero_cuenta} tiene un saldo disponible de S/. {cuenta.saldo}")

        try:
            monto = float(input("Ingrese el monto que desea mover: "))
            usuario.sumar_dinero(monto)
            cuenta.debitar(monto)

            print(f"Transaccion realizada exitosamente: ")
            print(f"Nuevo saldo del Usuario: {usuario.nombre} -> S/. {usuario.saldo} ")
            print(f"Nuevo saldo en la Cuenta: {cuenta.numero_cuenta} -> S/. {cuenta.saldo} ")
        except ValueError as e:
            print(f"Error: {e}")





