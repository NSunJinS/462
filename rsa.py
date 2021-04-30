import random
import math

def isPrime(x):
    factors = 0
    for i in range(int(x/2)):
        if  x % (i+1) == 0:
            factors+=1
    return factors == 1

prime_lb = 3
prime_ub = 512
primes = [x for x in range(prime_lb, prime_ub) if isPrime(x)]

# Adapted from https://www.geeksforgeeks.org/multiplicative-inverse-under-modulo-m/
def modInverse(a, m):
    m0 = m
    y = 0
    x = 1

    while (a > 1):
        q = a // m
        t = m

        # Euclidean algorithm
        m = a % m
        a = t
        t = y

        y = x - q * y
        x = t
    
    return x + m0 if x < 0 else x

class RSAKey:
    def __init__(self):
        self.p = None
        self.q = None
        self.n = None
        self.e = None
        self.d = None
    
    def generateKey(self):
        # Randomly pull two prime numbers
        self.p = random.choice(primes)
        primes.remove(self.p)
        self.q = random.choice(primes)
        
        self.n = self.p*self.q
        
        # Find viable e
        a = self.p-1
        b = self.q-1
        c = a*b
        m = abs(a*b) // math.gcd(a, b)

        self.e = 0
        # e must be coprime to c
        for x in range(2, c):
            if math.gcd(x, c) == 1:
                self.e = x
                break

        # Find d
        self.d = modInverse(self.e, m)

    def getPublicKey(self):
        return self.e

    def getPrivateKey(self):
        return self.d

    # Assumes msg is a string of chars
    def encryptMsg(self,msg):
        return [ord(msg[x])**self.e % self.n for x in range(0, len(msg))]

    # Assumes ctext is an array of integers
    def decryptMsg(self,ctext):
        return [ctext[x]**self.d % self.n for x in range(0, len(ctext))]