#!/usr/bin/env python3

# This module implements a class and functions for matching common patterns of
# error in the APA style of writing.
# This is based on a similar project by Jonathon Aquino:
# <https://github.com/JonathanAquino/apacheck>
#
# Copyright (c) 2017 Keefer Rourke <mail@krourke.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH
# REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY
# AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT,
# INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES WHATSOEVER RESULTING FROM
# LOSS OF USE, DATA OR PROFITS, WHETHER IN AN ACTION OF CONTRACT, NEGLIGENCE
# OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION WITH THE USE OR
# PERFORMANCE OF THIS SOFTWARE.

import re


class ApaMatch:
    def __init__(self):
        self.feedback = ""      # feedback string; explains error
        self.see = ""           # reference string; point to external style guide
        self.end = 0            # end character position for target
        self.start = 0          # start character position for target
        self.target = ""        # target substring that contains error with context
        self.suggestions = []   # list of replacement suggestions, if any

    def print(self):
        if self.start and self.end:
            print("Match from " + str(self.start) + " to " + str(self.end)
                  + " for:")
            if self.target:
                print("Target: " + self.target.strip())
        if self.feedback:
            print("Feedback: " + self.feedback.strip())
        if self.see:
            print("See: " + self.see)
        if self.suggestions:
            for s in self.suggestions:
                print("Suggestion: " + s.strip())

    def sprint(self):
        string = ''
        if self.start and self.end:
            string += ("Match from " + str(self.start) + " to " + str(self.end)
                       + " for:\n")
            if self.target:
                string += ("Target: " + self.target + "\n")
        if self.feedback:
            string += ("Feedback: " + self.feedback + "\n")
        if self.see:
            string += ("See: " + self.see + "\n")
        if self.suggestions:
            for s in self.suggestions:
                string += ("Suggestion: " + s + "\n")

        return string



