string = \
"""def f(int x) {
\tif x < 0
\t\tx = -x;
\treturn;
}"""

EMPTY = " \n\t"

# S -> [a-z]C | [a-z]
# C -> [a-z]C | [0-9]C | [a-z] S | [0-9] S | [a-z] | [0-9]

def transition(state: str, char: chr):
    if state == "s":
        if char.isalpha(): return "c"
        if char in EMPTY:
            #print(char, end='')
            return "s"
        else:
            #print("OUTRO", end='')
            return "s"
    elif state == "c":
        if char.isalpha() or char.isdigit(): return "c"
        if char in EMPTY:
            #print("IDENT", end=char)
            return "s"
        else:
            #print("IDENT OUTRO ", end='')
            return "s"
    print("ERROR")

current_state = "s"
symbol = ""
line_count = 1
tabela = {}
for char in string: 
    if char == "\n": line_count += 1
    symbol += char
    current_state = transition(current_state, char)
    if current_state == "s":
        symbol = symbol[:-1]
        if symbol:
            if symbol not in tabela: tabela[symbol] = []
            if (not tabela[symbol]) or tabela[symbol][-1] != line_count:
                tabela[symbol].append(line_count)
        symbol = ""
        
        
print(tabela)