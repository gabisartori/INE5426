class CFG:
  def __init__(self) -> None:
    self.rules: dict[str, list[str]] = {}
    self.rules_order: list[str] = []
    self.first: dict[str, set[str]] = {}
    self.follow: dict[str, set[str]] = {}
    self.start: str = ""
    self.first_follow()

  def first_follow(self) -> None:
    # First
    for rule in self.rules_order[::-1]:
      if self.first.get(rule) is None: self.first[rule] = set()
      self.first[rule].update(self.body_first(rule))

    # Follow
    self.follow[self.start] = {"$"}
    for rule in self.rules_order:
      if self.follow.get(rule) is None: self.follow[rule] = set()
      self.follow[rule].update(self.head_follow(rule))

  def body_first(self, body: str, visited=None) -> set[str]:
    if visited is None: visited = set()
    first = set()
    for symbol in body:
      if symbol == "": return first.union({""})
      if self.is_terminal(symbol): return first.union({symbol})
      if symbol in visited: continue

      visited.add(symbol)
      if self.first.get(symbol) and "" not in self.first[symbol]: return first.union(self.first[symbol]) 
      other_bodies = self.rules[symbol] if self.rules.get(symbol) is not None else []
      for other_body in other_bodies:
        first.update(self.body_first(other_body, visited))

    return first

  def head_follow(self, rule: str) -> set[str]:
    follow = set()
    for other_rule in self.rules:
      for body in self.rules[other_rule]:
        # Check if non-terminal is in the body of this other rule and store its index
        try: index = body.index(rule)
        except ValueError: continue
        while True:
          if index == len(body) - 1:
            tmp = self.follow[other_rule] if self.follow.get(other_rule) is not None else self.head_follow(other_rule)
            follow.update(tmp)
            break
          elif self.is_terminal(body[index+1]):
            follow.update(body[index+1])
            break
          else:
            rule_first = self.first[body[index+1]]
            follow.update(rule_first)
            if "" not in rule_first: break
            index += 1
    if "" in follow: follow.remove("")
    return follow

  def get_rule_id(self, variable: str, body: str) -> int:
    id = 1
    for rule in self.rules_order:
      for b in self.rules[rule]:
        if rule == variable and b == body:
          return id
        id += 1
    raise ValueError("Rule not found")

  def is_ll1(self):
    if self.is_left_recursive():
      print("Recursão à esquerda")
      return False
    if self.is_non_deterministic():
      print("Não determinismo")
      return False
    return True
  
  def is_left_recursive(self) -> bool:
    return any([self.is_rule_recursive(rule) for rule in self.rules_order])

  def is_rule_recursive(self, rule: str) -> bool:
    return any([self.body_starts_with_rule(rule, body) for body in self.rules[rule]])
  
  def body_starts_with_rule(self, rule: str, body: str, visited=None) -> bool:
    if visited is None: visited = set()
    for symbol in body:
      if symbol == "": return False
      if self.is_terminal(symbol): return False
      if symbol == rule:
        print(rule, body)
        return True
      if symbol in visited: continue
      visited.add(symbol)
      for other_body in self.rules[symbol]:
        if self.body_starts_with_rule(rule, other_body, visited):
          print(rule, body)
          return True
      if "" not in self.first[symbol]: return False
    return False

  def is_non_deterministic(self):
    for rule in self.rules:
      for i, body in enumerate(self.rules[rule]):
        for j, other_body in enumerate(self.rules[rule]):
          if i == j: continue
          if self.body_first(body).intersection(self.body_first(other_body))-{""}:
            return True
    return False

  def ll1_parser_table(self):
    if not self.is_ll1(): raise ValueError("This grammar is not LL(1)")
    table = []
    self.first_follow()
    for rule in self.rules_order:
      for body in self.rules[rule]:
        first = self.body_first(body)
        for symbol in first:
          if symbol == "":
            for follow in self.follow[rule]:
              table.append([rule, follow, self.get_rule_id(rule, body)])
          else:
            table.append([rule, symbol, self.get_rule_id(rule, body)])
    return table

  def table_string(self, table:list[list[str]]):
    order = lambda x: ord(x) if x.isalpha() else ord(x) + ord("z")
    table.sort(key=lambda x: x[2])
    table.sort(key=lambda x: order(x[1]))
    table.sort(key=lambda x: x[0])
    
    states = f"{{{','.join(sorted(self.rules_order))}}}"
    initial_state = self.start
    alphabet = f"{{{','.join(sorted(set([x[1] for x in table]), key=lambda x: order(x)))}}}"
    transitions = "".join([f"[{state},{read},{reduce}]" for state, read, reduce in table])
    output = f"{states};{initial_state};{alphabet};{transitions}"
    return output

  def first_follow_string(self) -> str:
    order = lambda x: ord(x) if x.isalpha() else ord(x) + ord("z")
    first = '; '.join([f"First({rule}) = {{{', '.join(sorted(self.first[rule], key=lambda x: order(x)))}}}" for rule in self.rules_order])
    follow = '; '.join([f"Follow({rule}) = {{{', '.join(sorted(self.follow[rule], key=lambda x: order(x)))}}}" for rule in self.rules_order])
    return f"{first}; {follow}"
  
  def __str__(self) -> str:
    return self.string

  @staticmethod
  def is_terminal(symbol: str) -> bool:
    return (not symbol.isupper() or symbol == "") and symbol != "$"


if __name__ == "__main__":
  cfg = CFG()
  cfg.rules = {
    "S": ["A+S", "A"],
    "A": ["B*A", "B"],
    "B": ["(S)", "1"],
  }
  cfg.rules_order = ["S", "A", "B", "C"]
  cfg.start = "S"
  print(cfg.first, cfg.follow)
  print(cfg.ll1_parser_table())