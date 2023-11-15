import socket
import sys

def main(player_number):

    #creates socket
    Player = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket created
    if player_number == 1:
        Player.connect(("127.0.0.1", 1234)) #attempts to create at specified IP at specified port	
    else:
        Player.connect(("127.0.0.1", 1235)) #attempts to create at specified IP at specified port
    #sends session key
    PSessionKey = "0"
    Player.send(PSessionKey.encode())
    pnumbers = Player.recv(1024)
    Parray = pnumbers.decode().split(" ")
    #round 1
    print(Parray)
    number_picked = input("Pick a number 1-3 which corresponds to shown value: ")
    Player.send(Parray[int(number_picked)-1].encode())
    Parray.pop(int(number_picked)-1)
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
    #round2
    print(Parray)
    number_picked = input("Pick a number 1-2 which corresponds to shown value: ")
    Player.send(Parray[int(number_picked)-1].encode())
    Parray.pop(int(number_picked)-1)
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
    #round3
    print("Your only number left is: " + Parray[0])
    Player.send(Parray[0].encode())
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
    #recv results
    win_or_loss = Player.recv(1024)
    print(win_or_loss.decode())
	

if __name__ == "__main__":
    player_number = sys.argv[1]
    main(int(player_number))
