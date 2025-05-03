# Analisador Léxico
## Requisitos
- [x] Gerar lista de tokens
- [ ] Gerar tabela de símbolos
  - [ ] Tipo do token
  - [ ] Valor do token
  - [ ] Posição no código (linha, coluna)
- [ ] O autômato criado automaticamente não está guardando referência para quais estados representam quais tokens, é preciso que essa informação seja atualizada sempre que os estados do autômato forem alterados por operações de união/determinização
## Adicionais
- [ ] Otimizar a função de transição do autômato finito com uma hash específica.
- [ ] Substituir if por comandos retornados pelas transições

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
