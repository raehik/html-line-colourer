import sys
import os
import argparse
import random

# default colours if -c file not passed
def_colours = ['0dcf00', 'd80000', 'bdc134', '00caca', '269006', 'c842c8']
def_step = 3
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

def alt_element(data, step):
    lst = [ [] for _ in range(step) ] # list comprehension to create an empty list
    for i in range(step):
        lst[i]= data[i::step]
    return lst

def get_random_elements_pop(l, req_len):
    """Return list of randomised elements from l with length req_len.
    
    Does not reuse elements, so fails if no. of elements in l is
    less than no. of elements in req_len.
    
    """
    if len(l) < req_len:                # if req_len is longer than l:
        sys.exit("length too long")     # exit because otherwise we'll return
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
parser.add_argument("-s", "--step", metavar="NUM", type=int, help="integer step to use for file")
args = parser.parse_args() # get command-line args

colours = open(args.colours).readline().strip().split() if args.colours else def_colours
step = args.step if args.step else def_step

data = get_input() # input as list
split_data = alt_element(data, step)

# check that we got something
if len(split_data[0]) == 0:
    sys.exit("ERROR: not one full 3-line passage found (file is < 3 lines)")

# check data was all right
if len(split_data[0]) != len(split_data[1]):
    sys.exit("ERROR: lists don't match up (not enough slaves for masters)")

# get formatted lists
master_formatted = []
slave_formatted = []
for i in range(len(split_data[0])):
    random_colours = get_random_elements_pop(colours, len(split_data[0][i].split())) # for each master line, get new random colours
    master_formatted.append(get_master(split_data[0][i].split(), random_colours))
    slave_formatted.append(get_slave(split_data[1][i].split(), random_colours, [ int(x) for x in split_data[2][i].split() ]))

# output to anki file
to_anki_file(file_name, master_formatted, slave_formatted)