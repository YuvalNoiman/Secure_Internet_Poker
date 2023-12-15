import socket
import sys
from Cryptodome.Cipher import AES
import secrets
import string
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

def main(player_number):

    #creates socket
    Player = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created
    if player_number == 1:
        Player.connect(("127.0.0.1", 1234)) #attempts to create at specified IP at specified port
        privKey = RSA.import_key(open("pub01.pem").read())	
    else:
        Player.connect(("127.0.0.1", 1235)) #attempts to create at specified IP at specified port
        privKey = RSA.import_key(open("pub02.pem").read())	
    #sends session key
    PSessionKey = ''.join(secrets.choice(string.ascii_uppercase + string.digits)
              for i in range(16))
    rsa_encrypt = PKCS1_OAEP.new(privKey, hashAlgo=None, mgfunc=None, randfunc=None)
    PSessionKey = PSessionKey.encode()
    Pcipher = AES.new(PSessionKey, AES.MODE_ECB)
    PSK = rsa_encrypt.encrypt(PSessionKey)
    Player.send(PSK)
    pnumbers = Player.recv(1024)
    pnumbers = unpad(Pcipher.decrypt(pnumbers),16)
    Parray = pnumbers.decode().split(" ")
    #round 1
    print(Parray)
    number_picked = input("Pick a number 1-3 which corresponds to shown value: ")
    Player.send(Pcipher.encrypt(pad(Parray[int(number_picked)-1].encode(),16)))
    Parray.pop(int(number_picked)-1)
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
    #round2
    print(Parray)
    number_picked = input("Pick a number 1-2 which corresponds to shown value: ")
    Player.send(Pcipher.encrypt(pad(Parray[int(number_picked)-1].encode(),16)))
    Parray.pop(int(number_picked)-1)
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
    #round3
    print("Your only number left is: " + Parray[0])
    Player.send(Pcipher.encrypt(pad(Parray[0].encode(),16)))
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
    #recv results
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
	

if __name__ == "__main__":
    player_number = sys.argv[1]
    main(int(player_number))

