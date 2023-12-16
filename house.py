import socket
from Cryptodome.Random.random import randint
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
    P1new = True
    P2new = True
    privKey = RSA.import_key(open("privhouse.pem").read())
    rsa_decrypt = PKCS1_OAEP.new(privKey, hashAlgo=None, mgfunc=None, randfunc=None)
    lost = "Round Lost!\n".encode()
    won = "Round Won!\n".encode()
    tie = "Round tied!\n".encode()
    winner = "You won!\n".encode()
    loser = "You lost!\n".encode()
    tied = "You tied!\n".encode()

    while True:
        if (P1new or P2new):
            print("Waiting for clients to connect...")

        if (P1new):
            P1Sock.listen(100)
            Player1, P1Info = P1Sock.accept()
            print("Player1 connected from: " + str(P1Info))
        if (P2new):
            P2Sock.listen(100)
            Player2, P2Info = P2Sock.accept()
            print("Player2 connected from: " + str(P2Info))

        # Receive the data the client has to send.
        # This will receive at most 1024 bytes
        if (P1new):
            P1SessionKey = rsa_decrypt.decrypt(Player1.recv(1024))
            P1Hash = SHA256.new(P1SessionKey)
            P1Signature = Player1.recv(1024)
            secure = 0
            try:
                P1key = RSA.import_key(open("pub01RSA.pem").read())
                verifier = pss.new(P1key)
                verifier.verify(P1Hash, P1Signature)
            except:
                secure += 1
                print("P1 using DSA signature")
            try:
                dsa = open("pub01DSA.pem", "r")
                P1key = DSA.import_key(dsa.read())
                dsa.close()
                verifier = DSS.new(P1key, 'fips-186-3')
                verifier.verify(P1Hash, P1Signature)
            except:
                secure += 1
                print("P1 using RSA signature")
            if (secure == 2):
                print("P1 session key not verified")
            P1cipher = AES.new(P1SessionKey, AES.MODE_ECB)

        if (P2new):
            P2SessionKey = rsa_decrypt.decrypt(Player2.recv(1024))
            P2Hash = SHA256.new(P2SessionKey)
            P2Signature = Player2.recv(1024)
            secure = 0
            try:
                P2key = RSA.import_key(open("pub02RSA.pem").read())
                verifier = pss.new(P2key)
                verifier.verify(P2Hash, P2Signature)
            except:
                secure += 1
                print("P2 using DSA signature")
            try:
                dsa = open("pub02DSA.pem", "r")
                P2key = DSA.import_key(dsa.read()) 
                dsa.close()
                verifier = DSS.new(P2key, 'fips-186-3')
                verifier.verify(P2Hash, P2Signature)
            except:
                secure += 1
                print("P2 using RSA signature")
            if (secure == 2):
                print("P2 session key not verified")
            P2cipher = AES.new(P2SessionKey, AES.MODE_ECB)

	# Generates player one's numbers
        p1numbers = str(randint(1, 15)) + " " + str(randint(1, 15)) + " " + str(randint(1, 15))
	# Generates player two's numbers
        p2numbers = str(randint(1, 15)) + " " + str(randint(1, 15)) + " " + str(randint(1, 15))
        Player1.send(P1cipher.encrypt(pad(p1numbers.encode(), 16)))
        Player2.send(P2cipher.encrypt(pad(p2numbers.encode(), 16)))

        p1Score = 0
        p2Score = 0
        for x in range(3):
            P1num = unpad(P1cipher.decrypt(Player1.recv(1024)),16).decode()
            P2num = unpad(P2cipher.decrypt(Player2.recv(1024)),16).decode()
            if (int(P1num) < int(P2num)):
                Player1.send(P1cipher.encrypt(pad(lost, 16)))
                Player2.send(P2cipher.encrypt(pad(won, 16)))
                p2Score += 1
            elif (int(P1num) > int(P2num)):
                Player1.send(P1cipher.encrypt(pad(won, 16)))
                Player2.send(P2cipher.encrypt(pad(lost, 16)))
                p1Score += 1
            else:
                Player1.send(P1cipher.encrypt(pad(tie, 16)))
                Player2.send(P2cipher.encrypt(pad(tie, 16)))

        #determine winner
        if (p1Score < p2Score):
            Player1.send(P1cipher.encrypt(pad(loser, 16)))
            Player2.send(P2cipher.encrypt(pad(winner, 16)))
        elif (p1Score > p2Score):
            Player1.send(P1cipher.encrypt(pad(winner, 16)))
            Player2.send(P2cipher.encrypt(pad(loser, 16)))
        else:
            Player1.send(P1cipher.encrypt(pad(tied, 16)))
            Player2.send(P2cipher.encrypt(pad(tied, 16)))

        P1Again = Player1.recv(1024)
        P1Again = unpad(P1cipher.decrypt(P1Again),16)
        P2Again = Player2.recv(1024)
        P2Again = unpad(P2cipher.decrypt(P2Again),16)
        P1new = False
        P2new = False
        if (P1Again.decode() == "Done Playing"):
            P1new = True
            Player1.close()
            del P1SessionKey, P1cipher, P1Hash
        if (P2Again.decode() == "Done Playing"):
            P2new = True
            Player2.close()
            del P2SessionKey, P2cipher, P2Hash
           


if __name__ == "__main__":
    main()