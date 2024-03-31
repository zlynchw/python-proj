from __future__ import print_function
import gmpy2
import time


# generate prime number
def __generate_prime__(rs):
    p = gmpy2.mpz_urandomb(rs, 1024)
    while not gmpy2.is_prime(p):
        p += 1
    return p


# generate L(x)
def __el__(x, n):
    fx = gmpy2.c_div((x - 1), n)
    return int(fx)


# key generation
def keygen():
    while True:
        random_state = gmpy2.random_state(int(time.time()))
        p = __generate_prime__(random_state)
        q = __generate_prime__(random_state)
        if gmpy2.gcd((p * q), ((p - 1) * (q - 1))) == 1:
            break
    n = p * q
    lmd = gmpy2.lcm((p - 1), (q - 1))
    random_state = gmpy2.random_state(int(time.time()))
    g = gmpy2.mpz_random(random_state, n ** 2)
    x = gmpy2.powmod(g, lmd, n ** 2)
    el1 = __el__(x, n)
    mu = gmpy2.powmod(el1, (-1), n)
    return (n, g), (lmd, mu, n)


# encryption of plaintext
def encrypt(plaintext, public_key):
    m = int(plaintext)
    n, g = public_key
    random_state = gmpy2.random_state(int(time.time()))
    r = gmpy2.mpz_random(random_state, n)
    c = gmpy2.powmod(g, m, n ** 2) * gmpy2.powmod(r, n, n ** 2)
    return c


# decryption of ciphertext
def decrypt(ciphertext, private_key):
    c = ciphertext
    lmd, mu, n = private_key
    x = gmpy2.powmod(c, lmd, n ** 2)
    el2 = __el__(x, n)
    result = gmpy2.mod((el2 * mu), n)
    return result


# main
if __name__ == "__main__":
    public_key1, private_key1 = keygen()
    plaintext1 = input("Enter first number:")
    plaintext2 = input("Enter second number:")
    ciphertext1 = encrypt(plaintext1, public_key1)
    ciphertext2 = encrypt(plaintext2, public_key1)
    result1 = ciphertext1 * ciphertext2
    result2 = decrypt(result1, private_key1)
    print("Ciphertext of first number:", ciphertext1.digits())
    print("Ciphertext of second number:", ciphertext2.digits())
    print("New Ciphertext:", result1.digits())
    print("New Plaintext:", result2.digits())
