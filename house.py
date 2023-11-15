import socket
from random import randint


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

        # Receive the data the client has to send.
        # This will receive at most 1024 bytes
        P1SessionKey = Player1.recv(1024)
        P2SessionKey = Player2.recv(1024)

	# Generates player one's numbers
        p1numbers = str(randint(1, 15)) + " " + str(randint(1, 15)) + " " + str(randint(1, 15))
	# Generates player two's numbers
        p2numbers = str(randint(1, 15)) + " " + str(randint(1, 15)) + " " + str(randint(1, 15))
	
        Player1.send(p1numbers.encode())
        Player2.send(p2numbers.encode())

        p1Score = 0
        p2Score = 0
        lost = "Round Lost!"
        lost = lost.encode()
        won = "Round Won!"
        won = won.encode()
        for x in range(3):
                P1num = Player1.recv(1024)
                P2num = Player2.recv(1024)
                if (int(P1num.decode()) < int(P2num.decode())):
                        Player1.send(lost)
                        Player2.send(won)
                        p2Score += 1
                else:
                        Player1.send(won)
                        Player2.send(lost)
                        p1Score += 1
        if (p1Score < p2Score):
                winner = "Player 2 is the winner!"
        else:
                winner = "Player 1 is the winner!"
        Player1.send(winner.encode())
        Player2.send(winner.encode())
        Player1.close()
        Player2.close()
           


if __name__ == "__main__":
    main()
