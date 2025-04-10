string = \
"""def f (int a) {
\tx = x + a;
\treturn;
}"""

# Estados
# s0
## [a-z] -> corpo_ident
## \s -> s0; return \s
## * -> s0; return outro
# corpo_ident
## [a-z] -> corpo_ident
## [0-9] -> corpo_ident
## \s -> s0; return ident
## * -> s0; return ident, outro



def transition(state: str, char: chr) -> tuple[str, str]:
    '''Returns the next state and the command to run on transition'''
    if state == 's':
        if char.isalpha(): return ('c', "")
        elif char.isspace(): return ('s', char)
        else: return ('s', "OUTRO")
    elif state == 'c':
        if char.isalpha() or char.isdigit(): return ('c', "")
        elif char.isspace(): return ('s', "IDENT"+char)
        else: return ('s', "IDENT OUTRO ")

current_state = "s"
for char in string:
    current_state, command = transition(current_state, char)
    if command: print(command, end='')
