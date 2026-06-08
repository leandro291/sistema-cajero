def limpiar_strings(texto: str) -> str:

    if not isinstance(texto, str):
        raise ValueError("Tipo de valor invalido, debe ser un string")
    
    texto_limpio = texto.strip()

    if not texto_limpio:
        raise ValueError("El texto no se debe encontrar vacio")
    
    return texto_limpio

def validar_luhn(numero):
    digitos = str(numero).replace(" ", "")
    
    if not digitos.isdigit():
        return False
        
    suma = 0
    es_segundo = False
    
    for digito in reversed(digitos):
        valor = int(digito)
        
        if es_segundo:
            valor *= 2
            if valor > 9:
                valor = (valor % 10) + 1
                
        suma += valor
        es_segundo = not es_segundo
        
    return suma % 10 == 0