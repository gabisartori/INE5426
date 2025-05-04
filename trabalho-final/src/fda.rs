use std::collections::{HashMap, HashSet};
use std::fs::File;
use std::io::{BufReader, BufRead, Read};
use std::error::Error;

use crate::{State, Symbol, Command, Token};

fn byte_vec_into_u32(vec: &Vec<u8>) -> u32 {
  let mut result = 0;
  for byte in vec.iter() {
    result *= 256;
    result += *byte as u32;
  }
  result
}

pub struct FDA {
  pub initial_state: State,
  pub transitions: HashMap<(State, Symbol), (State, Option<Command>)>,
  pub token_table: HashMap<State, Token>,
}

impl FDA {
  pub fn new(initial_state: State, transitions: HashMap<(State, Symbol), (State, Option<Command>)>, token_table: HashMap<State, Token>) -> FDA {

    FDA { initial_state, transitions, token_table }
  }

  pub fn from_file(file_path: &str) -> Result<FDA, Box<dyn Error>> {
    let file = File::open(file_path)?;
    let mut reader = BufReader::new(file);
    let mut _final_states: HashSet<u32> = HashSet::new();
    let mut transitions: HashMap<(State, Symbol), (State, Option<Command>)> = HashMap::new();

    // The first byte is the number of bytes per state
    // Hopefully no automaton will ever need more than 256 bytes to encode its states
    let mut buffer = [0u8; 1];
    reader.read_exact(&mut buffer)?;
    let state_size = buffer[0] as usize;
    
    // Next sequences of state_size bytes until [255]*state_size are the final states
    loop {
      let mut state_buffer = vec![0u8; state_size];
      reader.read_exact(&mut state_buffer)?;
      let state = byte_vec_into_u32(&state_buffer);
      if state == 255 { break; }
      _final_states.insert(state);
    }
    // Next groups of bytes are the transitions, in the format
    // (state, symbol, next_state). Each symbol is a single byte
    loop {
      let mut transition_buffer: Vec<u8> = vec![0u8; 2*state_size+1];
      match reader.read_exact(&mut transition_buffer) {
        Ok(_) => {
          let state = byte_vec_into_u32(&transition_buffer[..state_size].try_into().unwrap());
          let symbol = transition_buffer[state_size] as char;
          let next_state = byte_vec_into_u32(&transition_buffer[state_size+1..2*state_size+1].try_into().unwrap());
          let transition = next_state;
          let command: Option<Command> = None;
          transitions.insert((state, symbol), (transition, command));
        },
        Err(_) => break,
      }
    }
    
    // Read the token table
    let token_table_file = File::open("machines/lexer_table.automata")?;
    let reader = BufReader::new(token_table_file);
    let mut token_table = HashMap::new();
    for line in reader.lines() {
      let line = line?;
      let parts: Vec<&str> = line.split(':').collect();
      if parts.len() != 2 { return Err("Invalid token table format".into()); }
      let state = parts[0].parse::<u32>()?;
      let token = Token::from_str(parts[1])?;
      token_table.insert(state, token);
    }

    let fda = FDA::new(0, transitions, token_table);
    Ok(fda)
  }
}