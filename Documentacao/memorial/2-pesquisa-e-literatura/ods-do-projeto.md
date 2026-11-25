<!-- ! Alteração de IA - Revisar: arquivo novo com a pesquisa de em quais Objetivos de Desenvolvimento Sustentável (ODS) da ONU o projeto pode ser enquadrado, com a meta oficial de cada candidato, o que no repositório a sustenta, a força do vínculo, os descartados e os textos prontos para slide e banner.
     ! Motivo: o orientador pediu em 25/11/2026 que cada equipe informe o ODS considerado no projeto, nos slides e no banner da apresentação, e o Eric pediu o levantamento para o grupo escolher; sem ele a escolha sairia de memória, com meta citada de cabeça e vínculo exagerado. -->
# ODS do projeto: onde o agente cabe e onde não cabe

Pesquisa de 25/11/2026. Os números do projeto citados aqui foram copiados dos arquivos indicados (caminho e linha); nenhum foi digitado de memória.

## Resposta em uma frase

O encaixe mais defensável é o **ODS 9 (Indústria, Inovação e Infraestrutura), meta 9.5** (pesquisa científica e capacidade tecnológica), com **ODS 8, meta 8.2** (produtividade por modernização tecnológica e inovação) e **ODS 17, meta 17.6** (acesso compartilhado à ciência e à tecnologia) como apoio; nenhum ODS é medido de forma direta pelo projeto, e dizer o contrário seria exagero.

## O que o projeto fez e mediu que pode sustentar um ODS

Estes são os fatos de base. A tabela seguinte aponta para eles pela letra. Os números de linha do `README.md` são da manhã de 25/11/2026; o arquivo foi editado no mesmo dia pela frente do instalador, então procure pela seção se a linha não bater.

| Fato | Onde está |
|---|---|
| (A) Agente de testes que roda na máquina de quem testa: modelo de linguagem local (Ollama), só CPU, sem nuvem | `README.md`, linha 11; `Documentacao/TCC - ABNT 14724 - V1.md`, linhas 91 e 112 |
| (B) Justificativa de viabilidade: a maior parte das equipes não tem GPU nem pode enviar dados a um serviço externo; o trabalho mede o que um modelo quantizado faz numa máquina corporativa comum, sem administrador | `Documentacao/TCC - ABNT 14724 - V1.md`, linha 125 |
| (C) Máquina de medição: notebook corporativo com Intel i5-1235U, sem GPU dedicada | `Documentacao/TCC - ABNT 14724 - V1.md`, linha 706; `DETALHES-TECNICOS.md`, linha 777 |
| (D) Resultado da Fase 5: nos dez cenários medidos o agente reparou mais rápido que as pessoas, 66,3 s contra 219,7 s na média; p = 0,0020 no teste dos sinais | `README.md`, linhas 19 e 82; `Programacao/AgenteCore/experimentos/resultados_alvo/fase5/medicao.md`, linhas 7 e 19 |
| (E) Task Success (proporção de reparos que deram certo): agente 49 de 50 (98,0%), pessoas 14 de 30 (46,7%). O veredito deste número depende da sessão de um integrante só (decisão 151), por isso o resultado central é o do tempo, o fato D | `.../fase5/medicao.md`, linhas 53 e 54 |
| (F) Cura de seletor: curou as 160 quebras de localizador armadas na corrida 19, com mediana de 0,639 s, sem modelo de linguagem e sem GPU | `Documentacao/TCC - ABNT 14724 - V1.md`, linha 125 |
| (G) Diagnóstico de causa raiz com o modelo escolhido: 75,0% de acerto nos 36 casos de avaliação, numa repetição de controle | `Documentacao/TCC - ABNT 14724 - V1.md`, linha 125 |
| (H) Código aberto: licença MIT, com a lista de autores no próprio arquivo | `LICENSE`, linhas 1 a 5; selo no `README.md`, linha 5 |
| (I) Documentação pública (README, detalhes técnicos, memorial, painel) e instalador único para Windows, Linux e macOS, com prova de instalação por célula de teste | `README.md`, seção "Instalar e rodar" |
| (J) Entrega ao analista um relatório por caso, com a causa, a evidência e o grau de confiança | `Documentacao/TCC - ABNT 14724 - V1.md`, linha 91; `README.md`, linha 100 |
| (K) Ferramenta feita para reduzir o desgaste com manutenção de testes frágeis e o tempo de triagem manual | `Documentacao/TCC - ABNT 14724 - V1.md`, linhas 87 e 121 |

