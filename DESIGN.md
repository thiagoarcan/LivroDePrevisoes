---
name: Caderno de Previsões Operacionais em Dutos
description: Console operacional local em grafite e verde mineral
colors:
  primary: "#1c7460"
  primary-hover: "#175e4e"
  primary-text: "#ffffff"
  app: "#101719"
  surface: "#192326"
  navigation: "#141e20"
  surface-hover: "#233236"
  surface-active: "#2c4145"
  text: "#f0f5f3"
  text-secondary: "#c0ceca"
  text-muted: "#a8bdb6"
  border: "#657d75"
  divider: "#364a43"
  focus: "#84d8c2"
  info: "#99dfcc"
  success: "#237245"
  danger: "#b92e3d"
  warning: "#f3bd53"
  warning-text: "#201700"
  light-app: "#f0f3ef"
  light-surface: "#ffffff"
  light-navigation: "#e7eee8"
  light-text: "#1b3029"
  light-primary: "#17664f"
  light-divider: "#cddbd3"
  industrial-app: "#000000"
  industrial-surface: "#101010"
  industrial-text: "#ffffff"
  industrial-primary: "#ffdb44"
typography:
  headline:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "clamp(1.35rem,1.1rem + .6vw,1.85rem)"
    fontWeight: 650
    lineHeight: 1.25
    letterSpacing: "-.025em"
  title:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "1.075rem"
    fontWeight: 650
    letterSpacing: "-.015em"
  body:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "1rem"
    lineHeight: 1.45
  label:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: ".875rem"
    fontWeight: 600
  metric:
    fontFamily: "'Segoe UI', system-ui, sans-serif"
    fontSize: "1.65rem"
    fontWeight: 650
    lineHeight: 1.15
    letterSpacing: "-.035em"
rounded:
  input: "6px"
  button: "7px"
  compact-panel: "8px"
  fieldset: "10px"
  panel: "12px"
  dialog: "14px"
spacing:
  field-gap: ".5rem"
  grid-gap: "1rem"
  panel-padding: "1.25rem"
  section: "1.5rem"
components:
  button-primary:
    backgroundColor: "{colors.primary}"
    textColor: "{colors.primary-text}"
    rounded: "{rounded.button}"
    padding: ".55rem .9rem"
  button-primary-hover:
    backgroundColor: "{colors.primary-hover}"
  panel:
    backgroundColor: "{colors.surface}"
    textColor: "{colors.text}"
    rounded: "{rounded.panel}"
    padding: "1.25rem"
---

# Design System: Caderno de Previsões

## Overview

**Creative North Star: "Console operacional"**

Superfícies planas em grafite e verde mineral organizam uma ferramenta de trabalho contínuo. O contraste entre navegação, trabalho e contexto estabelece hierarquia sem imagens decorativas. A linguagem foi extraída do código entregue, sob a autorização de execução autônoma registrada em PRODUCT.md.

**Key Characteristics:**

- Hierarquia por tom, espaçamento e peso tipográfico.
- Controles locais, legíveis e operáveis sem recursos remotos.
- Estados operacionais acompanhados de texto.
- Composição adaptativa com prioridade para a atividade em curso.

## Colors

### Primary

O verde mineral identifica ações primárias; seu tom claro identifica foco e informação no tema escuro. O tema claro usa verde mais profundo. O tema industrial usa amarelo sobre superfícies pretas e preserva sua função de alto contraste.

### Neutral

Grafite no fundo, superfície ligeiramente elevada e navegação mais escura separam regiões. Divisores discretos organizam conteúdo; bordas de controles usam um tom mais visível.

**The Semantic State Rule.** Cores de prazo, alarme e conclusão mantêm nomes textuais; a cor não substitui a situação operacional.

## Typography

A família local Segoe UI, com fallback de sistema, é intencional para operação offline e ergonomia de aplicativo. Não há fonte display decorativa. Títulos, corpo e controles compartilham a mesma família, com os papéis registrados no frontmatter.

Títulos de tela são fluidos, com tratamento específico no celular (1.4rem). Números de métricas, relógio, contagens e tabelas usam algarismos tabulares. Painéis contextuais limitam parágrafos a 75ch; descrições do destaque também têm limite de leitura.

**The Local Type Rule.** A tipografia não introduz requisições de rede nem depende de fonte remota.

## Layout

A navegação desktop ocupa uma lateral de 232px e o cabeçalho permanece no topo. A altura real do cabeçalho é acompanhada pelo controlador, mantendo deslocamentos coerentes. O conteúdo usa largura disponível com margens fluidas; tabelas extensas têm rolagem dentro de sua região.

O modo automático distingue celular, tablet, convencional, widescreen e ultrawide. Abaixo de 768px, a composição vira coluna, a navegação inferior oferece quatro destinos e menus abrem recursos complementares. Inputs móveis têm altura mínima de 48px. Em tablet paisagem com largura a partir de 1000px, a lateral reduz para um trilho de 80px. A partir de 1920px e 2560px, o painel apresenta regiões simultâneas de trabalho e contexto. Entre 1400px e 1919px, indicadores do painel convencional ocupam sete colunas.

Áreas seguras, teclado virtual, redimensionamento e orientação têm regras específicas. O tamanho físico estreito prevalece sobre modos manuais incompatíveis. Formulários usam grids flexíveis; a ação de salvar permanece acessível no celular.

## Elevation & Depth

O sistema é plano por padrão, com tonalidade e bordas finas. Diálogos usam sombra ampla e deslocada; a navegação inferior móvel usa sombra discreta para separação do conteúdo. Alarmes possuem estados próprios; não transformar esses tratamentos em decoração genérica.

**The Working Surface Rule.** Profundidade comunica sobreposição ou separação funcional, não adorna cada painel.

## Shapes

Os raios variam por função: controles pequenos, campos, grupos e painéis seguem os tokens registrados. Diálogos possuem cantos mais suaves. Badges de estado são compactos; contadores de navegação usam cantos discretos. Elementos flexíveis permitem quebra de texto sem cortar ações.

## Components

Botões têm altura mínima de 44px, preenchimento compacto, peso 650 e foco visível. O primário usa verde; sucesso, perigo e aviso preservam semântica própria. O secundário usa superfície de hover; o contornado mantém borda legível. Estados de pressionamento deslocam o botão em 1px. Transições de cor e borda duram 160ms, respeitando movimento reduzido.

Inputs usam fundo da aplicação, borda de controle e mudança de borda ao receber foco. Labels permanecem visíveis. A regra global de foco usa contorno de 3px e deslocamento de 3px.

Painéis de trabalho usam a superfície principal; painéis contextuais usam o tom de navegação. Tabelas usam cabeçalhos menores, linhas alternadas discretas e números tabulares. A navegação ativa tem preenchimento tonal e peso maior, sem depender exclusivamente de hover.

O próximo evento recebe descrição proeminente, situação textual, contagem tabular e ações existentes. Ícones novos são SVG Lucide incorporados com licença; não exigem carregamento externo.

## Do's and Don'ts

### Do:

- **Do** preservar ações e conteúdo ao reorganizar a interface para outra largura.
- **Do** usar tokens semânticos nos três temas.
- **Do** manter foco visível, labels e estados textuais.
- **Do** incorporar recursos necessários ao HTML distribuído.

### Don't:

- **Don't** adicionar fontes remotas, CDN ou serviços obrigatórios.
- **Don't** alterar cálculos ou persistência para obter um resultado visual.
- **Don't** usar cor como única indicação de estado.
- **Don't** transformar tratamentos específicos de alarmes em estilo decorativo global.
