---
# ! Alteração de IA - Revisar: camada de leitura do verbete `escala_ou_unidade_errada`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/escala_ou_unidade_errada.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a seção Notas do modelo ficou vazia depois de o analista retirar o texto do modelo; o analista que lê precisa saber que o verbete lido pelo modelo ainda traz essas notas; a nota não dizia que o texto do modelo saiu só desta leitura e continua no verbete que o modelo lê.
id: escala_ou_unidade_errada
titulo: Escala ou unidade errada
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: escala_ou_unidade_errada
arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/models.py]
endpoints: [GET /api/produtos, GET /api/pedidos]
tabelas: [tbprodutos, tbpedido_reserva]
sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas]
palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid]
causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
verbete: erros/escala_ou_unidade_errada.md
hash_do_verbete: fd6f5d9b076b4228
gerado_em: 2026-11-07
curado: sim
---

# Escala ou unidade errada

Camada de leitura do verbete `escala_ou_unidade_errada` (`biblioteca_producao/erros/escala_ou_unidade_errada.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto. Trata da causa `escala_ou_unidade_errada` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.

## Como aparece na tela

- todos os valores errados pelo mesmo fator: conversão de unidade.
- só o arredondamento errado.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `precos cem vezes maiores`, `precos cem vezes menores`, `preco arredondado`, `data um dia antes`, `dobro de pessoas`.

## O que conferir

Causa, como o verbete a descreve: A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `tipo_divergente` (Tipo divergente), `formato_de_data_divergente` (Formato de data divergente), `chave_de_juncao_errada` (Chave de junção errada).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaAPI/app/models.py`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/pedidos`.
- Tabelas do banco: `tbprodutos`, `tbpedido_reserva`.
- Palavras que a busca usa para achar este verbete: `escala`, `unidade`, `centavos`, `reais`, `fator`, `cem`, `arredond`, `fuso`, `dia`, `dobro`, `multiplic`, `divid`.

## Notas do modelo

O verbete que o modelo lê traz 1 nota do modelo. A curadoria de 10/11/2026 a retirou desta leitura; ela continua em `biblioteca_producao/erros/escala_ou_unidade_errada.md`.

## Curadoria

Leitura revisada e aprovada. Descrições claras sobre conversão unitária e floating point errors (arredondamento e fusos). A nota do modelo (uma retificação da época 1) foi retirada desta leitura para não repetir sintomas; continua no verbete que o modelo lê.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
