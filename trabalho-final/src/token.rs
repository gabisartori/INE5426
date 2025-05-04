use std::error::Error;

#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum TokenType {
  ConstChar,
  ConstBool,
  ConstNull,
  Lparenthesis,
  Rparenthesis,
  Lbracket,
  Rbracket,
  Rbrace,
  Lbrace,
  Semicolon,
  Comma,
  VarType,
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
  OpBitwiseAnd,
  OpBitwiseOr,
  OpBitwiseXor,
  OpBitwiseNot,
  OpLBitshift,
  OpRBitshift,
  OpPlus,
  OpMinus,
  OpMult,
  OpDivision,
  OpWholeDivision,
  OpModular,
  OpPow,
  Id,
  ConstInt,
  ConstFloat,
  ConstString,
}

impl TokenType {
  pub fn from_str(s: &str) -> Result<TokenType, Box<dyn Error>> {
    match s {
      "const_char" => Ok(TokenType::ConstChar),
      "const_bool" => Ok(TokenType::ConstBool),
      "const_null" => Ok(TokenType::ConstNull),
      "lparenthesis" => Ok(TokenType::Lparenthesis),
      "rparenthesis" => Ok(TokenType::Rparenthesis),
      "lbracket" => Ok(TokenType::Lbracket),
      "rbracket" => Ok(TokenType::Rbracket),
      "rbrace" => Ok(TokenType::Lbrace),
      "lbrace" => Ok(TokenType::Rbrace),
      "semicolon" => Ok(TokenType::Semicolon),
      "comma" => Ok(TokenType::Comma),
      "var_type" => Ok(TokenType::VarType),
      "kw_if" => Ok(TokenType::KwIf),
      "kw_elif" => Ok(TokenType::KwElif),
      "kw_else" => Ok(TokenType::KwElse),
      "kw_while" => Ok(TokenType::KwWhile),
      "kw_for" => Ok(TokenType::KwFor),
      "kw_break" => Ok(TokenType::KwBreak),
      "kw_continue" => Ok(TokenType::KwContinue),
      "kw_return" => Ok(TokenType::KwReturn),
      "kw_def" => Ok(TokenType::KwDef),
      "kw_print" => Ok(TokenType::KwPrint),
      "kw_read" => Ok(TokenType::KwRead),
      "op_assign" => Ok(TokenType::OpAssign),
      "op_eq" => Ok(TokenType::OpEq),
      "op_ne" => Ok(TokenType::OpNe),
      "op_gt" => Ok(TokenType::OpGt),
      "op_ge" => Ok(TokenType::OpGe),
      "op_lt" => Ok(TokenType::OpLt),
      "op_le" => Ok(TokenType::OpLe),
      "op_and" => Ok(TokenType::OpAnd),
      "op_or" => Ok(TokenType::OpOr),
      "op_xor" => Ok(TokenType::OpXor),
      "op_not" => Ok(TokenType::OpNot),
      "op_bitwise_and" => Ok(TokenType::OpBitwiseAnd),
      "op_bitwise_or" => Ok(TokenType::OpBitwiseOr),
      "op_bitwise_xor" => Ok(TokenType::OpBitwiseXor),
      "op_bitwise_not" => Ok(TokenType::OpBitwiseNot),
      "op_l_bitshift" => Ok(TokenType::OpLBitshift),
      "op_r_bitshift" => Ok(TokenType::OpRBitshift),
      "op_plus" => Ok(TokenType::OpPlus),
      "op_minus" => Ok(TokenType::OpMinus),
      "op_mult" => Ok(TokenType::OpMult),
      "op_division" => Ok(TokenType::OpDivision),
      "op_whole_division" => Ok(TokenType::OpWholeDivision),
      "op_modular" => Ok(TokenType::OpModular),
      "op_pow" => Ok(TokenType::OpPow),
      "id" => Ok(TokenType::Id),
      "const_int" => Ok(TokenType::ConstInt),
      "const_float" => Ok(TokenType::ConstFloat),
      "const_string" => Ok(TokenType::ConstString),
      _ => Err(format!("Invalid TokenType: {}", s).into()),
    }
  }

  pub fn has_value(&self) -> bool {
    match self {
      TokenType::ConstChar | TokenType::ConstBool | TokenType::ConstInt | TokenType::ConstFloat | TokenType::ConstString | TokenType::Id | TokenType::VarType => true,
      _ => false,
    }
  }
}

#[derive(Debug, Clone)]
pub struct Token {
  pub token_type: TokenType,
  pub value: Option<String>,
  pub line: usize,
  pub column: usize,
}

impl Token {
  pub fn to_string(&self) -> String {
    let value_str = match &self.value {
      Some(value) => format!("'{}'", value),
      None => String::new(),
    };
    format!("Token {{ type: {:?}, value: {}, line: {}, column: {} }}", self.token_type, value_str, self.line, self.column)
  }
}

pub enum Command {
  Push
}