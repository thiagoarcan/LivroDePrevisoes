# Auditoria das referências visuais

Inspeção somente leitura dos três PDFs renderizados e imagens Designer adicionais, seguida de leitura de parts_html.py, parts_css.py e requisitos_extraidos.txt. A versão final confronta presença estrutural com capturas reais produzidas pelo auditor principal.

## Inventário conferido

- **Designer.pdf**, página 1: seis fluxos celulares (painel, pendentes, nova previsão, alarme, filtros e drawer) e dois tablets (painel em paisagem e lista/detalhe).
- **Designer (1).pdf**, página 1: três temas, Controle escuro, Profissional claro e Industrial alto contraste. Cada coluna demonstra painel celular/tablet, pendentes e formulário.
- **Designer (2).pdf**, página 1: monitor convencional, widescreen e ultrawide. Contém navegação lateral fixa, dashboard e regiões coordenadas. A prancha apresenta exemplos 1920×1080, 2560×1080 e ultrawide rotulado com resolução inconsistente; a intenção de composição prevalece sobre o número ilustrativo.
- As três renderizações têm tamanho 1600×1067 e **hashes de arquivo e de pixels distintos**. Não são duplicatas. Valores integrais no inventario_referencias.json.
- **Designer (1).png e Designer (2).png são duplicatas binárias exatas**, mostrando fluxos celulares/tablets. Seus nomes não correspondem à temática dos PDFs com mesmo sufixo; não podem substituí-los.
- **Designer (3).png e Designer.jpg** mostram a prancha dos três temas, com codificações diferentes. Foram examinados visualmente; não foi presumida identidade binária.
- **Designer.jpeg** mede 452×301 e é completamente branco: extremos RGB (255,255) em todos os canais. Não oferece referência visual utilizável.

## Critério de fidelidade

DOCX P0011-P0013 define wireframes como comportamentos de referência, não telas fixas. Portanto não se exige reprodução pixel a pixel, texto ilustrativo deformado, carcaças de dispositivos ou ícones idênticos. Exige-se conservar hierarquia, distribuição, navegação, prioridade operacional e reorganização por espaço disponível. DOCX P0023-P0025 especifica lateral fixa em monitor, painéis simultâneos em wide e regiões paralelas em ultra. Os três temas são referência visual explícita da prancha Designer (1).pdf; o DOCX menciona alternância de tema e acessibilidade, sem definir valores hexadecimais obrigatórios.

## Avaliação de estrutura e composição

Existe um sistema de superfícies, badges, cartões, tabelas e três temas coerente com a linguagem geral das pranchas. A aplicação contém estruturas específicas para cartão móvel, filtro inferior, alarmes em tela cheia, grade de métricas e lista/detalhe tablet. Isso demonstra implementação parcial da reorganização, sem comprovar que todos os fluxos funcionam ou cabem na tela.

As maiores divergências estruturais estão no desktop: navegação horizontal em lugar de lateral fixa; modo convencional sem painel lateral de alarmes; widescreen sem gráfico e três regiões simultâneas; ultrawide sem dashboard coordenado contendo lista, detalhe, métricas/gráficos e ações rápidas. Alargar o container não produz a composição demonstrada nas referências.

No celular há incompatibilidade objetiva de nomes de classes da barra inferior entre HTML e CSS. O cabeçalho continua com vários grupos e controles, enquanto a referência concentra a operação em barra compacta. A faixa de alarme usa deslocamento sticky fixo de 52px apesar da altura variável do cabeçalho. A hierarquia do spotlight existe, porém o contador é colocado abaixo da descrição em uma coluna em vez de junto ao estado no topo.

Os temas possuem tokens próprios, mas cores fixas ou inline de relógio, navegação e métricas podem comprometer a coerência do claro/industrial. A presença dos tokens não equivale à validação de contraste. Tamanhos de campos móveis recebem 16px; diversos rótulos e informações auxiliares permanecem menores que o recomendado pelo DOCX.

A matriz_visual.json registra 22 elementos com evidências e limites. Status “aderente na estrutura” comprova somente estrutura no código; não deve ser contado como fluxo aprovado sem captura e teste.


## Confronto final com capturas reais

