import hashlib as hl
import json

# Create a SHA256 hash for a given input string
def hash_string_256(string):
    return hl.sha256(string).hexdigest()

# Hashes a block and returns a string representation of it
def hash_block(block):
    return hash_string_256(json.dumps(block, sort_keys=True).encode())