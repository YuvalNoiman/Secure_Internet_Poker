import socket
import sys
import secrets
import string
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.PublicKey import RSA, DSA
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Signature import DSS, pss
from Cryptodome.Hash import SHA256

def main(player_number):

    #creates socket
    Player = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created
    if player_number == 1:
        Player.connect(("127.0.0.1", 1234)) #attempts to create at specified IP at specified port
        rsa_sig = RSA.import_key(open("priv01RSA.pem").read())
        dsa_sig = open("priv01DSA.pem", "r")
    else:
        Player.connect(("127.0.0.1", 1235)) #attempts to create at specified IP at specified port
        rsa_sig = RSA.import_key(open("priv02RSA.pem").read())
        dsa_sig = open("priv02DSA.pem", "r")

    #sends session key
    pubKey = RSA.import_key(open("pubhouse.pem").read())
    PSessionKey = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(16))
    PSessionKey = PSessionKey.encode()
    rsa_encrypt = PKCS1_OAEP.new(pubKey, hashAlgo=None, mgfunc=None, randfunc=None)
    hash = SHA256.new(PSessionKey)
    #picks signature type
    while True:
        number_picked = input("Type number 1 for RSA and number 2 for DSA: ")
        if (number_picked == "1"):
            signature = pss.new(rsa_sig).sign(hash)
            break
        elif (number_picked == "2"):
            signer = DSS.new(dsa_sig, 'fips-186-3')
            signature = signer.sign(hash)
            break
        else:
            print("Type a valid number!")	

    Pcipher = AES.new(PSessionKey, AES.MODE_ECB)
    PSK = rsa_encrypt.encrypt(PSessionKey)
    Player.send(PSK)
    Player.send(signature)
    pnumbers = Player.recv(1024)
    pnumbers = unpad(Pcipher.decrypt(pnumbers),16)
    Parray = pnumbers.decode().split(" ")
    #round 1
    print(Parray)
    while True:
        number_picked = input("Pick a number 1-3 which corresponds to shown value: ")
        if (number_picked == "1" or number_picked == "2" or number_picked == "3"):
            break
        else:
            print("Pick a valid number!")
    Player.send(Pcipher.encrypt(pad(Parray[int(number_picked)-1].encode(),16)))
    Parray.pop(int(number_picked)-1)
    win_or_loss = Player.recv(1024)
    print(unpad(Pcipher.decrypt(win_or_loss),16).decode())
    #round2
    print(Parray)
    while True:
        number_picked = input("Pick a number 1-2 which corresponds to shown value: ")
        if (number_picked == "1" or number_picked == "2"):
            break
        else:
            print("Pick a valid number!")
    Player.send(Pcipher.encrypt(pad(Parray[int(number_picked)-1].encode(),16)))
    Parray.pop(int(number_picked)-1)
    win_or_loss = Player.recv(1024)
    print(unpad(Pcipher.decrypt(win_or_loss),16).decode())
    #round3
    print("Your only number left is: " + Parray[0])
    Player.send(Pcipher.encrypt(pad(Parray[0].encode(),16)))
    win_or_loss = Player.recv(1024)
    print(unpad(Pcipher.decrypt(win_or_loss),16).decode())
    #recv results
    win_or_loss = Player.recv(1024)
    print(unpad(Pcipher.decrypt(win_or_loss),16).decode())
	

if __name__ == "__main__":
    player_number = sys.argv[1]
    main(int(player_number))

