"""
functions for prime number generation, coprime testing, ...
"""

def findPrimes_simple(upper=100):
    """
    create list of prime numbers explicitely
    using the modulo operator
    """
    # set array of prime numbers to empty array
    primes=[]
    # loop over potential prime numbers
    for n in range(2,upper):
        # inner loop to check division
        isprime=True
        for i in range(2,n):
            if ((n % i) == 0):
                isprime=False
               #break
        if (isprime): primes.append(n)
    return primes


def isPrime_list(n):
    import sys
    # create list of prime numbers
    primeList = findPrimes_simple(1000)
    # check is number is larger than larest element in list
    if (n > prime_list[-1]):
        sys.exit('Error: number larger than maximum in tabulated primes')
    # check if number is in list
    if n in primeList:
        return True
    return False


def isPrimeRabinMiller(n):
    """
    uses Rabin-Miller algorithm to estimate if n is a prime
    """
    import random
    # check if number is even, then break
    if n % 2 == 0: return False
    
    s = n - 1
    t = 0
    while s % 2 == 0:
        # keep halving s while it is even (and use t
        # to count how many times we halve s)
        s = s // 2
        t += 1
    for trials in range(5): # try to falsify num's primality 5 times
        a = random.randrange(2,n-1)
        v = pow(a, s, n)
        if v != 1: # this test does not apply if v is 1.
            i = 0
            while v != (n-1):
                if i == t-1:
                    return False
                else:
                    i += 1
                    v = (v**2) % n
    return True


def generateLargePrime(keysize=1024):
    """
    Return a random prime number of keysize bits in size
    """
    import random
    while True:
        number = random.randrange(2**(keysize-1), 2**(keysize))
        if isPrimeRabinMiller(number):
            return number


def primeFactors(n):
    """
    Determine all prime factors of a composite number
    """
    import numpy
    factors = []
    # first check how many 2 are in as prime factors
    while (n%2 == 0):
        factors.append(2)
        n = n/2
    # then, n is retured as odd number, and next we check other prime factors
    for i in range(3,int(numpy.sqrt(n))+1,2):
        while (n%i == 0):
            factors.append(i)
            n = n/i
    # remaining factor ...
    if (n > 2):
        factors.append(int(n))
    return factors


def greatestCommonDivisor(a,b):
    """
    Determine greatest common divisor for two numbers a,b
    """
    r = a%b
    while r:
        a = b
        b = r
        r = a%b
    return b


def RSAcreateKeys(keySize=1024):
    """
    create public-private key sequence for RSA crypting
    """
    import random
    import myCrypt
    # generate two large prime
    p = myCrypt.generateLargePrime(keySize)
    q = myCrypt.generateLargePrime(keySize)
    # calculate product of primes
    n = p*q
    # calculate phi-function
    phi=(p-1)*(q-1)
    # search number e, which is coprime to phi
    while True:
        # Keep trying random numbers for e until one is valid.
        e = random.randrange(2**(keySize-1),2**(keySize))
        if myCrypt.greatestCommonDivisor(e, (p-1)*(q-1)) == 1:
            break
    # calculate d as modular inverse e mod phi
    d = pow(e,-1,phi)    
    #print(p,q,n,e,d)
    # save askey pair
    publicKey = (keySize,n,e)
    privateKey = (keySize,n,d)
    return publicKey,privateKey


def RSAencrypt(message,publicKey,debug=False):
    """
    RSA encryption of a string, using the locale
    """
    # key key elements
    keySize,n,e = publicKey
    # conver text from string to byte
    messageBytes = message.encode()
    # encode bytes with RSA public key
    encrypt = []
    for byte in messageBytes:
        # encrypt with public key
        encrypt.append(pow(byte,e,n))
    if (debug):
        print(encrypt)
    return encrypt


def RSAdecrypt(cryptedMessage,privateKey,debug=False):
    """
    RSA encryption of a string, using the locale
    """
    # key key elements
    keySize,n,d = privateKey
    # decode bytes with private key
    decrypt = []
    for byte in cryptedMessage:
        decrypt.append(pow(byte,d,n))
    if (debug):
        print(decrypt)
    # convert byte array to string array and decode with unicode
    decrypt = bytearray(decrypt).decode()
    return decrypt
