##### Phase - 1: Importing all necessary files and Initializing the blockchain #####

# Importing
from functools import reduce
import hashlib as hl
from collections import OrderedDict
import json
import pickle
from hash_util import hash_string_256, hash_block

# The reward we give to miners for creating a new block
mining_reward = 10

# Initializing our empty blockchain list
blockchain = []

# Unhandled or open transactions that are yet to be added to a new block
open_transactions = []

# We are the owner of this blockchain node, hence this is our identifier (e.g. for sending coins)
owner = 'Aditya'

# Registered participants: Us + other people sending/ receiving coins
participants = {'Aditya'}




##### Phase - 2: Saving & Loading the Blockchain Data #####

# Saving the transactions and other details of our blockchain
def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            f.write(json.dumps(blockchain))
            f.write('\n')
            f.write(json.dumps(open_transactions))
            # Uncomment below block of code to save data using pickle and comment out json block of code
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!')

# Loading the transactions and other details of our blockchain
def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            # Uncomment below block of code to load data from pickle file and comment out json code
            # file_content = pickle.loads(f.read())
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            file_content = f.readlines()
            blockchain = json.loads(file_content[0][:-1])
            # We need to first convert the data loaded from the file because Transactions should use OrderedDict
            updated_blockchain = []
            for block in blockchain:
                updated_block = {
                    'previous_hash': block['previous_hash'],
                    'index': block['index'],
                    'proof': block['proof'],
                    'transactions': [OrderedDict(
                        [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])]) for tx in block['transactions']]
                }
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            # We need to convert  the loaded data because Transactions should use OrderedDict
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = OrderedDict(
                    [('sender', tx['sender']), ('recipient', tx['recipient']), ('amount', tx['amount'])])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except IOError:
        # Our starting block for the blockchain
        genesis_block = {
            'previous_hash': '',
            'index': 0,
            'transactions': [],
            'proof': 100
        }
        # Initializing our (empty) blockchain list
        blockchain = [genesis_block]
        # Unhandled or Unprocessed transactions that are yet to be a part of a block
        open_transactions = []
    finally:
        print('Cleaning Up!')

# Load the data from the file
load_data()




##### Phase - 3: Verifying & Authenticating the Blockchain #####

# Proof of Work
def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    # This hashing is used for Proof of work Algo
    guess_hash = hash_string_256(guess)
    # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
    return guess_hash[0:2] == '00'

def proof_of_work():
    """Generate a proof of work for the open transactions, the hash of the previous block and a random number (which is guessed until it fits)."""
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    # Try different PoW numbers and return the first valid one
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof

# Calculate and return the balance of a participant
def get_balance(participant):
    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of transactions that were already included in blocks of the blockchain
    tx_sender = [[tx['amount'] for tx in block['transactions']
                  if tx['sender'] == participant] for block in blockchain]

    # Fetch a list of all sent coin amounts for the given person (empty lists are returned if the person was NOT the sender)
    # This fetches sent amounts of open transactions (to avoid double spending)
    open_tx_sender = [tx['amount']
                      for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                         if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)

     # This was the previous logic used for calculating the amount of coins sent
    """ 
    amount_sent = 0
    # Calculate the total amount of coins sent
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    """

    # This fetches received coin amounts of transactions that were already included in blocks of the blockchain
    # We ignore open transactions here because you shouldn't be able to spend coins before the transaction was confirmed + included in a block
    tx_recipient = [[tx['amount'] for tx in block['transactions']
                     if tx['recipient'] == participant] for block in blockchain]
    amount_received = reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt)
                             if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)

    # Return the total balance
    return amount_received - amount_sent

# Returns the last value of the current blockchain
def get_last_blockchain_value():
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# Verifies a transaction by checking whether the sender has sufficient amount of coins
def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']

# Creating a Chain of Data( Append a new value as well as the last blockchain value to the blockchain )
def add_transaction(recipient, sender=owner, amount=1.0):
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
        save_data()
        return True
    return False




##### Phase - 4: Mining a new block in the Blockchain #####

# Mine a new block in the Blockchain ( Create a new block and add open transactions to it )
def mine_block():
    # Fetch the current last block of the blockchain
    last_block = blockchain[-1]
    # Hash the last block. So, we can compare it to the stored hash value
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # For rewarding miners, Mining Reward was created
    # reward_transaction = {
    #     'sender': 'mining_system',
    #     'recipient': owner,
    #     'amount': mining_reward
    # }
    reward_transaction = OrderedDict(
        [('sender', 'mining_system'), ('recipient', owner), ('amount', mining_reward)])
    # Copy transaction instead of manipulating the original open_transactions list
    # This ensures that if for some reason the mining should fail, we don't have the reward transaction stored in the open transactions
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }
    blockchain.append(block)
    return True

# Get the user input, transform it from a string to a float and store it in user_input
def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount

# Prompts the user for its choice and return it
def get_user_choice():
    user_input = input('Your choice: ')
    return user_input

# Output the blockchain list to the console
def print_blockchain_elements():
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)

# Analyze and Verify the Blockchain
# We skip checking the first block as there's no previous block with which it can be compared
# If first element of current block is equal to the previous entire block, chain is valid
def verify_chain():
# Basic Implementation
    """    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
    return is_valid """

# Improved Implementation
    """ Verify the current blockchain and return True if it's valid, False otherwise."""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True

# Verifies all open & unprocessed transactions
def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])




##### Phase - 5: User Interface #####

waiting_for_input = True

# User Input Interface
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output participants')
    print('5: Check transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):
            print('Added transaction!')
        else:
            print('Transaction failed!')
        print(open_transactions)
    elif user_choice == '2':
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')
    elif user_choice == 'h':
        # Make sure that you don't try to manipulate the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Aditya', 'amount': 100.0}]
            }
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition becomes False
        waiting_for_input = False
    else:
        print('Input was invalid, please pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        # Break out of the loop
        break
    print('Balance of {}: {:6.2f}'.format('Aditya', get_balance('Aditya')))
else:
    print('User left!')


print('Done!')
