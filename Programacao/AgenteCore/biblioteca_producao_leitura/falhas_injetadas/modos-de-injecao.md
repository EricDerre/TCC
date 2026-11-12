---
# ! Alteração de IA - Revisar: camada de leitura do verbete `modos-de-injecao`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/falhas_injetadas/modos-de-injecao.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura; a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: modos-de-injecao
titulo: Injeção de falhas da CobaiaAPI
sistema: CobaiaAPI
entidade_principal: Infraestrutura
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/routers/admin_fault.py, Programacao/CobaiaAPI/.env.example]
endpoints: [GET /api/admin/fault-mode, POST /api/admin/fault-mode]
sintomas: [um campo alterado e o resto integro, 500 com fault injection, atraso fixo de 2 s, corpo cortado]
palavras_chave: [fault, injecao, falha, modo, error_500, latency, type_drift, field_missing, field_renamed, malformed_json, target_field, probability, X-Admin-Token]
causas_relacionadas: [erro_interno_do_servidor, tempo_de_resposta_excedido, tipo_divergente, campo_ausente, campo_renomeado, resposta_truncada]
verbete: falhas_injetadas/modos-de-injecao.md
hash_do_verbete: 31eb2d19d8eebcc2
gerado_em: 2026-11-07
curado: sim
---

# Injeção de falhas da CobaiaAPI

Camada de leitura do verbete `modos-de-injecao` (`biblioteca_producao/falhas_injetadas/modos-de-injecao.md`). Tipo: funcionamento (descreve como uma parte do sistema funciona); estado: ativo (em vigor); sistema: CobaiaAPI (a API); entidade principal: Infraestrutura.

## O que é

Injetor com 7 modos: error_500, latency (2 s), type_drift (campo-alvo vira texto), field_missing (remove), field_renamed (vira <campo>_v2), malformed_json (corpo cortado) e normal.

## Como aparece na tela

- só um campo alterado, resto íntegro: modo com campo-alvo.
- detail "fault injection: error_500 em produto".

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `um campo alterado e o resto integro`, `500 com fault injection`, `atraso fixo de 2 s`, `corpo cortado`.

## O que conferir

Causa, como o verbete a descreve: Ligado por FAULT_MODE/FAULT_TARGET_FIELD no .env ou POST /api/admin/fault-mode com o cabeçalho `X-Admin-Token` (a chave de acesso do administrador); probability < 1 dá intermitência.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `erro_interno_do_servidor` (Erro interno do servidor (500)), `tempo_de_resposta_excedido` (Tempo de resposta excedido), `tipo_divergente` (Tipo divergente), `campo_ausente` (Campo ausente), `campo_renomeado` (Campo renomeado), `resposta_truncada` (Resposta truncada).

## Onde está no código

- Arquivos: `Programacao/CobaiaAPI/app/fault_injection.py`, `Programacao/CobaiaAPI/app/routers/admin_fault.py`, `Programacao/CobaiaAPI/.env.example`.
- Rotas da API (campo `endpoints`): `GET /api/admin/fault-mode`, `POST /api/admin/fault-mode`.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `fault`, `injecao`, `falha`, `modo`, `error_500`, `latency`, `type_drift`, `field_missing`, `field_renamed`, `malformed_json`, `target_field`, `probability`, `X-Admin-Token`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Leitura revisada e aprovada. O nome do cabeçalho de administração ficou entre crases, com o significado ao lado, para o filtro de termos técnicos do pacote Q2. A leitura não tinha notas do modelo e descreve com exatidão o mecanismo do injetor de falhas.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
