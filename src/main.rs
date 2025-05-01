use std::collections::{HashSet, HashMap};

type State = u32;
type Symbol = char;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
enum Token {
  Id,
  ConstInt,
  ConstFloat,
  ConstString,
  ConstChar,
  ConstBool,
  LParenthesis,
  RParenthesis,
  LBracket,
  RBracket,
  LBrace,
  RBrace,
  Comma,
  Semicolon,
  KwInt,
  KwFloat,
  KwString,
  KwChar,
  KwBool,
  KwIf,
  KwElif,
  KwElse,
  KwWhile,
  KwFor,
  KwBreak,
  KwContinue,
  KwReturn,
  KwDef,
  KwPrint,
  KwRead,
  OpAssign,
  OpEq,
  OpNe,
  OpGt,
  OpGe,
  OpLt,
  OpLe,
  OpAnd,
  OpOr,
  OpXor,
  OpNot,
  OpBitAnd,
  OpBitOr,
  OpBitXor,
  OpBitNot,
  OpPlus,
  OpMinus,
  OpMul,
  OpDiv,
  OpWholeDiv,
  OpMod,
  OpPow,
}

enum Command {
  Push
}

const S0: State = 0;
const RETURN0: State = 1;
const RETURN1: State = 2;
const RETURN2: State = 2;
const RETURN3: State = 3;
const RETURN4: State = 4;
const RETURN5: State = 5;
const IF0: State = 6;
const IF1: State = 7;
const SEMICOLON: State = 8;


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

  fn _accepts(&self, input: Vec<Symbol>) -> bool {
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

  for line in input.lines() {
    let initial_state = S0;
    let final_states = HashSet::from([S0]);
    let token_table: HashMap<State, Token> = HashMap::from([
      (RETURN5, Token::KwReturn),
      (IF1, Token::KwIf),
      (SEMICOLON, Token::Semicolon),
    ]);
    let transitions = HashMap::from([
      ((S0, ' '), (S0, None)),
      ((S0, '\n'), (S0, None)),
      ((S0, '\t'), (S0, None)),
      ((S0, 'r'), (RETURN0, None)),
      ((RETURN0, 'e'), (RETURN1, None)),
      ((RETURN1, 't'), (RETURN2, None)),
      ((RETURN2, 'u'), (RETURN3, None)),
      ((RETURN3, 'r'), (RETURN4, None)),
      ((RETURN4, 'n'), (RETURN5, None)),
      ((S0, 'i'), (IF0, None)),
      ((IF0, 'f'), (IF1, None)),
      ((S0, ';'), (SEMICOLON, None)),
      ]);

    let fsa = FSDA::new(initial_state, final_states, transitions);
    let input = (line.to_string() + "#").chars().collect::<Vec<_>>();
    let mut token_list: Vec<Token> = vec![];
    
    let mut i = 0;
    let mut token_value = String::new();
    let mut current_state = fsa.initial_state;
    while i < input.len() {
      // Reads the next symbol
      let symbol = &input[i];
      let next_state = fsa.transitions.get(&(current_state, *symbol));

      // Check the transition caused by the symbol
      match next_state {
        // If the transition is valid, just update the state and the token value
        // The command is not used in this example, but it could be used to perform actions
        Some((next_state, _command)) => {
          current_state = *next_state;
          // Ignore empty spaces
          if !(symbol.is_whitespace()) { token_value.push(*symbol); }
        },
        // If the transition is invalid, check if the current state is a final state
        // If it is, this means that a valid token was found
        // And the current symbol is the start of a possible new token
        // If it is not, this means that the token built until now is invalid and must be discarded
        None => {
          // If the current state is a final state, we have a valid token
          if token_table.contains_key(&current_state) {
            let token = token_table.get(&current_state).unwrap();
            token_list.push(token.clone());
            println!("Value: '{}'", token_value);
          }

          token_value.clear();
          if let Some((next_state, _command)) = fsa.transitions.get(&(fsa.initial_state, *symbol)) {
            current_state = *next_state;
            if !symbol.is_whitespace() { token_value.push(*symbol); }
          } else {
            current_state = fsa.initial_state;
            println!("Error: Invalid token at position {}: '{}'", i, symbol);
          }
        }
      }
      i += 1;
    }
    println!("Token list: {:?}\n", token_list);
  }
  Ok(())
}
