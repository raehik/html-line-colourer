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
        sys.exit("ERROR: col_order (3rd line) is not the same length as slave (2nd line).")
    for i in range(len(lst)):
        word = lst[i]
        if col_ord[i] == 0: # special: 0 = no colour
            lst_format.append(word + ' ')
        else:
            try:
                # TODO: probably move this lol
                # remember col_ord is used as a one-based list to ease
		# understanding - it also means 0 can be used specially
		# for no colour -change-
                lst_format.append('<font color="#' + colours[col_ord[i]-1] + '">' + word + '</font> ')
            except IndexError:
                sys.exit("ERROR: master (1st line) is not that long (less than " + str(col_ord[i]) + " word(s) long)")
    # join into one string then remove final char (= space)
    str_format = ''.join(lst_format)[:-1]
    return str_format






def makeMaster(l,cols):
    """."""
    for i in range(len(l)):
        word = l[i]



def wordFilter(word):
    word = word.replace('`', ' ')
    if word[-1] == ' ':
        word = word[:-1]
	return word
    else:
        return word + ' '





def tests():
    print(wordFilter("Poopydoopy") + '!')
tests()
