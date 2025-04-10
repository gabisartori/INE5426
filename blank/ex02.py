string = \
"""def f (int x) {
\tif x < 0
\t\t x = -x;
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
        if char.isalpha(): return ('c', "APPEND")
        elif char.isspace(): return ('s', "")
        else: return ('s', "")
    elif state == 'c':
        if char.isalpha() or char.isdigit(): return ('c', "APPEND")
        elif char.isspace(): return ('s', "PRINT")
        else: return ('s', "PRINT")

current_state = "s"
read = ""
table = {}
line = 1
def append(table, symbol, line):
    if symbol not in table: table[symbol] = []
    if not table[symbol] or table[symbol][-1] != line: table[symbol].append(line)

for char in string:
    # This should be a command returned by the transtion function but I ain't doing that now
    if char == '\n': line += 1
    
    current_state, command = transition(current_state, char)
    if command == "APPEND": read += char
    elif command == "PRINT":
        append(table, read, line)
        read = ""
    elif command == "PRINT+":
        append(table, read+char, line)
        read = ""


for symbol in sorted(table):
    print(symbol, '\t', table[symbol])
