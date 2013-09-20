import sys
import os
import argparse
import random

# default colours if -c file not passed
def_colours = ['0dcf00', 'd80000', 'bdc134', '00caca', '269006', 'c842c8']
# file to write to
file_name = "colourer-anki-import.txt"

def get_input():
    """Call the correct function(s) for the type of input given."""
    # check that we were given a file
    if args.file:
        if os.path.isfile(args.file):
            return file_to_list(args.file)
        else:
            sys.exit("not a file")
    else:
        sys.exit("clipboard support coming soon")

def file_to_list(orig_file):
    """Reads a file to a universal newline-stripped list."""
    with open(orig_file, 'r') as f:
        # first to string
        s = f.read()
    # then filter universal newlines
    lst = s.splitlines()
    # remove empty elements
    lst = filter(None, lst)
    return lst

def get_separate_lines(data):
    """Separates a list data into 3 lists of lists containing alternating lines."""
    i = 0
    master = []
    slave = []
    col_ord =[]
    while i < len(data)-2:
        master.append(data[i].split())
        slave.append(data[i+1].split())
        try:
            col_ord.append( [ int(x) for x in data[i+2].split() ] )
        except ValueError:
            sys.exit("ERROR: col_ord (3rd line) is not numeric")
        i += 3
    return (master, slave, col_ord)

def get_random_elements_pop(l, req_len):
    """Return list of randomised elements from l with length req_len.
    
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

def shuffle(l):
    """Returns a shuffled copy of list l."""
    l2 = l[:]           # copy l into l2
    random.shuffle(l2)  # shuffle l2
    return l2           # return shuffled l2

def get_master(lst, colours):
    """Colours a line as 'line 1'."""
    lst_format = [] # initialise list for appending to
    for i in range(len(lst)):
        word = lst[i]
        (space, word) = get_filter_backquote(word)
        lst_format.append('<font color="#' + colours[i] + '">' + word + '</font>' + space)
    # join into one string, remove final char (space)
    str_format = ''.join(lst_format)[:-1]
    return str_format

def get_filter_backquote(word):
    """Checks a word for backquotes."""
    if word.find('`') != -1: # if there is a backquote somewhere
        space = '' # no space between it and next word
        word = word.replace('`', '') # remove backquote
    else:
        space = ' ' # default to spacing words
    return (space, word)

def get_slave(lst, colours, col_ord):
    """Colours a line as 'line 2'."""
    lst_format = [] # initialise list for appending to
    if len(col_ord) != len(lst):
        sys.exit("ERROR: col_order (3rd line) is not the same length as slave (2nd line).")
    for i in range(len(lst)):
        word = lst[i]
        if col_ord[i] == 0: # special: 0 = no colour
            lst_format.append(word + ' ')
        else:
            try:
                #   col_ord[i]-1 = an int
                #   for example if we were given:
                #
                # example
                # first second
                # 56 1
                #
                #   then col_ord[i]-1 = 55
                #   it's all because if col_ord is 0, we use it differently
                #   so col_ord is used as a 1-index list (so it's easier to
                #   understand - I mean who would type '0' if they wanted that
                #   word to correspond to the 1st word?)
                lst_format.append('<font color="#' + colours[col_ord[i]-1] + '">' + word + '</font> ')
            except IndexError:
                sys.exit("ERROR: master (1st line) is not that long (less than " + str(col_ord[i]) + " word(s) long)")
    # join into one string then remove final char
    str_format = ''.join(lst_format)[:-1]
    return str_format

def to_anki_file(file, master, slave):
    open(file, "w").close() # clear file
    for i in range(len(master_formatted)):
        write_to_anki_file(file_name, master_formatted[i], slave_formatted[i])
    lines = open(file_name).read().strip()
    open(file_name, "w").write(lines)

def write_to_anki_file(file, master, slave):
    f = open(file,"a")
    f.write(master + ";" + slave + "\n")

# initialise argparse
parser = argparse.ArgumentParser(description="Colour lines randomly word-by-word with HTML <font> tags.")
parser.add_argument("file", help="file to use")
parser.add_argument("-c", "--colours", metavar="FILE", help="HTML colours to pick from")
# get command-line args
args = parser.parse_args()

# obtain input as list
data = get_input()

# get colours
colours = open(args.colours).readline().strip().split() if args.colours else def_colours

# split list into 3 lists, each containing lists
(master, slave, col_ord) = get_separate_lines(data)

# check that we got something
if len(master) == 0:
    sys.exit("ERROR: not one full 3-line passage found (file is < 3 lines)")

# check data was all right
if len(master) != len(slave):
    sys.exit("ERROR: lists don't match up (not enough slaves for masters)")

# get formatted lists
master_formatted = []
slave_formatted = []
for i in range(len(master)):
    random_colours = get_random_elements_pop(colours, len(master[i])) # for each master line, get new random colours
    master_formatted.append(get_master(master[i], random_colours))
    slave_formatted.append(get_slave(slave[i], random_colours, col_ord[i]))

# output to anki file
to_anki_file(file_name, master_formatted, slave_formatted)