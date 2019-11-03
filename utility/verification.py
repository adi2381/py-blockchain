# Provides methods for implementing the verification functionality

from utility.hash_util import hash_string_256, hash_block
from wallet import Wallet

# Verification class in our use case is a helper class which offers static & class-based verification & validation methods
class Verification:
    @staticmethod
    # Validate a proof of work number and see if it solves the POW algorithm (two leading 0s, set by us)
    # Arguments:
    #   transactions: The transactions of the block for which the proof is created.
    #   last_hash: The previous block's hash which will be stored in the current block.
    #   proof: The proof number we're testing.
    def valid_proof(transactions, last_hash, proof):
        # Create a string with all the hash inputs
        guess = (str([tx.to_ordered_dict() for tx in transactions]) + str(last_hash) + str(proof)).encode()
         # Hash the string; This hash is used for POW Algorithm and is not the same as stored in previous_hash
        guess_hash = hash_string_256(guess)
       # Only a hash (which is based on the above inputs) which starts with two 0s is treated as valid
        # If 10 0's are used instead of '00', this allows to control the speed at which new blocks are created 
        # so more 0's mean more time will be required to create a new block
        return guess_hash[0:2] == '00'

    # # Analyze and Verify the Blockchain, return True if it's valid else False    
    @classmethod
    def verify_chain(cls, blockchain):
        for (index, block) in enumerate(blockchain):
            if index == 0:
                continue
            if block.previous_hash != hash_block(blockchain[index - 1]):
                return False
            if not cls.valid_proof(block.transactions[:-1], block.previous_hash, block.proof):
                print('Proof of work is invalid')
                return False
        return True

    # # Verifies by checking whether sender has sufficient coins or not
    @staticmethod
    def verify_transaction(transaction, get_balance, check_funds=True):
        if check_funds:
            sender_balance = get_balance(transaction.sender)
            return sender_balance >= transaction.amount and Wallet.verify_transaction(transaction)
        else:
            return Wallet.verify_transaction(transaction)

    # Verifies all open & unprocessed transactions
    @classmethod
    def verify_transactions(cls, open_transactions, get_balance):
        return all([cls.verify_transaction(tx, get_balance, False) for tx in open_transactions])