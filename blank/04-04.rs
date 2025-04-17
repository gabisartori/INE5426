use std::collections::HashMap;

enum State {
  S = 0,
  C = 1
}

enum Command {
  NOTHING = 0,
  APPEND = 1,
  PUSH = 2
}

const EXEMPLO : &str = "def f(int x) {\n\tif x < 0\n\t\tx = -x;\n\treturn;\n}";

fn transition(state: State, char: char) -> (State, Command) {
  match state {
    State::S => {
      if char.is_alphabetic() { (State::C, Command::APPEND) } 
      else if char.is_whitespace() { (State::S, Command::NOTHING) } 
      else { (State::S, Command::NOTHING) }
    },
    State::C => {
      if char.is_alphabetic() || char.is_digit(10) { (State::C, Command::APPEND) } 
      else if char.is_whitespace() { (State::S, Command::PUSH) } 
      else { (State::S, Command::PUSH) }
    }
  }
}

fn main() {
  let mut state = State::S;
  let mut output: HashMap<String, Vec<i32>> = HashMap::new();
  let mut current_line = 1;
  let mut current_token = String::new();
  for char in EXEMPLO.chars() {
    if char == '\n' { current_line += 1; }
    let (new_state, command) = transition(state, char);
    state = new_state;
    match command {
      Command::NOTHING => {},
      Command::APPEND => { current_token.push(char); },
      Command::PUSH => {
        if current_token.is_empty() { break; }
        let entry = output.entry(current_token.clone()).or_insert(vec![]);
        if entry.last().unwrap_or(&0) != &current_line { entry.push(current_line); }
        current_token.clear();
      }
    }
  }
  let mut output: Vec<_> = output.into_iter().collect();
  output.sort_by(|a, b| a.0.cmp(&b.0));
  for (key, value) in &output {
    println!("{}: {:?}", key, value);
  }
}