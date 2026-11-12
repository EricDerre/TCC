<!-- ! Alteração de IA - Revisar: documento DERIVADO, gerado por experimento_analista.py --previa a partir de `fase4_biblioteca/` (trilha, registros e a biblioteca de antes do lote) (--check regera e compara); não editar à mão.
     ! Motivo: nenhum número digitado à mão; o relatório da Pré-Fase 4 do Memorial cola estes blocos. -->
# Prévia sem modelo da corrida 27: a ficha curta do caso e o prompt do analista de documentação, gerada em 2026-11-11

Sem modelo. A corrida 27 chama o modelo no papel de analista de documentação nos 54 casos de aprendizado da corrida 20 (24 diagnosticados pela tela e 30 pelo caso escrito; 37 diagnósticos certos e 17 errados), com a biblioteca de antes do lote (`1fca10f1a6f6`), que só é lida. Cada chamada leva as instruções fixas (hash `cbc4505b3c2052f1`, cerca de 608 tokens), o verbete da causa certa e a ficha curta do caso, montada por código a partir da trilha da corrida 20.

A ficha. Tem mediana de 289,5 tokens estimados e máximo de 388, dentro do orçamento de 400 (0 acima). O prompt inteiro tem mediana de 1146,5 tokens e máximo de 1399, contra 2358 da proposta de edição de hoje; pela taxa do modelo nesta máquina, cada chamada leva cerca de 91,55 s (hoje, 158,22 s), e as 54 inferências, cerca de 83 minutos.

O que a corrida consegue enxergar. A busca entregou o verbete da causa certa em 34 casos e o deixou fora dos entregues em 20: é nestes que um sinal de busca faz sentido, e o portão da busca exige que o caso passe a recebê-lo. Pela seleção da proposta de desenho, há lacuna na documentação em 20 casos (os 17 diagnósticos errados e 3 certos em que nenhum verbete entregue tratava da causa respondida), e em 34 não há; em 16 o verbete já registra o caso, e o desenho chamaria o analista em 18. Nesta corrida ele é chamado nos 54, para a comparação com a corrida 20 ser caso a caso, e a leitura separa os casos com lacuna dos sem lacuna, em que a saída esperada é nenhuma.

O que cada leitura precisa mostrar. Na corrida 20 o modelo fez 92 propostas em 54 casos e se absteve em 0; 6 das 92 afirmavam um fato; e, das 20 que passaram nos filtros, a revisão humana julgou 2 corretas. Para sair do ruído, a abstenção precisa aparecer em 6 casos ou mais; a forma, em 10 afirmações ou mais se as 54 respostas tiverem texto; e a parcela correta, em 9 corretas ou mais se 20 propostas forem revisadas.

Regra fixada antes da corrida (decisão 121). Três leituras contra a corrida 20, cada uma com um teste exato bilateral e o corte de 0,05. A abstenção: os casos em que o modelo responde que não há o que acrescentar, pareados caso a caso com a corrida 20 (McNemar). A forma do texto: a parcela das propostas com texto que afirmam um fato, isto é, que passam no portão da forma de instrução, contra a mesma conta nas propostas da corrida 20 (Fisher). A parcela correta: entre as propostas que passam nos filtros de hoje, as que a revisão humana às cegas julga corretas, contra as edições da corrida 20 (Fisher); essa leitura só tem veredito depois da revisão. Vale com a corrida completa e a ponte da versão do Ollama pareável com a Fase 3 (b + c até 2, decisão 47). Nenhum resultado muda o agente: a proposta do analista de documentação é base de desenho para depois da Fase 5.

O prompt inteiro do caso `lex-2`, como o modelo o recebe:

