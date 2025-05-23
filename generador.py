import secrets

def generar_secret_key(length=32):
  """
  Genera una clave secreta criptográficamente segura.

  Args:
    length (int): La longitud deseada de la clave en bytes.
                  Por defecto es 32 bytes (256 bits), que es una longitud común y segura.

  Returns:
    str: La clave secreta generada, codificada en hexadecimal.
  """
  return secrets.token_hex(length)

if __name__ == "__main__":
  # Generar una clave secreta de 32 bytes (256 bits)
  secret_key = generar_secret_key()
  print(f"Tu clave secreta generada: {secret_key}")
  print(f"Longitud de la clave (en caracteres hexadecimales): {len(secret_key)}")
  print(f"Longitud de la clave (en bytes, original): {len(secret_key) // 2}")

  print("\n--- Ejemplos con diferentes longitudes ---")
  # Generar una clave de 16 bytes (128 bits)
  secret_key_16 = generar_secret_key(16)
  print(f"Clave de 16 bytes: {secret_key_16}")
  print(f"Longitud (caracteres): {len(secret_key_16)}")

  # Generar una clave de 64 bytes (512 bits)
  secret_key_64 = generar_secret_key(64)
  print(f"Clave de 64 bytes: {secret_key_64}")
  print(f"Longitud (caracteres): {len(secret_key_64)}")