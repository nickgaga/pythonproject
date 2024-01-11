from cryptography.fernet import Fernet

# Genera una chiave casuale
key = Fernet.generate_key()

# Crea un oggetto Fernet con la chiave generata
cipher = Fernet(key)

# Dati da crittografare
data = b"Il mio messaggio segreto"

# Crittografa i dati
encrypted_data = cipher.encrypt(data)

print("Dati crittografati:", encrypted_data)

# Decrittografa i dati
decrypted_data = cipher.decrypt(encrypted_data)

print("Dati decrittografati:", decrypted_data)