Limites declarados no próprio repositório, que valem para qualquer ODS: o instalador está provado no Windows 11 da máquina-alvo e no Linux pelo WSL (o Linux dentro do Windows); ficaram sem teste Windows recém-instalado, Windows 10 e Linux fora do WSL (`README.md`, seção "Instalar e rodar"). A comparação com pessoas usou 30 medidas de pessoas, em três sessões (`fase5/medicao.md`, linha 54). O projeto **não mediu** consumo de energia, emissões, custo em dinheiro, nem efeito em escola ou em pessoa em situação de vulnerabilidade.

## Tabela dos candidatos

Texto das metas: versão em português das Nações Unidas no Brasil, página de cada objetivo (referências 1 a 8). Para o ODS 9 há também o texto adaptado ao Brasil pelo IPEA (referência 9), citado ao lado. Força do vínculo: forte, médio ou fraco.

| ODS e meta | Texto oficial | O que no projeto sustenta | Força | O que NÃO dá para afirmar |
|---|---|---|---|---|
| **9.5** | "Fortalecer a pesquisa científica, melhorar as capacidades tecnológicas de setores industriais em todos os países, particularmente os países em desenvolvimento, inclusive, até 2030, incentivando a inovação e aumentando substancialmente o número de trabalhadores de pesquisa e desenvolvimento por milhão de pessoas e os gastos público e privado em pesquisa e desenvolvimento." (ONU Brasil) | Pesquisa aplicada com método: fases, regras de decisão fixadas antes de cada rodada, comparação com pessoas (fatos D e E). Capacidade tecnológica de equipes de teste de software com máquina comum (fatos A, B, C). Inovação: agente que conserta o próprio teste e diagnostica contrato de API (fatos F, G, J) | **Médio** a forte. É pesquisa e inovação em tecnologia, e a meta é exatamente isso; o "médio" vem de a meta falar de indústria e de indicadores nacionais | Não aumentou número de pesquisadores nem gasto em P&D. Não é inovação industrial em escala: é um protótipo medido em duas aplicações-alvo, uma delas o site cedido por um integrante do grupo |
| **9.4** | "Até 2030, modernizar a infraestrutura e reabilitar as indústrias para torná-las sustentáveis, com eficiência aumentada no uso de recursos e maior adoção de tecnologias e processos industriais limpos e ambientalmente corretos; com todos os países atuando de acordo com suas respectivas capacidades." (ONU Brasil). IPEA: "Até 2030, modernizar a infraestrutura e reabilitar as atividades econômicas para torná-las sustentáveis, com foco no uso de recursos renováveis e maior adoção de tecnologias e processos industriais limpos e ambientalmente adequados." | Modernização de uma prática de software (manutenção de testes) com menos retrabalho humano (fatos D, K). Roda em hardware existente, sem exigir GPU nova (fatos B, C) | **Fraco** | Não mediu energia, carbono nem recurso nenhum. "Eficiência no uso de recursos" aqui seria tempo de pessoa e hardware reaproveitado, e a meta fala de indústria e infraestrutura físicas. Uma banca pode pedir o número de watts e o projeto não tem |
| **9.b** | "Apoiar o desenvolvimento tecnológico, a pesquisa e a inovação nacionais nos países em desenvolvimento, inclusive garantindo um ambiente político propício para, entre outras coisas, a diversificação industrial e a agregação de valor às commodities." (ONU Brasil) | Tecnologia desenvolvida no Brasil, por brasileiros, sem depender de serviço estrangeiro pago (fatos A, B) | **Fraco** | A meta é de política pública e de diversificação industrial; o projeto não é política nem mexeu em commodities. Usa modelos de empresas estrangeiras (Qwen, Granite) |
| **9.c** | "Aumentar significativamente o acesso às tecnologias de informação e comunicação e se empenhar para oferecer acesso universal e a preços acessíveis à internet nos países menos desenvolvidos, até 2020." (ONU Brasil) | Nenhuma: o instalador precisa de internet (`README.md`, seção "Instalar e rodar") | **Sem vínculo** (descartada, ver abaixo) | Não trata de acesso à internet nem de países menos desenvolvidos |
| **8.2** | "Atingir níveis mais elevados de produtividade das economias por meio da diversificação, modernização tecnológica e inovação, inclusive por meio de um foco em setores de alto valor agregado e dos setores intensivos em mão de obra." (ONU Brasil) | Ganho de produtividade medido no nível da tarefa: reparo em 66,3 s contra 219,7 s (fato D). O Task Success (fato E) aponta para o mesmo lado, mas o veredito dele depende de uma sessão só e não deve ir sozinho para o slide. Modernização tecnológica de um processo intensivo em mão de obra, o reparo manual de teste (fato K) | **Médio** | A produtividade da meta é a da economia. O projeto mediu o tempo de um reparo em dez cenários de laboratório, com 30 medidas de pessoas, e não a produtividade de uma empresa. O resultado vale para esses cenários, e o relatório da fase declara limites |
| **8.3** | "Promover políticas orientadas para o desenvolvimento que apoiem as atividades produtivas, geração de emprego decente, empreendedorismo, criatividade e inovação, e incentivar a formalização e o crescimento das micro, pequenas e médias empresas, inclusive por meio do acesso a serviços financeiros." (ONU Brasil) | Ferramenta gratuita e sem nuvem paga pode servir a equipes pequenas (fatos A, B, H) | **Fraco** | Meta de política de emprego e de pequenas empresas. O projeto não testou em nenhuma pequena empresa nem mediu emprego. "Gratuito" é custo de licença; o custo de operação não foi medido |
| **4.3** | "Até 2030, assegurar a igualdade de acesso para todos os homens e mulheres à educação técnica, profissional e superior de qualidade, a preços acessíveis, incluindo universidade." (ONU Brasil) | Nenhuma | **Sem vínculo** (descartada) | O projeto é de estudantes, mas não trata de acesso à educação |
| **4.4** | "Até 2030, aumentar substancialmente o número de jovens e adultos que tenham habilidades relevantes, inclusive competências técnicas e profissionais, para emprego, trabalho decente e empreendedorismo." (ONU Brasil) | Documentação pública que ensina a rodar e a ler o agente (fato I); o TCC mostra como medir um agente de QA com método (fato D) | **Fraco** | Não houve curso, oficina nem turma. Ninguém foi formado pelo projeto, e o ganho de habilidade das pessoas não foi medido |
| **12.2** | "Até 2030, alcançar a gestão sustentável e o uso eficiente dos recursos naturais." (ONU Brasil) | Roda em CPU comum, sem GPU e sem data center (fatos A, B, C) | **Fraco** | Não mediu consumo de energia, nem comparou com uma solução em nuvem. "Sem nuvem" não é o mesmo que "gasta menos" |
| **12.5** | "Até 2030, reduzir substancialmente a geração de resíduos por meio da prevenção, redução, reciclagem e reuso." (ONU Brasil) | Nenhuma | **Sem vínculo** (descartada) | Nada no projeto trata de resíduo |
| **12.a** | "Apoiar países em desenvolvimento a fortalecer suas capacidades científicas e tecnológicas para mudar para padrões mais sustentáveis de produção e consumo." (ONU Brasil) | Nenhuma além de 12.2 | **Sem vínculo** (descartada) | O projeto não apoia outro país nem muda padrão de consumo |
| **17.6** | "Melhorar a cooperação Norte-Sul, Sul-Sul e triangular regional e internacional e o acesso à ciência, tecnologia e inovação, e aumentar o compartilhamento de conhecimentos em termos mutuamente acordados, inclusive por meio de uma melhor coordenação entre os mecanismos existentes, particularmente no nível das Nações Unidas, e por meio de um mecanismo de facilitação de tecnologia global." (ONU Brasil) | Código aberto sob licença MIT, documentação pública e registro de cada decisão, o que permite que outras equipes reaproveitem o método e os dados (fatos H, I) | **Fraco a médio** | A meta é de cooperação entre países. O projeto não tem parceiro internacional, nem acordo, nem uso comprovado por terceiros. O repositório da disciplina é privado (`README.md`, linha 29); o principal precisa estar público para o argumento valer |
| **17.8** | "Operacionalizar plenamente o Banco de Tecnologia e o mecanismo de capacitação em ciência, tecnologia e inovação para os países menos desenvolvidos até 2017, e aumentar o uso de tecnologias de capacitação, em particular das tecnologias de informação e comunicação." (ONU Brasil) | Nenhuma | **Sem vínculo** (descartada) | A meta é sobre o Banco de Tecnologia da ONU e países menos desenvolvidos |
| **10.2** | "Até 2030, empoderar e promover a inclusão social, econômica e política de todos, independentemente da idade, gênero, deficiência, raça, etnia, origem, religião, condição econômica ou outra." (ONU Brasil) | Nenhuma | **Sem vínculo** (descartada) | Não houve público-alvo vulnerável nem acessibilidade medida |
| **13.2 e 13.3** | 13.2: "Integrar medidas da mudança do clima nas políticas, estratégias e planejamentos nacionais." 13.3: "Melhorar a educação, aumentar a conscientização e a capacidade humana e institucional sobre mitigação, adaptação, redução de impacto e alerta precoce da mudança do clima." (ONU Brasil) | Nenhuma | **Sem vínculo** (descartadas) | Não há medida de emissão, e o projeto não trata de clima |

