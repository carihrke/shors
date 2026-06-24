# RSA system for understanding and exploring how RSA works.
#
# Authors: Carson Ihrke and Will Geiger
# Date: June 24 (modified)

import random

# Euclidean Algorithm to find greatest common divisor
# @params: desired values to calculate gcd (a, b)
# @return: gcd (a)
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

# Extended Euclidean Algorithm for modular inverse
# @params: public key (e), euler's totient value (phi)
# @return: multiplicative inverse (d)
def multiplicative_inverse(e, phi):

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

# Key Generation for RSA
# @params: prime composites of N (p, q)
# @return: public key pair (e, n), private key pair (d, n)
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

# Encryption via RSA
# @params: public key (public_key), input to encrypt (plaintext)
# @return: encrypted input (cipher)
def encrypt(public_key, plaintext):
    e, n = public_key
    # Convert chars to integers and compute c = m^e mod n
    cipher = [pow(ord(char), e, n) for char in plaintext]
    return cipher

# Decryption via RSA
# @params: private key (private_key), input to decrypt (ciphertext)
# @return: decrypted input (plain)
def decrypt(private_key, ciphertext):
    d, n = private_key
    # Compute m = c^d mod n and convert back to chars
    plain = [chr(pow(char, d, n)) for char in ciphertext]
    return ''.join(plain)

# Execution on simple values of p and q
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