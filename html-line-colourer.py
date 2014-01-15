import sys
import os
import argparse
import random

def_colours = ['919AC', '59BCFF', 'CC0000', 'E69316', '8A5C2E', '005200', '33CC33', 'FF9DFF', '84299A', '82829B', ]
def_step = 3
def_output = "out.txt"
def_field_delim = '~'

def print_error(err, line=""):
    print("ERROR: " + err)
    if line != "":
        print("Line error was encountered in:")
        print(line)
    sys.exit()

def file_to_list(given_file):
    """Reads a file to a universal newline-stripped list."""
    try:
        f = open(given_file, 'r')
    except IOError:
        print_error("not a file")
    s = f.read()
    lst = s.splitlines() # listify, filter universal newlines
    lst = filter(None, lst) # remove empty elements (any newline spacing)
    return lst

def alt_element(data, step):
    lst = [ [] for _ in range(step) ] # create empty list
    for i in range(step):
        lst[i]= data[i::step] # group passages
    return lst

def get_random_elements_pop(l, req_len):
    """Return a list of shuffled elements from l with length req_len.
    
    Pops elements, so fails if no. of elements in l is less than req_len.
    
    """
    if len(l) < req_len:
        print_error("req_len can not be reached", l)
    rand_l = shuffle(l)
    while len(rand_l) != req_len:
        rand_l.pop() # pop elements until correct length
    return rand_l

def shuffle(l):
    """Returns a shuffled copy of list l."""
    l2 = l[:]           # copy l into l2
    random.shuffle(l2)  # shuffle l2
    return l2

def get_master(lst, colours):
    """Colours a line as 'line 1'."""
    lst_format = [] # initialise list for appending to
    for i in range(len(lst)):
        word = lst[i]
        (space, word) = word_filter(word)
        lst_format.append('<font color="#' + colours[i] + '">' + word + '</font>' + space)
    # join into one string, remove final char (space)
    str_format = ''.join(lst_format)[:-1]
    return str_format

def word_filter(word):
    """Checks a word for backquotes and does things with them."""
    if word.find('`') != -1: # if there is a backquote somewhere
        if word.find('`') == word.__len__()-1: # if only 1 and is at the end
            space = '' # no space between it and next word
            word = word.replace('`', '') # remove backquote
        else:
            space = ' '
	    word = word.replace('`',' ') # replace backquote(s) with spaces
    else:
        space = ' ' # default to spacing words
    return (space, word)

def get_slave(lst, colours, col_ord):
    """Colours a line as 'line 2'."""
    lst_format = [] # initialise list for appending to
    if len(col_ord) != len(lst):
        print_error("length of col_order (line 3) != length of slave (line 2)", lst)
    for i in range(len(lst)):
        word = lst[i]
        (space, word) = word_filter(word)
        if col_ord[i] == 0: # special: 0 = no colour
            lst_format.append(word + ' ')
        else:
            try:
                # TODO: probably move this lol
                # remember col_ord is used as a one-based list to ease
		# understanding - it also means 0 can be used specially
		# for no colour change (not necessarily black!)
                lst_format.append('<font color="#' + colours[col_ord[i]-1] + '">' + word + '</font>' + space)
            except IndexError:
                print_error("col_ord specified a word master (line 1) doesn't have - master is not that long (less than " + str(col_ord[i]) + " word(s) long)", lst)
    # join into one string then remove final char (= space)
    str_format = ''.join(lst_format)[:-1]
    return str_format

def to_anki_file(f, master, slave):
    f = open(f, "w")
    for i in range(len(master_formatted)):
        f.write(master[i] + field_delim + slave[i] + "\n")


# initialise argparse
parser = argparse.ArgumentParser(description="Colour lines randomly word-by-word with HTML <font> tags.")
parser.add_argument("file", help="file to use")
parser.add_argument("-c", "--colours", metavar="FILE", help="HTML colours to pick from")
parser.add_argument("-s", "--step", metavar="NUM", type=int, help="integer step to use for file")
parser.add_argument("-o", "--output", metavar="FILE", help="file to write to")
parser.add_argument("-d", "--delim", metavar="CHAR", help="char to use as Anki field delimiter")
args = parser.parse_args() # get command-line args

colours = open(args.colours).readline().strip().split() if args.colours else def_colours
step = args.step if args.step else def_step
output = args.output if args.output else def_output
field_delim = args.delim if args.delim else def_field_delim

data = file_to_list(args.file)
split_data = alt_element(data, step)

# check that we got something
if len(split_data[0]) == 0:
    print_error("no slave-master-colour passages found")

# check data was all right
if len(split_data[0]) != len(split_data[1]):
    print_error("not enough slaves for masters")

# get formatted lists
master_formatted = []
slave_formatted = []
for i in range(len(split_data[0])):
    random_colours = get_random_elements_pop(colours, len(split_data[0][i].split())) # for each master line, get new random colours
    master_formatted.append(get_master(split_data[0][i].split(), random_colours))
    slave_formatted.append(get_slave(split_data[1][i].split(), random_colours, [ int(x) for x in split_data[2][i].split() ]))

# output to anki file
to_anki_file(output, master_formatted, slave_formatted)
