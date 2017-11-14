import re

keywords = [
    'act',
    'ampersand',
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
    'equal',
    'expert',
    'five',
    'four',
    'fox',
    'golf',
    'hash',
    'hotel',
    'india',
    'julia',
    'kilo',
    'late',
    'lake',
    'left',
    'line',
    'mike',
    'minus',
    'nine',
    'november',
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
