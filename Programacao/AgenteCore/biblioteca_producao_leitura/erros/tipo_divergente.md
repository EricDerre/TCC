---
# ! Alteração de IA - Revisar: camada de leitura do verbete `tipo_divergente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/tipo_divergente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota dizia que a retirada protegia a busca ("RAG", "vetorial", "indexação semântica"), mas a camada de leitura não é buscada nem lida pelo modelo, e a busca deste projeto é por palavras; a nota retirada continua no verbete que o modelo lê.
id: tipo_divergente
titulo: Tipo divergente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: tipo_divergente
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada]
palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, convercao, json]
causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
verbete: erros/tipo_divergente.md
hash_do_verbete: b9fe74bb7153b778
gerado_em: 2026-11-07
curado: sim
---

# Tipo divergente

Camada de leitura do verbete `tipo_divergente` (`biblioteca_producao/erros/tipo_divergente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto. Trata da causa `tipo_divergente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").

## Como aparece na tela

- texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar.
- "89,90" com vírgula não converte; destaque fora de true/false sai literal.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `numero como texto`, `booleano como Sim`, `destaque 1`, `ordenacao errada`, `soma errada`.

## O que conferir

Causa, como o verbete a descreve: O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `valor_fora_do_dominio` (Valor fora do domínio), `formato_de_data_divergente` (Formato de data divergente), `escala_ou_unidade_errada` (Escala ou unidade errada).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/fault_injection.py`, `Programacao/CobaiaFront/produtos_api.php`, `Programacao/CobaiaAPI/app/routers/produtos.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/pedidos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `tipo`, `texto`, `string`, `numero`, `booleano`, `Sim`, `aspas`, `type_drift`, `str`, `virgula decimal`, `convercao`, `json`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/tipo_divergente.md`.

## Curadoria

Leitura revisada e aprovada. Descrição conceitual exata sobre divergências de tipos de dados em cargas JSON (string vs number vs boolean) e seu mapeamento para o injetor type_drift. A nota do modelo (época 101) foi retirada desta leitura; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
