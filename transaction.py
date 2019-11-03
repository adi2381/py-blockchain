from collections import OrderedDict

from utility.printable import Printable

# Transaction class represents an open transaction which can be added to a block to become processed transaction
class Transaction(Printable):
    def __init__(self, sender, recipient, signature, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signature = signature

    # Converts the transaction into a hashable OrderedDict
    def to_ordered_dict(self):
        return OrderedDict([('sender', self.sender), ('recipient', self.recipient), ('amount', self.amount)])
