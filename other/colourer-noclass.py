class Colourer():
    safe_delims = ['_', '^', '`']

    def __init__(self, delim):
        self.delim = self.setDelim(delim)
    
    def getDelim(self):
        return self.delim

    def setDelim(self, delim):
        if delim in self.getSafeDelims():
            self.delim = delim
        else:
            print("ERROR: delim not in safe_delims")
            return 1

    def getSafeDelims(self):
        return self.safe_delims

    def wordFilter(self, word):
        word = word.replace(self.delim, ' ')
        try:
            if word[-1] == ' ':
                word = word[:-1]
        except IndexError:
            pass
        return word

col = Colourer('_')
col.wordFilter("test_test_")
