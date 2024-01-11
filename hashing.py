import hashlib

stringa = "Ciao, mondo!"
hash_object = hashlib.sha256(stringa.encode())
hash_value = hash_object.hexdigest()

print("Stringa originale:", stringa)
print("Valore di hash SHA-256:", hash_value)
