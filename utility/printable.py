"""
Printable class represents a base class which implements 
the printing to console functionality. We convert everything 
to string as in our wallet functionality, output is in binary 
and so to maintain the readability of data, we use printable class
"""
class Printable:
    def __repr__(self):
        return str(self.__dict__)
