---
# ! Alteração de IA - Revisar: camada de leitura do verbete `consultas-sem-checagem`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/defeitos_conhecidos/consultas-sem-checagem.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
id: consultas-sem-checagem
titulo: Consultas sem checagem e cancelamento sem dono
sistema: CobaiaFront
entidade_principal: Pedido
tipo: defeito_conhecido
status: nao_corrigido
arquivos: [Programacao/CobaiaFront/cliente/registrar_reserva.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php, Programacao/CobaiaFront/conn/connect.php]
tabelas: [tbpedido_reserva]
sintomas: [reserva confirmada que nao aparece, reserva de outro cliente cancelada, redireciona sem gravar]
palavras_chave: [query, mysqli, retorno, checagem, silencioso, cancelar, id_pedido, url, dono, redirect]
causas_relacionadas: [dado_desatualizado, estado_da_tela_divergente, registro_duplicado]
verbete: defeitos_conhecidos/consultas-sem-checagem.md
hash_do_verbete: 223f7fb4798ff500
gerado_em: 2026-11-07
curado: sim
---

# Consultas sem checagem e cancelamento sem dono

Camada de leitura do verbete `consultas-sem-checagem` (`biblioteca_producao/defeitos_conhecidos/consultas-sem-checagem.md`). Tipo: defeito_conhecido (um defeito real do código cedido, mantido de propósito); estado: nao_corrigido (defeito sem correção no código cedido); sistema: CobaiaFront (o site PHP); entidade principal: Pedido.

## O que é

Nenhuma página PHP confere o retorno de $conn->query(): INSERT/UPDATE que falha segue em silêncio e a página redireciona como se tivesse gravado. cliente_cancelar.php:6 aceita qualquer id_pedido pela URL, sem checar o dono.

## Como aparece na tela

- reserva "confirmada" que não aparece depois.
- reserva de outra pessoa cancelada.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `reserva confirmada que nao aparece`, `reserva de outro cliente cancelada`, `redireciona sem gravar`.

## O que conferir

Causa, como o verbete a descreve: mysqli não lança exceção por padrão; a falha só aparece como dado ausente ou tela que não muda.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `dado_desatualizado` (Dado desatualizado (cache)), `estado_da_tela_divergente` (Estado da tela divergente da resposta), `registro_duplicado` (Registro duplicado).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/cliente/registrar_reserva.php`, `Programacao/CobaiaFront/cliente/cliente_cancelar.php`, `Programacao/CobaiaFront/conn/connect.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: `tbpedido_reserva`.
- Palavras que a busca usa para achar este verbete: `query`, `mysqli`, `retorno`, `checagem`, `silencioso`, `cancelar`, `id_pedido`, `url`, `dono`, `redirect`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: aprovada como estava.
