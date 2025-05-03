import sys
if len(sys.argv) != 2:
  print("Usage: python test.py <string>")
  sys.exit(1)
string = sys.argv[1]

final_states = set()
transitions = {}

with open("../machines/lexer.automata", "r") as f:
  current_state = 0
  symbol = ""
  next_state = 0
  while (char := f.read(1)) != chr(255): final_states.add(ord(char))
  count = 0
  
  while char := f.read(1):
    if count == 0:
      current_state = ord(char)
    elif count == 1:
      symbol = char
    elif count == 2:
      next_state = ord(char)
      transitions[(current_state, symbol)] = next_state
    count = (count+1)%3

current_state = 0
for char in string:
  if (current_state, char) in transitions: current_state = transitions[(current_state, char)]
  else:
    print(f"Error: No transition from state {current_state} with symbol '{char}'")
    current_state = -1
    break
print(current_state, current_state in final_states)