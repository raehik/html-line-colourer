import random
import sys

def error_msg(msg):
    """
    Print error message and flush the clipboard.
    """
    print("ERROR: " + msg)
    print("Please check the help with the -h option for further help.")
    print("(flush clipboard code)")

def shuffle(l):
    """Returns a shuffled copy of list l."""
    l2 = l[:]           # copy l into l2
    random.shuffle(l2)  # shuffle l2
    return l2           # return shuffled l2

def get_random_elements_pop(l, req_len):
    """
    Return list of randomised elements from l with length req_len.
    
    Does not reuse elements, so fails if no. of elements in l is
    less than no. of elements in req_len.
    """
    if len(l) < req_len:                # if req_len is longer than l:
        error_msg("length too long")
        sys.exit()                      # exit because otherwise we'll return
                                        # a list without length req_len
    rand_l = shuffle(l)
    while len(rand_l) != req_len:       # until rand_l is right length:
        rand_l.pop()                    # pop elements until correct length
    return rand_l