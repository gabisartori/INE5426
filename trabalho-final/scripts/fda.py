State = frozenset[str|int]

class FDA:
  def __init__(self, string: str=None) -> None:
    self.string: str = string
    self.initial_state: State = None
    self.transitions: dict[State, dict[str, frozenset[State]]] = {}
    self.final_states: frozenset[State] = frozenset()
    self.states: frozenset[State] = frozenset((frozenset(("qm",)),))
    self.num_states: int = 0
    self.alphabet: set[chr] = set()
    if self.string: self.from_string()
    if self.initial_state is not None: self.enumerate_states()

  def transition_count(self) -> int:
    '''Retorna o número de transições do autômato.'''
    count = 0
    for state in self.transitions:
      for symbol in self.transitions[state]:
        count += len(self.transitions[state][symbol])
    return count

  def from_string(self) -> None:
    temp_states = set()
    num_states, initial_state, final_states, alphabet, *transitions = self.string.split(';')
    initial_state = int(initial_state) if initial_state.isdigit() else initial_state
    final_states = [int(x) if x.isdigit() else x for x in final_states[1:-1].split(',')]

    self.num_states = int(num_states)
    self.initial_state = frozenset((initial_state,))
    self.final_states = frozenset(frozenset((state,)) for state in final_states)
    self.alphabet = frozenset(alphabet[1:-1].split(','))
    transitions = [transition for transition in transitions if transition]
    for transition in transitions:
      state, symbol, next_state = transition.split(',')
      if symbol == "": symbol = "&"
      state = int(state) if state.isdigit() else state
      next_state = int(next_state) if next_state.isdigit() else next_state
      state = frozenset((state,))
      next_state = frozenset((next_state,))
      if state not in self.transitions: self.transitions[state] = {}
      if symbol not in self.transitions[state]: self.transitions[state][symbol] = frozenset()
      self.transitions[state][symbol] = self.transitions[state][symbol].union(frozenset((next_state,)))
      temp_states.add(state)
      temp_states.update(self.transitions[state][symbol])
    self.states = frozenset(temp_states)

  def is_deterministic(self):
    '''Busca por transições por ε ou por um estado que tenha mais de um destino para um mesmo símbolo.'''
    for state in self.transitions:
      if "&" in self.transitions[state]: return False
      for symbol in self.alphabet:
        if symbol not in self.transitions[state]: continue
        if len(self.transitions[state][symbol]) > 1: return False
    return True

  def enumerate_states(self) -> 'FDA':
    '''Converte todos os estados do autômato em ints de 0 a n-1, sendo n o número de estados do autômato.'''
    '''Exemplo: um autômato com 3 estados {"A", "B", "C"} vira {"0", "1", "2"}'''
    non_initial_states = self.states.difference(frozenset((self.initial_state,)))
    states = {
      **{self.initial_state: 0},
      **{state: i+1 for i, state in enumerate(non_initial_states)}
    }
    self.states = frozenset(frozenset((states[state],)) for state in self.states)
    self.initial_state = frozenset((states[self.initial_state],))
    self.final_states = frozenset(frozenset((states[state],)) for state in self.final_states)
    new_transtions = {}
    for state, transtions in self.transitions.items():
      enumerated_state = frozenset((states[state],))
      if enumerated_state not in new_transtions: new_transtions[enumerated_state] = {}
      for symbol, next_states in transtions.items():
        if symbol not in new_transtions[enumerated_state]: new_transtions[enumerated_state][symbol] = frozenset()
        for next_state in next_states:
          new_transtions[enumerated_state][symbol] = new_transtions[enumerated_state][symbol].union(frozenset((frozenset((states[next_state],)),)))
    self.transitions = new_transtions
    return self

  def union(self, other: 'FDA') -> 'FDA':
    '''Realiza a união entre dois autômatos.'''
    a = self.copy().enumerate_states()
    b = other.copy().enumerate_states()
    union = FDA()
    b_start = len(a.transitions)+1

    union.initial_state = frozenset((0,))
    union.alphabet = a.alphabet.union(b.alphabet)
    # Self states will be shifted by 1 to allow the new initial state as 0,
    # and the other automaton will be shifted by the number of states in the first automaton
    # I'm pretty sure every automata given to this part of the algorithm will have states going from 0 to n-1
    union.states = frozenset(self.add_int_to_state(state, 1) for state in self.states).union(
      frozenset(self.add_int_to_state(state, b_start) for state in other.states)
    ).union(
      frozenset((union.initial_state,))
    )
    union.num_states = len(union.states)
    union.final_states = frozenset(self.add_int_to_state(state, 1) for state in a.final_states).union(
      frozenset(self.add_int_to_state(state, b_start) for state in b.final_states)
    )
    self_transtion = {
      self.add_int_to_state(state, 1): {
        symbol: frozenset(self.add_int_to_state(next_state, 1) for next_state in next_states) for symbol, next_states in a.transitions[state].items()
      } for state in a.transitions 
    }
    other_transition = {
      self.add_int_to_state(state, b_start): {
        symbol: frozenset(self.add_int_to_state(next_state, b_start) for next_state in next_states) for symbol, next_states in b.transitions[state].items()
      } for state in b.transitions
    }
    self_initial_trasitions = {
      union.initial_state: {
        '&': frozenset((frozenset((1,)), frozenset((b_start,))))
      }
    }
    union.transitions = {
      **self_transtion,
      **other_transition,
      **self_initial_trasitions
    }

    return union

  @staticmethod
  def concat_to_state_name(state: State, string: str) -> State:
    '''Concatena o nome do estado com uma string.'''
    '''Exemplo: um estado "A" vira "0A"'''
    return frozenset(f"{string}{state_part}" for state_part in state)

  @staticmethod
  def add_int_to_state(state: State, num: int) -> State:
    '''Adiciona um número inteiro ao número do estado.'''
    '''O estado deve ser numérico.'''
    '''Exemplo: um estado "0" vira "0+1"'''
    return frozenset(int(state_part)+num for state_part in state)

  @staticmethod
  def state_to_string(state: State) -> str:
    '''Une as partes de um estado em uma string.'''
    '''Exemplo: um estado {"A", "B"} vira "AB"'''
    return f"{{{','.join(sorted([str(state_part) for state_part in state]))}}}"

  def __str__(self) -> str:
    num_states = str(self.num_states)
    initial_state = self.state_to_string(self.initial_state)
    alphabet = ','.join(sorted(self.alphabet))
    final_states = ','.join([self.state_to_string(str(state)) for state in sorted(self.final_states)])
    transitions = ';'.join([','.join([self.state_to_string(state), symbol, self.state_to_string(next_state)]) for state, symbol, next_state in self.transitions_as_tuples()])

    return f"{num_states};{initial_state};{{{final_states}}};{{{alphabet}}};{transitions}"

  def deterministic_equivalent(self) -> 'FDA':
    def epsilon_closure(state: State, closure: set=None) -> State:
      '''Retorna o ε* de um estado, realizando uma busca em profundidade.'''
      if closure is None: closure = set(state)
      if state not in self.transitions or "&" not in self.transitions[state]: return frozenset(closure)

      for reachable_state in self.transitions[state]["&"]:
        if reachable_state not in closure:
          reachable_state_closure: State = epsilon_closure(reachable_state)
          closure.update(reachable_state_closure)

      return frozenset(closure)

    # Se o autômato já é determinístico, retorna uma cópia dele mesmo
    if self.is_deterministic(): return self.copy()

    deterministic = FDA()
    # Trata todo autômato não determinístico como se tivesse transições por ε
    # Caso não tenha, ε* de cada estado é ele mesmo, não influenciando no resultado
    states_epsilon_closure: dict[State, State] = {}
    for state in self.states.difference({'qm'}): states_epsilon_closure[state] = epsilon_closure(state)

    # Construir o autômato determinístico equivalente

    # Conjunto temporário para armaenar os estados a serem incluídos no autômato determinístico
    temp_states: set[State] = set()

    # O estado inicial do autômato determinístico é o ε* do estado inicial do autômato não determinístico
    deterministic.initial_state = states_epsilon_closure[self.initial_state]
    
    # O alfabeto do autômato determinístico é o mesmo do autômato não determinístico, sem o símbolo ε
    deterministic.alphabet = self.alphabet.copy().difference({"&"})
    
    # Começa a construir as transições do autômato determinístico, partindo do estado inicial
    deterministic.transitions = {}
    stack = [deterministic.initial_state]
    while stack:
      # Adiciona o estado visitado ao conjunto de estados do autômato determinístico
      current_state = stack.pop()
      temp_states.add(current_state)

      # Prepara a tabela de transições para receber o novo estado
      if current_state not in deterministic.transitions:
        deterministic.num_states += 1
        deterministic.transitions[current_state] = {}

      # Para cada símbolo do alfabeto, visita os estados alcançáveis a partir do estado atual
      for symbol in sorted(deterministic.alphabet.difference({"&"})):
        next_state: set[str] = set()
        for state in sorted(current_state):
          state = frozenset((state,))
          if state not in self.transitions or symbol not in self.transitions[state]: continue
          next_state.update({states_epsilon_closure[huh] for huh in self.transitions[state][symbol]})
        if not next_state: continue
        next_state = frozenset([state_part for x in next_state for state_part in x])
        deterministic.transitions[current_state][symbol] = frozenset([next_state])
        if next_state not in temp_states:
          stack.append(next_state)

    # Agora que todos os estados foram calculados, o conjunto temporário pode ser transformado em um conjunto imutável
    deterministic.states = frozenset(temp_states)
    # Adiciona ao conjunto de estados finais do autômato determinístico os estados que contém algum estado final do autômato não determinístico
    for state in deterministic.states:
      for final_state in self.final_states:
        if final_state.intersection(state):
          deterministic.final_states = deterministic.final_states.union(frozenset((state,)))
          break

    deterministic.string = str(deterministic)
    return deterministic

  def copy(self) -> 'FDA':
    copy = FDA()
    copy.string = self.string
    copy.initial_state = self.initial_state
    copy.final_states = self.final_states.copy()
    copy.states = self.states.copy()
    copy.num_states = self.num_states
    copy.alphabet = self.alphabet.copy()
    copy.transitions = {state: {symbol: next_state.copy() for symbol, next_state in self.transitions[state].items()} for state in self.transitions}
    return copy

  def transitions_as_tuples(self) -> list:
    '''Retorna as transições do autômato como uma lista de tuplas (estado, símbolo, próximo estado) para facilitar a ordenação da saída do programa.'''
    transitions = []
    for state in self.transitions:
      for symbol in self.transitions[state]:
        for next_state in self.transitions[state][symbol]:
          transitions.append((state, symbol, next_state))

    transitions.sort(key=lambda x: sorted(x[1])) # Ordena as transições pelo símbolo
    transitions.sort(key=lambda x: sorted(x[0])) # Ordena as transições pelo estado de origem
    return transitions

# Debug stuff

if __name__ == "__main__":
  def show_automaton(automaton: FDA) -> None:
    '''Mostra o autômato em formato de tabela.'''
    print(f"Estados: {automaton.states}")
    print(f"Estado inicial: {automaton.initial_state}")
    print(f"Estados finais: {automaton.final_states}")
    print(f"Alfabeto: {automaton.alphabet}")
    print("Transições:")
    for state in automaton.transitions:
      for symbol in automaton.transitions[state]:
        for next_state in automaton.transitions[state][symbol]:
          print(f"{state} --{symbol}--> {next_state}")
    print()

  fda = FDA("2;b;{d};{a,0};b,a,d;d,a,d;d,0,d")
  fdb = FDA("2;0;{1};{c,d};0,c,1;0,d,1;1,c,0;1,d,0")
  for transition, next_state in fda.transitions.items():
    for symbol, next_states in next_state.items():
      print(f"{transition} --{symbol}--> {next_states}")