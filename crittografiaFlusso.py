def KSA(key):
    key_length = len(key)
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % key_length]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def PRGA(S):
    i = 0
    j = 0
    while True:
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        K = S[(S[i] + S[j]) % 256]
        yield K

def RC4(key, plaintext):
    S = KSA(key)
    keystream = PRGA(S)
    ciphertext = []
    for byte in plaintext:
        ciphertext.append(byte ^ next(keystream))
    return bytes(ciphertext)
def print_bits(byte):
    # Stampa i bit di un byte come una sequenza di 0 e 1
    for i in range(7, -1, -1):
        bit = (byte >> i) & 1
        print(bit, end='')
    print()
key = b'Key'  # Chiave di esempio
plaintext = b'Hello, world!'  # Testo in chiaro di esempio

ciphertext = RC4(key, plaintext)


print("Testo cifrato:", ciphertext)
for byte in ciphertext:
    print_bits(byte)

decrypted_text = RC4(key, ciphertext)


print("Testo decifrato:", decrypted_text.decode())

for byte in decrypted_text:
    print_bits(byte)
