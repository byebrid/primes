""" Created 30 December, 2018 by Byebrid.
primes_btwn(start, stop) returns all primes between start and stop.
All primes less than stop end up being calculated or taken from the text file
this function creates, called primes.txt.
This makes this very inefficient for very large values of start and stop, unless
all previous primes have been calculated (in which case, this would be quite
efficient).
"""

import math
import os
import getpass

# Path to the document that will store all the primes.
path = os.getcwd() + '/primes.txt'


def update_prime_list():
    """Creates updated prime_list, last_prime.
    """
    global prime_list, last_prime
    with open(path, 'r') as f:
        lines = f.readlines()
        prime_list = list(map(lambda p: int(p.strip('\n')), lines))
    last_prime = prime_list[-1]


def is_prime(x):
    """Returns True if x is prime.
    """
    sqrt = math.floor(math.sqrt(x))	         # To test for primes, only need to check up till square root.
    for p in prime_list:
        if x % p == 0:
            return False
        elif p >= sqrt:
            return True
        elif p == last_prime:
            for n in range(p, sqrt + 1, 2):	 # Go through all odd numbers after and including last_prime
                if x % n == 0:
                    return False
                elif n == sqrt or n == sqrt - 1:
                    return True


def primes_btwn(start, stop):
    """Returns list of all primes between start and stop (inclusive).  Creates a document in the given directory if it does not already exist.
    """
    # Handling typeErrors
    if type(start) != int or type(stop) != int:
        if type(start) is float:
            return primes_btwn(math.floor(start), stop)
        if type(stop) is float:
            return primes_btwn(start, math.floor(stop))
        else:
            raise TypeError('Arguments must be positive integers')
    if start < 0 or stop < 0:
        raise TypeError('Arguments must be > 0.')
    if start > stop:
        return primes_btwn(stop, start)

    result = []
    new_primes = [] # new primes calculated as required
    highest_check = math.floor(math.sqrt(stop))

    def add_to_doc(new_primes):
        with open(path, 'a') as f:
            if type(new_primes) == int:
                f.write('\n' + str(new_primes))
            elif type(new_primes) == list:
                for p in new_primes:
                    f.write('\n' + str(p))

    def doc_or_new_primes(n):
        """Decides if n needs to be added to the document (and update_prime_list) or if it can simply be added after all computations have been completed.
        """
        if n <= highest_check:                      # Only need to update document here if the new primes will be needed to determine if stop is prime.
            add_to_doc(n)
            update_prime_list()
        else:
            new_primes.append(n)

    try:
        # If document exists, initiate prime_list, and check if some/all primes in desired range have already been calculated.
        if os.path.exists(path):
            update_prime_list()                                     # Creates prime_list and last_prime
            if last_prime + 1 >= stop:           					# If all primes in range have already been calculated: retrieve all from doc.
                print('Retrieving primes from document...')
                for p in prime_list:
                    if p >= start and p <= stop:
                        result.append(p)
                    elif p > stop:
                        break

            elif last_prime < start:                    			# If no primes in range have yet been calculated: determine all primes above last_prime up to stop.
                print('Calculating primes...')
                for n in range(last_prime + 2, stop + 1, 2):
                    if is_prime(n):
                        doc_or_new_primes(n)
                        if n >= start:
                            result.append(n)

            elif last_prime >= start:                    			# If some, but not all primes in range, have already been calculated: retrieve from doc, and then determine rest.
                print('Retrieving some primes from document...')
                for prime in prime_list:
                    if prime >= start:
                        result.append(prime)

                print('Determining if there are more primes...')
                for n in range(last_prime + 2, stop + 1, 2):
                    if is_prime(n):
                        doc_or_new_primes(n)
                        result.append(n)

        else:
            print('Creating document to store primes...')
            with open(path, 'w') as f:
                f.write('2\n3')
            return primes_btwn(start, stop)

    except KeyboardInterrupt:
        print('\n\nProgram was interrupted but newly calculated primes were added to document.')
        print('Highest prime so far is',new_primes[-1],'\n')

    add_to_doc(new_primes)
    return result

primes_btwn(1, 100000)
