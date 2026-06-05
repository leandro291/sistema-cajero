from typing import Dict
from pydantic import ValidationError
from models import Cuenta, CuentaSchema, Usuario, UsuarioSchema, Tarjeta, TarjetaSchema, Cajero, CajeroSchema

class SistemaCajero:
    def __init__(self):
        self.usuarios: Dict[str, "Usuario"]  = {}
        self.cuentas: Dict[str, "Cuenta"] = {}
        self.tarjetas: Dict[str, "Tarjeta"] = {}
        self.cajeros: Dict[str, "Cajero"] = {}

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
                raise ValueError(f"No existen usuarios registradas en el sistema")
            
            print(f"\n------ VINCULACION DE CUENTAS ------ ")

            self._lista_de_usuarios()

            dni_usuario = (input("Ingrese DNI del usuario: "))
            if dni_usuario not in self.usuarios:
                raise ValueError("El DNI ingresado no se encuentra registrado")
            
            print(f"\n------ CREACION DE CUENTA ------ ")
            numero_cuenta = (input("Ingrese el numero de cuenta: "))
            if numero_cuenta in self.cuentas:
                raise ValueError("La cuenta seleccionada ya se encuentra vinculada")

            tipo_cuenta = (input("Ingrese su tipo de cuenta: "))

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
                raise ValueError(f"No existen usuarios registradas en el sistema")
            if len(self.cuentas) == 0:
                raise ValueError("No existen cuentas bancarias registradas en el sistema para vincular una tarjeta.")

            print(f"\n------  VINCULACION DE TARJETAS ------ ")
            self._lista_de_usuarios()

            dni_usuario = input("Ingrese DNI del usuario al que desea vincular: ").strip()
            usuario: "Usuario" = self.usuarios.get(dni_usuario)

            if not usuario:
                raise ValueError("El DNI ingresado no se encuentra registrado.")

            if len(usuario.cuentas) == 0:
                raise ValueError(f"{usuario.nombre} no tiene cuentas registradas")
            
            print(f"\n------  CUENTAS DISPONIBLES DE {usuario.nombre.upper()} ------ ")
            for cuenta in usuario.cuentas:
                print(f"- {cuenta}")

            numero_cuenta = input("Ingrese el numero de cuenta: ").strip()
            if numero_cuenta not in self.cuentas:
                raise ValueError("La cuenta ingresada no se encuentra registrado")
            
            print(f"\n------  CREACION DE TARJETA ------ ")

            pin = input("Ingrese el PIN para su nueva tarjeta: ").strip()
            
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
        try:

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

            monto = float(input("Ingrese el monto que desea mover: S/. "))
            cuenta.acreditar(monto)
            usuario.sumar_dinero(monto)

            print(f"Transaccion realizada exitosamente: ")
            print(f"Nuevo saldo del Usuario: {usuario.nombre} -> S/. {usuario.saldo} ")
            print(f"Nuevo saldo en la Cuenta: {cuenta.numero_cuenta} -> S/. {cuenta.saldo} ")

        except ValidationError as e:
            print("\nError en los datos ingresados:")
            for error in e.errors():
                print(f" - {error['msg']}")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error inesperado: {e}")

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





