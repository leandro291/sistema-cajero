from services import SistemaCajero
from pydantic import ValidationError
from utils.logger import Logger
import os
os.system('cls')

class CajeroUI:
    def __init__(self):
        self.sistema_cajero = SistemaCajero() 
    
    def iniciar(self) -> None:
        while True:
            try:
                print("=" * 40)
                print(" SISTEMA BANCARIO Y CAJERO ATM ".center(40, "-"))
                print("=" * 40)
                print("[1]. Administrar")
                print("[2]. Usar Cajero")
                print("[3]. Salir")

                opc = input("\nSeleccione una opcion: ").strip()

                match(opc):
                    case "1":
                        self.submenu_administrador()

                    case "2":
                        self.submenu_cajero()

                    case "3":
                        print(f"Saliendo del sistema....")
                        break
                    case _:
                        print(f"Opcion invalida. Vuelva a seleccionar una opcion")
                        continue

            except KeyboardInterrupt as e:
                print(f"Ha ocurrido un error de teclado: {e}")
            except Exception as e:
                print(f"Ha ocurrio un error inesperado {e}")
    
    def submenu_administrador(self) -> None:
        while True:
            try:
                print("\n" + "=" * 40)
                print(" ADMINISTRACION ".center(40, "-"))
                print("=" * 40)
                print("[1]. Registrar nuevo cliente")
                print("[2]. Aperturar cuenta bancaria")
                print("[3]. Emitir tarjeta de debito")
                print("[4]. Depositar dinero a cuenta") 
                print("[5]. Ver total de Transacciones") 
                print("[6]. Regresar al menu principal")

                opc = input("\nIngrese una opcion: ").strip()

                match(opc):
                    case "1":
                        print("\n" + "=" * 40)
                        print(" REGISTRO DE USUARIOS ".center(40, "-"))
                        print("=" * 40)
                        try: 
                            nombre = input("Ingrese su nombre: ").strip().title()
                            dni = input("Ingrese su DNI: ").strip()
                            saldo = float(input("Ingrese dinero incial: S/. "))

                            dni_registrado = self.sistema_cajero.crear_usuario(nombre, dni, saldo)

                            nombre_split = nombre.split()
                            primer_nombre = nombre_split[0]

                            print(f"\n{primer_nombre} con DNI {dni_registrado} ha sido registrado con exito en el Sistema")

                        except ValidationError as e:
                            print("\nHa ocurrido un error en los datos ingresados:")
                            for error in e.errors():
                                Logger.add_to_log("error", str(error['msg']))
                                print(f"- {error['msg']}")
                        except ValueError as e:
                            Logger.add_to_log("warn", str(e))
                            print(f"\n{e}")

                    case "2":
                        print("\n" + "=" * 40)
                        print(" VINCULACION DE CUENTAS ".center(40, "-"))
                        print("=" * 40)
                        try:
                            usuarios = self.sistema_cajero._listar_usuarios()
                            print("\n" + " LISTA DE USUARIOS ".center(40, "-"))
                            for usuario in usuarios.values():
                                print(f"- {usuario}")
                            print("-" * 40)

                            dni_usuario = input("\nIngrese DNI del usuario al que desea vincular: ").strip()

                            print("\n" + "=" * 40)
                            print(" CREACION DE CUENTAS ".center(40, "-"))
                            print("=" * 40)
                            print("[1]. Ahorro")
                            print("[2]. Corriente")

                            opc = input("\nIngrese el tipo de cuenta que desea: ").strip()
                            tipo_cuenta=""

                            match(opc):
                                case "1":
                                    tipo_cuenta="Ahorro"
                                case "2":
                                    tipo_cuenta="Corriente"
                                case _:
                                    print("Tipo de cuenta seleccionada invalida")
                                    continue

                            cuenta_registrada = self.sistema_cajero.crear_y_vincular_cuenta(dni_usuario, tipo_cuenta)

                            print(f"\nLa cuenta {cuenta_registrada} de tipo {tipo_cuenta} ha sido creada con exito")

                        except ValidationError as e:
                            print("\nHa ocurrido un error en los datos ingresados:")
                            for error in e.errors():
                                Logger.add_to_log("error", str(error['msg']))
                                print(f"- {error['msg']}")
                        except ValueError as e:
                            Logger.add_to_log("warn", str(e))
                            print(f"\n{e}")

                    case "3":
                        print("\n" + "=" * 40)
                        print(" VINCULACION DE TARJETAS ".center(40, "-"))
                        print("=" * 40)

                        try:
                            usuarios = self.sistema_cajero._listar_usuarios()

                            print("\n" + " LISTA DE USUARIOS ".center(40, "-"))
                            for usuario in usuarios.values():
                                print(f"- {usuario}")
                            print("-" * 40)

                            dni_usuario = input("\nIngrese DNI del usuario al que desea vincular: ").strip()
                            cuentas = self.sistema_cajero._listar_cuentas_por_usuario(dni_usuario)

                            print("\n" + " LISTA DE CUENTAS ".center(40, "-"))
                            for cuenta in cuentas:
                                print(f"- {cuenta}")
                            print("-" * 40)

                            numero_cuenta = input("\nIngrese el Numero de Cuenta de la Cuenta a la que desea vincular: ").strip()

                            print("=" * 40)
                            print(" CREACION DE TARJETAS ".center(40, "-"))
                            print("=" * 40)
                            pin = input("Ingrese el PIN para su nueva tarjeta: ").strip()

                            tarjeta_creada = self.sistema_cajero.crear_y_vincular_tarjeta(dni_usuario, numero_cuenta, pin)

                            print(f"\nLa tarjeta {tarjeta_creada} ha sido creada exitosamente en la cuenta {numero_cuenta}")

                        except ValidationError as e:
                            print("\nHa ocurrido un error en los datos ingresados:")
                            for error in e.errors():
                                Logger.add_to_log("error", str(error['msg']))
                                print(f"- {error['msg']}")
                        except ValueError as e:
                            Logger.add_to_log("warn", str(e))
                            print(f"\n{e}")

                    case "4":
                        try:
                            print("\n" + "=" * 40)
                            print(" DEPOSITAR FONDOS A CUENTA ".center(40, "-"))
                            print("=" * 40)

                            print("\n" + " LISTA DE USUARIOS ".center(40, "-"))
                            for usuario in usuarios.values():
                                print(f"- {usuario}")
                            print("-" * 40)

                            dni_usuario = input("\nIngrese DNI del usuario: ").strip()
                            cuentas = self.sistema_cajero._listar_cuentas_por_usuario(dni_usuario)

                            print("\n" + " LISTA DE CUENTAS ".center(40, "-"))
                            for cuenta in cuentas:
                                print(f"- {cuenta}")
                            print("-" * 40)

                            numero_cuenta = input("\nIngrese el numero de cuenta: ").strip()
                            monto = float(input("Ingres el monto a depositar: "))

                            nuevo_efectivo, nuevo_saldo = self.sistema_cajero.depositar_fondos_cuenta(dni_usuario, numero_cuenta, monto)

                            print("\nTransacción realizada exitosamente.")
                            print(f"Nuevo efectivo del usuario: S/. {nuevo_efectivo}")
                            print(f"Nuevo saldo en la cuenta bancaria: S/. {nuevo_saldo}")

                        except ValidationError as e:
                            print("Ha ocurrido un error en los datos ingresados:")
                            for error in e.errors():
                                Logger.add_to_log("error", str(error['msg']))
                                print(f"- {error['msg']}")
                        except ValueError as e:
                            Logger.add_to_log("warn", str(e))
                            print(f"\n{e}")

                    case "5":
                        transacciones = self.sistema_cajero.obtener_historial_transacciones()
                        for transaccion in transacciones.values():
                            print(transaccion)

                    case "6":
                        print(f"Regresando al menu principal...")
                        break

                    case _:
                        print(f"Opcion invalida. Vuelva a seleccionar una opcion")
                        continue

            except Exception as e:
                print(f"Ha ocurrido un error: {e}")

    def submenu_cajero(self) -> None:

        print("\n" + "=" * 40)
        print(" INGRESO AL CAJERO (ATM) ".center(40, "-"))
        print("=" * 40)

        numero_tarjeta = input("\nInserte el numero de su tarjeta: ").strip()
        try:
            tarjeta_validada = self.sistema_cajero.verificar_tarjeta(numero_tarjeta)
            autenticado = False

            while not autenticado:
                pin_ingresado = input("Ingrese su PIN de 6 dígitos (o 'X' para cancelar): ").strip()

                if pin_ingresado.upper() == 'X':
                    print("Operación cancelada. Retirando tarjeta...")
                    break

                try:
                    cuenta_activa = self.sistema_cajero._autenticar_usuario(tarjeta_validada, pin_ingresado)
                    print("Autentificacion realizada exitosamente")
                    autenticado = True

                    while True:
                        try:
                            print("\n" + "=" * 40)
                            print(f" BIENVENIDO: {self.sistema_cajero.obtener_nombre_por_cuenta(cuenta_activa.numero_cuenta)} ".center(40, "-"))
                            print("=" * 40)
                            print("[1] Consultar Saldo")
                            print("[2] Retirar Efectivo")
                            print("[3] Ver Historial de Movimientos")
                            print("[4] Retirar Tarjeta")

                            opc = input("\nSeleccione una opcion: ").strip()

                            match(opc):
                                case "1":
                                    print(f"El saldo actual de la cuenta es S/. {cuenta_activa.saldo}")

                                case "2":
                                    try:
                                        monto = float(input("Ingrese el monto que desea retirar: S/. "))
                                        transaccion, usuario, cuenta =self.sistema_cajero.retirar_dinero_cajero(cuenta_activa, monto)

                                        print(f"Transaccion aprobada")
                                        print(f"Por favor, retire sus S/. {monto} de la bandeja")
                                        print(f"Su nuevo saldo de cuenta es: S/. {cuenta.saldo}")
                                        print(f"Su nuevo saldo de usuario es: S/. {usuario.saldo}")
                                    except ValidationError as e:
                                        print("\nHa ocurrido un error en los datos ingresados:")
                                        for error in e.errors():
                                            Logger.add_to_log("error", str(error['msg']))
                                            print(f"- {error['msg']}")
                                    except ValueError as e:
                                        Logger.add_to_log("warn", str(e))
                                        print(f"\n{e}")

                                case "3":
                                    try:
                                        transacciones_cuenta = self.sistema_cajero.transaccion_por_cuenta(cuenta_activa)
                                        for transaccion in transacciones_cuenta:
                                            print(transaccion)
                                    except ValidationError as e:
                                        print("\nHa ocurrido un error en los datos ingresados:")
                                        for error in e.errors():
                                            Logger.add_to_log("error", str(error['msg']))
                                            print(f"- {error['msg']}")
                                    except ValueError as e:
                                        Logger.add_to_log("warn", str(e))
                                        print(f"\n{e}")

                                case "4":
                                    print(f"Retirando tarjeta...")
                                    break
                            
                                case _:
                                    print(f"Opcion invalida. Vuelva a seleccionar una opcion")
                                    continue

                        except KeyboardInterrupt as e:
                            print(f"{e}")
                        except Exception as e:
                            print(f"\n{e}")

                except ValueError as e:
                    Logger.add_to_log("warn", str(e))
                    print(f"\n{e}")
                except Exception as e:
                    print(f"\n{e}")

        except ValueError as e:
            Logger.add_to_log("warn", str(e))
            print(f"\n{e}")
        except Exception as e:
            print(f"\n{e}")

        

