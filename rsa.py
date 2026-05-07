import random

# Helper: Euclidean Algorithm to find greatest common divisor
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Helper: Extended Euclidean Algorithm for modular inverse
def multiplicative_inverse(e, phi):
    d = 0
    x1, x2 = 0, 1
    y1, y2 = 1, 0
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi // e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2 - temp1 * x1
        y = y2 - temp1 * y1
        
        x2, x1 = x1, x
        y2, y1 = y1, y
    
    if temp_phi == 1:
        return y2 % phi

# 1. Key Generation
def generate_keypair(p, q):
    n = p * q
    phi = (p - 1) * (q - 1)

    # Choose e such that 1 < e < phi and gcd(e, phi) = 1
    e = 65537 # Common choice for e
    if gcd(e, phi) != 1:
        e = random.randrange(1, phi)
        while gcd(e, phi) != 1:
            e = random.randrange(1, phi)

    # Compute d (the private key exponent)
    d = multiplicative_inverse(e, phi)
    
    # Public key is (e, n), Private key is (d, n)
    return ((e, n), (d, n))

# 2. Encryption
def encrypt(public_key, plaintext):
    e, n = public_key
    # Convert chars to integers and compute c = m^e mod n
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

# 3. Decryption
def decrypt(private_key, ciphertext):
    d, n = private_key
    # Compute m = c^d mod n and convert back to chars
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# --- Execution ---
p = 61
q = 53
public, private = generate_keypair(p, q)

message = "Hello!"
encrypted_msg = encrypt(public, message)
decrypted_msg = decrypt(private, encrypted_msg)

print(f"Public Key: {public}")
print(f"Private Key: {private}")
print(f"Encrypted: {encrypted_msg}")
print(f"Decrypted: {decrypted_msg}")