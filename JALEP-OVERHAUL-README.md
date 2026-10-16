# JALEP Mano — UI Overhaul

Camada visual adicional para a exportação estática existente. Não substitui o conteúdo original.

## O que acrescenta
- foco de teclado mais visível e link para pular ao conteúdo;
- barra de progresso de leitura;
- botão acessível de voltar ao topo;
- menu móvel fecha com Escape e ao escolher um link;
- indicação `aria-current="page"` na navegação;
- ajustes responsivos e respeito a `prefers-reduced-motion`;
- backup automático antes de modificar HTML.

## Pré-visualização
Execute `./run-local.sh` na pasta `jalep-mano` e abra o endereço mostrado.

## Segurança
O script não faz commit nem push. Revise `git diff` antes de publicar. O backup fica em `.backup-jaLEP-overhaul-<data>/`.
