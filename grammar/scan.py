import re

keywords = [
    'act',
    'ampersand',
    'and',
    'arch',
    'backslash',
    'bang',
    'bravo',
    'break',
    'carrot',
    'camel',
    'campbell',
    'charlie',
    'colon',
    'come',
    'control',
    'call on',
    'delta',
    'dollar',
    'dot',
    'double',
    'down',
    'echo',
    'eco',
    'eight',
    'english',
    'end',
    'equal',
    'expert',
    'five',
    'four',
    'for',
    'fox',
    'golf',
    'great',
    'hash',
    'hotel',
    'home',
    'india',
    'julia',
    'kilo',
    'late',
    'lake',
    'left',
    'less',
    'last',
    'line',
    'mike',
    'minus',
    'nine',
    'november',
    'nov',
    'number',
    'one',
    'oscar',
    'papa',
    'percent',
    'plus',
    'phrase',
    'queen',
    'question',
    'rate',
    'rectangle',
    'right',
    'romeo',
    'sami',
    'small',
    'something',
    'scratch',
    'sentence',
    'seven',
    'sierra',
    'single',
    'six',
    'sky',
    'slap',
    'slash',
    'space',
    'star',
    'square',
    'tab',
    'tango',
    'three',
    'free',
    'two',
    'underscore',
    'uniform',
    'up',
    'victor',
    'victoria',
    'whiskey',
    'whisky',
    'word',
    'xray',
    'yankee',
    'zero',
    'zulu'
]

class Token:
    def __init__(self, type, wordno=-1, extra=''):
        self.type = type
        self.extra = extra
        self.wordno = wordno

    def __cmp__(self, o):
        return cmp(self.type, o)
    def __repr__(self):
        return str(self.type)

def scan(line):
    tokens = []
    wordno = 0
    for t in line.lower().split():
        wordno += 1
        if(t in keywords):
            tokens.append(Token(t, wordno))
        else:
            tokens.append(Token('ANY', wordno, t))
    tokens.append(Token('END'))
    print tokens
    return tokens
