from services import SistemaCajero

def main():
    
    sistema = SistemaCajero()
    while True:
        try:
            print("\n" + "="*45)
            print("SISTEMA BANCARIO Y CAJERO ATM")
            print("="*45)
            
            print("\n--- AGENCIA BANCARIA  ---")
            print("[1]. Registrar nuevo cliente")
            print("[2]. Aperturar cuenta bancaria")
            print("[3]. Emitir tarjeta de débito")
            print("[4]. Depositar efectivo a cuenta") 
            
            print("\n--- OPERACIONES EN EL CAJERO ---")
            print("[5]. Consultar saldo disponible") 
            print("[6]. Retirar dinero efectivo") 
            print("[7]. Salir del sistema")

            opc = int(input("Ingrese una opción: "))
                
            match opc:
                case 1:
                    sistema.crear_usuario()
                case 2:
                    sistema.crear_y_vincular_cuenta()
                case 3:
                    sistema.crear_y_vincular_tarjeta()
                case 4:
                    sistema.depositar_fondos_cuenta()
                case 5:
                    pass
                case 6:
                    sistema.retirar_dinero_cajero()
                case 7:
                    print("Saliendo del sistema...")
                    break  
                case _:
                    print("pción inválida. Vuelva a seleccionar una opción.")

        except KeyboardInterrupt:
            print("\nPrograma interrumpido por el usuario (Ctrl+C). Saliendo...")
            break
        except Exception as e:
            print(f"\nError crítico inesperado: {e}")

if __name__ == "__main__":
    main()