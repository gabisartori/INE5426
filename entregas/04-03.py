string = \
"""def f(int a) {
\tx = x + a;
\treturn;
}"""

EMPTY = " \n\t"

# S -> [a-z]C | [a-z]
# C -> [a-z]C | [0-9]C | [a-z] S | [0-9] S | [a-z] | [0-9]

def transition(state: str, char: chr):
    if state == "s":
        if char.isalpha(): return "c"
        if char in EMPTY:
            print(char, end='')
            return "s"
        else:
            print("OUTRO", end='')
            return "s"
    elif state == "c":
        if char.isalpha() or char.isdigit(): return "c"
        if char in EMPTY:
            print("IDENT", end=char)
            return "s"
        else:
            print("IDENT OUTRO ", end='')
            return "s"
    print("ERROR")

current_state = "s"
for char in string: current_state = transition(current_state, char)