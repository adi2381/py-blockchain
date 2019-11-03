import hashlib as hl
import json

# __all__ = ['hash_string_256', 'hash_block']

# Uses SHA256 hashing algorithm to hash a given input string
def hash_string_256(string):
    return hl.sha256(string).hexdigest()

# Hashes a block and returns a str representation of it
def hash_block(block):
    hashable_block = block.__dict__.copy()
    hashable_block['transactions'] = [tx.to_ordered_dict() for tx in hashable_block['transactions']]
    return hash_string_256(json.dumps(hashable_block, sort_keys=True).encode())