def limpiar_strings(texto: str) -> str:

    if not isinstance(texto, str):
        raise ValueError("Tipo de valor invalido, debe ser un string")
    
    texto_limpio = texto.strip()

    if not texto_limpio:
        raise ValueError("El texto no se debe encontrar vacio")
    
    return texto_limpio