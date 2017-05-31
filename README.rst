pyapa
=====

A Python module for checking APA style in writing.

This module provides an abstraction class, mostly composed of regular
expressions. This project does not aim to cover the entire APA style
guide, but it does attempt to cover several common errors with style.

To make errors easier to visually locate, 5 characters of context are
sometimes given, depending on the detected error.

apa.ApaCheck object class
-------------------------

This class documents regular expressions to match style errors.

The `apa.ApaCheck.match()` method generates an array of ApaMatch objects
and stores them in `ApaCheck.Matches` for easy access.

apa.ApaMatch object class
-------------------------

This class contains the following members:

 * `ApaMatch.feedback` a unicode string intended to hold a brief
   explanation of an associated error
 * `ApaMatch.end` the position of the character in a text which marks
   the end of the target character span
 * `ApaMatch.start` the position of the character in a text which marks
   the beginning of the target character span
 * `ApaMatch.target` the matching string that contains an error
 * `ApaMatch.suggestions` a list of suggested replacement strings; at
   this time, the list is only ever one element long




Example usage
-------------

From the interpreter:

>>> import apa
>>> a = apa.ApaCheck()
>>> text = u'Papaya are delicious fruit, it was concluded (Author, et
    al. 2017).'
>>> a.match(text)
[<apa.ApaMatch object at 0x000000000000>]
>>> len(a.Matches)
1
>>> a.Matches[0].print()
Match from 48 to 66 for:
Target: uthor, et al. 2017
Feedback: Do not put a comma before 'et al.'
Suggestion: uthor et al. 2017


