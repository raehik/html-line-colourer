import sys
import random
import win32clipboard
import argparse

def error_msg(msg):
    """
    Prints an error message and flushes the clipboard.
    """
    print("ERROR: " + msg)
    print("Please check the help with the -h option for further help.")
    print("(flush clipboard code)")
    sys.exit()

def get_random_elements_pop(list, req_length):
    """
    Returns a list of randomised list elements with length req_length.
    
    Does not reuse elements, so fails if no. of elements in colour_codes is
    less than no. of elements in list.
    """
    random.shuffle(list)
    while len(list) > req_length:
        list.pop() # get it down to required_length
    if len(list) != req_length: # i.e. if orig_list was too small
        error_msg("get_random_elements_pop error")
    return list

def get_random_elements_any(orig_list, required_length):
    """
    Returns a random list of orig_list elements with length required_length.
    
    Elements may be chosen more than once (so it's good to have a big
    orig_list).
    """
    rand_list = random.shuffle(orig_list)
    while len(rand_list) > required_length:
        rand_list.pop() # get it down to required_length
    if len(rand_list) != required_length: # i.e. if orig_list was too small
        error_msg("get_random_elements_any error")
    return list_rand

def format_master(list, colour):
    arr_format = [] # initialise list for appending
    for num in range(len(list)):
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

def file_exists(file):
    try:
        with open(file): pass
    except IOError:
        sys.exit("ERROR: file doesn't exist.")
    return 0

def to_clipboard(formatted_text, orig=''): # easy access function to set clipboard
    win32clipboard.OpenClipboard()
    win32clipboard.EmptyClipboard()
    win32clipboard.SetClipboardText(formatted_text)
    win32clipboard.CloseClipboard()
    if orig != '': # if orig supplied
        if len(orig) < 21: # if is 20 chars or shorter
            print("Set clipboard to '" + orig + "'") # print all with no ellipsis
        else:
            print("Set clipboard to '" + orig[0:20] + "...'") # print first 20 chars with ellipsis
    else:
        print("Set clipboard to '" + formatted_text[0:20] + "...'") # print first 20 chars of formatted - better than no output

def print_output(file=""):
    if file:
        pass

def format_lines(lines_arr, len):
    num = 0
    for current_line in range(len):
        if current_line % 4 != 0:
            continue
        num += 1
        master = lines_arr[current_line]
        slave = lines_arr[current_line+1]
        colour_order = lines_arr[current_line+2]

        master_sep = master.split()
        slave_sep = slave.split()
        colour_order = colour_order.split() # overwrite because string has no use
        # master
        raw_input("(press Enter to format + copy master no." + str(num) + ")")
        word_colours = choose_colours(master_sep, colour_codes) # randomise colours
        master_formatted = format_master(master_sep, word_colours) # use those colours
        to_clipboard(master_formatted, master) # set clipboard to processed array

        # slave
        raw_input("(press Enter to format + copy slave no." + str(num) + ")")
        slave_formatted = format_slave(slave_sep, word_colours, colour_order)
        to_clipboard(slave_formatted, slave)


col_choices = ['0dcf00', 'd80000', 'bdc134', '00caca', '269006', 'c842c8']
# initialise argparse
parser = argparse.ArgumentParser(description="Colour lines with HTML <font> tags.")
parser.add_argument("-f", "--file", help="file to use", default="")
args = parser.parse_args() # get command-line args

# get data
if not args.file: # if -f FILE not passed
    print("Using clipboard")
    win32clipboard.OpenClipboard()
    data = win32clipboard.GetClipboardData()
    win32clipboard.CloseClipboard()
else:
    print("Using file " + args.file)
    # then read file
    with open (args.file, "r") as f:
        data = f.read()

data_sep = data.splitlines() # split into list using universal newlines
# now we check for correct no. of elements
if (len(data_sep) + 1)%4 != 0:
    print(len(data_sep))
    sys.exit("ERROR: no. of lines not equal to (multiple of 4) - 1. Please check your input.")

format_lines(data_sep, len(data_sep))

print("")
raw_input("Finished. Press Enter to exit...")