```text
Você cuida da documentação de um sistema: uma interface web e a API que ela chama. Um agente de testes usou essa documentação para apontar a causa de uma falha, e uma pessoa conferiu o diagnóstico. Depois destas instruções vêm o verbete da causa certa e a ficha do caso. Diga se o verbete precisa de um acréscimo para que um PRÓXIMO caso parecido, e não este, seja diagnosticado certo.

Escolha UMA saída:
- sinal_de_busca: o verbete já explica a causa, mas a busca não o entregou ao agente. Dê palavras-chave ou sintomas que um caso parecido traria, para a busca achar o verbete.
- nota: falta no verbete um fato sobre o sistema. Escreva a frase como ela vai ficar no verbete.
- retificacao: um trecho do verbete está errado. Copie o trecho igual e escreva a frase certa.
- nenhuma: o verbete já bastava, ou a ficha não mostra o que falta.

Regras:
- O TEXTO é a frase que entra no verbete, escrita como afirmação sobre o sistema. Exemplo de forma, de outro sistema: "O serviço de e-mail responde 202 antes de entregar a mensagem." Não escreva pedido nem instrução: nada de "Adicionar", "Corrigir", "Incluir" ou "Verificar".
- Fale do sistema e do tipo de falha, em termos gerais. Não copie o sintoma da ficha e não cite o identificador do caso.
- Só cite arquivos, rotas e tabelas que apareçam no verbete.
- TEXTO com 60 a 280 caracteres, uma ou duas frases, sem lista. MOTIVO com 20 a 240 caracteres: diga qual dado da ficha mostrou a lacuna.
- Uma proposta só.

Formato, exatamente assim:

PROPOSTA
OPERACAO: sinal_de_busca | nota | retificacao | nenhuma
PALAVRAS_CHAVE: <ate 5 termos novos separados por virgula, ou "nenhuma">
SINTOMAS: <ate 3 sintomas novos separados por virgula, ou "nenhum">
TRECHO: <so em retificacao: o trecho do verbete que esta errado, copiado igual>
TEXTO: <so em nota e retificacao: a frase como vai ficar no verbete>
MOTIVO: <qual dado da ficha mostrou a lacuna>
FIM

=====

VERBETE DA CAUSA CERTA (é nele que o acréscimo entra)
[corpo_nao_e_json] Corpo não é JSON
A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere. Sinais: console "Unexpected token <"; texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO". Causa: Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página. Notas: Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho.

=====

FICHA DO CASO (montada por código, a partir do que o agente registrou)
REQUISIÇÃO: GET /api/produtos
STATUS HTTP: 200
SINTOMA: A conferência 'grid com 14 cartões' falhou: esperava 14 elementos; viu 0 elementos. A resposta não é JSON (começa por '<html><body><h1>...'). A tela mostra 140 linha(s) a menos que a referência; faltam: - img; - img; - img. A tela mostra 1 linha(s) a mais que a referência; sobram: - text: "Erro ao carregar produtos da CobaiaAPI: Unexpected token '<', \"<html><bod\"... is not valid JSON".
DIFERENÇA MEDIDA CONTRA O CONTRATO: a resposta não é JSON: veio como página ou texto com marcação.
BUSCA: entregou ao agente [corpo_nao_e_json] Corpo não é JSON; [mensagens-de-erro-do-codigo] Índice de mensagens literais do código; [erro_interno_do_servidor] Erro interno do servidor (500). O verbete da causa certa, [corpo_nao_e_json], ficou na posição 1 da busca, entre os entregues.
RESPOSTA DO AGENTE: causa corpo_nao_e_json; campo nenhum; confiança alta.
CONFERÊNCIAS QUE NÃO CONFERIRAM: nenhuma.
DECISÃO DE QUEM REVISOU: diagnóstico aceito. Causa certa: corpo_nao_e_json. Campo afetado: nenhum.

Responda só com o bloco PROPOSTA, no formato acima.
```