Conferência da letra: os textos das metas 9.5, 8.2 e 17.6, as três recomendadas, foram conferidos palavra por palavra nas páginas das Nações Unidas no Brasil em 25/11/2026 (referências 1, 2 e 5) e batem com a tabela. As outras metas vieram de uma ferramenta de leitura que resume o conteúdo antes de devolvê-lo; antes de citar qualquer uma delas entre aspas, confira a letra na página original.

## Recomendação

**Principal: ODS 9, meta 9.5.** Motivo da ordem: é a única meta cujo verbo descreve o que o trabalho é, uma pesquisa científica que desenvolve capacidade tecnológica e inovação. O vínculo é com pesquisa e capacidade tecnológica, não com a infraestrutura ou a indústria sustentável das metas 9.1 a 9.4. Tem prova no repositório: método com regras fixadas antes, medição contra pessoas e resultado com intervalo e teste (fatos D e E).

**Apoio 1: ODS 8, meta 8.2.** Motivo: é onde o número principal do projeto cai, o reparo mais rápido (fato D). Fica em apoio porque a meta fala da produtividade da economia e a medição é de laboratório.

**Apoio 2: ODS 17, meta 17.6.** Motivo: sustenta o que o projeto tem de aberto, a licença MIT, a documentação e o instalador (fatos H e I). Fica em último porque a meta é de cooperação entre países, que o projeto não fez.

