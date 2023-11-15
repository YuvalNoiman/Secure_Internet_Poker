# Secure_Internet_Poker
This project implements poker on the Internet. It will accept two players. The house has each
player’s public key.
1.
Each player generates a session key and distributes the session key to the house securely.
The session key is used to encrypt message sent between the house and the players.
2.
The house randomly generates three numbers between 1 and 15 and sends the numbers to
player.
3.
The house randomly generates three numbers between 1 and 15 and sends the numbers to
player.
4.
There are three rounds. In each round, each player chooses a number out of the three
numbers and sends the number to the server. The server compares the number. The
player who chose larger numbers than the other for at least two rounds wins. At the end
of the 3rd round, the house announces the winner.
5.
The session key will be destroyed after a player leaves a current session.
Your implementation must provide both confidentiality and digital signature. For digital sig-
nature you must provide the user with a choice of using RSA or Digital Signature Algorithm
(DSA;
https://bit.ly/2TvvGSt).
Both digital signature schemes must be supported.