<!-- tabela:tb_f4_analista_previa_resumo -->
| Casos | Pela tela | Pelo caso escrito | Diagnósticos certos | Verbete certo entregue | Verbete certo fora dos entregues | Ficha: tokens (mediana) | Ficha: tokens (máximo) | Prompt: tokens (mediana) | Prompt da proposta de hoje (mediana) | Segundos por chamada (estimados) | Minutos estimados |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 54 | 24 | 30 | 37 | 34 | 20 | 289,5 | 388 | 1146,5 | 2358 | 91,55 | 83 |
<!-- /tabela:tb_f4_analista_previa_resumo -->
<!-- tabela:tb_f4_analista_previa_selecao -->
| Casos | Com lacuna na documentação | Diagnósticos errados | Certos sem verbete que trate da causa | Sem lacuna | O verbete já registra o caso | O desenho chamaria o analista |
|---|---|---|---|---|---|---|
| 54 | 20 | 17 | 3 | 34 | 16 | 18 |
<!-- /tabela:tb_f4_analista_previa_selecao -->
<!-- tabela:tb_f4_analista_previa_poder -->
| Leitura | Corrida 20 | O que a corrida 27 precisa mostrar para sair do ruído |
|---|---|---|
| abstenção | 0 de 54 casos | 6 casos ou mais |
| forma do texto | 6 de 92 propostas afirmam um fato | 10 afirmações ou mais em 54 |
| parcela correta | 2 de 20 edições revisadas | 9 corretas ou mais em 20 revisadas |
<!-- /tabela:tb_f4_analista_previa_poder -->
<!-- tabela:tb_f4_analista_previa_casos -->
| Caso | Origem | Diagnóstico certo | Causa respondida | Causa certa | Confiança | Verbete certo entregue | Posição na busca | Com lacuna | O verbete já registra o caso | O desenho chamaria | Ficha: tokens | Prompt: tokens |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `lex-2` | tela | sim | `corpo_nao_e_json` | `corpo_nao_e_json` | alta | sim | 1 | não | sim | não | 336 | 1241 |
| `lex-3` | tela | sim | `corpo_vazio` | `corpo_vazio` | média | sim | 1 | não | não | não | 297 | 1169 |
| `lex-5` | fixture | sim | `resposta_truncada` | `resposta_truncada` | alta | sim | 3 | não | sim | não | 234 | 1146 |
| `sin-1` | tela | sim | `campo_ausente` | `campo_ausente` | alta | sim | 1 | não | sim | não | 302 | 1133 |
| `sin-2` | tela | sim | `campo_renomeado` | `campo_renomeado` | média | não | 5 | não | não | não | 328 | 1210 |
| `sin-3` | tela | não | `tipo_divergente` | `estrutura_aninhada_divergente` | média | não | 5 | sim | não | sim | 330 | 1231 |
| `semt-2` | tela | sim | `tipo_divergente` | `tipo_divergente` | alta | não | 4 | não | não | não | 308 | 1131 |
| `semt-4` | fixture | sim | `formato_de_data_divergente` | `formato_de_data_divergente` | alta | sim | 2 | não | não | não | 234 | 1061 |
| `tra-2` | fixture | não | `nome_nulo_vindo_da_view` | `chave_de_juncao_errada` | média | não | 4 | sim | não | sim | 318 | 1330 |
| `tra-3` | tela | não | `tipo_divergente` | `chave_de_juncao_errada` | baixa | sim | 7 | sim | sim | não | 271 | 1283 |
| `tra-5` | fixture | não | `contagem_inconsistente` | `escala_ou_unidade_errada` | baixa | não | 13 | sim | não | sim | 291 | 1251 |
| `run-3` | tela | sim | `limite_de_requisicoes` | `limite_de_requisicoes` | alta | não | 5 | sim | não | sim | 388 | 1213 |
| `run-5` | fixture | sim | `registro_duplicado` | `registro_duplicado` | alta | não | 5 | sim | não | sim | 277 | 1090 |
| `efe-4` | fixture | não | `colecao_no_lugar_de_objeto` | `estado_da_tela_divergente` | baixa | sim | 2 | sim | não | sim | 297 | 1119 |
| `lex-6` | fixture | não | `recurso_inexistente` | `corpo_nao_e_json` | baixa | sim | 1 | sim | não | sim | 236 | 1141 |
| `lex-9` | tela | sim | `corpo_nao_e_json` | `corpo_nao_e_json` | média | sim | 1 | não | sim | não | 336 | 1241 |
| `lex-12` | tela | sim | `corpo_nao_e_json` | `corpo_nao_e_json` | média | sim | 1 | não | não | não | 336 | 1241 |
| `sin-6` | tela | sim | `campo_ausente` | `campo_ausente` | alta | sim | 1 | não | não | não | 296 | 1127 |
| `sin-8` | fixture | sim | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | média | sim | 3 | não | não | não | 250 | 1163 |
| `sin-9` | tela | sim | `campo_renomeado` | `campo_renomeado` | alta | sim | 6 | não | sim | não | 324 | 1206 |
| `sin-12` | fixture | não | `colecao_no_lugar_de_objeto` | `campo_ausente` | baixa | não | 9 | sim | não | sim | 245 | 1076 |
| `sin-13` | tela | não | `tipo_divergente` | `estrutura_aninhada_divergente` | média | sim | 5 | sim | sim | não | 369 | 1270 |
| `sin-15` | fixture | sim | `colecao_no_lugar_de_objeto` | `colecao_no_lugar_de_objeto` | média | sim | 3 | não | sim | não | 234 | 1147 |
| `semt-6` | tela | não | `contagem_inconsistente` | `tipo_divergente` | média | não | 8 | sim | não | sim | 325 | 1149 |
| `semt-7` | fixture | não | `formato_de_data_divergente` | `tipo_divergente` | baixa | não | 5 | sim | não | sim | 233 | 1056 |
| `semt-10` | tela | sim | `tipo_divergente` | `tipo_divergente` | alta | não | 4 | não | não | não | 308 | 1131 |
| `semt-11` | fixture | sim | `valor_fora_do_dominio` | `valor_fora_do_dominio` | média | sim | 3 | não | sim | não | 239 | 1108 |
| `semt-12` | fixture | sim | `formato_de_data_divergente` | `formato_de_data_divergente` | média | sim | 3 | não | não | não | 237 | 1064 |
| `semt-13` | tela | sim | `tipo_divergente` | `tipo_divergente` | alta | não | 8 | não | não | não | 216 | 1040 |
| `semt-15` | fixture | sim | `valor_fora_do_dominio` | `valor_fora_do_dominio` | baixa | não | 4 | não | não | não | 278 | 1146 |
| `tra-6` | tela | sim | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | baixa | não | 15 | não | não | não | 336 | 1296 |
| `tra-7` | tela | não | `campo_renomeado` | `chave_de_juncao_errada` | média | não | 15 | sim | não | sim | 388 | 1399 |
| `tra-9` | fixture | não | `formato_de_data_divergente` | `escala_ou_unidade_errada` | média | não | 11 | sim | não | sim | 279 | 1239 |
| `tra-12` | tela | sim | `escala_ou_unidade_errada` | `escala_ou_unidade_errada` | média | sim | 15 | não | sim | não | 353 | 1313 |
| `tra-13` | tela | não | `imagem_fora_do_dominio` | `chave_de_juncao_errada` | baixa | não | 8 | sim | não | sim | 310 | 1321 |
| `tra-14` | tela | sim | `contagem_inconsistente` | `contagem_inconsistente` | média | sim | 2 | não | não | não | 310 | 1135 |
| `run-6` | fixture | sim | `erro_interno_do_servidor` | `erro_interno_do_servidor` | média | sim | 1 | não | sim | não | 269 | 1185 |
| `run-7` | tela | sim | `recurso_inexistente` | `recurso_inexistente` | alta | sim | 4 | não | sim | não | 388 | 1246 |
| `run-8` | fixture | sim | `recurso_inexistente` | `recurso_inexistente` | média | sim | 1 | não | não | não | 298 | 1156 |
| `run-11` | fixture | não | `valor_fora_do_dominio` | `dado_desatualizado` | média | não | 4 | sim | não | sim | 256 | 1079 |
| `run-12` | fixture | sim | `erro_interno_do_servidor` | `erro_interno_do_servidor` | média | sim | 1 | não | sim | não | 284 | 1200 |
| `run-14` | fixture | sim | `dado_desatualizado` | `dado_desatualizado` | alta | sim | 1 | não | não | não | 277 | 1101 |
| `run-15` | tela | sim | `tempo_de_resposta_excedido` | `tempo_de_resposta_excedido` | média | não | 6 | sim | não | sim | 266 | 1094 |
| `efe-6` | fixture | sim | `localizador_quebrado` | `localizador_quebrado` | média | sim | 1 | não | não | não | 262 | 1134 |
| `efe-8` | fixture | sim | `estado_da_tela_divergente` | `estado_da_tela_divergente` | média | sim | 2 | não | não | não | 254 | 1076 |
| `efe-9` | fixture | sim | `localizador_quebrado` | `localizador_quebrado` | alta | sim | 1 | não | não | não | 261 | 1132 |
| `efe-10` | fixture | não | `valor_fora_do_dominio` | `estado_da_tela_divergente` | baixa | sim | 3 | sim | não | sim | 367 | 1189 |
| `efe-11` | fixture | não | `localizador_quebrado` | `estado_da_tela_divergente` | baixa | não | 6 | sim | não | sim | 241 | 1063 |
| `efe-12` | fixture | sim | `localizador_quebrado` | `localizador_quebrado` | alta | sim | 1 | não | sim | não | 255 | 1126 |
| `efe-13` | fixture | não | `dado_desatualizado` | `estado_da_tela_divergente` | média | sim | 1 | sim | não | sim | 342 | 1164 |
| `efe-15` | fixture | sim | `estado_da_tela_divergente` | `estado_da_tela_divergente` | alta | sim | 1 | não | não | não | 288 | 1110 |
| `lex-13` | fixture | sim | `corpo_vazio` | `corpo_vazio` | alta | sim | 1 | não | sim | não | 205 | 1078 |
| `lex-14` | fixture | sim | `resposta_truncada` | `resposta_truncada` | alta | sim | 2 | não | sim | não | 229 | 1141 |
| `lex-15` | tela | sim | `corpo_nao_e_json` | `corpo_nao_e_json` | média | sim | 1 | não | não | não | 336 | 1241 |
<!-- /tabela:tb_f4_analista_previa_casos -->
