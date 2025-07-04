use std::collections::HashMap;
use std::error::Error;

use crate::grammar::token_type::TokenType;

type State = u32;
type Symbol = char;

fn byte_vec_into_u32(vec: &[u8]) -> u32 {
  let mut result = 0;
  for byte in vec.iter() {
    result *= 256;
    result += *byte as u32;
  }
  result
}

pub struct FDA {
  pub initial_state: State,
  pub transitions: HashMap<(State, Symbol), State>,
  pub token_table: HashMap<State, TokenType>,
}

impl FDA {
  pub fn new(initial_state: State, transitions: HashMap<(State, Symbol), State>, token_table: HashMap<State, TokenType>) -> FDA {

    FDA { initial_state, transitions, token_table }
  }

  pub fn from_file() -> Result<FDA, Box<dyn Error>> {
    // /machines/lexer.automata precisa existir durante a compilação do projeto
    // O mesmo vale para /machines/lexer_table.automata
    let raw_bytes = include_bytes!("../machines/lexer.automata");
    let mut transitions: HashMap<(State, Symbol), State> = HashMap::new();

    // O primeiro byte do arquivo contém o tamanho do estado em bytes
    // Espera-se que nenhum autômato tenha mais do que 2^256 estados, então o tamanho do estado é limitado a 256 bytes
    let state_size = raw_bytes[0] as usize;
    // Próximos bytes são as transições, no formato
    // (estado, símbolo, próximo_estado). Cada símbolo é um único byte
    let mut i = 1;
    while i < raw_bytes.len() {
      let Some(transition) = raw_bytes.get(i..i+2*state_size+1) else { break; };
      let state = byte_vec_into_u32(&transition[..state_size]);
      let symbol = transition[state_size] as char;
      let next_state = byte_vec_into_u32(&transition[state_size+1..2*state_size+1]);
      let transition = next_state;
      transitions.insert((state, symbol), transition);
      i += 2*state_size + 1;
    }
    
    // Read the token table
    let token_table_content = include_str!("../machines/lexer_table.automata");
    let mut token_table = HashMap::new();
    for line in token_table_content.lines() {
      let parts: Vec<&str> = line.split(':').collect();
      if parts.len() != 2 { return Err("Invalid token table format".into()); }
      let state = parts[0].parse::<u32>()?;
      let token = TokenType::from_str(parts[1])?;
      token_table.insert(state, token);
    }

    let fda = FDA::new(0, transitions, token_table);
    Ok(fda)
  }

  /// Retorna o próximo estado dado o estado atual e o símbolo lido.
  /// Essa função segue uma lógica de camadas (apesar de que apenas uma camada foi utilizada)
  /// A ideia é que existem grupos de símbolos, cada um com o seu nível de prioridade.
  /// Cada transição é uma sequência de tentativas para cada nível de símbolos.
  /// O mais prioritário é o símbolo específico, caso a transição (estado, símbolo) não exista, busca-se uma transição no pŕoximo nível.
  /// Para o pŕoximo nível é usado o caracter '\x00', que representa um wildcard, ou seja, qualquer símbolo.
  /// Após verificar todos os níveis, se nenhuma transição for encontrada então a transição é inválida.
  /// Inicialmente essa função foi pensada para utilizar várias camadas, por exemplo: letra específica, conjunto de letras/números, wildcard.
  /// Porém, isso seria incompatível com o algoritmo de determinização existente, que não identificaria uma transição por letra genérica e por letra específica como sendo não determinismo.
  pub fn transition(&self, state: State, symbol: Symbol) -> Option<&State> {
    if self.transitions.contains_key(&(state, symbol)) { self.transitions.get(&(state, symbol)) }
    // Group transitions: If the specific character doesn't have a transition, check if there's a transition for a group in which the character belongs
    // Yeah for now there are no groups and I'm not sure if there'll ever be any.
    // If the all groups above failed, check for the wildcard symbol. It skips any check and just runs the transition for whatever symbol it has read
    else if self.transitions.contains_key(&(state, '\x00')) { self.transitions.get(&(state, '\x00')) }
    else { None }
  }
}