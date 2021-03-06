# Parser, based on John Aycock's SPARK examples

from spark import GenericParser
from spark import GenericASTBuilder
from errors import GrammaticalError
from ast import AST
from copy import deepcopy

class CoreParser(GenericParser):
    def __init__(self, start):
        GenericParser.__init__(self, start)

    def typestring(self, token):
        return token.type

    def error(self, token):
        raise GrammaticalError(
            "Unexpected token `%s' (word number %d)" % (token, token.wordno))

    def p_chained_commands(self, args):
        '''
            chained_commands ::= single_command
            chained_commands ::= single_command chained_commands
        '''
        if(len(args) == 1):
            return AST('chain', None, [ args[0] ])
        else:
            args[1].children.insert(0, args[0])
            return args[1]

    def p_single_command(self, args):
        '''
            single_command ::= letter
            single_command ::= sky_letter
            single_command ::= movement
            single_command ::= character
            single_command ::= editing
            single_command ::= english
            single_command ::= word_sentence
            single_command ::= word_phrase
            single_command ::= word_camel
            '''
        return args[0]

    def p_movement(self, args):
        '''
            movement ::= up     repeat
            movement ::= down   repeat
            movement ::= left   repeat
            movement ::= right  repeat
        '''
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('movement', [ args[0] ])
            ])
        else:
            return AST('movement', [ args[0] ])

    def p_repeat(self, args):
        '''
            repeat ::=
            repeat ::= num
        '''
        if len(args) > 0:
            return args[0]
        else:
            return None

    def p_number(self, args):
        '''
            num ::= zero
            num ::= one
            num ::= two
            num ::= three
            num ::= free
            num ::= four
            num ::= for
            num ::= five
            num ::= six
            num ::= seven
            num ::= eight
            num ::= nine
        '''
        # doesn't work right now
        #for v in value:
        #    self.__doc__ += "number ::= " + v
        value = {
            'zero'  : 0,
            'one'   : 1,
            'two'   : 2,
            'three' : 3,
            'free' : 3,
            'four'  : 4,
            'for'  : 4,
            'five'  : 5,
            'six'   : 6,
            'seven' : 7,
            'eight' : 8,
            'nine'  : 9
        }
        return value[args[0].type]

    def p_sky_letter(self, args):
        '''
            sky_letter ::= sky letter
        '''
        ast = args[1]
        ast.meta[0] = ast.meta[0].upper()
        return ast

    def p_letter(self, args):
        '''
            letter ::= arch
            letter ::= bravo
            letter ::= charlie
            letter ::= delta
            letter ::= eco
            letter ::= echo
            letter ::= fox
            letter ::= golf
            letter ::= hotel
            letter ::= india
            letter ::= julia
            letter ::= kilo
            letter ::= line
            letter ::= mike
            letter ::= november
            letter ::= nov
            letter ::= oscar
            letter ::= papa
            letter ::= queen
            letter ::= romeo
            letter ::= sierra
            letter ::= tango
            letter ::= uniform
            letter ::= victor
            letter ::= victoria
            letter ::= whiskey
            letter ::= whisky
            letter ::= xray
            letter ::= expert
            letter ::= yankee
            letter ::= zulu
            letter ::= number repeat
        '''
        if(args[0].type == 'expert'): args[0].type = 'x'
        if(args[0].type == 'number'):
            return AST('char', str(args[1]))

        return AST('char', [ args[0].type[0] ])

    def p_character(self, args):
        '''
            character ::= act
            character ::= colon
            character ::= call on
            character ::= single
            character ::= double
            character ::= equal
            character ::= space
            character ::= tab
            character ::= bang
            character ::= hash
            character ::= dollar
            character ::= percent
            character ::= carrot
            character ::= ampersand
            character ::= star
            character ::= late
            character ::= rate
            character ::= minus
            character ::= underscore
            character ::= plus
            character ::= backslash
            character ::= dot
            character ::= slash
            character ::= question
            character ::= break
            character ::= lake
            character ::= square
            character ::= rectangle
            character ::= sami
            character ::= something
            character ::= come
            character ::= great
            character ::= small
            character ::= end
            character ::= and
            character ::= home
            character ::= control
        '''
        value = {
            'act'   : 'Escape',
            'colon' : 'colon',
            'call on' : 'colon',
            'single': 'apostrophe',
            'double': 'quotedbl',
            'equal' : 'equal',
            'space' : 'space',
            'tab'   : 'Tab',
            'bang'  : 'exclam',
            'hash'  : 'numbersign',
            'dollar': 'dollar',
            'percent': 'percent',
            'carrot': 'asciicircum',
            'ampersand': 'ampersand',
            'star': 'asterisk',
            'late': 'parenleft',
            'rate': 'parenright',
            'minus': 'minus',
            'underscore': 'underscore',
            'plus': 'plus',
            'backslash': 'backslash',
            'dot': 'period',
            'slash': 'slash',
            'question': 'question',
            'break': 'braceright',
            'lake': 'braceleft',
            'square': 'bracketleft',
            'rectangle': 'bracketright',
            'sami': 'semicolon',
            'something': 'semicolon',
            'come': 'comma',
            'great': 'greater',
            'small': 'less',
            'end': 'End',
            'and': 'End',
            'home': 'Home',
            'control' : 'ctrl+'
        }
        return AST('raw_char', [ value[args[0].type] ])

    def p_editing(self, args):
        '''
            editing ::= slap        repeat
            editing ::= scratch     repeat
        '''
        value = {
            'slap'  : 'Return',
            'scratch': 'BackSpace'
        }
        if args[1] != None:
            return AST('repeat', [ args[1] ], [
                AST('raw_char', [ value[args[0].type] ])
            ])
        else:
            return AST('raw_char', [ value[args[0].type] ])



    def p_english(self, args):
        '''
            english ::= word ANY
        '''
        return AST('sequence', [ args[1].extra ])

    def p_word_sentence(self, args):
        '''
            word_sentence ::= sentence word_repeat
        '''
        if(len(args[1].children) > 0):
            args[1].children[0].meta = args[1].children[0].meta.capitalize()
        return args[1]

    def p_word_phrase(self, args):
        '''
            word_phrase ::= phrase word_repeat
        '''
        return args[1]

    def p_word_camel(self, args):
        '''
            word_camel ::= campbell word_repeat
            word_camel ::= camel word_repeat
        '''
        print dir(args[1])
        if(len(args[1].children) > 0):
            camelCase = ''
            first = True #we use it not to capitalise the first character
            for a in args[1].children:
                if first:
                    camelCase += a.meta
                    first = False
                else:
                    camelCase += a.meta.capitalize()

            args[1].children[0].meta = camelCase
            child = deepcopy(args[1].children[0])
            del args[1].children #we throw away all childes
            args[1].children = [child] #insert only the 1 generated and having the camelCase meta

        return args[1]


    def p_word_repeat(self, args):
        '''
            word_repeat ::= ANY
            word_repeat ::= ANY word_repeat
        '''
        if(len(args) == 1):
            return AST('word_sequence', None,
                [ AST('null', args[0].extra) ])
        else:
            args[1].children.insert(0, AST('null', args[0].extra))
            return args[1]

class SingleInputParser(CoreParser):
    def __init__(self):
        CoreParser.__init__(self, 'single_input')

    def p_single_input(self, args):
        '''
            single_input ::= END
            single_input ::= chained_commands END
        '''
        if len(args) > 0:
            return args[0]
        else:
            return AST('')

def parse(tokens):
    parser = SingleInputParser()
    return parser.parse(tokens)
