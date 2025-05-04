import sys
import json
if len(sys.argv) != 2:
  print("Usage: python test.py <string>")
  sys.exit(1)
string = sys.argv[1]

final_states = set()
transitions = {}

with open("../machines/lexer.automata", "rb") as f:
  state_size = int.from_bytes(f.read(1), byteorder='big')
  while True:
    bytes = f.read(state_size)
    if bytes == bytearray([255]*state_size): break
    state_num = int.from_bytes(bytes, byteorder='big')
    final_states.add(state_num)
  
  while transition := f.read(2*state_size+1):
    current_state, symbol, next_state = transition[:state_size], transition[state_size:state_size+1], transition[state_size+1:]
    cs_n = int.from_bytes(current_state, byteorder='big')
    ns_n = int.from_bytes(next_state, byteorder='big')
    symbol = int.from_bytes(symbol, byteorder='big')
    transitions[(cs_n, chr(symbol))] = ns_n

current_state = 0
with open("../machines/lexer_tabela.automata", "r") as f:
  state_token_list = json.load(f)

for char in string:
  if (current_state, char) in transitions: current_state = transitions[(current_state, char)]
  else:
    print(f"Error: No transition from state {current_state} with symbol '{char}'")
    current_state = -1
    break
print(current_state, current_state in final_states, state_token_list[str(current_state)] if str(current_state) in state_token_list else "None")