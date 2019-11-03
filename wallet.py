from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
import Crypto.Random
import binascii

# Wallet class generates a wallet for us which contains our public and private keys & manages transaction signing & verification
class Wallet:

    def __init__(self, node_id):
        self.private_key = None
        self.public_key = None
        self.node_id = node_id

    # Create a new pair of private and public keys
    def create_keys(self):
        private_key, public_key = self.generate_keys()
        self.private_key = private_key
        self.public_key = public_key

    # Saves the keys to a file (wallet.txt)
    def save_keys(self):
        if self.public_key != None and self.private_key != None:
            try:
                with open('wallet-{}.txt'.format(self.node_id), mode='w') as f:
                    f.write(self.public_key)
                    f.write('\n')
                    f.write(self.private_key)
                return True
            except (IOError, IndexError):
                print('Saving wallet failed...')
                return False

    # Loads the keys from the wallet.txt
    def load_keys(self):
        try:
            with open('wallet-{}.txt'.format(self.node_id), mode='r') as f:
                keys = f.readlines()
                public_key = keys[0][:-1]
                private_key = keys[1]
                self.public_key = public_key
                self.private_key = private_key
            return True
        except (IOError, IndexError):
            print('Loading wallet failed...')
            return False

    # Generate a new pair of private and public key
    def generate_keys(self):
        private_key = RSA.generate(1024, Crypto.Random.new().read)
        public_key = private_key.publickey()
        return (binascii.hexlify(private_key.exportKey(format='DER')).decode('ascii'), binascii.hexlify(public_key.exportKey(format='DER')).decode('ascii'))

    # Sign a transaction and return the signature
    # RSA is a cryptography algorithm
    # binascii.hexlify is used to convert binary data to hexadecimal representation
    def sign_transaction(self, sender, recipient, amount):
        signer = PKCS1_v1_5.new(RSA.importKey(binascii.unhexlify(self.private_key)))
        h = SHA256.new((str(sender) + str(recipient) + str(amount)).encode('utf8'))
        signature = signer.sign(h)
        return binascii.hexlify(signature).decode('ascii')

    # Verify signature of transaction
    @staticmethod
    def verify_transaction(transaction):
        public_key = RSA.importKey(binascii.unhexlify(transaction.sender))
        verifier = PKCS1_v1_5.new(public_key)
        h = SHA256.new((str(transaction.sender) + str(transaction.recipient) + str(transaction.amount)).encode('utf8'))
        return verifier.verify(h, binascii.unhexlify(transaction.signature))