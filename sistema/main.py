from models import Usuario, UsuarioSchema, Cuenta, CuentaSchema
from pydantic import ValidationError

diccionario_usuario = {}

def crear_usuario() -> None:
    print("========= CREACION DE USUARIO =========")

    nombre = input("Ingrese su nombre: ")
    dni = input("Digite su DNI: ")
    dinero_inicial = float(input("Ingrese con cuanto dinero se registrará: "))

    validador_usuario = UsuarioSchema(nombre=nombre, dni=dni, dinero_inicial=dinero_inicial)
    usuario = Usuario(nombre=validador_usuario.nombre, dni=validador_usuario.dni, dinero_incial=validador_usuario.dinero_inicial)

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
    
def main():

    try:

        while True:
            print("======== SISTEMA DE CAJERO ========")
            print("[1]. Crear nuevo usuario")
            print("[2]. Vincular una nueva cuenta")
            print("[3]. Ver usuarios de sapaso")
            print("[4]. Salir")

            opc = int(input("Ingrese una opcion: "))

            match(opc):
                case 1:
                    crear_usuario()
                case 2:
                    vincular_cuenta()
                case 3:
                    ver_usuarios()
                case 4:
                    break

    except ValidationError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()