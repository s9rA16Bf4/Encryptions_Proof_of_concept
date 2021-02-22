#!/usr/bin/sage -python
from random import randint
from sage.all import is_prime, euler_phi, gcd, power_mod

# This program requires to be run in sagemath

class u1:
    alpha = {"a":0,"b":1, "c":2, "d":3, "e":4, "f":5, "g":6, "h":7, "i":8, "j":9, "k":10, "l":11,
            "m":12, "n":13, "o":14, "p":15, "q":16 , "r":17 , "s":18, "t":19, "u":20, "v":21, "w":22, "x":23,
            "y":24, "z":25, " ":26, ".":27, ",":28, "!":29, "?":30 }

    p = 0
    m = []
    c = []
    perm = [[], [], [], []]
    e = []
    n = []
    k = []
    std_length = 256

    def load_in_alpha(self, n):
        if (n not in alpha.keys()):
            self.alpha[n] = len(alpha)

    def set_msg_length(self, n):
        """ Sets the message length """
        if (type(n) != int):
            print("[Error] Expected a int. Got "+ str(type(n))+ ". Exiting!")
            return None
        else:
            self.std_length = n

    def set_p(self, p):
        """ Sets which value p should have """
        if (is_prime(p) is False):
            print("[Error] The value of p must be a prime!")
            return None

        if (euler_phi(p) < self.std_length):
            print("[Warning] Weak value for p. Only "+str(euler_phi(p))+" possible values for e and k")
        if (euler_phi(p-1) < self.std_length):
            print("[Warning] Weak value for p-1. Only "+str(euler_phi(p-1))+" possible values for n")
        self.p = p

    def load_msg(self, m):
        for c in m:
            try:
                self.m.append(self.char_to_dec(c))
            except:
                print("[Error]: Unknown character "+ str(c))

    def load_crypt(self, c):
        if (type(c) == list):
            self.c = c
        else:
            print("You're gonna have to manually convert every block")
            

    def load_perm(self, perm):
        temp_perm = []
        for i, _ in enumerate(self.perm):
            temp_perm.append(perm[i])
        self.perm = temp_perm

    def load_e(self, e):
        self.e = e

    def load_k(self, k):
        self.k = k

    def load_n(self, n):
        self.n = n       

    def encrypt_all(self):
        """ Wrapper """
        if (self.p == 0):
            print("[Error] You must set a value on P beforehand")
            return None
        if (len(self.m) == 0):
            print("[Error] You must load your message beforehand")
            return None
        
        print("[Status] Setup face, generating all values")
        self.gen_perm()
        self.gen_n()
        self.gen_e()
        self.gen_k()
        self.buff_msg()


        print("[Status] Encrypting message")
        for i, _ in enumerate(self.m):
            self.c.append(self.encrypt(self.m[self.perm[0][i]], self.e[self.perm[1][i]], self.n[self.perm[2][i]] , self.k[self.perm[3][i]], self.p))
        print("\n[Status] Your encrypted message is..")
        print(self.c)

        print("\nor..")
        temp = ""
        for n in self.c:
            if (n < len(self.alpha)):
                n = self.dec_to_char(n)
            temp += str(n)
        print(temp)

        print("\n[Imporant] And your keys are..")
        print("\nPerms: "+str(self.perm))
        print("\nE: "+ str(self.e))
        print("\nK: "+ str(self.k))
        print("\nN: "+ str(self.n))

    def decrypt_all(self):
        """ Wrapper """
        if (self.p == 0):
            print("[Error] You must set a value on P beforehand")
            return None
        if (len(self.c) == 0):
            print("[Error] You must load your encrypted message beforehand")
            return None
        if (len(self.perm[0]) == 0):
            print("[Error] You must load your permutations beforehand")
            return None
        if (len(self.n) == 0 or len(self.e) == 0 or len(self.k) == 0):
            print("[Error] You must load your keys beforehand")
            return None
        
        print("[Status] Setup face, generating all inverse values")
        self.perm[0] = self.gen_inv_perm(self.perm[0])
        self.gen_inv_n()
        self.gen_inv_e()
        self.gen_inv_k()

        print("[Status] Decrypting message")
        temp = []
        for i, _ in enumerate(self.c):
            temp.append(self.decrypt(self.c[self.perm[0][i]], self.e[self.perm[1][self.perm[0][i]]], self.n[self.perm[2][self.perm[0][i]]] , self.k[self.perm[3][self.perm[0][i]]], self.p))
        temp2 = ""
        for n in temp:
            if (n < len(self.alpha)):
                n = self.dec_to_char(n)
                if (n == "x"):
                    break
            temp2 += str(n)
        print("[Status] Your decrypted message is..")
        print(temp2)

    
    def encrypt(self, m, e, n, k, p):
        """ Encrypts the char m """
        return ((((m*e*(k**2))**n)) % p)

    def decrypt(self, c, d, n, k, p):
        """ Decrypts the encrypted charcter c """
        return (((c**n)* d *(k**2)) % p)

    def dec_to_char(self, n):
        """ Returns the character based upon the integer value, else None """
        for key in self.alpha.keys():
            if (self.alpha[key] == n):
                return key
        return None
        
    def char_to_dec(self, n):
        """ Returns the integer value for the character n, else None """
        try:
            return self.alpha[n.lower()]
        except:
            return None
    
    def gen_perm(self):
        """ Generates a permutation """
        for li in self.perm:
            while(len(li) < self.std_length):
                rand = randint(0, self.std_length-1)
                if (rand not in li):
                    li.append(rand)

    def gen_inv_all_perm(self):
        """ Returns the inverse for the loaded permuations """
        temp_perm = [[], [], [], []]
        for x, li in enumerate(temp_perm):
            for std in range(0, len(self.perm[x])):
                for i,val in enumerate(self.perm[x]):
                    if (std == val):
                        li.append(i)
        self.perm = temp_perm

    def gen_inv_perm(self, n):
        if (type(n) != list):
            print("[Error] Expected a list, got a "+ str(type(n))+ ". Exiting!")
        else:
            temp_perm = []
            for std in range(0, len(n)):
                for i,val in enumerate(n):
                    if (std == val):
                        temp_perm.append(i)
            return temp_perm


    def buff_msg(self):
        """ Extends the message length by adding extra characters """
        while(len(self.m) < self.std_length):
            self.m.append(self.alpha["x"])

    def gen_n(self):
        x = 2
        while(len(self.n) < self.std_length):
            x = x % (self.p-1) -1
            if (gcd(x, self.p-1) == 1):
                self.n.append(x)
            x += 7

    def gen_inv_n(self):
        temp = []
        for n in self.n:
            temp.append(power_mod(n, -1, self.p-1))
        self.n = temp

    def gen_k(self):
        x = 2
        while(len(self.k) < self.std_length):
            x = ((x)**2)%self.p
            if (gcd(x, self.p) == 1):
                self.k.append(x)
            x += 7

    def gen_inv_k(self):
        temp = []
        for n in self.k:
            temp.append(power_mod(n, -1, self.p))
        self.k = temp

    def gen_e(self):
        x = 2
        while(len(self.e) < self.std_length):
            x = x%self.p
            if (gcd(x, self.p) == 1):
                self.e.append(x)
            x += 7

    def gen_inv_e(self):
        temp = []
        for n in self.e:
            temp.append(power_mod(n, -1, self.p))
        self.e = temp
