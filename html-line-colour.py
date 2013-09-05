import sys
from random import randint
import win32clipboard

def choose_colours(arr):
    col_choices = ['0dcf00', 'd80000', 'bdc134', '00caca', '269006', 'c842c8']
    if len(col_choices) < len(arr):
        sys.exit("ERROR: not enough possible colour choices for given array (array has too many elements/words).")
    chosen = []
    for num in range(len(arr)): # loop for each word
        rand_col = col_choices.pop(randint(0, len(col_choices)-1)) # pop random colour
        chosen.append(rand_col)
    return chosen

def format_master(arr, colour):
    arr_format = []
    for num in range(len(arr)):
        word = arr[num]
        if word.find('`')!=-1: # if there is a backquote somewhere
            space = '' # no space between it and next word
            word = word.replace('`', '') # remove backquote
        else:
            space = ' ' # default to spacing words
        arr_format.append('<font color="#' + colour[num] + '">' + word + '</font>' + space)
    str_format = ''.join(arr_format)[:-1] # join into one string then remove final char
    return str_format

def format_slave(arr, word_colours, order):
    arr_format = []
    if len(order) != len(arr):
        sys.exit("ERROR: colour_order is not same length as slave.")
    for num in range(len(arr)):
        word = arr[num]
        if int(order[num]) == 0: # 0 = no colour
            arr_format.append('<font color="#000000">' + word + '</font> ')
        else:
            arr_format.append('<font color="#' + word_colours[int(order[num])-1] + '">' + word + '</font> ')
    str_format = ''.join(arr_format)[:-1] # join into one string then remove final char
    return str_format

def to_clipboard(formatted_text, orig=''): # easy access function to set clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(formatted_text)
    win32clipboard.CloseClipboard()
    if orig != '':
        print("Set clipboard to '" + orig[0:20] + "...'") # prints first 20 chars of provided orig
    else:
        print("Set clipboard")

def file_len(fname):
    with open(fname) as f:
        i = -1
        for i, l in enumerate(f):
            pass
    return i + 1


if len(sys.argv) < 2: # if no parameters were passed
    sys.exit("ERROR: no file passed.")

passed_file = sys.argv[1]
# check file exists
try:
   with open(passed_file): pass
except IOError:
    sys.exit("ERROR: file doesn't exist.")

# check file has correct no. of lines
len_f = file_len(passed_file)
if len_f % 3 != 0:
    sys.exit("ERROR: file does not have number of lines equal to a multiple of 3. Please make sure your file is correct and remove any trailing lines.")

f = open(passed_file)
for num in range(len_f / 3):
    master = f.readline().rstrip('\r\n')
    slave = f.readline().rstrip('\r\n')
    colour_order = f.readline().rstrip('\r\n')
    # arrays are much more useful
    master_sep = master.split()
    slave_sep = slave.split()
    colour_order = colour_order.split() # overwrite because string has no use
    
    # master
    raw_input("(press Enter to format + copy master no." + str(num+1) + ")")
    word_colours = choose_colours(master_sep) # randomise colours
    master_formatted = format_master(master_sep, word_colours) # use those colours
    to_clipboard(master_formatted, master) # set clipboard to processed array

    # slave
    raw_input("(press Enter to format + copy slave no." + str(num+1) + ")")
    slave_formatted = format_slave(slave_sep, word_colours, colour_order)
    to_clipboard(slave_formatted, slave)
