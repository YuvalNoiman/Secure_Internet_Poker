import socket
import sys

def main(player_number):

    if player_number == 1:
	#creates socket
        Player1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created
        Player1.connect(("127.0.0.1", 1234)) #attempts to create at specified IP at specified port
    	#sends session key
        P1SessionKey = "0"
        Player1.send(P1SessionKey.encode())
        p1numbers = Player1.recv(1024)
        p1array = p1numbers.decode().split(" ")
	#round 1
        print(p1array)
        number_picked = input("Pick a number 1-3 which corresponds to shown value")
        Player1.send(p1array[int(number_picked)-1].encode())
        p1array.pop(int(number_picked)-1)
        win_or_loss = Player1.recv(1024)
        print(win_or_loss.decode())
	#round2
        print(p1array)
        number_picked = input("Pick a number 1-2 which corresponds to shown value")
        Player1.send(p1array[int(number_picked)-1].encode())
        p1array.pop(int(number_picked)-1)
        win_or_loss = Player1.recv(1024)
        print(win_or_loss.decode())
	#round3
        print(p1array[0] + "This is your only number left")
        Player1.send(p1array[0].encode())
        win_or_loss = Player1.recv(1024)
        print(win_or_loss.decode())
	#recv results
        win_or_loss = Player1.recv(1024)
        print(win_or_loss.decode())
	
    else:
	#creates socket
        Player2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created
        Player2.connect(("127.0.0.1", 1235)) #attempts to create at specified IP at specified port
 	#sends session key
        P2SessionKey = "1"
        Player2.send(P2SessionKey.encode())
        p2numbers = Player2.recv(1024)
        p2array = p2numbers.decode().split(" ")
        print(p2array)
        number_picked = input("Pick a number 1-3 which corresponds to shown value")
        Player2.send(p2array[int(number_picked)-1].encode())
        p2array.pop(int(number_picked)-1)
        win_or_loss = Player2.recv(1024)
        print(win_or_loss.decode())
	#round2
        print(p2array)
        number_picked = input("Pick a number 1-2 which corresponds to shown value")
        Player2.send(p2array[int(number_picked)-1].encode())
        p2array.pop(int(number_picked)-1)
        win_or_loss = Player2.recv(1024)
        print(win_or_loss.decode())
	#round3
        print(p2array[0] + "This is your only number left")
        Player2.send(p2array[0].encode())
        win_or_loss = Player2.recv(1024)
        print(win_or_loss.decode())
	#recv results
        win_or_loss = Player2.recv(1024)
        print(win_or_loss.decode())
	

if __name__ == "__main__":
    player_number = sys.argv[1]
    main(int(player_number))
