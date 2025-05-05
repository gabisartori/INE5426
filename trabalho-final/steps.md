# Analisador Léxico
## Requisitos
- [x] Gerar lista de tokens
  - [x] Autômato para reconher qualquer token
  - [x] Tabela relacionando estados do autômato aos tokens
- [x] Gerar tabela de símbolos
  - [x] Tipo do token
  - [x] Valor do token
  - [x] Posição no código (linha, coluna)
- [x] O autômato criado automaticamente não está guardando referência para quais estados representam quais tokens, é preciso que essa informação seja atualizada sempre que os estados do autômato forem alterados por operações de união/determinização
## Adicionais
- [ ] Otimizar a função de transição do autômato finito com uma hash específica.
- [x] Substituir if por comandos retornados pelas transições; Os "comandos" foram substituídos pela classificação do token. A ação é sempre determinada pelo tipo do token que acaba de ser lido, logo a existência de comandos específicos para cada transição é desnecessária. Além disso, o único comando observado até o momento foi o de armazenar o valor do token lido junto do tipo. Acredito que no máximo do máximo será feita a distinção para decodificar constantes numéricas em vez de armazenar seus valores como strings.

# Analisador Sintático
## Requisitos
- [ ] Gerar árvore sintática

## Adicionais
- [ ] Usar a posição do token para notificar em que parte do código erros sintáticos acontecem

# Analisador Semântico
## Requisitos
- [ ] Não sei.

## Adicionais
- [ ] Usar a posição do token para notificar em que parte do código erros sintáticos acontecem