Foram examinadas visualmente 12 capturas representativas: celular auto e manual no painel; celular manual em nova previsão; tablet automático no painel e manual em pendentes; desktop automático; dashboards widescreen e ultrawide; pendentes ultrawide; e dashboards dos três temas. Os três PDFs foram examinados integralmente antes dessa comparação.

**Fluxos móveis (Designer.pdf):** o modo automático em celular preserva controles e navegação desktop, com grande extravasamento à direita e métricas antes do destaque. O modo celular manual reorganiza a ordem e cria cartões, mas conserva cabeçalho em quatro faixas e controles fora do viewport. A barra inferior é visivelmente composta por botões brancos nativos, com Novo quadrado, confirmando a incompatibilidade de classes. No formulário manual a barra de salvar aparece sobre campos intermediários na captura, com grande área vazia no fim do cartão. Essa captura fullPage comprova a composição registrada; a duração da obstrução sob rolagem requer teste específico.

**Tablet (Designer.pdf):** o automático não apresenta o comportamento de referência; tabela estreita quebra descrições em várias linhas e o cabeçalho continua muito alto. O manual mostra lista e detalhe lado a lado, mas o detalhe selecionado está praticamente vazio: apenas situação, contador, abas e ações, sem os dados operacionais mostrados na referência. A navegação horizontal permanece.

**Temas (Designer (1).pdf e Designer (3).png):** a identidade geral escuro/claro/preto é perceptível. O claro conserva gradiente cinza/azulado muito amplo no spotlight e textos ciano, verde e amarelo claros; o industrial, após estabilização das transições, confirma ação primária amarela com texto preto e navegação clara. Persistem azul fixo no destaque/cabeçalho/aba ativa e timer vermelho escuro, sem exigir reprodução literal de todas as cores da prancha. No escuro o timer vermelho escuro tem destaque insuficiente sobre marinho. São observações visuais, não medições WCAG.

**Desktop amplo (Designer (2).pdf):** convencional, wide e ultra confirmam navegação horizontal. Wide apenas divide destaque e alarmes acima de tabela ampla; ultra estica a mesma estrutura, com muito espaço vazio. Nenhum reproduz lista central, contexto/gráficos à direita e ações rápidas da prancha. Na tela Pendentes ultra os cartões ocupam parte da primeira linha e o detalhe quase vazio fica distante; a área extra não acrescenta as regiões operacionais coordenadas previstas.

## Limites da avaliação visual

As capturas finais adicionais incluem alarme aberto, drawer aberto e filtros. O drawer corresponde à composição esperada. O alarme tem dimensão de viewport e quatro ações empilhadas, porém o timer escuro não recebe destaque adequado e o teste mantém foco fora do modal. Filtros divergem objetivamente: abrem no fluxo estático da página, com altura 664.94px, em vez de painel inferior; a classe active-sheet prevista no CSS não é aplicada. V03 e estados vazios permanecem sem confirmação visual específica. O texto “Alarmes Ativos (0)” acompanhado de cartões foi observado, porém sua consistência funcional pertence à auditoria de dados/comportamento. Não se atribuiu nota percentual de fidelidade, pois wireframes orientam comportamentos e não uma comparação pixel a pixel.


## Revisão das evidências estabilizadas

As capturas iniciais de temas foram substituídas pelo auditor após detectar transições CSS ainda em curso. A revisão usa animações desativadas e espera de estabilização: **não há falha de botão azul nem de navegação escura no tema industrial estabilizado**. Ação primária amarela/preta e texto da navegação claro foram reinspecionados visualmente e confirmados por theme_colors em testes_estados.json. No claro persistem superfícies claras, gradiente cinza/azul no destaque e textos ciano/verde/amarelo claros; a necessidade de medição de contraste continua, sem deduzir reprovação WCAG somente pela captura.

O relógio com placeholders das capturas iniciais era efeito do harness pausar o timer antes do primeiro tick, não falha da aplicação. Não foi registrado como defeito.

O teste de filtragem evidencia um problema adicional de informação: após filtro PIG o spotlight mantém a descrição da bomba atrasada, mas o contador passa a Faltam 2h29. A aparência isolada do cartão não garante consistência do evento representado. O teste da lousa em detalhes também encontrou container externo display:none apesar de container interno block e imagem sem retângulo visível; isso limita a aderência à consulta de anotações prevista.
