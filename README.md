# TP_TEST_LOGICIEL

## Table of Contents
1. [General Informations](#general-informations)
2. [Installation](#installation)
3. [How to run tests?](#tests)
4. [How to execute?](#execute)
5. [Runners and Dockers](#runners-docker)
6. [Members](#members)

## General Informations
This repo is a P2P communication project in Test Driven Development module. A server runs to link clients between them thanks to a database. After requesting IP and Port of another registered user, users can directly communicate together without the server.

## Installation

### Python 
Install from : https://www.python.org/downloads/  
This app was built with Python 3.6.3

### Others libraries
This repo uses Requests to send HTTP requests.
OpenSSL library is used to signed message and encrypt it thanks to an existing certificate.
Flask is used to create a server.
Docopt is used to parse arguments given in terminal.
To install:
```sh
pip install requests pyopenssl flask docopt

```

### Cloning repo
With HTTPS:
```sh
git clone https://github.com/TPtestLogiciel/TP_TEST_LOGICIEL.git
``` 
or with SSH:
```sh
git clone git@github.com:TPtestLogiciel/TP_TEST_LOGICIEL.git
``` 
Once the repo is cloned, go to TP_TEST_LOGICIEL/:
```sh
cd TP_TEST_LOGICIEL/
```

## How to run tests?

We used Unittest to run our tests.
***
Each test file tests one functionnality: 
* p2p/test_p2p_client.py tests all client functions and servers responses of clients.
* server/test_bdd.py tests database requirements.
* server/test_server.py sends requests to server and tests its response.
***
### Let's run tests!
To test p2p client:
```sh
python3 p2p/test_p2p_client.py
```
To test database:
```sh
python3 server/test_bdd.py
```
To test server:
```sh
python3 server/test_server.py
```
This will display testing issues if any, OK else.

We used mock (MagicMock and patch in unittest.mock lib) to mock server part in p2p_client.py to avoid dealing with all input the user as to enter to register in database.

## How to execute ?

To execute our p2p application, first launch server. The default server port is 8000:
```sh
python3 server/server.py [--port=<int>]
```
Launching the server first will allow clients to connect to it to register and communicate with other users.

Then, execute a client and provide its port (8001) and server port (8000):
```sh
python3 p2p/p2p_client.py --port_source=8001 --port_server=8000
```
In terminal, you should see some input requests to register to the database. You have to enter your username, a password and the path to your public certificate in order to signed message you will send. You have to generate your key before launching p2p_client so you can provide the path. We provided 2 publics keys (cert.pem and cert2.pem) and 1 private key (private.pem) for our tests but you can use them to execute our application.
Then, the terminal asks a last question: the username of the person you want to talk to. This person must be registered in the database. If so, you will be in communication with that person (if connected ;)).

Another client can be executed to see in the p2p communication is working. You can repeat the previous command, but do not forget to change the --port_source!
You will register and be in communication with the other user.

**Because of a lack of time and expertise, our application is only working with a local IP. It can be enhanced in the future to work with any IP.**

## Runners and Docker

Devops work

## Members
This project was well lead and carried out by our Scrum Master, Alexandra.
Our p2p client program and its tests was mainly done by Steven, Edern and Lola, with obviously some help by other members. All encrypt functions was all made by Steven.
Our server program and its tests was mainly done by Mohamed-Ali and Florent, with the help of Nikolaï and Edern at some point of the project.
Our database and its tests was done by Nikolaï.
All runners and docker handler was made by our DevOps, Maxime.

### Roles
***
* __Scrum Master__: Alexandra
* __DevOps and Docker Master__: Maxime
* __P2P Master__: Edern
* __IP Master__: Mohamed-Ali
* __HTTP Master__: Florent
* __OpenSSL Master__: Steven
* __DB Master__: Nikolaï
* __Git Master__: Lola
***