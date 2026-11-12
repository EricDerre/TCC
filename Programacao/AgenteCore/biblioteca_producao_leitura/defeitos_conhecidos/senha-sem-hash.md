---
# ! Alteração de IA - Revisar: camada de leitura do verbete `senha-sem-hash`, GERADA por biblioteca_leitura.py a partir do cabeçalho e das seções de biblioteca_producao/defeitos_conhecidos/senha-sem-hash.md (Pós-Fase 4, pacote Q1, decisão 103); pronta para curadoria à mão.
# ! Motivo: o verbete que o modelo lê não muda (a biblioteca de produção continua com o mesmo hash); o que chega ao analista sai desta camada, na regra de escrita dos comentários deste repositório (direto, sem jargão, código de situação com o significado junto). Com `curado: sim` o gerador deixa de regravar o arquivo.
# ! Alteração de IA - Revisar: (10/11/2026) 3 consertos do Claude no texto que o analista escreveu na curadoria desta leitura; o antes e o depois de cada troca estão em Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md.
# ! Motivo: o que foi revisado é a leitura; o verbete que o modelo lê não mudou; o termo continuava sem o significado na primeira menção, e os filtros de texto do pacote Q2 seguiam reprovando a leitura; a nota chamava as épocas de "treinamento"; neste projeto o modelo não é treinado: época é a rodada em que ele propôs acréscimos à biblioteca; a nota retirada continua no verbete que o modelo lê.
id: senha-sem-hash
titulo: Senha em texto puro, MD5 na edição, sem hash no login
sistema: CobaiaFront
entidade_principal: Usuario
tipo: defeito_conhecido
status: nao_corrigido
arquivos: [Programacao/CobaiaFront/admin/usuario_insere.php, Programacao/CobaiaFront/admin/usuario_atualiza.php, Programacao/CobaiaFront/admin/login.php]
tabelas: [tbusuarios]
sintomas: [usuario nao consegue entrar apos edicao, redirecionado para invasor]
palavras_chave: [senha, md5, hash, texto puro, login, invasor, usuario_insere, usuario_atualiza]
causas_relacionadas: [estado_da_tela_divergente, valor_fora_do_dominio]
verbete: defeitos_conhecidos/senha-sem-hash.md
hash_do_verbete: 92fbc53c65361c7b
gerado_em: 2026-11-07
curado: sim
---

# Senha em texto puro, MD5 na edição, sem hash no login

Camada de leitura do verbete `senha-sem-hash` (`biblioteca_producao/defeitos_conhecidos/senha-sem-hash.md`). Tipo: defeito_conhecido (um defeito real do código cedido, mantido de propósito); estado: nao_corrigido (defeito sem correção no código cedido); sistema: CobaiaFront (o site PHP); entidade principal: Usuario.

## O que é

Cadastro grava senha em texto puro (usuario_insere.php), edição grava MD5 (usuario_atualiza.php), login compara sem hash, o resumo embaralhado da senha, que não se desfaz (login.php:7). Mantido de propósito.

## Como aparece na tela

- usuário deixa de entrar depois de editado no painel.

Sintomas que a busca reconhece (campo `sintomas` do cabeçalho): `usuario nao consegue entrar apos edicao`, `redirecionado para invasor`.

## O que conferir

Causa, como o verbete a descreve: Após edição a senha guardada é MD5 e o login compara com o texto digitado: nunca bate; cai em invasor.php. As contas do seed estão em texto puro e funcionam.

Causas vizinhas, que se confundem com esta (campo `causas_relacionadas`): `estado_da_tela_divergente` (Estado da tela divergente da resposta), `valor_fora_do_dominio` (Valor fora do domínio).

## Onde está no código

- Arquivos: `Programacao/CobaiaFront/admin/usuario_insere.php`, `Programacao/CobaiaFront/admin/usuario_atualiza.php`, `Programacao/CobaiaFront/admin/login.php`.
- Rotas da API: nenhuma declarada.
- Tabelas do banco: `tbusuarios`.
- Palavras que a busca usa para achar este verbete: `senha`, `md5`, `hash`, `texto puro`, `login`, `invasor`, `usuario_insere`, `usuario_atualiza`.

## Notas do modelo

Nenhuma nota do modelo neste verbete.

## Curadoria

Leitura revisada e aprovada. O termo `hash` foi explicado no texto, para o filtro de termos técnicos do pacote Q2. O documento aborda com precisão o defeito intencional de desalinhamento de senhas no sistema legado PHP. A leitura não tinha notas do modelo.

Curada em 10/11/2026 por um analista, com o Eric passando a leitura e colando a resposta, na página da curadoria: texto revisado. Depois, 3 consertos do Claude neste texto, a pedido do Eric (o que mudou e por quê: `Programacao/AgenteCore/experimentos/resultados_alvo/fase4/curadoria_leituras/consertos.md`).
