enum State {
  S = 0,
  C = 1
}

const EXEMPLO : &str = "def f(int a) {\n\tx = x + a;\n\treturn;\n}";

fn transition(state: State, char: char) -> (State, String) {
  match state {
    State::S => {
      if char.is_alphabetic() { (State::C, String::from("")) } 
      else if char.is_whitespace() { (State::S, String::from(char)) } 
      else { (State::S, String::from("OUTRO")) }
    },
    State::C => {
      if char.is_alphabetic() || char.is_digit(10) { (State::C, String::from("")) } 
      else if char.is_whitespace() { (State::S, String::from("IDENT") + &String::from(char)) } 
      else { (State::S, String::from("IDENT OUTRO")) }
    }
  }
}

fn main() {
  let mut state = State::S;
  let mut output = String::new();
  for char in EXEMPLO.chars() {
    let (new_state, command) = transition(state, char);
    state = new_state;
    if !(output.chars().last().unwrap_or(' ').is_whitespace() || command.chars().next().unwrap_or(' ').is_whitespace()) {
      output = format!("{} {}", output, command);
    } else {
      output = format!("{}{}", output, command);
    }
  }
  println!("{}", output);

  // Ok(())
}