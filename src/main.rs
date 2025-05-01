use std::collections::{HashSet, HashMap};
// use std::hash::Hash;

type State = u32;
type Symbol = char;
type Command = String;

const S0: State = 0;
const S1: State = 1;
const S2: State = 2;
const A0: Symbol = '0';
const A1: Symbol = '1';

struct FSDA {
  initial_state: State,
  final_states: HashSet<State>,
  transitions: HashMap<(State, Symbol), (State, Option<Command>)>,
  _states: HashSet<State>,
  _alphabet: HashSet<Symbol>,
}

impl FSDA {
  fn new(initial_state: State, final_states: HashSet<State>, transitions: HashMap<(State, Symbol), (State, Option<Command>)>) -> FSDA {
    let _states = transitions.keys().map(|(state, _)| *state).collect::<HashSet<_>>();
    let _alphabet = transitions.keys().map(|(_, symbol)| *symbol).collect::<HashSet<_>>();

    FSDA { initial_state, final_states, transitions, _states, _alphabet }
  }

  fn accepts(&self, input: Vec<Symbol>) -> bool {
    let mut current_state = self.initial_state;
    for symbol in input {
      if let Some((next_state, _command)) = self.transitions.get(&(current_state, symbol)) {
        current_state = *next_state;
      } else {
        return false;
      }
    }
    self.final_states.contains(&current_state)
  }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
  // Read args
  let args: Vec<String> = std::env::args().collect();
  if args.len() < 2 { return Err("Usage: <input_file>".into()); }
  let input_file = &args[1];
  let input = std::fs::read_to_string(input_file)?;
  let lines = input.lines();

  for line in lines {
    let initial_state = S0;
    let final_states = HashSet::from([S0]);
    let transitions = HashMap::from([
      ((S0, A0), (S0, None)),
      ((S0, A1), (S1, None)),
      ((S1, A0), (S2, None)),
      ((S1, A1), (S0, None)),
      ((S2, A0), (S1, None)),
      ((S2, A1), (S2, None)),
    ]);

    let fsa = FSDA::new(initial_state, final_states, transitions);
    let input = line.chars().collect::<Vec<Symbol>>();
    let result = fsa.accepts(input);
    println!("Input {} accepted: {}", line, result);
  }
  Ok(())
}
