# Minecraft Rust — canais de teste

Esta política vale para todas as builds Android distribuídas para teste.

## Identificação obrigatória

Toda build deve ter um canal, número sequencial e resumo verificável:

- **TESTE 01** — diagnóstico da interface atual e correção do sistema de localização.
- **ALPHA 01** — primeira versão do novo shell do launcher, com navegação própria.
- **ALPHA 02** — integração funcional das páginas e ações.
- **BETA 01** — fluxo completo de uso, persistência e regressão.
- **RELEASE** — somente após aprovação dos testes.

O nome do produto permanece **Minecraft Rust** em todos os idiomas e canais.

## Regra para publicar uma build

Uma APK não pode ser chamada de concluída apenas porque compilou. O artefato precisa incluir:

1. canal e número no nome do arquivo;
2. commit de origem e SHA-256;
3. lista de alterações e limitações conhecidas;
4. resultado de compilação;
5. checklist de testes funcionais executados.

Se um teste depende de um aparelho físico e não foi executado, deve aparecer como **não testado no dispositivo**, nunca como aprovado.

## Critérios mínimos para o sistema de idiomas

- Português (Brasil), Español e English;
- a seleção muda os textos de todas as páginas do launcher;
- a preferência permanece após fechar e abrir o aplicativo;
- textos dinâmicos, diálogos, mensagens de erro, botões e estados vazios também usam o idioma selecionado;
- identificadores técnicos, nomes de arquivos e o nome **Minecraft Rust** não são traduzidos.

## Critérios do launcher próprio

A interface será dividida em páginas e componentes próprios, com navegação e estado centralizados. Cada ação visual precisa chamar uma operação real do backend. Elementos ainda sem operação implementada devem aparecer como indisponíveis ou em desenvolvimento, nunca como botões falsamente funcionais.

## Histórico de testes

| Identificador | Estado | Objetivo |
|---|---|---|
| Build anterior (run 45) | Compilou; não validou localização completa no aparelho | UI parcial |
| TESTE 01 | Em desenvolvimento | Auditoria da localização e arquitetura do launcher |
| ALPHA 01 | Planejada | Novo shell e navegação |