# defines patterns for common errors and builds an array of ApaMatch objects
class ApaCheck:
    # pattern for year, YYYY or n.d.
    YEAR = r"(\b\d{4}|n\.d\.)"

    # set up regex matching for common mistakes with one word of context

    # letters that appear immediately after a year should be lowercase
    yearletter = re.compile(r"(\b\d{4}[A-Z][),])")

    # do not put a comma before 'et al.'
    etalcomma = re.compile(r"((\w+), et al\..{0,5})")

    # TODO: Incorrect to assume that any reference should be followed by a period
    '''
    # put a period after the date in a reference
    refdatedot = re.compile(r"""((\w+\s+)                  # context
                                (                          # start group
                                \(                         # open paren
                                (\b\d\d\d\d|n\.d\.)[^)]*   # year
                                \)                         # close paren
                                [^.]                       # error
                                ))                         # close group
                            """, re.X)
    '''

    # if this is an article, consider using lowercase
    # detects titlecase within a reference
    reftitlecase = re.compile(r"""(\)\.\s*(?:[A-Z][^\s]*\s?)+(\.))""")

    # every period should be followed by a space
    # unmatched by URL patterns
    stopspace = re.compile(r"""((\w+)                 # context
                               (?!\b).\.[^ ,\n0-9)]   # match
                               (\w+))                 # context
                           """, re.X)
    
    # multiple references should be combined with a semicolon
    joinrefstyle = re.compile(
        r"\([^)]+"+YEAR+"\)([\s+,;]*\([^)]+"+YEAR+"\))+"
    )

    # place the period after an in-text citation
    refbeforedot = re.compile(r"(\.\s+\([^)]+"+YEAR+"\))")
   
    # if only the year is in brackets for an in-text citation, use "and" to
    # separate author names
    # Hans & Yorke (2006) contradict ...
    ampintextref = re.compile(r"[\w\s]+\s&\s[\w\s]+\("+YEAR+"\)")

    # if author names are in brackets for an in-text citation, use an & to
    # separate them
    # ... literature (Hans and Yorke, 2006).
    andinbracketref = re.compile(r"\([^)]+\sand\s[^)]+\s"+YEAR+"\)")
    
    # patterns to be exempted
    url = re.compile(r"(http|ftp|file|https)://([\w_-]+(?:(?:\.[\w_-]+)+))"
                     + r"([\w.\b]*[\w\b])")
    email = re.compile(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", re.MULTILINE)

    
    # init ApaCheck object with an optional context length
    def __init__(self):
        self.Matches = []

    # build an array of matches from the text
    def match(self, text):
        self.Matches = []
        # find matches for each regexp
        matchList = list(re.finditer(self.yearletter, text))
        matchList += list(re.finditer(self.etalcomma, text))
        #matchList += list(re.finditer(self.refdatedot, text))
        matchList += list(re.finditer(self.reftitlecase, text))
        matchList += list(re.finditer(self.stopspace, text))
        matchList += list(re.finditer(self.joinrefstyle, text))
        matchList += list(re.finditer(self.refbeforedot, text))
        matchList += list(re.finditer(self.ampintextref, text))
        matchList += list(re.finditer(self.andinbracketref, text))

        unmatchList = list(re.finditer(self.url, text))
        unmatchList += list(re.finditer(self.email, text))

        # append to Match array
        for match in matchList:
            newMatch = ApaMatch()
            newMatch.start = match.start()
            newMatch.end = match.end()
            newMatch.target = text[newMatch.start:newMatch.end]

            suggestion = ""

            if match.re == self.yearletter:
                newMatch.feedback = (u"Letters that appear immediately after a year should be lowercase.")
                suggestion = newMatch.target.lower()

            elif match.re == self.etalcomma:
                newMatch.feedback = (u"Do not put a comma before 'et al.'")
                newMatch.see = "http://academicguides.waldenu.edu/writingcenter/apa/citations/etal"
                suggestion = re.sub(r", ", " ", newMatch.target)

                '''
                elif match.re == self.refdatedot:
                    newMatch.feedback = (u"References go at the end of sentences; end your sentence after the reference.")
                    s = newMatch.target
                    suggestion = re.sub(r"\)\s", r").", newMatch.target)
                '''

            elif match.re == self.reftitlecase:
                newMatch.feedback = (u"If this is an article title, consider using lowercase.")
                s = newMatch.target.lower()
                s = s[4:]
                suggestion = newMatch.target[:4]
                suggestion += s

            elif match.re == self.stopspace:
                newMatch.feedback = (u"Every period should be followed by a space.")
                suggestion = re.sub(r"\.", r". ", newMatch.target)

                # double check that this isn't a false positive
                for unMatch in unmatchList:
                    falsePositive = text[unMatch.start():unMatch.end()]
                    if re.search(newMatch.target, falsePositive):
                        newMatch = ""
                        suggestion = ""
                        break

            elif match.re == self.joinrefstyle:
                newMatch.feedback = (u"Multiple parentheticals should be combined using a semicolon.")
                newMatch.see = "http://www.apastyle.org/learn/faqs/references-in-parentheses.aspx"
                suggestion = re.sub(r"\)[\s+,;]*\(", r"; ", newMatch.target)

            elif match.re == self.refbeforedot:
                newMatch.feedback = (u"In text citations belong as part of the preceeding sentence. Place the period after the citation.")
                s = newMatch.target[:2]
                suggestion = newMatch.target[2:]
                suggestion += s

            elif match.re == self.andinbracketref:
                newMatch.feedback = (u"Use '&' to separate parenthesized author names.")
                suggestion = re.sub(r"&", r"and", newMatch.target)
                newMatch.see = "http://blog.apastyle.org/apastyle/2011/02/changes-parentheses-bring.html"

            elif match.re == self.ampintextref:
                newMatch.feedback = (u"Use 'and' to separate in-text author names.")
                suggestion = re.sub(r"and", r"&", newMatch.target)

            if newMatch and suggestion:
                newMatch.suggestions.append(suggestion)
                self.Matches.append(newMatch)

        return self.Matches
