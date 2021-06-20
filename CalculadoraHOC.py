import ply.lex as lex
import ply.yacc as yacc

class MiLexer(object):
    # List of token names.   This is always required
    tokens = (
       'NUM',
       'MAS',
       'MENOS',
       'MULT',
       'DIV',
       'PAR_IZQ',
       'PAR_DER',
       'POW',
       'T_SEN',
       'T_COS',
       'T_TAN'
    )

    # Regular expression rules for simple tokens
    t_NUM = r'\d'
    t_MAS = r'\+'
    t_MENOS = r'-'
    t_MULT = r'\*'
    t_DIV = r'/'
    t_PAR_IZQ = r'\('
    t_PAR_DER = r'\)'
    t_POW = r'\^'
    t_T_SEN = r'sen'
    t_T_COS = r'cos'
    t_T_TAN = r'tan'

    # A regular expression rule with some action code
    # Note addition of self parameter since we're in a class

    # Define a rule so we can track line NUMs
    def t_newline(self,t):
        r'\n+'
        t.lexer.lineno += len(t.value)

    # A string containing ignored characters (spaces and tabs)
    t_ignore  = ' \t'

    # Error handling rule
    def t_error(self,t):
        print("Illegal character '%s'" % t.value[0])
        t.lexer.skip(1)

    # Build the lexer
    def build(self,**kwargs):
        self.lexer = lex.lex(module=self, **kwargs)

    # Test it output
    def test(self,data):
        self.lexer.input(data)
        while True:
             tok = self.lexer.token()
             if not tok:
                 break
             print(tok)


# Asociación de operadores y precedencia
# ya que la gramatica es ambigua
precedence = (
    ('left','MAS','MENOS'),
    ('left','MULT','DIV'),
    ('right','UMENOS'),
    )



# Build the lexer and try it out
m = MiLexer()
m.build()           # Build the lexer

parser = yacc.yacc()

m.test("tan(31 + 41)^2")


