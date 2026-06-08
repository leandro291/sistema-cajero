# Sistema de Gestión de Cajeros Automáticos (ATM)

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)
![Arquitectura](https://img.shields.io/badge/Arquitectura-MVC-success?style=for-the-badge)
![Seguridad](https://img.shields.io/badge/Seguridad-Bcrypt-red?style=for-the-badge)
![Auditoría](https://img.shields.io/badge/Auditoría-Logging-yellow?style=for-the-badge)

Un sistema desarrollado en Python que simula el sistema de una entidad bancaria y la interfaz de usuario de un cajero automático. El proyecto opera actualmente en memoria RAM.

## Características Principales

El sistema simula operaciones bancarias reales mediante los siguientes módulos:

* **Auditoría y Trazabilidad (Logs):**
  * Registro centralizado de errores, advertencias y excepciones (`Logger`) para facilitar la depuración y el monitoreo del sistema en tiempo real.
* **Seguridad y Autenticación:**
  * Validación de tarjetas mediante comprobación matemática con el **Algoritmo de Luhn**.
  * Encriptación y verificación de PINs usando `bcrypt`.
  * Bloqueo automático de tarjetas por seguridad tras 3 intentos fallidos consecutivos.
* **Administración Bancaria (Core):**
  * Registro y validación de nuevos clientes en el sistema.
  * Apertura de productos financieros (Cuentas de Ahorro y Corriente).
  * Emisión y vinculación de Tarjetas de Débito a cuentas específicas.
* **Operaciones de Cajero (ATM):**
  * Consulta interactiva de saldos.
  * Retiro de efectivo con validación cruzada (fondos del usuario vs. disponibilidad de billetes en la máquina).
  * Depósitos de fondos a cuentas.
  * Generación y lectura del historial de transacciones.

## Stack Tecnológico

* **Lenguaje:** Python Puro.
* **Validación de Datos:** Pydantic (Validación estricta de tipos).
* **Seguridad:** Bcrypt (Hashing de contraseñas/PINs).
* **Control de Errores:** Logging (Sistema de auditoría interno).

## Arquitectura y Diseño

El proyecto está diseñado bajo un **patrón arquitectónico MVC (Modelo-Vista-Controlador)**, desacoplando la interfaz de consola de las reglas de negocio.

```text
📦 sistema_cajero
 ┣ 📂 controllers
 ┃ ┗ 📜 sistema.py       # Cerebro del sistema (Reglas de negocio)
 ┣ 📂 models
 ┃ ┗ 📜 clases.py        # Entidades puras (Usuario, Cuenta, Tarjeta)
 ┣ 📂 utils
 ┃ ┣ 📜 logger.py        # Sistema de registro de eventos y errores
 ┃ ┗ 📜 validadores.py   # Utilidades independientes (Algoritmo de Luhn)
 ┣ 📂 views
 ┃ ┗ 📜 cajeroui.py      # Interfaz de consola e interacción con el usuario
 ┗ 📜 main.py            # Archivo de arranque
 ```

## ⚙️ Requisitos e Instalación

Para ejecutar este proyecto de manera local, tenemos que tener Python instalado y seguir estos pasos exactos en tu terminal:

**1. Clonar el repositorio y acceder a la carpeta:**
```bash
git clone https://github.com/leandro291/sistema-cajero
cd sistema
```

## 📦 Dependencias

Ejecuta los siguientes comandos en tu terminal uno por uno para instalar las librerías necesarias para el proyecto:

```bash
pip install annotated-types==0.7.0
pip install bcrypt==5.0.0
pip install pydantic==2.13.4
pip install pydantic_core==2.46.4
pip install typing-inspection==0.4.2
pip install typing_extensions==4.15.0
```

## 💻 Uso y Ejecución

El único punto de entrada de la aplicación es el archivo `main.py`. Asegúrate de estar ubicado en la raíz del proyecto en tu terminal y ejecuta el siguiente comando para iniciar el simulador bancario:

```bash
python main.py
```