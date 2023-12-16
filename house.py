import socket
from random import randint
from Cryptodome.Cipher import AES
from Cryptodome.Util.Padding import pad
from Cryptodome.Util.Padding import unpad
from Cryptodome.PublicKey import RSA
from Cryptodome.Cipher import PKCS1_OAEP

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

        #PB1 = RSA.import_key(open("priv01.pem").read())
        #PB2 = RSA.import_key(open("priv02.pem").read())
        #rsa_decrypt1 = PKCS1_OAEP.new(PB1, hashAlgo=None, mgfunc=None, randfunc=None)
        #rsa_decrypt2 = PKCS1_OAEP.new(PB2, hashAlgo=None, mgfunc=None, randfunc=None)
        privhouse = RSA.import_key(open("privhouse.pem").read())
        rsa_decrypt = PKCS1_OAEP.new(privhouse, hashAlgo=None, mgfunc=None, randfunc=None)

        # Receive the data the client has to send.
        # This will receive at most 1024 bytes
        P1SessionKey = rsa_decrypt.decrypt(Player1.recv(1024))
        P1cipher = AES.new(P1SessionKey, AES.MODE_ECB)
        P2SessionKey = rsa_decrypt.decrypt(Player2.recv(1024))
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