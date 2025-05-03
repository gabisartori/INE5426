import sys
if len(sys.argv) != 2:
  print("Usage: python test.py <string>")
  sys.exit(1)
string = sys.argv[1]

final_states = set()
transitions = {}

with open("../machines/lexer.automata", "r") as f:
  state_size = ord(f.read(1))
  while True:
    char = f.read(state_size)
    if char == chr(255)*state_size: break
    state_num = 0
    for byte in char: state_num = (state_num << 8) + ord(byte)
    final_states.add(state_num)
  
  while transition := f.read(2*state_size+1):
    current_state, symbol, next_state = transition[:state_size], transition[state_size:state_size+1], transition[state_size+1:]
    cs_n = 0
    ns_n = 0
    for byte in current_state: cs_n = (cs_n << 8) + ord(byte)
    for byte in next_state: ns_n = (ns_n << 8) + ord(byte)
    transitions[(cs_n, symbol)] = ns_n

current_state = 0
for char in string:
  if (current_state, char) in transitions: current_state = transitions[(current_state, char)]
  else:
    print(f"Error: No transition from state {current_state} with symbol '{char}'")
    current_state = -1
    break
print(current_state, current_state in final_states)