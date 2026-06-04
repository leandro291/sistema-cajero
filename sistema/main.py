from models import Usuario, UsuarioSchema, Cuenta, CuentaSchema, Tarjeta, TarjetaSchema, Cajero, CajeroSchema
from services import SistemaCajero
from pydantic import ValidationError

diccionario_usuario = {}

def crear_usuario() -> None:
    print("========= CREACION DE USUARIO =========")

    nombre = input("Ingrese su nombre: ")
    dni = input("Digite su DNI: ")
    dinero_inicial = float(input("Ingrese con cuanto dinero se registrará: "))

    validador_usuario = UsuarioSchema(nombre=nombre, dni=dni, dinero_inicial=dinero_inicial)
    usuario = Usuario(nombre=validador_usuario.nombre, dni=validador_usuario.dni, dinero_inicial=validador_usuario.dinero_inicial)

    diccionario_usuario[usuario.dni] = usuario

    print("Usuario ha sido creado con exito")

def ver_usuarios() -> bool:

    if len(diccionario_usuario) == 0:

        print("El sistema actualmente no encuentra con usuarios registrados")
        return False

    print("========= VISUALIZACION DE USUARIOS =========")
    for key, value in diccionario_usuario.items():
        print(f"{key} -> {value}")

    return True

def vincular_cuenta() -> None:

    print("========= VINCULACION DE CUENTA =========")

    if not ver_usuarios():
        return False

    dni_usuario = input("Ingrese el DNI del usuario del usuario que desea crear cuenta: ")
    usuario_encontrado: "Usuario" = diccionario_usuario.get(dni_usuario, None)

    if not usuario_encontrado:
        print("El usuario no se encuentra en el sistema ")
        return
    
    print("========= CREACION DE CUENTA =========")
    print("[1]. Ahorro")
    print("[2]. Corriente")
    opc = int(input("Ingrese que tipo de cuenta desea registrar: "))

#xd

    #Aca podria hacer uso de un import ramdon para los numeros de la visa
    #Para la tarjeta un algoritmo de Luhn
    match(opc):
        case 1:
            validacion_cuenta = CuentaSchema(numero_cuenta="VISA-1092", tipo_cuenta="ahorro")
            cuenta = Cuenta(validacion_cuenta.numero_cuenta, validacion_cuenta.tipo_cuenta)
        case 2:
            validacion_cuenta = CuentaSchema(numero_cuenta="VISA-1092", tipo_cuenta="corriente")
            cuenta = Cuenta(validacion_cuenta.numero_cuenta, validacion_cuenta.tipo_cuenta)
        case _:
            print("El tipo de cuenta ingresado no es valido")
            return
        
    usuario_encontrado.crear_cuenta(cuenta=cuenta)
    print("Cuenta creada con exito")

def crear_tarjeta() -> bool:
    print("========= CREACION DE TARJETA =========")
    #Primero debe seleccionar a un usuario
    if not ver_usuarios():
        return False
    
    obtener_usuario = input("Ingrese el DNI: ")
    usuario_encontrado: "Usuario" = diccionario_usuario.get(obtener_usuario, None)

    if not usuario_encontrado:
        print("El usuario no se encuentra en el sistema ")
        return
    
    diccionario_cuentas = usuario_encontrado.cuentas
    for key, value in diccionario_cuentas.items():
        print(f"{key} -> {value}")
    
    obtener_cuenta = input("Ingrese el numero de Cuenta: ")
    cuentra_encontrada: "Cuenta" = diccionario_cuentas.get(obtener_cuenta, None)

    if not cuentra_encontrada:
        print("El usuario no se encuentra en el sistema ")
        return
    
    print("========= CREACION DE TARJETA =========")
    validacion_tarjeta = TarjetaSchema(pin="123456")
    tarjeta = Tarjeta(pin=validacion_tarjeta)

    cuentra_encontrada.vincular_tarjeta(tarjeta)

    print("La tarjeta se creado correctamente")
    return True 

def verificador_flujos() -> None:
    if not ver_usuarios():
        return False

    obtener_usuario = input("Ingrese el DNI: ")
    usuario_encontrado: "Usuario" = diccionario_usuario.get(obtener_usuario, None)

    if not usuario_encontrado:
        print("El usuario no se encuentra en el sistema ")
        return
    
    diccionario_cuentas = usuario_encontrado.cuentas

    if len(diccionario_cuentas) == 0:
        print(f"No se encuentran cuentas vinculadas a su nombre")
        return

    for key, value in diccionario_cuentas.items():
        print(f"{key} -> {value}")
    
    obtener_cuenta = input("Ingrese el numero de Cuenta: ")
    cuentra_encontrada: "Cuenta" = diccionario_cuentas.get(obtener_cuenta, None)

    if not cuentra_encontrada:
        print("El usuario no se encuentra en el sistema ")
        return
    
    print("========= VISUALIZACION DE TARJETAS =========")
    diccionario_tarjetas = cuentra_encontrada.tarjetas
    for key, value in diccionario_tarjetas.items():
        print(f"{key} -> {value}")
    
    return True

#Probando las clases aparte
def probar():
    try:
        
        user = Usuario("Leandro", "12345678", 1500.00)
        cuenta = Cuenta("VISA-1982", "ahorro")
        tarjeta = Tarjeta("123456")
        cajero = Cajero(5000.00)

        user.crear_cuenta(cuenta)
        cuenta.vincular_tarjeta(tarjeta)

        print(user)
        print(cuenta)

        user.depositar(cuenta, 200.0)

        print(user)
        print(cuenta)

        while True:

            cajero.retirar_dinero(cuenta, tarjeta, "123456", 100.00)
            break

        print(cuenta)
        print(cajero)



    except ValidationError as e:
        print(f"Error: {e}")

def main():

    try:

        while True:
            print("======== SISTEMA DE CAJERO ========")
            print("[1]. Registrar usuario")
            print("[2]. Vincular una cuenta")
            print("[3]. Vincular una tarjeta")
            print("[4]. Visualizar flujo magnetico")
            print("[5]. Salir")

            opc = int(input("Ingrese una opcion: "))

            match(opc):
                case 1:
                    crear_usuario()
                case 2:
                    vincular_cuenta()
                case 3:
                    crear_tarjeta()
                case 4:
                    verificador_flujos()
                case 5:
                    break

    except ValidationError as e:
        print(f"Error: {e}")
    except ValueError as e:
        print(f"Error: {e}")

def probar2():
    try:

        sistema = SistemaCajero()
        sistema.crear_usuario()
        sistema.crear_y_vincular_cuenta()
        print(sistema.usuarios)
        print(sistema.cuentas)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    #main()
    probar2()