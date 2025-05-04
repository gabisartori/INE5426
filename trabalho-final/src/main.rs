mod token;
mod fda;
mod lexer;

use lexer::Lexer;

type State = u32;
type Symbol = char;

fn main() -> Result<(), Box<dyn std::error::Error>> {
  // Read file containing test cases
  let args: Vec<String> = std::env::args().collect();
  if args.len() < 2 { return Err("Usage: <input_file>".into()); }
  let input_file = &args[1];
  let input = std::fs::read_to_string(input_file)?;

  // Run each test case
  for line in input.lines() {
    let lexer = Lexer::new();
    let token_list = lexer.parse(line)?;
    for token in token_list {
      println!("{}", token.to_string());
    }
    println!();
  }
  Ok(())
}
