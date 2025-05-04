mod token;
mod fda;

use token::Token;
use token::Command;
use fda::FDA;

type State = u32;
type Symbol = char;

fn main() -> Result<(), Box<dyn std::error::Error>> {
  // Read args
  let args: Vec<String> = std::env::args().collect();
  if args.len() < 2 { return Err("Usage: <input_file>".into()); }
  let input_file = &args[1];
  let input = std::fs::read_to_string(input_file)?;

  for line in input.lines() {
    let fsa = FDA::from_file("machines/lexer.automata")?;
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
          if fsa.token_table.contains_key(&current_state) {
            let token = fsa.token_table.get(&current_state).unwrap();
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
