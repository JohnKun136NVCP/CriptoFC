# Ejercicios de 6 a 7
## Ejercicio 6
Como primer punto es el acomodo de matrices para que sea más sencillo es cifrado y así mismo el descifrado.

```python
IP = [
58,50,42,34,26,18,10,2,
60,52,44,36,28,20,12,4,
62,54,46,38,30,22,14,6,
64,56,48,40,32,24,16,8,
57,49,41,33,25,17,9,1,
59,51,43,35,27,19,11,3,
61,53,45,37,29,21,13,5,
63,55,47,39,31,23,15,7
]
FP = [
40,8,48,16,56,24,64,32,
39,7,47,15,55,23,63,31,
38,6,46,14,54,22,62,30,
37,5,45,13,53,21,61,29,
36,4,44,12,52,20,60,28,
35,3,43,11,51,19,59,27,
34,2,42,10,50,18,58,26,
33,1,41,9,49,17,57,25
]

E = [
32,1,2,3,4,5,
4,5,6,7,8,9,
8,9,10,11,12,13,
12,13,14,15,16,17,
16,17,18,19,20,21,
20,21,22,23,24,25,
24,25,26,27,28,29,
28,29,30,31,32,1
]

P = [
16,7,20,21,
29,12,28,17,
1,15,23,26,
5,18,31,10,
2,8,24,14,
32,27,3,9,
19,13,30,6,
22,11,4,25
]

PC1 = [
57,49,41,33,25,17,9,
1,58,50,42,34,26,18,
10,2,59,51,43,35,27,
19,11,3,60,52,44,36,
63,55,47,39,31,23,15,
7,62,54,46,38,30,22,
14,6,61,53,45,37,29,
21,13,5,28,20,12,4
]

PC2 = [
14,17,11,24,1,5,
3,28,15,6,21,10,
23,19,12,4,26,8,
16,7,27,20,13,2,
41,52,31,37,47,55,
30,40,51,45,33,48,
44,49,39,56,34,53,
46,42,50,36,29,32
]

KEY_SHIFT = [
1,1,2,2,2,2,2,2,
1,2,2,2,2,2,2,1
]
# S_BOXES
S_BOXES = [
[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
 [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
 [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
 [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],

[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
 [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
 [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
 [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],

[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
 [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
 [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
 [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],

[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
 [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
 [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
 [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],

[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
 [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
 [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
 [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],

[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
 [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
 [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
 [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],

[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
 [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
 [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
 [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],

[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
 [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
 [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
 [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

# --- FUNCIONES ---

def permute(block, table, bits):
    result = 0
    for p in table:
        result = (result << 1) | ((block >> (bits - p)) & 1)
    return result


def left_rotate(val, shift, size):
    return ((val << shift) & ((1 << size) - 1)) | (val >> (size - shift))


def sbox_substitution(block):
    result = 0
    for i in range(8):
        chunk = (block >> (42 - 6*i)) & 0x3F
        row = ((chunk & 0x20) >> 4) | (chunk & 1)
        col = (chunk >> 1) & 0xF
        result = (result << 4) | S_BOXES[i][row][col]
    return result


def generate_keys(key):
    keys = []
    key = permute(key, PC1, 64)

    left = (key >> 28) & 0xFFFFFFF
    right = key & 0xFFFFFFF

    for shift in KEY_SHIFT:
        left = left_rotate(left, shift, 28)
        right = left_rotate(right, shift, 28)

        combined = (left << 28) | right
        keys.append(permute(combined, PC2, 56))

    return keys


def des_block(block, keys):
    block = permute(block, IP, 64)

    left = (block >> 32) & 0xFFFFFFFF
    right = block & 0xFFFFFFFF

    for k in keys:
        temp = right

        right = permute(right, E, 32)
        right ^= k
        right = sbox_substitution(right)
        right = permute(right, P, 32)
        right ^= left

        left = temp

    combined = (right << 32) | left
    return permute(combined, FP, 64)


def des_encrypt(data, key):
    keys = generate_keys(key)
    result = b""

    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], "big")
        enc = des_block(block, keys)
        result += enc.to_bytes(8, "big")

    return result


def des_decrypt(data, key):
    keys = generate_keys(key)
    keys.reverse()
    result = b""

    for i in range(0, len(data), 8):
        block = int.from_bytes(data[i:i+8], "big")
        dec = des_block(block, keys)
        result += dec.to_bytes(8, "big")

    return result
message = b"noche697"
key_text = "data7Qa="
key = int.from_bytes(key_text.encode(), "big")
# En serio ya fue mucha ayuda xd, nada más tiene que investigar como convertir a base64 para cifrado y descifrado
# cipher = des_encrypt(message, key), cipher_base64 = base64.b64encode(cipher).decode("ascii") Con esto tienes el 98% del ejercicio xd.
# Solo la implemntación es para ir buscando en un archivo para el siguiente ejercicio, si quieres copiarlo y pegarlo solo CITALO xD.
```
Estas matrices ya están predefinidas por lo tanto no a que moverle ya que sino no va salir el cifrado y descifrado.

