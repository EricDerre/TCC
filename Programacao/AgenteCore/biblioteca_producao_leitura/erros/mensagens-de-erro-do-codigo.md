---
# ! Alteração de IA - Revisar: camada de leitura do verbete `mensagens-de-erro-do-codigo`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/erros/mensagens-de-erro-do-codigo.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; a explicação tinha sido posta dentro das aspas, e a mensagem que a API devolve de verdade é só "token inválido"; entre crases o texto literal não conta como termo sem explicação; a nota falava em "poluição semântica residual", que não descreve nada desta camada, e citava o termo fora de crases, o que fazia a leitura reprovar no mesmo filtro que a nota dizia atender.
id: mensagens-de-erro-do-codigo
titulo: Índice de mensagens literais do código
sistema: Ambos
entidade_principal: Infraestrutura
tipo: funcionamento
status: ativo
arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py, Programacao/CobaiaFront/rodape_contato_envia.php]
sintomas: [mensagem de erro na tela, detail no json de erro]
palavras_chave: [mensagem, literal, detail, erro ao carregar, nenhum produto retornado, atencao erro, token invalido, modo invalido, falha no email, indice]
causas_relacionadas: [recurso_inexistente, erro_interno_do_servidor, corpo_nao_e_json, corpo_vazio, estado_da_tela_divergente]
verbete: erros/mensagens-de-erro-do-codigo.md
hash_do_verbete: 752e16f29bbdc4ab
gerado_em: 2026-11-07
curado: sim
---

# Índice de mensagens literais do código

Camada de leitura do verbete `mensagens-de-erro-do-codigo` (`biblioteca_producao/erros/mensagens-de-erro-do-codigo.md`). Tipo: funcionamento (descreve como uma parte do sistema funciona); estado: ativo (em vigor); sistema: Ambos (o site PHP e a API); entidade principal: Infraestrutura.

## O que é

Página: "Carregando produtos da CobaiaAPI..."; "Nenhum produto retornado pela API." (não é lista, ou vazia); "Erro ao carregar produtos da CobaiaAPI: <msg>" ("HTTP <n>" se resp.ok falso). API: "produto/cliente/pedido não encontrado" (404), `"token inválido"` (403: a chave de acesso do administrador foi recusada), "modo inválido" (400), "fault injection: error_500 em <ent>" (500). PHP: "Atenção ERRO: ..." (connect.php:16), "falha no email" (rodape_contato_envia.php:33).

## Como aparece na tela

- O verbete não lista sinais; valem os sintomas do cabeçalho, abaixo.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `mensagem de erro na tela`, `detail no json de erro`.

## O que conferir

O verbete não descreve a causa nem como confirmar; confira pelos sinais acima e pelos arquivos abaixo.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `recurso_inexistente` (Recurso inexistente (404 e vizinhos)), `erro_interno_do_servidor` (Erro interno do servidor (500)), `corpo_nao_e_json` (Corpo não é JSON), `corpo_vazio` (Corpo vazio), `estado_da_tela_divergente` (Estado da tela divergente da resposta).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/produtos_api.php`, `Programacao/CobaiaFront/conn/connect.php`, `Programacao/CobaiaAPI/app/routers/produtos.py`, `Programacao/CobaiaAPI/app/routers/pedidos.py`, `Programacao/CobaiaAPI/app/routers/admin_fault.py`, `Programacao/CobaiaFront/rodape_contato_envia.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: nenhuma declarada.
- Palavras que a busca usa para achar este verbete: `mensagem`, `literal`, `detail`, `erro ao carregar`, `nenhum produto retornado`, `atencao erro`, `token invalido`, `modo invalido`, `falha no email`, `indice`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Leitura revisada e aprovada. A mensagem literal da API ficou entre crases, com o significado ao lado, para o filtro de termos técnicos do pacote Q2. O documento funciona como um dicionário das mensagens fixas do código, e a leitura não tinha notas do modelo.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
