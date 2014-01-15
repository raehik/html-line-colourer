html-line-colourer
======================

## Summary
Randomly colours the first line (with HTML font tags), then colours the second line relative to the assigned colours in the first line. That is, the second line is mapped to the first (via a third numeric line) and they are randomly coloured.

Basically, it allows you to automate the (HTML) colouring of lines. Think translations: the first line is coloured randomly, then the second line (a translation of the first) is coloured so that 'matching words' have the same colour.

## Syntax
Though the first two lines are processed differently, both are filtered for the backtick character ('\`'). You use backticks to change whether spaces should be present. It's a bit complicated:

- To 'connect' words, e.g. a main word and its suffix, you put a backtick on the end of the first word. That's all. Normal spacing. In the output, the words will have no spaces between them, but otherwise are **completely seperate words**.
- To seperate a 

signify when the meaning of the master word is either:
	not explained in one word, or
	needs adjacent words to be considered.
That is, when a 'word' in either the master or the slave is not actually just one word separated by spaces.

For example, the Latin *inquit* means 'he said'. But 'he said' is two words.
Worse still, the Latin *certandum est* can be translated as 'we must fight' in the context of the Aeneid (Book XII).


Though in the former problem, you can simply make 'he' and 'said' individually point to *inquit*, if I ever want to do any clever mangling of the words and such given as input, the program must know which phrases link to which other phrases. Using backticks may not look so neat, but the program will understand better what you mean when you translate *quantus* as 'as\`great\`as'.


### word`word
Spaces two words but counts them as one word inside -- that is, the two parts will be apart but coloured the same. Useful for when PPPs and the rest, because you may want to see/translate a word as one actual concept. For example, you might translate *certandum est* to 'we must fight', but it's pretty difficult to show which individual bits of the word translate: it's easier to translate that 'block' into another one. And because that second block may be made up of one word OR multiple words, we have this and the next one.
### word` word
Joins two words but counts them as separate words inside -- that is, the two parts will be together but coloured differently. Incredibly useful for prefixes and suffixes and Latin (e.g. *telum\`que*)

## Further explanation
Each passage should be 3 lines long: a 'master' line, a 'slave' line, and a line showing how the slave words maps to the master words.
