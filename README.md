html-line-colourer
======================

Colours each word separately in a given line using a list of possible HTML colours, then colours a second given line using a variable denoting which word-colour each word should have.

Basically, it allows you to automate the (HTML) colouring of lines. Think translations: the first line is coloured randomly, then the second line (a translation of the first) is coloured so that 'matching words' have the same colour.

SYNTAX
======

***word`word***
Separates two words but counts them as one word inside -- that is, the two parts will be apart but coloured the same. Useful for when PPPs and the rest, because you may want to see/translate a word like `certandum est` as one 'thing'.

***word` word***
Joins two words but counts them as separate words inside -- that is, the two parts will be together but coloured differently. Useful for prefixes and suffixes and Latin (e.g. telumque)
