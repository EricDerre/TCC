---
# ! Alteração de IA - Revisar: camada de leitura do verbete `campo_ausente`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/campo_ausente.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: campo_ausente
titulo: Campo ausente
sistema: CobaiaAPI
entidade_principal: Produto
tipo: erro
status: ativo
causa_raiz: campo_ausente
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
endpoints: [GET /api/produtos, GET /api/pedidos]
sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado]
palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave]
causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
verbete: erros/campo_ausente.md
hash_do_verbete: a3930487b2c2d181
gerado_em: 2026-11-07
curado: sim
---

# Campo ausente

Camada de leitura do verbete `campo_ausente` (`biblioteca_producao/erros/campo_ausente.md`). Tipo: erro (uma causa da taxonomia, com os sinais dela na tela e no corpo da resposta); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Produto. Trata da causa `campo_ausente` da taxonomia: é o verbete que o agente cita quando responde essa causa.

## O que é

Uma chave do contrato não vem no objeto: nem com nulo. No JavaScript a leitura vira undefined.

## Como aparece na tela

- nome ausente: cartão "(sem nome)"; preço ausente: botão imprime "undefined".
- id ausente: botão de detalhe ou cancelar sem identificador, clique sem efeito.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `cartao sem titulo`, `sem nome`, `undefined na tela`, `botao que nao faz nada`, `nulo_inesperado`.

## O que conferir

Causa, como o verbete a descreve: O modo field_missing remove o campo-alvo (fault_injection.py). Diferença para campo_renomeado: nenhuma chave nova aparece no lugar.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `campo_renomeado` (Campo renomeado), `nulo_inesperado` (Nulo inesperado), `estrutura_aninhada_divergente` (Estrutura aninhada divergente).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/fault_injection.py`, `Programacao/CobaiaFront/produtos_api.php`.
- Rotas da API (campo `endpoints`): `GET /api/produtos`, `GET /api/pedidos`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `ausente`, `falta`, `faltando`, `sem o campo`, `undefined`, `field_missing`, `chave`.

## Notas do modelo

O que segue é texto do modelo, acrescentado durante as Fases 3 e 4 e aceito na curadoria; não foi conferido por código.

> [época 1, caso sin-1, nota] Adicionar nota sobre a remoção de campos no fault_injection.py. Motivo: O caso demonstrou que a remoção de campos pode causar sintomas como 'undefined', indicando a necessidade de documentar melhor esse cenário.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
