from models import Cuenta, CuentaSchema, Usuario, UsuarioSchema
from typing import Dict

class SistemaCajero:
    def __init__(self):
        self.usuarios: Dict[str, "Usuario"]  = {}
        self.cuentas: Dict[str, "Cuenta"] = {}

    def _lista_de_usuarios(self) -> None:
        print("=== LISTA DE USUARIOS ===")
        for key, values in self.usuarios.items():
            print(f"{key} -> {values}")
    
    def crear_usuario(self) -> None:
        print(f"=======REGISTRO DE USUARIOS =======")
        nombre = input("Ingrese su nombre: ").strip().capitalize()
        dni = input("Ingrese su DNI: ").strip()
        dinero_inicial = float(input("Ingrese dinero incial: "))
        
        validacion_usuario = UsuarioSchema(
            nombre=nombre,
            dni=dni,
            dinero_inicial=dinero_inicial
        )

        usuario = Usuario(
            nombre=validacion_usuario.nombre,
            dni=validacion_usuario.dni,
            dinero_inicial=validacion_usuario.dinero_inicial
        )

        self.usuarios[usuario.dni] = usuario
        print(f"{usuario.nombre} ha sido registrado con exito")

    def crear_y_vincular_cuenta(self) -> None:
        print(f"======= VINCULACION DE CUENTAS =======")
        self._lista_de_usuarios()

        dni_usuario = input("Ingrese DNI del usuario al que desea vincular").strip()
        if dni_usuario not in self.usuarios:
            raise ValueError("El DNI ingresado no se encuentra registrado")

        numero_cuenta = input("Ingrese el numero de cuenta: ").strip()
        if numero_cuenta in self.cuentas:
            raise ValueError("La cuenta seleccionada ya se encuentra vinculada")

        tipo_cuenta = input("Ingrese su tipo de cuenta: ").strip()

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
        usuario: "Usuario" = self.usuarios[dni_usuario]
        usuario.vincular_cuenta(cuenta.numero_cuenta)
        print(f"La cuenta {cuenta.numero_cuenta} ha sido vinculada correctamente hacia {usuario.nombre}")

def main():
    sistema = SistemaCajero()

    sistema.crear_usuario()

    print(sistema.usuarios)

if __name__ == "__main__":
    main()