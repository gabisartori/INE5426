mod token;
mod fda;
mod lexer;

use lexer::Lexer;

type State = u32;
type Symbol = char;

fn main() -> Result<(), Box<dyn std::error::Error>> {
  // Read the file to be compiled from command line arguments
  let args: Vec<String> = std::env::args().collect();
  if args.len() < 2 { return Err("Usage: <input_file>".into()); }
  let input_file = &args[1];
  let input = std::fs::read_to_string(input_file)?;

  // Run each test case
  let lexer = Lexer::new();
  let token_list = lexer.parse(&input)?;
  for token in token_list {
    println!("{}", token.to_string());
  }

  Ok(())
}
