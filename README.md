# Programming Assignment #3 - TCP Client Server

_CST 311-30, Introduction to Computer Networks, Online_

# Contents
1. [Team](#team)
2. [Project Description](#project-description)
3. [Resources](#resources)
4. [Program Flow](#program-flow)
    1. [server](#server)
    2. [client](#client)
5. [Work Division](#work-division)
    - [Larry Chiem](#larry-chiem)
    - [Ian Rowe](#ian-rowe)
    - [Raymond Shum](#raymond-shum)
    - [Nicholas Stankovich](#nicholas-stankovich)

# Project Description
This project implements a TCP chat room using two scripts: client.py and server.py.

[Return to Top](#contents)

# Team
**LEAD: TBD**

MEMBERS: Larry Chiem, Ian Rowe, Raymond Shum, Nicholas Stankovich

[Return to Top](#contents)

# Resources
- [Project Spec. Sheet](https://github.com/InnovaTree/CST311_PA3_TCP_Client_Server/blob/main/Documentation/Programming_Assignment%20_3_TCP_Client_Server%20revised%2010092020.pdf)
- [Multithreading Video](https://www.youtube.com/watch?v=6eqC1WTlIqc)
- [Multithreading Tutorial](https://realpython.com/intro-to-python-threading/)

[Return to Top](#contents)

# Program Flow
Note: This flow matches the output in the assignment spec sheet.

## Server

>1. Server waits for both clients to establish a connection with it.
>    1. Server prints: "The server is waiting to receive two connections...."
>2. As each connection is established, server prints: "Accepted {number_of} connection, calling it client {name}"
>3. **Only** after connections to both clients are established:
>    1. Server sends message to both clients: "Client {name} has connected."
>    2. Server prints: "Waiting to receive messages from client {name} and client {name}...." 
>    2. Server begins to listen to both clients for messages.
>        - For each client, server creates a thread to listen for messages, assigns it that client and starts it.
>4. Server waits until it has received a message from both clients.
>5. Once both messages have been received:
>    1. Server sends message to both clients: "{client_name}: {first_message} received before {client_name}: {second_message}"
>6. Server tells both clients to close their connections.
>    1. Server prints: "Waiting a bit for clients to close their connections"
>7. Server closes its connections to the clients.
>8. Server waits for threads to join.
>    1. Server prints: "Done."
    
## Client

>1. Client connects to server.
>2. Client waits for server to confirm that it can send messages.
>3. After receiving confirmation:
>    1. Client creates a thread to receive messages and starts it.
>    2. Client asks for user input: "Enter a message to send to the server: "
>4. Client waits for server to respond with a message.
>5. Client ends connection with server when asked.
>6. Client joins single thread.

[Return to Top](#contents)

# Work Division

## Larry Chiem

[Return to Top](#contents)

## Ian Rowe

[Return to Top](#contents)

## Raymond Shum

[Return to Top](#contents)

## Nicholas Stankovich

[Return to Top](#contents)
