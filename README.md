html-line-colourer
======================

# Summary
Colours each word separately in a given line using a list of possible HTML colours, then colours a second given line using a variable denoting which word-colour each word should have.

Basically, it allows you to automate the (HTML) colouring of lines. Think translations: the first line is coloured randomly, then the second line (a translation of the first) is coloured so that 'matching words' have the same colour.

# Syntax

You use backticks to signify when the meaning of the master word is either:
	not explained in one word, or
	needs adjacent words to be considered.
That is, when a 'word' in either the master or the slave is not actually just one word separated by spaces.

For example, the Latin *inquit* means 'he said'. But 'he said' is two words.
Worse still, the Latin *certandum est* can be translated as 'we must fight' in the context of the Aeneid (Book XII).


Though in the former problem, you can simply make 'he' and 'said' individually point to *inquit*, if I ever want to do any clever mangling of the words and such given as input, the program must know which phrases link to which other phrases. Using backticks may not look so neat, but the program will understand better what you mean when you translate *quantus* as 'as`great`as'.


## word`word
Spaces two words but counts them as one word inside -- that is, the two parts will be apart but coloured the same. Useful for when PPPs and the rest, because you may want to see/translate a word like `certandum est` as one 'thing'.

## word` word
Joins two words but counts them as separate words inside -- that is, the two parts will be together but coloured differently. Incredibly useful for prefixes and suffixes and Latin (e.g. telumque)
