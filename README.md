# Blockchain Project
<img src="https://github.com/adi2381/py-blockchain/blob/master/cover.png" height="300" width="450">
This project is an implementation of blockchain and it's concepts in Python & Flask with Postman used for API development

## Getting Started

1. [Download Anaconda](https://www.anaconda.com/distribution/)
2. [Download Visual Studio Code](https://code.visualstudio.com/)
3. [Download Postman](https://www.getpostman.com/)
4. Clone the directory and open it in **vs code**
5. In terminal, enter **activate** to activate the **base** environment of Anaconda
> *Install the below dependencies to avoid any errors incase they're not already installed*
6. Install Flask

`pip install flask`

7. Install Flask-Cors

`pip install -U flask-cors`

8. Install requests Lib

`pip install requests`

9. Install pycrypto (collection of hash functions)

`pip install pycrypto`

10.  In the terminal, run the following command

`python node.py` 

> *or to run multiple nodes, in a new terminal*

`python node.py -p<port_number>` 

11. Open Postman Client, Test the below API Calls

## API Calls
Below is a list of API calls and short description about what they do, these api calls can conveniently be executed in Postman
Localhost & Port have been set in node.py file, by default I've set them as 0.0.0.0 with port=5000

### Blockchain 
Creates a blockchain.txt file that contains information regarding the transactions and other information related to the blockchain

* [POST] Mine a Block:

`localhost:5000/mine`

* [GET] Get snapshot of current blockchain:

`localhost:5000/chain`

### Transaction

* [POST] Add a New Transaction:

`localhost:5000/transaction`

Before executing the above api call, in Postman, 
Go to "Body" > "Raw" > Select "Json" in the current window and enter the following data:

`eg. { "recipient": "NameofRecipient", "amount": 5 }`

* [GET] Get a List of all Open Transactions:

`localhost:5000/transactions`

### Wallet
creates a wallet.txt file with your port number that contains information regarding your wallet such as public key, private key

* [POST] Generate Wallet:

`localhost:5000/wallet`

* [GET] Fetch Wallet:

`localhost:5000/wallet`

* [GET] Fetch Wallet Balance:

`localhost:5000/balance`

### Node/Server
You can run multiple nodes and test communication between the two by opening two terminals inside **vs code** and executing the **python node.py** file with arguments **-p 5001** or **--port 5001**. So, it will look like **python node.py -port 5001**

You can create as many nodes/servers you want by using the open ports and appending them to the **python node.py --port <port_number>** command

* [POST] Add Peer Node to Your Chain Network:

`localhost:5000/node`

Before executing the above api call, in Postman, 
Go to "Body" > "Raw" > Select "Json" in the current window and enter the following data:

`e.g. { "node": "localhost:5001" }`

* [DELETE] Delete Peer Node:

`e.g. localhost:5000/node/localhost:5001`

* [GET] Get all the Nodes in your Network:

`localhost:5000/nodes`

## File Contents
* block.py - represents single block of our blockchain
* blockchain.py - represents the blockchain
* node.py - contains all the routes for API calls
* node_console.py - provides a user interface using while loop to interact with blockchain from within the vs code terminal
* transaction.py - represents open transactions
* wallet.py - Implements functionality to generate wallet, public & private key and other security related algorithm
* API_calls_screenshot Folder - contains screenshots of successful API calls and their output
* Utility > hash_util.py - Implements functionality to hash a block 
* Utility > printable.py - Converts binary data to string for printing in console
* Utility > verification.py - Implements proof of work and verification of chain and transactions

* Legacy_blockchain_files - contains old files related to project

## Shoutout
Huge credits to Dapp university & howCode for explaining the concepts and how to implement them in python. 
1. [Dapp University Video Link](https://www.youtube.com/watch?v=pZSegEXtgAE)
2. [howCode Video Link](https://www.youtube.com/watch?v=b81Ib_oYbFk)
