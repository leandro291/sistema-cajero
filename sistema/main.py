from services import SistemaCajero
from pydantic import ValidationError

def main():

    while True:
        try:
            sistema = SistemaCajero()
            
            print("\n---- Sistema de Cajero (ATM) ----")
            print("[1]. Administracion")
            print("[2]. Movimiento virtual (Usuario <-> Cuenta) ")
            print("[3]. Movimiento Fisico (ATM)")
            print("[4]. Salir")

            opc = int(input("Ingrese una opcion: "))
                
            match(opc):
                case 1:

                    while True:
                        print("\n ---- Administracion ----")
                        print("[1]. Registrar nuevo usuario")
                        print("[2]. Vincular cuenta bancaria")
                        print("[3]. Emitir tarjeta de débito")
                        print("[4]. Salir")

                        opc = int(input("Ingrese una opcion: "))
                        
                        match(opc):
                            case 1:
                                sistema.crear_usuario()
                            case 2:
                                sistema.crear_y_vincular_cuenta()
                            case 3:
                                sistema.crear_y_vincular_tarjeta()
                            case 4:
                                break
                            case _:
                                print("Opcion invalida. Vuelva a seleccionar una opcion")

                case 2:

                    while True:
                        print("\n ---- Movimientos virtuales ----")
                        print("[1]. Transferencia entrante (Ingresar dinero)")
                        print("[2]. Transferencia saliente (Retirar a billetera)")
                        print("[3]. Salir")

                        opc = int(input("Ingrese una opcion: "))

                        match(opc):
                            case 1:
                                pass
                            case 2:
                                pass
                            case 3:
                                pass
                            case _:
                                pass

                case 3:
                    while True:
                        print("\n ---- Movimiento Fisico ----")
                        print("[1]. Usar Cajero Automático")
                        print("[2]. Salir")

                        opc = int(input("Ingrese una opcion: "))

                        match(opc):
                            case 1:
                                pass
                            case 2:
                                pass
                            case 3:
                                pass
                            case _:
                                pass
                    
                case 4:
                    print(f"Saliendo del sistema...")
                    break

                case _:
                    print("Opcion invalida. Vuelva a seleccionar una opcion")
        except KeyboardInterrupt as e:
            print(f"Error: {e}")
        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
