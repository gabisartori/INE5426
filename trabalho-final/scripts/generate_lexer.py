import json
from fda import FDA

VALID_LETTERS = {
  chr(i) for i in range(256) if chr(i).isalpha() and chr(i).islower()
}

with open("../grammars/tokens.json", "r") as f: token_types = json.load(f)
automata: dict[str, FDA] = {}
for token_type, token_data in token_types.items():
  '''Cria um autômato finito determinístico para cada tipo de token.
  Alguns tokens são definidos apenas por uma string, como palavras reservadas. Nesse caso, basta criar uma cadeia de estados, uma para cada letra da string.
  Outros tokens já estão definidos como autômatos, para poupar o trabalho de parsear a regex que representa o token. Como identificadores ou números.
  Não sei ainda onde colocar essa informação. É útil pontuar que a união dos autômatos criará um autômato não determinístico, pois existem trechos em comum entre diferentes tokens, por exemplo toda palavra reservada pode ser apenas o começo de um identificador.
  Como o algoritmo de determinização de autômatos já está implementado, é importante que todo caso em que esse não determinismo ocorra, as transições sejam feitas de forma que a implementação do algoritmo de determinização consiga identificá-las e tratá-las.
  Basicamente isso é importante pois símbolos como "." serão utilizados para que a transição ocorra para _qualquer caracter_, mas quando existem outras transições saindo desse estadom, é importante que "." seja expandido para todas as transiçẽos de forma que o não determinismo seja percebido pelo algoritmo de determinização e tratado.
  No saco de strings e chars, é possível (e crucial*) utilizar o "." pois nenhum outro token segue o formato de começar com aspas (simples ou duplas). Porém, para um identificador, é preciso expandir "." em {a, b, c.. y, z}, pois outros tokens também podem ser aceitos por .*. Logo, há não determinismo que precisa ser tratado.
  * Motivo pelo qual o "." é crucial para o parsing de strings e chars, e porque outros tokens precisam utilizar a-z em vez de ".": "." poderia ser expandido para todas as letras do alfabeto, porém há de se considerar que em vez de usar apenas a tabela ASCII, espera-se que o lexer funcione para identificar qualquer string UTF, fazendo com que "." possa assumir milhares de valores, o que criaria um autômato desnecessariamente grande para parsear identificadores. Então, strings e chars usam "." para poder aceitar _qualquer_ valor UTF inserido pelo usuário, enquanto identificadores expandem n transições para cada letra aceita pela linguagem.
  Para expandir "." para todas as letras aceitas pela linguagem, irei usar or conjunto {chr(i) if chr(i).isalpha() and chr(i).islower() for i in range(256)}
  '''
  if "string" in token_data:
    # Create a finite automaton for each letter of the string
    strings = token_data["string"]
    if isinstance(strings, str): strings = [strings]
    transitions = {}
    finals = set()
    counter = 0
    for string in strings:
      if 0 in transitions: transitions[0] = {**transitions[0], **{string[0]: counter+1}}
      else: transitions[0] = {string[0]: counter+1}
      start = counter
      for i in range(1, len(string)):
        char = string[i]
        if start+i in transitions: transitions[start+i] = {**transitions[start+i], **{string[i]: start+i+1}}
        else: transitions[start+i] = {string[i]: start+i+1}
        counter += 1
      counter += 1
      finals.add(counter-1)
    finals = {frozenset((i,)) for i in finals}
    transitions = {
      frozenset((c,)): {
        symbol: frozenset((frozenset((next_state,)),)) for symbol, next_state in next_states.items()
        } for c, next_states in transitions.items()
      }
    automaton = FDA()
    automaton.alphabet=frozenset(c for string in strings for c in string)
    automaton.states=frozenset(frozenset((i,)) for i in range(counter+1))
    automaton.transitions=transitions
    automaton.initial_state=frozenset((0,))
    automaton.final_states=finals
    automata[token_type] = automaton
  else:
    # The automaton is already defined in the json file, just convert it to a fda
    final_states = {state for state in token_data["final_states"]}
    transitions = {}
    alphabet = set()
    for current_state, symbol, next_state in token_data["transitions"]:
      if current_state not in transitions: transitions[current_state] = {}
      if len(symbol) == 1:
        transitions[current_state][symbol] = next_state
        alphabet.add(symbol)
      elif "-" in symbol and len(symbol) == 3:
        start, end = symbol.split("-")
        for i in range(ord(start), ord(end)+1):
          transitions[current_state][chr(i)] = next_state
          alphabet.add(chr(i))
      elif symbol == "\\c":
        for i in VALID_LETTERS:
          transitions[current_state][i] = next_state
          alphabet.add(i)
      elif symbol == "\\d":
        for i in range(10):
          transitions[current_state][str(i)] = next_state
          alphabet.add(str(i))
      elif symbol == "\\.":
        transitions[current_state]["\\."] = next_state
      else:
        raise ValueError(f"Invalid symbol {symbol} in transitions")

    transitions = {
      frozenset((c,)): {
        symbol: frozenset((frozenset((next_states, )),)) for symbol, next_states in next_states.items()
      } for c, next_states in transitions.items()
    }
    automaton = FDA()
    automaton.alphabet=frozenset(alphabet)
    states = set()
    for state, transtions in transitions.items():
      states.add(state)
      for next_states in transtions.values():
        states.update(next_states)
    automaton.states=frozenset(states)
    automaton.transitions=transitions
    automaton.initial_state=frozenset((0,))
    automaton.final_states=frozenset(frozenset((i,)) for i in final_states)
    automata[token_type] = automaton

mega_automaton = None
for token_type, automaton in automata.items():
  if mega_automaton is None: mega_automaton = automaton
  else: mega_automaton = mega_automaton.union(automaton)
  print(token_type, mega_automaton.transition_count())  

def int_to_64(number):
  """Converts an integer to a base64 string."""
  base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
  result = ""
  while number > 0:
    result = base64_chars[number % 64] + result
    number //= 64
  return result if result else "0"

def base64_to_int(base64_str):
  """Converts a base64 string to an integer."""
  base64_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
  result = 0
  for char in base64_str:
    result = result * 64 + base64_chars.index(char)
  return result

def clear_state(state): 
  string = ""
  for state_part in state:
    if isinstance(state_part, frozenset):
      string += str(state_part)[11:-2]
    else:
      string += str(state_part)
  number = int(string)
  number_base64 = int_to_64(number)
  return number

mega_automaton = mega_automaton.deterministic_equivalent().enumerate_states()
transition_list = []
for state in sorted(mega_automaton.transitions):
  for symbol in sorted(mega_automaton.transitions[state]):
    for next_state in mega_automaton.transitions[state][symbol]:
      transition_list.append((clear_state(state), symbol, clear_state(next_state)))

with open("../grammars/lexer.json", "w") as f:
  json.dump({
    "transitions": transition_list,
    "final_states": [clear_state(state) for state in mega_automaton.final_states],
    "initial_state": clear_state(mega_automaton.initial_state)
  }, f)
print("Lexer generated successfully.")
print(f"Lexer has {len(automata)} automata and {len(mega_automaton.final_states)} final states.")
print(f"Lexer has {len(mega_automaton.states)} states and {mega_automaton.transition_count()} transitions.")
