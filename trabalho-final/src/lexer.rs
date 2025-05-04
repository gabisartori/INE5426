use crate::fda::FDA;
use crate::token::Token;
use std::error::Error;


pub struct Lexer {
  pub fda: FDA
}

impl Lexer {
  pub fn new() -> Lexer {
    let fda = FDA::from_file("machines/lexer.automata").expect("Lexer automata file not found");
    Lexer { fda }
  }

  pub fn parse(&self, input: &str) -> Result<Vec<Token>, Box<dyn Error>> {
    let mut line_count = 1;
    let mut column_count = 0;
    let mut current_state = self.fda.initial_state;
    let mut token_list: Vec<Token> = vec![];
    let mut token_value = String::new();
    let mut string_or_char = false;
    for char in input.chars() {
      // Keep track of current position in the input
      if char == '\n' { line_count += 1; column_count = 0; } 
      else if char != '\n' { column_count += 1; }
      // Language only accepts uppercase letters inside of strings
      else if char == '"' || char == '\'' { string_or_char = !string_or_char; }
      let character = if !string_or_char && char.is_alphabetic() { char.to_ascii_lowercase() } else { char };
      
      // Process the character
      let next_state = self.fda.transitions.get(&(current_state, character));
      match next_state {
        // If the transition is valid, just update the state and the token value
        Some(next_state) => {
          current_state = *next_state;
          // Ignore empty spaces
          if !(character.is_whitespace()) { token_value.push(character); }
        },
        // If the transition is invalid, check if the current state is a final state
        // If it is, this means that a valid token was found
        // And the current symbol is the start of a possible new token
        // If it is not, this means that the token built until now is invalid and must be discarded
        None => {
          // If the current state is a final state, we have a valid token
          if self.fda.token_table.contains_key(&current_state) {
            let token_type = self.fda.token_table.get(&current_state).unwrap();
            let token = Token{
              token_type: *token_type,
              value: if token_type.has_value() {Some(token_value.clone())} else { None },
              line: line_count,
              column: column_count-token_value.len(),
            };
            token_list.push(token);
          }

          token_value.clear();
          // Now that the previous token is stored
          // Check if the current character is a valid start of a token
          // If it is, execute the transition
          // If it is not, return the lexical error and reset the state
          if let Some(next_state) = self.fda.transitions.get(&(self.fda.initial_state, character)) {
            current_state = *next_state;
            if !character.is_whitespace() { token_value.push(character); }
          } else {
            current_state = self.fda.initial_state;
            println!("Error: Invalid token at line {}, column {}: '{}'", line_count, column_count, character);
          }
        }
      }
    }
    // If the last token is valid, add it to the list
    if self.fda.token_table.contains_key(&current_state) {
      let token_type = self.fda.token_table.get(&current_state).unwrap();
      let token = Token{
        token_type: *token_type,
        value: if token_type.has_value() {Some(token_value.clone())} else { None },
        line: line_count,
        column: column_count-token_value.len(),
      };
      token_list.push(token);
    }
    // If the last token is not valid, return an error
    else if !token_value.is_empty() {
      println!("Error: Invalid token at line {}, column {}: '{}'", line_count, column_count, token_value);
    }
    Ok(token_list)
  }
}