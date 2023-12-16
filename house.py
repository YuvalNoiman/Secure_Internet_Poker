import socket
from random import randint
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.PublicKey import RSA, DSA
from Cryptodome.Signature import DSS, pss
from Cryptodome.Hash import SHA256

def main():

    # Create a two socket
    P1Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    P2Sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # Associate the socket with the port
    P1Sock.bind(('',1234))
    P2Sock.bind(('',1235))
    P1Sock.listen(100)
    P2Sock.listen(100)

    while True:
        print("Waiting for clients to connect...")

        Player1, P1Info = P1Sock.accept()
        Player2, P2Info = P2Sock.accept()

        print("Player1 connected from: " + str(P1Info))
        print("Player2 connected from: " + str(P2Info))

        privKey = RSA.import_key(open("privhouse.pem").read())
        rsa_decrypt = PKCS1_OAEP.new(privKey, hashAlgo=None, mgfunc=None, randfunc=None)

        # Receive the data the client has to send.
        # This will receive at most 1024 bytes
        P1SessionKey = rsa_decrypt.decrypt(Player1.recv(1024))
        P1Hash = SHA256.new(P1SessionKey)
        P1Signature = Player1.recv(1024)
        try:
            P1key = RSA.import_key(open("pub01RSA.pem").read())
            verifier = pss.new(P1key)
            verifier.verify(P1Hash, P1Signature)
        except:
            print("P1 using DSA signature")
        try:
            dsa = open("pub01DSA.pem", "r")
            P1key = DSA.import_key(dsa.read())
            dsa.close()
            verifier = DSS.new(P1key, 'fips-186-3')
            verifier.verify(P1Hash, P1Signature)
        except:
            print("P1 using RSA signature")
        P1cipher = AES.new(P1SessionKey, AES.MODE_ECB)
        P2SessionKey = rsa_decrypt.decrypt(Player2.recv(1024))
        P2Signature = Player2.recv(1024)
        try:
            P2key = RSA.import_key(open("pub02RSA.pem").read())
            verifier = pss.new(P2key)
            verifier.verify(P2Hash, P2Signature)
        except:
            print("P2 using DSA signature")
        try:
            dsa = open("pub02DSA.pem", "r")
            P2key = DSA.import_key(dsa.read()) 
            dsa.close()
            verifier = DSS.new(P2key, 'fips-186-3')
            verifier.verify(P2Hash, P2Signature)
        except:
            print("P2 using RSA signature")
        P2cipher = AES.new(P2SessionKey, AES.MODE_ECB)

	# Generates player one's numbers
        p1numbers = str(randint(1, 15)) + " " + str(randint(1, 15)) + " " + str(randint(1, 15))
	# Generates player two's numbers
        p2numbers = str(randint(1, 15)) + " " + str(randint(1, 15)) + " " + str(randint(1, 15))
        Player1.send(P1cipher.encrypt(pad(p1numbers.encode(), 16)))
        Player2.send(P2cipher.encrypt(pad(p2numbers.encode(), 16)))

        p1Score = 0
        p2Score = 0
        lost = "Round Lost!\n"
        lost = lost.encode()
        won = "Round Won!\n"
        won = won.encode()
        for x in range(3):
                P1num = Player1.recv(1024)
                P1num = unpad(P1cipher.decrypt(P1num),16)
                P2num = Player2.recv(1024)
                P2num = unpad(P2cipher.decrypt(P2num),16)
                if (int(P1num.decode()) < int(P2num.decode())):
                        Player1.send(P1cipher.encrypt(pad(lost, 16)))
                        Player2.send(P2cipher.encrypt(pad(won, 16)))
                        p2Score += 1
                else:
                        Player1.send(P1cipher.encrypt(pad(won, 16)))
                        Player2.send(P2cipher.encrypt(pad(lost, 16)))
                        p1Score += 1
        winner = "You won!"
        loser = "You lost!"
        if (p1Score < p2Score):
                Player1.send(P1cipher.encrypt(pad(loser.encode(), 16)))
                Player2.send(P2cipher.encrypt(pad(winner.encode(), 16)))
        else:
                Player1.send(P1cipher.encrypt(pad(winner.encode(), 16)))
                Player2.send(P2cipher.encrypt(pad(loser.encode(), 16)))
        Player1.close()
        Player2.close()
           


if __name__ == "__main__":
    main()