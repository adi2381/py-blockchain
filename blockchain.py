MINING_REWARD = 10

# Initializing our (empty) blockchain list
# genesis block is the very first block hardcoded into blockchain
genesis_block = {
        'previous_hash': '', 
        'index': 0, 
        'transactions': []
    }
    #convert above dictionary into one string, to do that use for loop
blockchain = [genesis_block]
open_transactions = []
owner = 'Admin'
participants = {'Admin'}

#genesis block -> its the very first block thats hard coded into the blockchain

def hash_block(block):
    return '-'.join([str(block[key]) for key in block])

def get_balance(participants):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participants] for block in blockchain]
    amount_sent = 0
    for tx in tx_sender:
        if len(tx) > 0:
            amount_sent += tx[0]
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participants] for block in blockchain]
    amount_sent = 0
    for tx in tx_recipient:
        if len(tx) > 0:
            amount_sent += tx[0]
    return amount_recieved - amount_sent

def get_last_blockchain_value():
    """ Returns the last value of the current blockchain. """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# This function accepts two arguments.
# One required one (transaction_amount) and one optional one (last_transaction)
# The optional one is optional because it has a default value => [1]


def add_transaction(recipient, sender='Admin', amount=1.0):
    """ Append a new value as well as the last blockchain value to the blockchain.

    Arguments:
    sender, recipient, amount
    """
    transaction = {
        'sender':sender,
        'recipient':recipient,
        'amount':amount
        }
    if verify_transaction(transaction):
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)

    

#processes open_transactions
def mine_block():
    #to get hash of prevous block
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    reward_transaction = {
        'sender': 'MINING',
        'recipient': owner,
        'amount': MINING_REWARD
    }
    open_transactions.append(reward_transaction)
    #using for loop on dictionary, for loop iterates through keys by default
    block = {
        'previous_hash': 'hashed_block', 
        'index': len(blockchain), 
        'transactions': open_transactions
    }
    blockchain.append(block)
    return True
        

def get_transaction_value():
    """ Returns the input of the user (a new transaction amount) as a float. """
    # Get the user input, transform it from a string to a float and store it in user_input
    tx_recipient = input("Enter the recipient of the transaction: ")
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount


def get_user_choice():
    """Prompts the user for its choice and return it."""
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    """ Output all blocks of the blockchain. """
    # Output the blockchain list to the console
    for block in blockchain:
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)


def verify_chain():
    """ Verify the current blockchain and return True if it's valid, False otherwise."""
    """enumerate returns a tuple which contains index of the element and the element itself"""
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] == hash_block(blockchain[index-1]):
            return False
    return True

    


waiting_for_input = True

# A while loop for the user input interface
# It's a loop that exits once waiting_for_input becomes False or when break is called
while waiting_for_input:
    print('Please choose')
    print('1: Add a new transaction value')
    print('2: Mine a new Block')
    print('3: Output the blockchain blocks')
    print('4: Output Participants')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        receipient, amount = tx_data
        # Add the transaction amount to the blockchain
        add_transaction(receipient, amount=amount)
    elif user_choice == '2':
        if mine_block():
         open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == 'h':
        # Make sure that you don't try to "hack" the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash' : '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Admin', 'amount': '1.0'}]
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
    print(get_balance('Admin'))
else:
    print('User left!')


print('Done!')