### O que uma banca pode questionar

- **ODS 9.5:** "Vocês aumentaram P&D ou número de pesquisadores?" Não. Responda que o trabalho é uma pesquisa aplicada que gera capacidade tecnológica, e não que mexeu nos indicadores nacionais da meta. Uma banca também pode lembrar que a meta fala de setores industriais; o ponto fraco é aí.
- **ODS 8.2:** "Isso é produtividade da economia?" Não. Diga "produtividade no reparo de teste, medida em dez cenários", com o 66,3 s contra 219,7 s, e que não se generaliza a uma empresa. As pessoas somam 30 medidas de três sessões, e a regra do projeto trata os cenários, não as pessoas, como unidade (`fase5/medicao.md`, linha 5).
- **ODS 17.6:** "Com quem vocês cooperaram?" Com ninguém fora do grupo. Diga "acesso aberto ao conhecimento", e só use isso se o repositório principal estiver público na apresentação.
- **Nunca afirmar:** sustentabilidade ambiental, economia de energia ou de dinheiro, inclusão e educação. Nenhuma foi medida.

## Textos prontos

Todos os números vêm de `fase5/medicao.md` e do README, nas linhas citadas.

**ODS 9, meta 9.5 (principal)**
- Slide: "ODS 9, meta 9.5: pesquisa e inovação em tecnologia. Um agente de testes com modelo de linguagem local, só em CPU, reparou os defeitos em 66,3 s em média, contra 219,7 s das pessoas, em dez cenários."
- Banner: "ODS 9 (meta 9.5): inovação em teste de software que roda numa máquina comum, sem nuvem."

**ODS 8, meta 8.2 (apoio)**
- Slide: "ODS 8, meta 8.2: produtividade por modernização tecnológica. Nos dez cenários medidos, o reparo pelo agente foi em média 153,4 s mais rápido que o manual. O resultado vale para esses cenários, não para uma empresa inteira."
- Banner: "ODS 8 (meta 8.2): reparo de teste automatizado mais rápido que o manual."

**ODS 17, meta 17.6 (apoio)**
- Slide: "ODS 17, meta 17.6: acesso compartilhado à tecnologia. Código aberto com licença MIT, documentação pública e um instalador único para Windows, Linux e macOS, provado no Windows 11 e no Linux pelo WSL."
- Banner: "ODS 17 (meta 17.6): código aberto e documentado para outras equipes reaproveitarem."

## Descartados, com o motivo

- **9.c:** trata de acesso universal à internet nos países menos desenvolvidos. O projeto precisa de internet só para instalar.
- **9.4 e 9.b:** ficaram na tabela como fracos. Se o grupo quiser só um ODS no slide, não são recomendados: 9.4 pediria medida de energia e 9.b é de política pública.
- **8.3:** é de política de emprego e de pequenas empresas, sem teste com empresa.
- **4.3:** é acesso à educação. 4.4 ficou como fraco porque ninguém foi formado pelo projeto.
- **12.2, 12.5, 12.a:** 12.2 só se sustentaria com consumo de energia medido, e o projeto não mediu. 12.5 e 12.a não têm vínculo.
- **17.8:** é sobre o Banco de Tecnologia da ONU.
- **10 (10.2) e 13 (13.2, 13.3):** sem vínculo no repositório. Não foi encontrado nenhum texto do projeto sobre inclusão, desigualdade, clima ou emissões.

