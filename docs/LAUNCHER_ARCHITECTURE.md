# Minecraft Rust — arquitetura do launcher próprio

## Decisão técnica

O cliente Android atual usa uma interface nativa desenhada em Rust pelo próprio renderer do aplicativo. Não é uma página web nem uma Activity Kotlin com telas independentes. Por isso, a primeira implementação do launcher próprio deve continuar na camada Android Rust e reaproveitar o ciclo de vida, o renderer e os serviços do cliente.

Não vamos reescrever o motor do jogo para trocar o launcher.

## Separação de camadas

1. **Shell visual** — estrutura responsiva, barra lateral, cabeçalho, área de conteúdo, navegação e sistema de temas.
2. **Páginas** — Início/Jogar, Instalações, Mods, Shaders, Texturas, Skins e Configurações.
3. **Componentes** — cartões, botões, seletores, listas, diálogos, miniaturas e estados vazios.
4. **Estado e navegação** — uma rota atual, estado de cada página, foco/seleção, carregamento e mensagens.
5. **Localização** — chaves de tradução centralizadas para pt-BR, es e en; nenhum texto de tela deve ser traduzido isoladamente dentro de cada widget.
6. **Adaptadores de ações** — conectam cada botão às operações já existentes de instalação, importação, contas, arquivos, catálogo e configurações.

## Regra de integração

A interface não deve fingir que uma ação existe. Cada botão precisa chamar um adaptador real e apresentar carregamento, sucesso ou erro. Se uma operação ainda não estiver implementada no motor, o controle deve estar claramente marcado como indisponível/em desenvolvimento.

## Plano de implementação

### TESTE 01 — auditoria e localização
- mapear todas as strings visíveis, inclusive diálogos, avisos, erros, tooltips e estados vazios;
- criar catálogo de traduções centralizado;
- verificar que a escolha de idioma atualiza todas as páginas e sobrevive ao reinício;
- manter **Minecraft Rust** sem tradução.

### ALPHA 01 — novo shell
- criar layout raiz independente do desenho atual das páginas;
- barra lateral e área de conteúdo com coordenadas relativas ao conteúdo, não à janela inteira;
- navegação e estado centralizados;
- página inicial com hierarquia visual inspirada no launcher oficial, usando arte e ícones originais.

### ALPHA 02 — páginas funcionais
- integrar Instalações, Mods, Shaders, Texturas e Skins;
- miniaturas e metadados reais;
- importação, ativação, remoção e seleção ligadas ao backend existente.

### BETA 01 — validação
- testes de toque, rolagem, teclado, orientação retrato/paisagem e persistência;
- teste de todos os idiomas em todas as páginas;
- checklist em aparelho físico antes de marcar a versão como aprovada.

## Fora de escopo da troca visual

A reformulação do launcher não deve alterar renderização do jogo, FPS, drivers Vulkan/Turnip ou desempenho. Essas mudanças precisam de testes separados.