Ahora bien el pseudocódigo es:
```
// Todas las variables son de 64 bits sin signo

// Pre-procesamiento: rellenar con la diferencia de tamaño en bytes
rellenar el mensaje hasta alcanzar múltiplos de 64 bits de longitud

var clave // La clave proporcionada por el usuario
var claves[16]
var izquierda, derecha

// Generar claves

// PC1 (64 bits a 56 bits) 
clave := permutación(clave, PC1)
izquierda := (clave desplazamiento_derecha 28) and 0xFFFFFFF
derecha := clave and 0xFFFFFFF

para i desde 1 hasta 16 hacer
    derecha := rotar_izquierda(derecha, DESPLAZAMIENTO_clave[i])
    izquierda := rotar_izquierda(izquierda, DESPLAZAMIENTO_clave[i])
    var concatenado := (izquierda desplazamiento_izquierda 28) or derecha
    // PC2 (56 bits a 48 bits)
    claves[i] := permutación(concatenado, PC2)
fin para

// Para descifrar un mensaje invertir el orden de las claves
si descifrar entonces
    invertir claves
fin si

// Cifrar o Descifrar
para cada bloque de 64 bits del mensaje rellenado hacer
    var tmp

    // IP
    bloque := permutación(bloque, IP)
    izquierda := bloque desplazamiento_derecha 32
    derecha := bloque and 0xFFFFFFFF
    para i desde 1 hasta 16 hacer
        tmp := derecha
        // E (32 bits a 48 bits)
        derecha := expansión(derecha, E)
        derecha := derecha xor claves[i]
        // Sustitución (48 bits a 32 bits)
        derecha := sustitución(derecha)
        // P
        derecha := permutación(derecha, P)
        derecha := derecha xor izquierda
        izquierda := tmp
    fin para
    // Concatenar derecha e izquierda
    var bloque_cifrado := (derecha desplazamiento_izquierda 32) or izquierda
    // FP
    bloque_cifrado := permutación(bloque_cifrado, FP)
fin para
```

Por cierto para los ejercicio **6** y **7** no se permite utilizar módulos que hagan cifrado DES, sino lo tienen que contruir por ustedes mismos. Sin embargo, pueden usarlos como de guía.

Por ejemplo, este programa tiene varias cosas interesantes, vea el pseudocódigo y verá a lo que me refiero. 

```python
from Crypto.Cipher import DES
from Crypto.Random import get_random_bytes
import binascii

def des_encrypt(plaintext, key):
    # DES uses an 8-byte key (64 bits, 56 effective bits)
    # Key must be exactly 8 bytes
    if len(key) != 8:
        raise ValueError("Key must be exactly 8 bytes long")
        
    # EAX mode requires a nonce (Number used once)
    nonce = get_random_bytes(16) 
    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    
    # Data to be encrypted must be bytes
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    
    # Return nonce, ciphertext, and tag for decryption/verification
    return nonce, ciphertext, tag

def des_decrypt(nonce, ciphertext, tag, key):
    # Key must be exactly 8 bytes
    if len(key) != 8:
        raise ValueError("Key must be exactly 8 bytes long")

    cipher = DES.new(key, DES.MODE_EAX, nonce=nonce)
    try:
        # Decrypts and verifies the tag to ensure integrity
        decrypted_data = cipher.decrypt_and_verify(ciphertext, tag)
        return decrypted_data.decode('utf-8')
    except ValueError:
        return "Message is corrupted or key is incorrect"

    # --- Usage Example ---
    secret_key = b'root2026' # Generate a random 8-byte key
    original_message = "You cannot run on root! Use 777 to run it!"
    # Encrypt the message
    nonce, ciphertext, tag = des_encrypt(original_message, secret_key)
    print(f"Original: {original_message}")
    print(f"Encrypted (hex): {binascii.hexlify(ciphertext).decode('utf-8')}")
    cipher_base64 = base64.b64encode(ciphertext).decode("ascii")
    print("Cipher Base64:", cipher_base64)
    # Decrypt the message
    decrypted_message = des_decrypt(nonce, ciphertext, tag, secret_key)
    print(f"Decrypted: {decrypted_message}")

```
El que me diga con exactitud cuál es la diferencia entre su código y este, además tiene que ver con lo que se está implementando, tendrá un extra de 0.5 en su tarea.

## Ejercicio 7

Para este ejercicio es más como un ataque de fuerza bruta pero en este caso las llaves son a lo más de longitud 8 y el texto igual, eso tiene un razón de ser, más en la parte que dice de investigación.

Use el archivo [words](words.txt), implemente otro código en dónde pueda hacer una ataque por fuerza bruta en cada una de las llaves. (Sí da un resultado xd).

Pregunta (Sí es obligatoria contestar): ¿Qué pasaría si no se consiguiera las claves? ¿Cuánto tiempo se taradaría su computadora si solo supiera lo básico? 

## Ejercicio 8 
Vaya a la siguiente [sqlinyection](sqlinjection/README.md)