Outras metas do ODS 9 (9.1, 9.2, 9.3) foram lidas na página e não servem: tratam de infraestrutura, indústria e crédito a pequenas indústrias.

## Orientação oficial sobre declarar ODS em trabalho acadêmico

Não encontrei orientação da UNICID nem da Cruzeiro do Sul Educacional sobre como declarar ODS em TCC; a busca não trouxe nada dessas instituições. Não encontrei orientação da ONU nem do IPEA sobre formato em trabalho acadêmico: o IPEA publica as metas adaptadas ao Brasil e os Cadernos ODS, que servem para citar a meta, não para formatar o trabalho. Achei só uma página de programa de pós-graduação da UFSCar que diz que, pelas instruções da CAPES, o produto final deve mencionar os ODS relacionados à pesquisa (referência 10). É fonte de terceiro, sobre pós-graduação, e não prova que vale para a graduação. O caminho certo é perguntar à coordenação do curso e ao orientador qual formato esperam, e citar o ODS pelo número da meta, como "ODS 9, meta 9.5".

## Lacunas

- Texto oficial: abri as páginas em português da ONU no Brasil e a página do ODS 9 do IPEA. Não consegui conferir direto a resolução A/RES/70/1 nem sdgs.un.org (não foram abertas nesta rodada), nem as páginas do IPEA dos ODS 4, 8, 10, 12, 13 e 17. A letra das três metas recomendadas foi conferida na página (ver a nota depois da tabela); a das outras fica para o grupo, se forem usadas.
- O texto adaptado pelo IPEA para o 9.5 traz metas numéricas nacionais; não foram usadas.
- Nada sobre consumo de energia: se o grupo quiser sustentar 9.4 ou 12.2, é preciso medir antes de escrever.
- Se o repositório principal ficará público na apresentação não consta nos arquivos lidos; a recomendação do 17.6 depende disso.
- Nenhum ODS tem indicador próprio medido pelo projeto; o enquadramento é por afinidade, e o texto deve dizer "contribui para a discussão de", nunca "atinge".

## Referências

1. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 9: Indústria, Inovação e Infraestrutura**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/9>. Acesso em: 25 nov. 2026.
2. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 8: Trabalho Decente e Crescimento Econômico**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/8>. Acesso em: 25 nov. 2026.
3. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 4: Educação de Qualidade**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/4>. Acesso em: 25 nov. 2026.
4. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 12: Consumo e Produção Responsáveis**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/12>. Acesso em: 25 nov. 2026.
5. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 17: Parcerias e Meios de Implementação**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/17>. Acesso em: 25 nov. 2026.
6. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 10: Redução das Desigualdades**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/10>. Acesso em: 25 nov. 2026.
7. ORGANIZAÇÃO DAS NAÇÕES UNIDAS NO BRASIL. **Objetivo 13: Ação Contra a Mudança Global do Clima**. Brasília: ONU Brasil, [s.d.]. Disponível em: <https://brasil.un.org/pt-br/sdgs/13>. Acesso em: 25 nov. 2026.
8. ORGANIZAÇÃO DAS NAÇÕES UNIDAS. Assembleia Geral. **Transformando nosso mundo: a Agenda 2030 para o Desenvolvimento Sustentável**. Resolução A/RES/70/1. Nova York: ONU, 2015. Fonte primária dos textos acima; não aberta diretamente nesta rodada (ver Lacunas).
9. INSTITUTO DE PESQUISA ECONÔMICA APLICADA. **ODS 9: metas nacionais**. Brasília: IPEA, [s.d.]. Disponível em: <https://www.ipea.gov.br/ods/ods9.html>. Acesso em: 25 nov. 2026.
10. UNIVERSIDADE FEDERAL DE SÃO CARLOS. Programa de Pós-Graduação em Sustentabilidade na Gestão Ambiental. **Procedimento para agendamento, realização e entrega de Trabalho de Conclusão de Curso**. São Carlos: UFSCar, [s.d.]. Disponível em: <https://www.ppgsga.ufscar.br/pt-br/gestao-academica/procedimento-de-entrega-de-trabalho-de-conclusao-de-curso>. Acesso em: 25 nov. 2026. (Fonte de terceiro; lida só pelo resumo da busca.)
