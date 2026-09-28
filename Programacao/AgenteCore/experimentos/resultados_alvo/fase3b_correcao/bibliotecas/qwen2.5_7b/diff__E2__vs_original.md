<!-- ! Alteração de IA - Revisar: diff entre duas cópias da biblioteca (epoca-0 -> epoca-2), GERADO por evolucao_biblioteca.escrever_diff.
     ! Motivo: os totais e o diff abaixo vêm de comparar os arquivos .md das duas
     pastas byte a byte; reescrever isto à mão ficaria desatualizado na próxima
     época — não editar, só regravar. -->

# Diff da biblioteca: epoca-0 -> epoca-2

| Métrica | Valor |
|---|---|
| Arquivos novos | 43 |
| Arquivos removidos | 0 |
| Arquivos tocados | 0 |
| Linhas acrescentadas | 1151 |
| Linhas removidas | 0 |
| Caracteres antes | 0 |
| Caracteres depois | 70758 |
| Caracteres acrescentados | 70758 |
| Tokens estimados acrescentados | 27215 |

```diff
--- epoca-0/aprendidos/atualizacao-da-interface.md
+++ epoca-2/aprendidos/atualizacao-da-interface.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 2 a partir do caso efe-10 (Fase 3).
+# ! Motivo: Este verbete ajudaria a prevenir futuros casos onde a interface não reflete as atualizações da API devido a problemas de sincronização.
+id: atualizacao-da-interface
+titulo: Atualização da Interface
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+sintomas: [interface desatualizada, divergencia entre api e interface]
+palavras_chave: [atualizacao, interface, sincronismo]
+causas_relacionadas: [dado_desatualizado, estado_da_tela_divergente]
+---
+## Resumo
+Adicionar verbete sobre a importância de manter a interface atualizada com a API, evitando divergências.
+
+## Sinais
+- interface desatualizada
+- divergencia entre api e interface
--- epoca-0/aprendidos/atualizacao_imediata.md
+++ epoca-2/aprendidos/atualizacao_imediata.md
@@ -0,0 +1,15 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso efe-13 (Fase 3).
+# ! Motivo: Este novo verbete explica a prática atual de atualização imediata, que foi a causa da visualização de dados desatualizados neste caso.
+id: atualizacao_imediata
+titulo: Atualização imediata do grid
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php]
+palavras_chave: [innerhtml, sobrescrita, grid]
+causas_relacionadas: [estado_da_tela_divergente]
+---
+## Resumo
+O grid é atualizado imediatamente com innerHTML, independentemente do status da requisição. Isso pode resultar em visualização de dados antigos.
--- epoca-0/aprendidos/conversao-de-unidade.md
+++ epoca-2/aprendidos/conversao-de-unidade.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso tra-6 (Fase 3).
+# ! Motivo: Este caso demonstra a importância de explicitar a necessidade de aplicar o fator correto na conversão de unidades monetárias, evitando erros de escala.
+id: conversao-de-unidade
+titulo: Conversão de unidade
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
+sintomas: [precos cem vezes menores]
+palavras_chave: [fator, decimal, unidade]
+causas_relacionadas: [escala_ou_unidade_errada]
+---
+## Resumo
+Adicionar instruções sobre a necessidade de aplicar o fator correto na conversão do valor_produto.
+
+## Sinais
+- precos cem vezes menores
--- epoca-0/aprendidos/conversao-de-valor.md
+++ epoca-2/aprendidos/conversao-de-valor.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso tra-12 (Fase 3).
+# ! Motivo: Este caso demonstrou a necessidade de uma regra específica para a conversão de valores DECIMAL para float, para evitar arredondamentos incorretos.
+id: conversao-de-valor
+titulo: Conversão de valor DECIMAL para float
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py]
+sintomas: [arredondamento incorreto, valor fora do dominio]
+palavras_chave: [conversao, arredondamento, decimal, float]
+causas_relacionadas: [escala_ou_unidade_errada, valor_fora_do_dominio]
+---
+## Resumo
+Adicionar regra para conversão correta de valor DECIMAL para float no _to_dict.
+
+## Sinais
+- arredondamento incorreto
+- valor fora do dominio
--- epoca-0/aprendidos/interface-estados.md
+++ epoca-2/aprendidos/interface-estados.md
@@ -0,0 +1,19 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso efe-4 (Fase 3).
+# ! Motivo: Este novo verbete ajudaria a documentar a necessidade de estados consistentes na interface, facilitando diagnósticos futuros.
+id: interface-estados
+titulo: Estados da Interface
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+sintomas: [lista vazia, botao que nao muda]
+palavras_chave: [estado, interface, atualizacao]
+causas_relacionadas: [estado_da_tela_divergente]
+---
+## Resumo
+Definir estados claros para a interface e garantir que a lógica de atualização esteja corretamente implementada.
+
+## Sinais
+- lista vazia
+- botao que nao muda
--- epoca-0/aprendidos/interface-frontend.md
+++ epoca-2/aprendidos/interface-frontend.md
@@ -0,0 +1,14 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso efe-10 (Fase 3).
+# ! Motivo: Este novo verbete ajudaria a documentar a interação entre a API e a interface, destacando a necessidade de atualizações corretas do DOM e a dependência de redirects, prevenindo divergências de estado.
+id: interface-frontend
+titulo: Interface Frontend
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: aprendido
+status: ativo
+palavras_chave: [atualizacao, dom, innerhtml, redirect]
+causas_relacionadas: [estado_da_tela_divergente, tipo_divergente]
+---
+## Resumo
+Adicionar a interface frontend como uma entidade, destacando a importância de atualizações corretas do DOM e a dependência de redirects.
--- epoca-0/aprendidos/rotas-inexistentes.md
+++ epoca-2/aprendidos/rotas-inexistentes.md
@@ -0,0 +1,20 @@
+---
+# ! Alteração de IA - Revisar: verbete criado pelo modelo qwen2.5:7b na época 1 a partir do caso run-8 (Fase 3).
+# ! Motivo: Este caso mostrou a necessidade de um verbete dedicado para rotas inexistentes, pois a documentação atual não abrange essa situação específica.
+id: rotas-inexistentes
+titulo: Rotas Inexistentes
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: aprendido
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py]
+sintomas: [404 com id valido, rota inexistente]
+palavras_chave: [404, rotas, id, rota]
+causas_relacionadas: [recurso_inexistente]
+---
+## Resumo
+Adicionar um novo verbete para rotas inexistentes, especificando que um 404 com id válido pode indicar que a rota ou recurso buscado não existe.
+
+## Sinais
+- 404 com id valido
+- rota inexistente
--- epoca-0/contratos/contrato-pedido.md
+++ epoca-2/contratos/contrato-pedido.md
@@ -0,0 +1,26 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (contrato).
+# ! Motivo: reúne os três endpoints de pedido, os códigos de erro reais e a divergência
+# de busca (exata na API, substring no PHP). Conferido em pedidos.py e cliente/index.php.
+id: contrato-pedido
+titulo: Contrato de /api/pedidos
+sistema: CobaiaAPI
+entidade_principal: Pedido
+tipo: contrato
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaFront/cliente/index.php]
+endpoints: [GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
+tabelas: [tbpedido_reserva, tbusuarios]
+sintomas: [data em outro formato, status desconhecido, 422 sem login, cliente nao encontrado]
+palavras_chave: [contrato, pedidos, reservas, login, cpf, id_pedido, pessoas, data_pedido, status, nome, 201, 404, 422, cancelar]
+causas_relacionadas: [formato_de_data_divergente, valor_fora_do_dominio, recurso_inexistente, campo_ausente]
+---
+## Resumo
+GET /api/pedidos?login=<cpf>; POST /api/pedidos {id_clientes, pessoas, data_pedido} → 201; POST /api/pedidos/{id}/cancelar. Campos: id_pedido, pessoas, data_pedido AAAA-MM-DD, status 'Em Análise'|'Cancelado', nome, cpf.
+
+## Sinais
+- data noutro formato ou como número
+- status fora dos dois valores
+
+## Causa
+cpf vem de login_usuario (pedidos.py). Busca exata na API; o site usa LIKE '%login%' (cliente/index.php:4).
--- epoca-0/contratos/contrato-produto.md
+++ epoca-2/contratos/contrato-produto.md
@@ -0,0 +1,34 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (contrato).
+# ! Motivo: campo a campo, com a diferença declarado × real (Decimal no schema, número
+# em ponto flutuante no fio). Conferido em schemas.py e produtos.py.
+id: contrato-produto
+titulo: Contrato de /api/produtos
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: contrato
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/schemas.py, Programacao/CobaiaAPI/app/routers/produtos.py]
+endpoints: [GET /api/produtos, GET /api/produtos/{id}]
+tabelas: [tbprodutos, tbtipos]
+sintomas: [chave a mais ou a menos, lista no lugar de objeto, preco como texto, lista incompleta, ultimo item cortado, lista onde se espera objeto, ou o inverso]
+palavras_chave: [contrato, produtos, id, nome, resumo, tipo, preco, imagem, destaque, lista, objeto, 404, produto nao encontrado, schema, json, campos, divergencia]
+causas_relacionadas: [campo_ausente, campo_renomeado, colecao_no_lugar_de_objeto, tipo_divergente, recurso_inexistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-6) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
+---
+## Resumo
+GET /api/produtos devolve lista; GET /api/produtos/{id} devolve objeto (404 "produto não encontrado"). Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano.
+
+## Sinais
+- chave a mais ou a menos: campo ausente ou renomeado
+- lista onde se espera objeto, ou o inverso
+
+## Causa
+Origem tbprodutos + rótulo de tbtipos (produtos.py _to_dict). preco sai 89.9 (número), embora o schema declare Decimal.
+
+## Notas do modelo
+- [E1 · lex-5 · nota] Notar que o contrato especifica a estrutura do JSON esperado, mas não aborda o truncamento de resposta. — Motivo: Destacar a necessidade de incluir o risco de truncamento de resposta no contrato, pois é uma causa comum de problemas de integração.
+- [E1 · sin-6 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Corrigir "preco número" para "preco Decimal" para refletir o tipo correto em valor_produto. — Motivo: Este trecho mostra a divergência entre o tipo declarado no contrato e o tipo real na resposta, evidenciando a necessidade de manter a consistência entre ambos.
+- [E1 · sin-13 · retificação de "Campos: id inteiro, nome texto, resumo texto|nulo, tipo texto, preco número, imagem texto|nulo, destaque booleano."] Adicionar observação sobre possíveis nomes diferentes para o campo tipo no verbete. — Motivo: O caso mostrou que o campo tipo pode ser renomeado ou ter seu tipo divergente, necessitando de uma observação explícita no verbete.
--- epoca-0/defeitos_conhecidos/ancora-saiba-mais.md
+++ epoca-2/defeitos_conhecidos/ancora-saiba-mais.md
@@ -0,0 +1,24 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (defeito conhecido).
+# ! Motivo: defeito real do código cedido, mantido de propósito; a linha 34 do mesmo
+# arquivo está certa e serve de contraste. Conferido em produtos_geral.php.
+id: ancora-saiba-mais
+titulo: Link "Saiba Mais..." abre produto vazio
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: defeito_conhecido
+status: nao_corrigido
+arquivos: [Programacao/CobaiaFront/produtos_geral.php, Programacao/CobaiaFront/produto_detalhes.php]
+sintomas: [saiba mais abre produto vazio, id_produto vazio na url, link nao encontrado pelo roteiro]
+palavras_chave: [saiba mais, ancora, href, aspas, id_produto, produtos_geral, detalhe, link]
+causas_relacionadas: [localizador_quebrado, recurso_inexistente, estado_da_tela_divergente]
+---
+## Resumo
+Nas listagens do site PHP, "Saiba Mais..." abre produto_detalhes.php?id_produto= vazio: a aspa que fecha o href vem antes do id (produtos_geral.php:51); o link da imagem (linha 34) está certo.
+
+## Sinais
+- Saiba Mais leva a produto sem dados
+- roteiro que procura o link pelo id não o encontra
+
+## Causa
+Defeito do código original, sem correção. Na aba de API o botão é button.saiba-mais[data-id], sem esse problema.
--- epoca-0/defeitos_conhecidos/consultas-sem-checagem.md
+++ epoca-2/defeitos_conhecidos/consultas-sem-checagem.md
@@ -0,0 +1,25 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (defeito conhecido).
+# ! Motivo: nenhuma página confere o retorno de query(), e o cancelamento aceita qualquer
+# id pela URL — duas ausências reais que produzem "gravou mas não aparece".
+id: consultas-sem-checagem
+titulo: Consultas sem checagem e cancelamento sem dono
+sistema: CobaiaFront
+entidade_principal: Pedido
+tipo: defeito_conhecido
+status: nao_corrigido
+arquivos: [Programacao/CobaiaFront/cliente/registrar_reserva.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php, Programacao/CobaiaFront/conn/connect.php]
+tabelas: [tbpedido_reserva]
+sintomas: [reserva confirmada que nao aparece, reserva de outro cliente cancelada, redireciona sem gravar]
+palavras_chave: [query, mysqli, retorno, checagem, silencioso, cancelar, id_pedido, url, dono, redirect]
+causas_relacionadas: [dado_desatualizado, estado_da_tela_divergente, registro_duplicado]
+---
+## Resumo
+Nenhuma página PHP confere o retorno de $conn->query(): INSERT/UPDATE que falha segue em silêncio e a página redireciona como se tivesse gravado. cliente_cancelar.php:6 aceita qualquer id_pedido pela URL, sem checar o dono.
+
+## Sinais
+- reserva "confirmada" que não aparece depois
+- reserva de outra pessoa cancelada
+
+## Causa
+mysqli não lança exceção por padrão; a falha só aparece como dado ausente ou tela que não muda.
--- epoca-0/defeitos_conhecidos/senha-sem-hash.md
+++ epoca-2/defeitos_conhecidos/senha-sem-hash.md
@@ -0,0 +1,24 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (defeito conhecido).
+# ! Motivo: inconsistência real entre cadastro, edição e login, mantida de propósito;
+# explica por que uma conta editada pelo painel deixa de entrar. Conferido nos três php.
+id: senha-sem-hash
+titulo: Senha em texto puro, MD5 na edição, sem hash no login
+sistema: CobaiaFront
+entidade_principal: Usuario
+tipo: defeito_conhecido
+status: nao_corrigido
+arquivos: [Programacao/CobaiaFront/admin/usuario_insere.php, Programacao/CobaiaFront/admin/usuario_atualiza.php, Programacao/CobaiaFront/admin/login.php]
+tabelas: [tbusuarios]
+sintomas: [usuario nao consegue entrar apos edicao, redirecionado para invasor]
+palavras_chave: [senha, md5, hash, texto puro, login, invasor, usuario_insere, usuario_atualiza]
+causas_relacionadas: [estado_da_tela_divergente, valor_fora_do_dominio]
+---
+## Resumo
+Cadastro grava senha em texto puro (usuario_insere.php), edição grava MD5 (usuario_atualiza.php), login compara sem hash (login.php:7). Mantido de propósito.
+
+## Sinais
+- usuário deixa de entrar depois de editado no painel
+
+## Causa
+Após edição a senha guardada é MD5 e o login compara com o texto digitado — nunca bate; cai em invasor.php. As contas do seed estão em texto puro e funcionam.
--- epoca-0/erros/campo_ausente.md
+++ epoca-2/erros/campo_ausente.md
@@ -0,0 +1,30 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: descreve o que o JS faz com um campo que falta (undefined), conferido em
+# produtos_api.php, e o modo field_missing que produz o sintoma.
+id: campo_ausente
+titulo: Campo ausente
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: campo_ausente
+arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
+endpoints: [GET /api/produtos, GET /api/pedidos]
+sintomas: [cartao sem titulo, sem nome, undefined na tela, botao que nao faz nada, nulo_inesperado]
+palavras_chave: [ausente, falta, faltando, sem o campo, undefined, field_missing, chave]
+causas_relacionadas: [campo_renomeado, nulo_inesperado, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: nota acrescentada.
+---
+## Resumo
+Uma chave do contrato não vem no objeto — nem com nulo. No JavaScript a leitura vira undefined.
+
+## Sinais
+- nome ausente: cartão "(sem nome)"; preço ausente: botão imprime "undefined"
+- id ausente: botão de detalhe ou cancelar sem identificador, clique sem efeito
+
+## Causa
+O modo field_missing remove o campo-alvo (fault_injection.py). Diferença para campo_renomeado: nenhuma chave nova aparece no lugar.
+
+## Notas do modelo
+- [E1 · sin-1 · nota] Adicionar nota sobre a remoção de campos no fault_injection.py. — Motivo: O caso demonstrou que a remoção de campos pode causar sintomas como 'undefined', indicando a necessidade de documentar melhor esse cenário.
--- epoca-0/erros/campo_renomeado.md
+++ epoca-2/erros/campo_renomeado.md
@@ -0,0 +1,30 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: o modo field_renamed acrescenta o sufixo _v2; a distinção para campo_ausente é
+# a chave nova com o mesmo valor. Conferido em fault_injection.py.
+id: campo_renomeado
+titulo: Campo renomeado
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: campo_renomeado
+arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/schemas.py]
+endpoints: [GET /api/produtos, GET /api/pedidos]
+sintomas: [chave desconhecida no lugar da esperada, _v2, campo com outro nome, titulo vazio, nome correto, categoria e preco corretos]
+palavras_chave: [renomead, outro nome, _v2, descricao, situacao, imagem_url, field_renamed, chave inesperada, campo-renomeado, contrato, cliente]
+causas_relacionadas: [campo_ausente, estrutura_aninhada_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-9) - Revisar: retificação acrescentada.
+---
+## Resumo
+O valor existe sob outra chave: falta a esperada e aparece uma desconhecida com o mesmo tipo e conteúdo (preco → preco_v2, nome → descricao, status → situacao).
+
+## Sinais
+- o resto do objeto confere; uma chave sumiu e outra sobrou
+- vazio ou undefined só naquele campo
+
+## Causa
+O modo field_renamed troca o campo-alvo por <campo>_v2 (fault_injection.py). Fora dele: contrato mudou no servidor sem atualizar o cliente.
+
+## Notas do modelo
+- [E1 · sin-9 · retificação de "Fora dele: contrato mudou no servidor sem atualizar o cliente."] Corrigir a afirmação para "Contrato mudou no servidor sem atualizar o cliente e API não reflete as mudanças." — Motivo: O caso mostrou que a documentação não refletiu a necessidade de atualizar o cliente quando o contrato muda, causando a renomeação do campo sem que o cliente o refletisse.
--- epoca-0/erros/chave_de_juncao_errada.md
+++ epoca-2/erros/chave_de_juncao_errada.md
@@ -0,0 +1,31 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: registra as junções reais (FK de tipo e de cliente) e o LIKE por substring do
+# site, que pode casar mais de um cliente. Conferido em models.py e cliente/index.php.
+id: chave_de_juncao_errada
+titulo: Chave de junção errada
+sistema: Ambos
+entidade_principal: Pedido
+tipo: erro
+status: ativo
+causa_raiz: chave_de_juncao_errada
+arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaFront/cliente/index.php]
+endpoints: [GET /api/produtos, GET /api/pedidos]
+tabelas: [tbprodutos, tbtipos, tbusuarios, tbpedido_reserva]
+sintomas: [nome de outra pessoa na reserva, categoria errada, imagem de outro produto, nome da categoria no titulo]
+palavras_chave: [juncao, join, chave, id, fk, cliente errado, categoria errada, troca, admin, like, substring, registro errado, campo derivado]
+causas_relacionadas: [nulo_inesperado, escala_ou_unidade_errada, valor_fora_do_dominio]
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-3) - Revisar: retificação acrescentada.
+---
+## Resumo
+Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva.
+
+## Sinais
+- afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios
+- o dado existe no banco, ligado ao registro errado
+
+## Causa
+Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente.
+
+## Notas do modelo
+- [E1 · tra-3 · retificação de "Tipo e formato certos, mas o valor é de OUTRO registro: categoria ou imagem alheia no produto, nome ou cpf de outro usuário na reserva. Sinais: afeta campo derivado de junção (tipo, nome, cpf, imagem), não os próprios; o dado existe no banco, ligado ao registro errado. Causa: Junções: id_tipo_produto e id_clientes (models.py). No site, cliente/index.php:4 usa LIKE '%login%' — CPF substring de outro casa mais de um cliente."] Corrigir a junção entre tbprodutos e tbtipos, garantindo que id_tipo_produto esteja corretamente ligado a tbtipos.id_tipo. — Motivo: O sintoma mostrou que a categoria do produto estava incorreta, indicando uma junção errada entre as tabelas.
--- epoca-0/erros/codificacao_incorreta.md
+++ epoca-2/erros/codificacao_incorreta.md
@@ -0,0 +1,24 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: o charset é fixado em três pontos (connect.php, config.py, schema); conferido.
+id: codificacao_incorreta
+titulo: Codificação de caracteres incorreta
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: codificacao_incorreta
+arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/config.py, Programacao/CobaiaFront/banco/schema_completo.sql]
+sintomas: [acentos trocados por simbolos, caracteres estranhos nos nomes, texto legivel mas com acentos errados]
+palavras_chave: [codificacao, encoding, utf-8, utf8, latin-1, acento, mojibake, charset, duplo, ã, Ã]
+causas_relacionadas: [corpo_nao_e_json, tipo_divergente]
+---
+## Resumo
+JSON válido e estrutura certa, mas textos com acento corrompidos: bytes latin-1 declarados utf-8, ou utf-8 convertido duas vezes ("Pão" vira "PÃ£o").
+
+## Sinais
+- só campos de texto livre afetados; números e chaves intactos
+- parte dos registros certa e parte errada: conversão dupla parcial
+
+## Causa
+Banco e conexões em utf8 (connect.php:7, config.py); se corrompe, o dado foi gravado errado ou um intermediário reconverteu.
--- epoca-0/erros/colecao_no_lugar_de_objeto.md
+++ epoca-2/erros/colecao_no_lugar_de_objeto.md
@@ -0,0 +1,32 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: lista × objeto é a diferença entre as duas rotas de produto; conferido em
+# produtos.py e no modal de produtos_api.php.
+id: colecao_no_lugar_de_objeto
+titulo: Coleção no lugar de objeto (ou o inverso)
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: colecao_no_lugar_de_objeto
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_api.php]
+endpoints: [GET /api/produtos, GET /api/produtos/{id}]
+sintomas: [detalhe sem preencher campos, colchetes ao redor do valor, nenhum produto retornado]
+palavras_chave: [lista, array, colecao, objeto, unico, recurso, colchetes, detalhe, modal]
+causas_relacionadas: [estrutura_aninhada_divergente, campo_ausente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-8) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-15) - Revisar: retificação acrescentada.
+---
+## Resumo
+Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (["Carnes"]).
+
+## Sinais
+- modal "Produto #1"/"(sem descrição)": p é lista
+- categoria com colchetes: campo veio como lista
+
+## Causa
+GET /api/produtos devolve lista, GET /api/produtos/{id} objeto (produtos.py); a página não confere a forma antes de ler os campos.
+
+## Notas do modelo
+- [E1 · sin-8 · retificação de "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes'])."] Corrigir que GET /api/produtos/{id} deve devolver um objeto, não uma lista. — Motivo: O caso mostrou que a documentação não especificava claramente que GET /api/produtos/{id} deve retornar um único objeto, causando confusão.
+- [E1 · sin-15 · retificação de "Forma trocada: lista onde se esperava objeto único (GET /api/produtos/{id} devolvendo [{...}]), objeto onde se esperava lista, ou escalar como lista (['Carnes'])."] Corrigir que o campo "tipo" deve ser tratado como uma string, não uma lista. — Motivo: O sintoma mostrou que o campo "tipo" foi tratado como uma lista, quando na verdade é uma string.
--- epoca-0/erros/contagem_inconsistente.md
+++ epoca-2/erros/contagem_inconsistente.md
@@ -0,0 +1,27 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: a API real não tem total nem paginação — qualquer envelope com contagem já
+# é sinal de outra origem; conferido em produtos.py.
+id: contagem_inconsistente
+titulo: Contagem inconsistente
+sistema: Ambos
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: contagem_inconsistente
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_destaque.php]
+endpoints: [GET /api/produtos]
+tabelas: [tbprodutos]
+sintomas: [total diferente dos itens, pagina vazia com total positivo, quatro destaques mas cinco cartoes]
+palavras_chave: [contagem, total, itens, pagina, paginacao, quantidade, destaques, inconsistente, zero]
+causas_relacionadas: [estrutura_aninhada_divergente, dado_desatualizado, estado_da_tela_divergente]
+---
+## Resumo
+Dois números que deveriam bater não batem: total 14 e lista com 1; total 0 com itens; página 2 vazia com total 14; contador de destaques diferente dos cartões.
+
+## Sinais
+- total e lista vêm de consultas diferentes
+- rótulo numérico que não corresponde ao renderizado
+
+## Causa
+GET /api/produtos devolve a lista crua, sem total nem paginação (produtos.py:34-43); o seed tem 14 produtos, 5 em destaque. Envelope com total indica outra versão.
--- epoca-0/erros/corpo_nao_e_json.md
+++ epoca-2/erros/corpo_nao_e_json.md
@@ -0,0 +1,31 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: um verbete por rótulo do conjunto fechado, com o ponto real do código que
+# produz o sintoma neste sistema; conferido em connect.php e produtos_api.php.
+id: corpo_nao_e_json
+titulo: Corpo não é JSON
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: corpo_nao_e_json
+arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaFront/produtos_api.php]
+sintomas: [token inesperado no inicio da resposta, html no lugar de json, warning do php antes do json, parse_falho, listagem_nao_carrega]
+palavras_chave: [json, html, xml, parse, token inesperado, warning, fatal, gateway, proxy, atencao erro, content-type, erro de sintaxe, parse_falho]
+causas_relacionadas: [resposta_truncada, corpo_vazio, erro_interno_do_servidor]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-2) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-9) - Revisar: nota acrescentada.
+---
+## Resumo
+A resposta chega (às vezes 200 e Content-Type application/json), mas o corpo é HTML, XML ou aviso em texto — o parse falha no primeiro caractere.
+
+## Sinais
+- console "Unexpected token <"
+- texto legível antes ou no lugar do JSON: Warning do PHP, página de gateway, "Atenção ERRO"
+
+## Causa
+Falha de conexão no site imprime "Atenção ERRO" em HTML (connect.php:16); Warning/Fatal do PHP saem antes da saída; gateway fora devolve a própria página.
+
+## Notas do modelo
+- [E1 · lex-2 · nota] Adicionar um exemplo de sintoma específico, como "Página de erro HTML em vez de JSON", para melhorar a identificação de casos onde o corpo da resposta não é JSON. — Motivo: Este exemplo mostra que a documentação não abrange casos onde o erro é causado por uma página de erro HTML em vez de JSON, o que pode ser um sintoma comum de problemas de conexão ou falhas do servidor.
+- [E1 · lex-9 · nota] Adicionar um exemplo de sintoma para clarificar que XML também pode causar parse falho. — Motivo: Este caso mostrou que XML também pode causar parse falho, mas a documentação não destaca isso.
--- epoca-0/erros/corpo_vazio.md
+++ epoca-2/erros/corpo_vazio.md
@@ -0,0 +1,31 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: separa "sem corpo" de "lista vazia", que a página trata de forma diferente;
+# conferido em produtos_api.php.
+id: corpo_vazio
+titulo: Corpo vazio
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: corpo_vazio
+arquivos: [Programacao/CobaiaFront/produtos_api.php]
+sintomas: [carregando indefinidamente, tela em branco sem erro, fim inesperado da entrada em corpo vazio]
+palavras_chave: [vazio, sem corpo, branco, 204, espacos, nenhum byte, carregando]
+causas_relacionadas: [resposta_truncada, corpo_nao_e_json, estado_da_tela_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-13) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-13) - Revisar: nota acrescentada.
+---
+## Resumo
+Status de sucesso e nenhum byte útil no corpo (vazio, só espaços, ou 204). Diferente de "[]", lista vazia, que é JSON válido.
+
+## Sinais
+- resp.json() falha em zero caracteres: "Erro ao carregar produtos" ou "Carregando..." parado
+- "[]" mostra "Nenhum produto retornado pela API."
+
+## Causa
+Nenhuma rota da CobaiaAPI devolve 204 nem corpo vazio; se chega vazio, foi cortado antes de sair (servidor, proxy) ou a rota errada respondeu.
+
+## Notas do modelo
+- [E1 · lex-13 · nota] Adicionar exemplo de sintoma: "Tabela de reservas vazia, sem erro." — Motivo: Este exemplo mostra que a falta de dados no corpo da resposta pode ser indiretamente observada pela ausência de conteúdo na interface, sem necessariamente retornar um erro, o que não estava claramente documentado.
+- [E1 · lex-13 · nota] Adicionar: "Nenhuma resposta ou resposta vazia pode ser retornada por nenhuma rota da CobaiaAPI." — Motivo: Este exemplo ilustra que a ausência de resposta ou resposta vazia é uma condição que deve ser explicitamente verificada, pois ela não retorna um erro HTTP, mas pode afetar a interface.
--- epoca-0/erros/dado_desatualizado.md
+++ epoca-2/erros/dado_desatualizado.md
@@ -0,0 +1,30 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: a API lê o banco a cada requisição e não envia cabeçalhos de cache; a
+# defasagem entre painel PHP e API é o sinal de cache intermediário. Conferido.
+id: dado_desatualizado
+titulo: Dado desatualizado (cache)
+sistema: Infraestrutura
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: dado_desatualizado
+arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/database.py]
+endpoints: [GET /api/pedidos, GET /api/produtos]
+sintomas: [reserva nova nao aparece, cancelamento volta a ativo ao recarregar, produto novo demora a aparecer, status inconsistente, reserva cancelada aparecendo como ativa]
+palavras_chave: [cache, desatualizado, velho, antigo, Age, Cache-Control, max-age, defasagem, minutos, stale, api, get, php]
+causas_relacionadas: [estado_da_tela_divergente, registro_duplicado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-11) - Revisar: retificação acrescentada.
+---
+## Resumo
+Uma escrita confirmada (201/200) não aparece na leitura seguinte e surge minutos depois sem nova ação — a leitura veio de uma cópia antiga.
+
+## Sinais
+- cabeçalhos Age ou Cache-Control: max-age no GET
+- o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa
+
+## Causa
+A CobaiaAPI consulta o banco a cada requisição (database.py) e não envia cache; leitura defasada indica proxy ou cache do navegador entre a página e a API.
+
+## Notas do modelo
+- [E1 · run-11 · retificação de "Sinais: cabeçalhos Age ou Cache-Control: max-age no GET; o painel PHP (lê o banco direto) já mostra o dado; só a API atrasa."] Adicionar "A leitura defasada indica que a API está lendo dados antigos do banco, enquanto o painel PHP atualiza em tempo real." — Motivo: Este texto destaca a causa raiz do problema, mostrando que a desatualização dos dados é devido à API ler dados antigos do banco, enquanto o painel PHP atualiza em tempo real, o que não foi evidente no caso original.
--- epoca-0/erros/erro_interno_do_servidor.md
+++ epoca-2/erros/erro_interno_do_servidor.md
@@ -0,0 +1,32 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: lista as origens reais de 500 (injetor e banco fora) e a diferença crucial:
+# no site PHP, banco fora não dá 500, dá HTML. Conferido em produtos.py e connect.php.
+id: erro_interno_do_servidor
+titulo: Erro interno do servidor (500)
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: erro_interno_do_servidor
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/conn/connect.php]
+endpoints: [GET /api/produtos, POST /api/pedidos]
+sintomas: [HTTP 500, Internal Server Error, fault injection error_500, falha intermitente]
+palavras_chave: [500, erro interno, internal server error, exception, excecao, fault injection, intermitente, banco fora, falha_interna, injetor, excecao_nao_tratada]
+causas_relacionadas: [corpo_nao_e_json, tempo_de_resposta_excedido, limite_de_requisicoes]
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-6) - Revisar: nota acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-12) - Revisar: nota acrescentada.
+---
+## Resumo
+500 com {"detail": ...}: falha própria da API. detail "fault injection: error_500 em produto" é o injetor; "Internal Server Error" é exceção não tratada.
+
+## Sinais
+- intermitente sem padrão: injetor com probability < 1
+- em toda requisição: banco inacessível ou defeito na rota
+
+## Causa
+Rotas convertem ErrorFault em 500 (produtos.py:42). No site PHP, banco fora NÃO dá 500: imprime "Atenção ERRO" em HTML (connect.php:16).
+
+## Notas do modelo
+- [E1 · run-6 · nota] Adicionar que este erro pode ocorrer devido a falhas no banco de dados ou em rotas, e que a mensagem genérica pode esconder problemas específicos. — Motivo: Este caso mostrou que a mensagem de erro genérica pode esconder problemas específicos, como falhas no banco de dados, que não são explicitamente mencionados na documentação.
+- [E1 · run-12 · nota] Adicionar que este erro pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota. — Motivo: Este caso mostrou que o erro interno do servidor pode ocorrer de forma intermitente, sem padrão, e que pode ser causado por problemas no banco de dados ou rota, evidenciando a necessidade de uma nota sobre esse comportamento.
--- epoca-0/erros/escala_ou_unidade_errada.md
+++ epoca-2/erros/escala_ou_unidade_errada.md
@@ -0,0 +1,33 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: a API não aplica escala nenhuma (float direto do DECIMAL, DATE sem fuso), o
+# que faz qualquer fator ou deslocamento ser sinal de tradução errada. Conferido.
+id: escala_ou_unidade_errada
+titulo: Escala ou unidade errada
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: escala_ou_unidade_errada
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/models.py]
+endpoints: [GET /api/produtos, GET /api/pedidos]
+tabelas: [tbprodutos, tbpedido_reserva]
+sintomas: [precos cem vezes maiores, precos cem vezes menores, preco arredondado, data um dia antes, dobro de pessoas]
+palavras_chave: [escala, unidade, centavos, reais, fator, cem, arredond, fuso, dia, dobro, multiplic, divid, conversao]
+causas_relacionadas: [tipo_divergente, formato_de_data_divergente, chave_de_juncao_errada]
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-6) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-12) - Revisar: retificação acrescentada.
+---
+## Resumo
+Tipo e formato certos, mas o número está noutra escala ou unidade: centavos por reais (8990), fração (0.899), arredondado (90), data deslocada um dia, quantidade dobrada.
+
+## Sinais
+- todos os valores errados pelo mesmo fator: conversão de unidade
+- só o arredondamento errado
+
+## Causa
+A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela.
+
+## Notas do modelo
+- [E1 · tra-6 · retificação de "A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela."] Corrigir a conversão do valor_produto para float, aplicando o fator correto. — Motivo: Este caso mostrou que a conversão direta do DECIMAL para float sem aplicar o fator correto resulta em preços errados, evidenciando a necessidade de uma correção na documentação.
+- [E1 · tra-12 · retificação de "Sinais: todos os valores errados pelo mesmo fator: conversão de unidade; só o arredondamento errado. Causa: A API não aplica fator nenhum: float(valor_produto) direto do DECIMAL (produtos.py:28), DATE em isoformat sem fuso (pedidos.py:23); o fator veio de fora dela."] Adicionar exemplo de conversão incorreta de valor_produto DECIMAL(9,2) para float, causando arredondamento. — Motivo: Este caso mostrou que a documentação não era suficiente para alertar sobre a necessidade de conversão correta do valor DECIMAL para float, o que resultou em arredondamento.
--- epoca-0/erros/estado_da_tela_divergente.md
+++ epoca-2/erros/estado_da_tela_divergente.md
@@ -0,0 +1,34 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: quando a resposta está certa e a tela errada, a causa está no JS ou na
+# ausência de atualização; descreve o que o código faz de fato. Conferido em produtos_api.php
+# e reserva_cli.php.
+id: estado_da_tela_divergente
+titulo: Estado da tela divergente da resposta
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: erro
+status: ativo
+causa_raiz: estado_da_tela_divergente
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/cliente/reserva_cli.php]
+sintomas: [api respondeu certo mas a tela nao, carregando parado, lista vazia com resposta cheia, botao continua habilitado apos cancelar, lista vazia, botao que nao muda]
+palavras_chave: [tela, estado, divergente, render, renderiza, atualiza, recarregar, filtro, ordem aleatoria, carregando, innerHTML, cancelar, redirect]
+causas_relacionadas: [localizador_quebrado, dado_desatualizado, corpo_vazio]
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-4) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-8) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-10) - Revisar: retificação acrescentada.
+---
+## Resumo
+A rede está certa — status e corpo conferem — e o usuário vê outra coisa: "Carregando" parado, lista vazia, botão que não muda.
+
+## Sinais
+- nenhum erro de console nem status de erro
+- recarregar corrige: o estado não foi atualizado
+
+## Causa
+produtos_api.php só limpa "Carregando..." no then() do fetch e substitui o grid por innerHTML; na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7).
+
+## Notas do modelo
+- [E1 · efe-4 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica de cancelamento para não depender de redirect, garantindo a atualização do estado da tela. — Motivo: Este caso mostrou que a lógica de atualização da interface não está sincronizada com a resposta da API, evidenciando a necessidade de uma revisão na implementação do cancelamento.
+- [E1 · efe-8 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a implementação do cancelamento para que não dependa apenas do redirect, mas também limpe o estado da tela corretamente. — Motivo: Esta retificação mostra que a implementação atual está incompleta e que o cancelamento deve ser tratado de forma mais robusta, o que pode ajudar a prevenir erros semelhantes no futuro.
+- [E1 · efe-10 · retificação de "na área do cliente, cancelar depende do redirect (cliente_cancelar.php:7)."] Corrigir a lógica de cancelamento para não depender do redirect, garantindo que a interface seja atualizada corretamente. — Motivo: Este caso mostrou que a lógica de atualização da interface pode estar incorreta, mesmo com dados corretos na rede. A documentação sobre o estado da tela divergente não foi explicita sobre a necessidade de atualização do DOM.
--- epoca-0/erros/estrutura_aninhada_divergente.md
+++ epoca-2/erros/estrutura_aninhada_divergente.md
@@ -0,0 +1,32 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: a página checa Array.isArray e imprime objetos com JSON.stringify — é o que
+# torna cada forma de aninhamento visível de um jeito. Conferido em produtos_api.php.
+id: estrutura_aninhada_divergente
+titulo: Estrutura aninhada divergente
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: estrutura_aninhada_divergente
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/schemas.py]
+endpoints: [GET /api/produtos]
+sintomas: [object Object, envelope data, lista dentro de objeto, campo virou objeto, envelope na raiz, campo como objeto]
+palavras_chave: [aninhad, envelope, data, itens, objeto, nivel, profundidade, object Object, stringify, estrutura, aninhamento, divergencia]
+causas_relacionadas: [colecao_no_lugar_de_objeto, campo_renomeado, contagem_inconsistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-13) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-11) - Revisar: retificação acrescentada.
+---
+## Resumo
+Chaves existem, mas noutro nível: lista num envelope ({"data": {"itens": [...]}}) ou campo simples como objeto ({"id": 1, "nome": "Carnes"}).
+
+## Sinais
+- envelope na raiz: Array.isArray falha, "Nenhum produto retornado"
+- campo como objeto: cartão imprime [object Object]
+
+## Causa
+Contrato real: lista crua na raiz e tipo como texto (produtos.py _to_dict); envelope ou aninhamento veio de outra versão ou intermediário.
+
+## Notas do modelo
+- [E1 · sin-13 · retificação de "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'})."] Adicionar exemplo de estrutura aninhada divergente no verbete. — Motivo: O exemplo de sintoma observado mostrou que a estrutura pode variar entre um envelope e um campo simples, necessitando de um exemplo explícito no verbete.
+- [E1 · efe-11 · retificação de "Chaves existem, mas noutro nível: lista num envelope ({'data': {'itens': [...]}}) ou campo simples como objeto ({'id': 1, 'nome': 'Carnes'})."] Corrigir a estrutura da resposta da API para ser consistente, evitando envelopes ou campos simples aninhados, para padronizar o desenpacotamento dos dados. — Motivo: Este caso mostrou que a estrutura da resposta pode variar, causando problemas de desenpacotamento, e a documentação não explicitava essa possibilidade.
--- epoca-0/erros/formato_de_data_divergente.md
+++ epoca-2/erros/formato_de_data_divergente.md
@@ -0,0 +1,31 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: a API serializa a data com isoformat(); qualquer outro formato é divergência.
+# Conferido em pedidos.py:23.
+id: formato_de_data_divergente
+titulo: Formato de data divergente
+sistema: CobaiaAPI
+entidade_principal: Pedido
+tipo: erro
+status: ativo
+causa_raiz: formato_de_data_divergente
+arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/schemas.py]
+endpoints: [GET /api/pedidos, POST /api/pedidos]
+tabelas: [tbpedido_reserva]
+sintomas: [Invalid Date, data como numero, data em formato brasileiro, data noutro formato, data deslocada um dia]
+palavras_chave: [data, formato, iso, AAAA-MM-DD, dd/mm/aaaa, timestamp, epoch, Invalid Date, data_pedido, unidade]
+causas_relacionadas: [escala_ou_unidade_errada, tipo_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso tra-9) - Revisar: retificação acrescentada.
+---
+## Resumo
+data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta.
+
+## Sinais
+- "Invalid Date" na listagem: formato brasileiro ou texto não reconhecido
+- número grande no lugar da data: timestamp
+
+## Causa
+A API devolve data_pedido.isoformat() (pedidos.py:23), sempre AAAA-MM-DD. Em escala_ou_unidade_errada a data é legível mas deslocada; aqui é ilegível.
+
+## Notas do modelo
+- [E1 · tra-9 · retificação de "data_pedido deve ser texto AAAA-MM-DD. Chega noutro formato (10/09/2026), como segundos (1789084800) ou com hora e fuso — e o cliente não interpreta."] Adicione que o formato ISO 8601 é obrigatório e que datas devem ser passadas no formato AAAA-MM-DD, sem hora ou fuso horário. Corrija que o timestamp deve ser convertido para o formato ISO 8601 antes de ser devolvido. — Motivo: Este caso mostrou que a documentação não esclareceu claramente que o formato ISO 8601 é obrigatório e que datas devem ser passadas no formato AAAA-MM-DD, sem hora ou fuso horário.
--- epoca-0/erros/limite_de_requisicoes.md
+++ epoca-2/erros/limite_de_requisicoes.md
@@ -0,0 +1,26 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: a CobaiaAPI não implementa limite de requisições — um 429 só pode vir de
+# fora dela, e isso é o que o modelo precisa saber. Conferido em main.py e nos routers.
+id: limite_de_requisicoes
+titulo: Limite de requisições (429)
+sistema: Infraestrutura
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: limite_de_requisicoes
+arquivos: [Programacao/CobaiaAPI/app/main.py, Programacao/CobaiaFront/produtos_api.php]
+endpoints: [GET /api/produtos]
+sintomas: [HTTP 429, too many requests, rate limit, para de funcionar apos varias tentativas]
+palavras_chave: [429, limite, rate limit, too many requests, retry_after, cota, excesso, recarregar]
+causas_relacionadas: [tempo_de_resposta_excedido, erro_interno_do_servidor]
+---
+## Resumo
+Status 429: o servidor ou um intermediário recusou por excesso de requisições num intervalo. Resposta rápida e com corpo — não é lentidão nem erro interno.
+
+## Sinais
+- funciona, depois falha após recarregar muitas vezes
+- "Erro ao carregar produtos da CobaiaAPI: HTTP 429"; pode vir retry_after
+
+## Causa
+A CobaiaAPI não tem limitador (main.py só registra CORS e routers); um 429 vem de proxy, gateway ou servidor diferente do esperado.
--- epoca-0/erros/localizador_quebrado.md
+++ epoca-2/erros/localizador_quebrado.md
@@ -0,0 +1,29 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: lista os seletores REAIS da página e a ausência de ORDER BY que torna a
+# posição dos cartões instável. Conferido em produtos_api.php e produtos.py:38.
+id: localizador_quebrado
+titulo: Localizador (seletor) quebrado
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: erro
+status: ativo
+causa_raiz: localizador_quebrado
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/produtos_geral.php]
+sintomas: [elemento nao encontrado, tempo esgotado procurando elemento, seletor casou dois elementos, texto do botao diferente]
+palavras_chave: [seletor, localizador, css, xpath, id, classe, data-id, texto, ambiguo, unico, nth-child, ordem, roteiro, timeout, elemento, ambiguidade]
+causas_relacionadas: [estado_da_tela_divergente, recurso_inexistente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso efe-12) - Revisar: nota acrescentada.
+---
+## Resumo
+Nenhuma requisição falhou: o roteiro não acha o elemento (seletor não casa) ou acha mais de um (ambíguo). O problema é o localizador, não o dado.
+
+## Sinais
+- "Ver mais" vs "Saiba Mais...", data-produto vs data-id: texto ou atributo inexistente
+- nth-child que funciona às vezes: ordem não garantida
+
+## Causa
+Elementos reais de produtos_api.php: #produtos-api-grid, .thumbnail, button.saiba-mais[data-id], #modalDetalhe; a lista da API não tem ORDER BY (produtos.py:38).
+
+## Notas do modelo
+- [E1 · efe-12 · nota] Adicionado que o localizador pode ser ambíguo, encontrando mais de um elemento com o mesmo seletor. — Motivo: Este caso mostrou que o diagnóstico precisa considerar a ambiguidade no seletor, o que não estava claro na documentação original.
--- epoca-0/erros/mensagens-de-erro-do-codigo.md
+++ epoca-2/erros/mensagens-de-erro-do-codigo.md
@@ -0,0 +1,17 @@
+---
+# ! Alteração de IA - Revisar: índice mensagem literal → ponto do código → causa (Fase 2-B).
+# ! Motivo: é o "caminho pré-definido" pedido para a biblioteca — a mensagem que o usuário
+# vê leva direto ao arquivo e à causa. Todas conferidas nos fontes citados.
+id: mensagens-de-erro-do-codigo
+titulo: Índice de mensagens literais do código
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: funcionamento
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py, Programacao/CobaiaFront/rodape_contato_envia.php]
+sintomas: [mensagem de erro na tela, detail no json de erro]
+palavras_chave: [mensagem, literal, detail, erro ao carregar, nenhum produto retornado, atencao erro, token invalido, modo invalido, falha no email, indice]
+causas_relacionadas: [recurso_inexistente, erro_interno_do_servidor, corpo_nao_e_json, corpo_vazio, estado_da_tela_divergente]
+---
+## Resumo
+Página: "Carregando produtos da CobaiaAPI..."; "Nenhum produto retornado pela API." (não é lista, ou vazia); "Erro ao carregar produtos da CobaiaAPI: <msg>" ("HTTP <n>" se resp.ok falso). API: "produto/cliente/pedido não encontrado" (404), "token inválido" (403), "modo inválido" (400), "fault injection: error_500 em <ent>" (500). PHP: "Atenção ERRO: ..." (connect.php:16), "falha no email" (rodape_contato_envia.php:33).
--- epoca-0/erros/nulo_inesperado.md
+++ epoca-2/erros/nulo_inesperado.md
@@ -0,0 +1,27 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: aponta as duas origens legítimas de nulo (colunas nullable e LEFT JOIN da
+# view) e o campo que NÃO pode vir nulo pelo código; conferido em models.py e na view.
+id: nulo_inesperado
+titulo: Nulo inesperado
+sistema: Ambos
+entidade_principal: Pedido
+tipo: erro
+status: ativo
+causa_raiz: nulo_inesperado
+arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/routers/produtos.py]
+endpoints: [GET /api/produtos, GET /api/pedidos]
+tabelas: [tbprodutos, vw_tbpedidos]
+sintomas: [null onde havia valor, saudacao vazia, R$ 0,00 para produto com preco, produto some do filtro]
+palavras_chave: [nulo, null, None, vazio, nullable, saudacao, Ola, left join, view]
+causas_relacionadas: [campo_ausente, valor_fora_do_dominio, chave_de_juncao_errada]
+---
+## Resumo
+A chave existe e vem null onde o contrato promete valor. Diferente de campo_ausente: a chave está lá.
+
+## Sinais
+- nome nulo: "Olá, !" na área do cliente; preco nulo: cartão sem valor
+- tipo nulo: produto some de filtros por categoria
+
+## Causa
+Origens legítimas: resumo, valor_produto e imagem_produto são nullable (models.py:33-35) e vw_tbpedidos faz LEFT JOIN. tipo nulo não sai de produtos.py (p.tipo.rotulo_tipo).
--- epoca-0/erros/recurso_inexistente.md
+++ epoca-2/erros/recurso_inexistente.md
@@ -0,0 +1,30 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: os quatro 404 com mensagem própria e o 404 de rota são distinguíveis pelo
+# detail — é o que aponta o ponto do código. Conferido em produtos.py, pedidos.py, admin_fault.py.
+id: recurso_inexistente
+titulo: Recurso inexistente (404 e vizinhos)
+sistema: CobaiaAPI
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: recurso_inexistente
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaAPI/app/routers/admin_fault.py]
+endpoints: [GET /api/produtos/{id}, GET /api/pedidos, POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
+sintomas: [HTTP 404, Not Found, produto nao encontrado, cliente nao encontrado, pedido nao encontrado, rota errada]
+palavras_chave: [404, not found, nao encontrado, inexistente, rota, endpoint, singular, plural, 403, 422, detail, campo de busca errado]
+causas_relacionadas: [erro_interno_do_servidor, localizador_quebrado]
+# ! Alteração por modelo qwen2.5:7b (E1, caso run-7) - Revisar: nota acrescentada.
+---
+## Resumo
+404: id ou rota inexistente. O detail diz qual: "produto não encontrado" (produtos.py:52), "cliente não encontrado" (pedidos.py:37,52), "pedido não encontrado" (pedidos.py:74); "Not Found" genérico é rota inexistente (ex.: /api/produto).
+
+## Sinais
+- id válido e ainda 404: campo de busca errado (login × id)
+- vizinhos: 403 no admin sem token; 422 sem login
+
+## Causa
+Cada 404 com mensagem vem de db.get/filter vazio na rota.
+
+## Notas do modelo
+- [E1 · run-7 · nota] Adicionar um exemplo de campo de busca errado, como login × id, para ilustrar melhor a causa raiz. — Motivo: Este exemplo ilustra uma situação que pode causar confusão, mostrando que mesmo com um ID válido, o erro 404 pode ocorrer devido a um campo de busca incorreto.
--- epoca-0/erros/registro_duplicado.md
+++ epoca-2/erros/registro_duplicado.md
@@ -0,0 +1,27 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: nem a API nem o formulário PHP têm chave de idempotência — reenvio grava de
+# novo. Conferido em pedidos.py e registrar_reserva.php.
+id: registro_duplicado
+titulo: Registro duplicado
+sistema: Ambos
+entidade_principal: Pedido
+tipo: erro
+status: ativo
+causa_raiz: registro_duplicado
+arquivos: [Programacao/CobaiaAPI/app/routers/pedidos.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
+endpoints: [POST /api/pedidos, GET /api/pedidos]
+tabelas: [tbpedido_reserva]
+sintomas: [duas reservas identicas, dois 201 seguidos, cobranca em duplicidade]
+palavras_chave: [duplicad, duplicat, repetid, reenvio, clique duplo, F5, idempot, dois registros, ids consecutivos]
+causas_relacionadas: [dado_desatualizado, contagem_inconsistente]
+---
+## Resumo
+A mesma escrita gravada mais de uma vez: reservas iguais com ids consecutivos, duas respostas 201 para um único gesto.
+
+## Sinais
+- registros idênticos exceto pelo id
+- dois POST com o mesmo corpo na sequência
+
+## Causa
+POST /api/pedidos insere sem chave de idempotência (pedidos.py:46-66): clique duplo vira duas linhas. registrar_reserva.php insere a cada POST — recarregar após reservar reenvia o formulário.
--- epoca-0/erros/resposta_truncada.md
+++ epoca-2/erros/resposta_truncada.md
@@ -0,0 +1,30 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: o modo malformed_json produz exatamente isso; conferido em produtos.py:19.
+id: resposta_truncada
+titulo: Resposta truncada
+sistema: CobaiaAPI
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: resposta_truncada
+arquivos: [Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/fault_injection.py]
+sintomas: [fim inesperado da entrada, json cortado, content-length menor que o corpo, lista incompleta, ultimo item cortado, corpo cortado]
+palavras_chave: [truncad, cortad, incomplet, unexpected end, content-length, tamanho, parcial, malformed_json, truncamento, conexao, proxy]
+causas_relacionadas: [corpo_nao_e_json, corpo_vazio, tempo_de_resposta_excedido]
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-5) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso lex-14) - Revisar: nota acrescentada.
+---
+## Resumo
+O corpo começa como JSON válido e termina no meio de um valor ou chave — faltam bytes; o parse falha com "Unexpected end of JSON input".
+
+## Sinais
+- primeiros itens íntegros, o último cortado ou sem o colchete final
+- Content-Length menor que o esperado
+
+## Causa
+O modo malformed_json devolve corpo cortado de propósito (produtos.py:19). Fora dele: limite num proxy, conexão encerrada durante o envio.
+
+## Notas do modelo
+- [E1 · lex-5 · retificação de "Fora dele: limite num proxy, conexão encerrada durante o envio."] Corrigir a descrição para incluir que o truncamento pode ser causado por limites de proxy ou interrupção de conexão. — Motivo: Esclarecer que limites de proxy ou interrupção de conexão podem causar truncamento, ajudando a diagnosticar casos futuros.
+- [E1 · lex-14 · nota] Adicione um exemplo de como verificar o Content-Length na documentação para evitar esse problema. — Motivo: Este caso mostrou que a verificação do Content-Length é crucial para detectar respostas truncadas, e a documentação não aborda isso explicitamente.
--- epoca-0/erros/tempo_de_resposta_excedido.md
+++ epoca-2/erros/tempo_de_resposta_excedido.md
@@ -0,0 +1,26 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: o modo latency é o único atraso previsto (2 s fixos); o fetch da página não
+# define timeout próprio. Conferido em fault_injection.py e produtos_api.php.
+id: tempo_de_resposta_excedido
+titulo: Tempo de resposta excedido
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: erro
+status: ativo
+causa_raiz: tempo_de_resposta_excedido
+arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php]
+endpoints: [GET /api/produtos]
+sintomas: [demora de segundos, timeout, conexao encerrada por tempo, carregando por muito tempo]
+palavras_chave: [timeout, lento, lentidao, demora, latencia, segundos, tempo esgotado, volume, 2 s]
+causas_relacionadas: [limite_de_requisicoes, erro_interno_do_servidor, corpo_vazio]
+---
+## Resumo
+A resposta demora além do aceitável ou nunca chega: sem status (conexão encerrada) ou 200 tardio. 429 e 500 respondem rápido com um código — aqui não.
+
+## Sinais
+- 200 correto com segundos de espera: atraso no servidor ou no caminho
+- sem status, "Failed to fetch": o cliente desistiu antes
+
+## Causa
+O modo latency dorme 2 s fixos (fault_injection.py:66); atrasos maiores vêm de banco, rede ou carga; o fetch da página não tem tempo limite.
--- epoca-0/erros/tipo_divergente.md
+++ epoca-2/erros/tipo_divergente.md
@@ -0,0 +1,30 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: type_drift converte com str(); texto numérico ainda formata na tela, então o
+# sintoma aparece em ordenação/soma. Conferido em fault_injection.py e produtos_api.php.
+id: tipo_divergente
+titulo: Tipo divergente
+sistema: CobaiaAPI
+entidade_principal: Produto
+tipo: erro
+status: ativo
+causa_raiz: tipo_divergente
+arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaFront/produtos_api.php, Programacao/CobaiaAPI/app/routers/produtos.py]
+endpoints: [GET /api/produtos, GET /api/pedidos]
+sintomas: [numero como texto, booleano como Sim, destaque 1, ordenacao errada, soma errada, destaque booleano sai literal]
+palavras_chave: [tipo, texto, string, numero, booleano, Sim, aspas, type_drift, str, virgula decimal, convercao]
+causas_relacionadas: [valor_fora_do_dominio, formato_de_data_divergente, escala_ou_unidade_errada]
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: retificação acrescentada.
+---
+## Resumo
+Chave certa com o tipo JSON errado: número entre aspas ("89.90"), booleano como texto ("Sim") ou número (1), inteiro como texto ("4").
+
+## Sinais
+- texto numérico com ponto ainda formata; a falha aparece ao ordenar ou somar
+- "89,90" com vírgula não converte; destaque fora de true/false sai literal
+
+## Causa
+O modo type_drift aplica str() ao campo-alvo (fault_injection.py:76). A API converte DECIMAL em número e 'Sim'/'Não' em booleano (_to_dict).
+
+## Notas do modelo
+- [E1 · semt-13 · retificação de "destaque fora de true/false sai literal."] Corrigir que destaque booleano saia literal, garantindo que seja convertido corretamente para True ou False. — Motivo: O caso mostrou que a conversão incorreta de booleano afeta a apresentação do preço, indicando a necessidade de corrigir essa conversão.
--- epoca-0/erros/valor_fora_do_dominio.md
+++ epoca-2/erros/valor_fora_do_dominio.md
@@ -0,0 +1,31 @@
+---
+# ! Alteração de IA - Revisar: verbete de causa raiz da biblioteca base (Fase 2-B).
+# ! Motivo: lista os domínios reais (ENUM do banco e min do HTML) e onde não há validação;
+# conferido em schema_completo.sql, models.py e registrar_reserva.php.
+id: valor_fora_do_dominio
+titulo: Valor fora do domínio
+sistema: Ambos
+entidade_principal: Pedido
+tipo: erro
+status: ativo
+causa_raiz: valor_fora_do_dominio
+arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaFront/cliente/registrar_reserva.php]
+endpoints: [GET /api/pedidos, GET /api/produtos]
+tabelas: [tbpedido_reserva, tbprodutos]
+sintomas: [status desconhecido, pessoas zero, destaque 2, reserva sem botao de cancelar, botao de cancelar some, status inesperado]
+palavras_chave: [dominio, enum, permitido, conjunto, status, Pendente, Concluido, pessoas, zero, negativo, destaque, validacao]
+causas_relacionadas: [tipo_divergente, formato_de_data_divergente, nulo_inesperado]
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-11) - Revisar: retificação acrescentada.
+---
+## Resumo
+Tipo certo, valor fora do conjunto permitido: status diferente de 'Em Análise'/'Cancelado', destaque diferente de true/false, pessoas menor que 1.
+
+## Sinais
+- reserva nem ativa nem cancelada na tela: status inesperado
+- 0 ou negativo em pessoas: o mínimo só existe no HTML
+
+## Causa
+status e destaque são ENUM no banco (schema_completo.sql:37); pessoas ≥ 1 é só min= do HTML (registrar_reserva.php:55); a API não valida o que devolve.
+
+## Notas do modelo
+- [E1 · semt-11 · retificação de "Valor fora do domínio"] Adicionar validação no status do pedido na API para evitar valores fora do domínio. — Motivo: Este caso mostrou que a API não valida o status do pedido, permitindo valores inválidos como 'Concluido', o que afeta a exibição de botões na interface.
--- epoca-0/falhas_injetadas/modos-de-injecao.md
+++ epoca-2/falhas_injetadas/modos-de-injecao.md
@@ -0,0 +1,25 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (mecanismo de falha).
+# ! Motivo: o cobaia tem um injetor de falhas de propósito; documentar o efeito exato de
+# cada modo no fio é o que permite ao modelo reconhecer "um campo só, o resto íntegro".
+id: modos-de-injecao
+titulo: Injeção de falhas da CobaiaAPI
+sistema: CobaiaAPI
+entidade_principal: Infraestrutura
+tipo: funcionamento
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/fault_injection.py, Programacao/CobaiaAPI/app/routers/admin_fault.py, Programacao/CobaiaAPI/.env.example]
+endpoints: [GET /api/admin/fault-mode, POST /api/admin/fault-mode]
+sintomas: [um campo alterado e o resto integro, 500 com fault injection, atraso fixo de 2 s, corpo cortado]
+palavras_chave: [fault, injecao, falha, modo, error_500, latency, type_drift, field_missing, field_renamed, malformed_json, target_field, probability, X-Admin-Token]
+causas_relacionadas: [erro_interno_do_servidor, tempo_de_resposta_excedido, tipo_divergente, campo_ausente, campo_renomeado, resposta_truncada]
+---
+## Resumo
+Injetor com 7 modos: error_500, latency (2 s), type_drift (campo-alvo vira texto), field_missing (remove), field_renamed (vira <campo>_v2), malformed_json (corpo cortado) e normal.
+
+## Sinais
+- só um campo alterado, resto íntegro: modo com campo-alvo
+- detail "fault injection: error_500 em produto"
+
+## Causa
+Ligado por FAULT_MODE/FAULT_TARGET_FIELD no .env ou POST /api/admin/fault-mode com X-Admin-Token; probability < 1 dá intermitência.
--- epoca-0/negocio/entidade-produto.md
+++ epoca-2/negocio/entidade-produto.md
@@ -0,0 +1,32 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
+# ! Motivo: dá ao modelo o que o contrato de campos não diz — de onde cada campo vem e
+# como é traduzido entre banco e API. Conferido em models.py, produtos.py e seed.sql.
+id: entidade-produto
+titulo: Produto e sua categoria
+sistema: Ambos
+entidade_principal: Produto
+tipo: funcionamento
+status: ativo
+arquivos: [Programacao/CobaiaAPI/app/models.py, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaFront/banco/seed.sql]
+endpoints: [GET /api/produtos, GET /api/produtos/{id}]
+tabelas: [tbprodutos, tbtipos]
+sintomas: [nome da categoria no titulo do cartao, preco com grandeza estranha, nulo_inesperado, escala_ou_unidade_errada, preco cru, separador decimal como virgula]
+palavras_chave: [produto, categoria, tipo, preco, destaque, imagem, resumo, cardapio, picanha, convercao, valor, formatacao, decimal, separador]
+causas_relacionadas: [chave_de_juncao_errada, escala_ou_unidade_errada, tipo_divergente]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-1) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-13) - Revisar: nota acrescentada.
+---
+## Resumo
+Item do cardápio em tbprodutos, ligado a uma categoria de tbtipos (Carnes, Bebidas, Acompanhamentos, Sobremesas). 14 produtos; o id 1 é Picanha ao Alho, Carnes, 89,90.
+
+## Sinais
+- título com nome de categoria: junção trocada
+- preço com grandeza estranha: conversão de valor_produto
+
+## Causa
+valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano.
+
+## Notas do modelo
+- [E1 · sin-1 · retificação de "Causa: valor_produto é DECIMAL(9,2) e destaque_produto ENUM('Sim','Não'); produtos.py (_to_dict) converte em número e booleano."] Corrigir a conversão do preço e destaque no _to_dict de produtos.py. — Motivo: O caso mostrou que a conversão incorreta de tipos pode levar a sintomas como 'undefined' e '89.9', indicando uma necessidade de revisão na conversão de tipos.
+- [E1 · semt-13 · nota] Adicionar nota sobre a necessidade de formatação correta do preço no front-end, considerando o formato brasileiro. — Motivo: O caso demonstra a importância de uma formatação correta do preço, independentemente da conversão do backend.
--- epoca-0/negocio/fluxo-reserva-e-cancelamento.md
+++ epoca-2/negocio/fluxo-reserva-e-cancelamento.md
@@ -0,0 +1,26 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
+# ! Motivo: as regras de data e de pessoas existem só no HTML — o modelo precisa saber
+# que o servidor aceita qualquer valor, senão diagnostica "validação" onde não há.
+id: fluxo-reserva-e-cancelamento
+titulo: Fluxo de reservar e cancelar
+sistema: Ambos
+entidade_principal: Pedido
+tipo: regra
+status: ativo
+arquivos: [Programacao/CobaiaFront/cliente/registrar_reserva.php, Programacao/CobaiaFront/cliente/cliente_cancelar.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
+endpoints: [POST /api/pedidos, POST /api/pedidos/{id}/cancelar]
+tabelas: [tbpedido_reserva]
+sintomas: [data aceita fora da janela, reserva alheia cancelada, pessoas zero]
+palavras_chave: [reservar, cancelar, data, janela, dois dias, noventa dias, pessoas, minimo, validacao, formulario]
+causas_relacionadas: [valor_fora_do_dominio, dado_desatualizado, estado_da_tela_divergente]
+---
+## Resumo
+Reserva em cliente/registrar_reserva.php e cancelamento em reserva_cli.php; a API espelha em POST /api/pedidos e POST /api/pedidos/{id}/cancelar.
+
+## Sinais
+- regra de data e quantidade só no navegador
+- reserva alheia cancelada sem checagem de dono
+
+## Causa
+Data hoje+2 a hoje+90 e pessoas ≥ 1 são só min/max do HTML (registrar_reserva.php:28-35,55); cancelar grava 'Cancelado' (pedidos.py:75).
--- epoca-0/negocio/limites-do-sistema.md
+++ epoca-2/negocio/limites-do-sistema.md
@@ -0,0 +1,24 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (o que o sistema NÃO faz).
+# ! Motivo: pedido explícito do desenho — documentação comum omite as ausências, e é
+# justamente a falta de validação e de checagem que explica dado inválido gravado sem erro.
+id: limites-do-sistema
+titulo: O que o sistema não faz
+sistema: Ambos
+entidade_principal: Infraestrutura
+tipo: limite
+status: ativo
+arquivos: [Programacao/CobaiaFront/conn/connect.php, Programacao/CobaiaAPI/app/routers/produtos.py, Programacao/CobaiaAPI/app/schemas.py]
+sintomas: [dado invalido gravado, falha silenciosa, contrato do docs diferente da resposta]
+palavras_chave: [validacao, servidor, silencioso, checagem, hash, response_model, docs, declarado, real]
+causas_relacionadas: [valor_fora_do_dominio, campo_ausente, tipo_divergente, dado_desatualizado]
+---
+## Resumo
+Não valida data nem pessoas no servidor; não confere o retorno de $conn->query() em página nenhuma; não checa se a reserva cancelada é do cliente; não faz hash da senha no login.
+
+## Sinais
+- dado inválido gravado sem mensagem
+- redireciona como se tivesse gravado e nada mudou: SQL falhou em silêncio
+
+## Causa
+A API não revalida a resposta: rotas devolvem JSONResponse cru (produtos.py:1-7); o /docs mostra o esperado, não o que sai pela rede.
--- epoca-0/negocio/pagina-produtos-api.md
+++ epoca-2/negocio/pagina-produtos-api.md
@@ -0,0 +1,25 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (fronteira de integração).
+# ! Motivo: é a única página com fetch() JSON do cobaia; as mensagens literais que ela
+# imprime e o que faz com cada campo são o elo entre a resposta HTTP e o que o usuário vê.
+id: pagina-produtos-api
+titulo: Aba "Produtos (API)", a fronteira JSON
+sistema: CobaiaFront
+entidade_principal: Interface
+tipo: funcionamento
+status: ativo
+arquivos: [Programacao/CobaiaFront/produtos_api.php]
+endpoints: [GET /api/produtos, GET /api/produtos/{id}]
+sintomas: [carregando produtos parado, nenhum produto retornado, erro ao carregar produtos, R$ NaN, object Object]
+palavras_chave: [produtos_api, fetch, cartao, card, modal, saiba mais, formatarPreco, Number, NaN, data-id, status, grid]
+causas_relacionadas: [estado_da_tela_divergente, localizador_quebrado, corpo_vazio, tipo_divergente]
+---
+## Resumo
+produtos_api.php monta os cartões com fetch() em localhost:8000/api/produtos — a única fronteira JSON do cobaia; detalhe via GET /api/produtos/{id}.
+
+## Sinais
+- "Carregando..." parado: o fetch nunca resolveu
+- "Nenhum produto retornado pela API.": não é lista, ou vazia
+
+## Causa
+formatarPreco() usa Number(): preço não numérico sai cru; tipo objeto sai via JSON.stringify; botão button.saiba-mais[data-id].
--- epoca-0/negocio/pedido-reserva.md
+++ epoca-2/negocio/pedido-reserva.md
@@ -0,0 +1,34 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
+# ! Motivo: o domínio fechado do status e o LEFT JOIN da view são as duas fontes reais de
+# valor_fora_do_dominio e nulo_inesperado em reservas; conferido em schema_completo.sql.
+id: pedido-reserva
+titulo: Reserva de mesa (pedido)
+sistema: Ambos
+entidade_principal: Pedido
+tipo: funcionamento
+status: ativo
+arquivos: [Programacao/CobaiaFront/banco/schema_completo.sql, Programacao/CobaiaFront/cliente/reserva_cli.php, Programacao/CobaiaAPI/app/routers/pedidos.py]
+endpoints: [GET /api/pedidos]
+tabelas: [tbpedido_reserva, vw_tbpedidos, tbusuarios]
+sintomas: [status com texto desconhecido, reserva de outro cliente, linha de reserva vazia, reserva_incompleta, reserva_normal, reserva_nao_ativa_nem_cancelada, status_inesperado, reserva_vazia, cliente_sem_reserva]
+palavras_chave: [reserva, pedido, status, em analise, cancelado, pessoas, data_pedido, id_clientes, view, campos_nulos, renderizacao_incorreta, enum, validacao, left_join, nulo, renderizacao]
+causas_relacionadas: [valor_fora_do_dominio, nulo_inesperado, chave_de_juncao_errada]
+# ! Alteração por modelo qwen2.5:7b (E1, caso sin-12) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-15) - Revisar: retificação acrescentada.
+# ! Alteração por modelo qwen2.5:7b (E1, caso semt-15) - Revisar: retificação acrescentada.
+---
+## Resumo
+Reserva em tbpedido_reserva: id_pedido, id_clientes (chave para tbusuarios), pessoas, data_pedido, status. Status só admite 'Em Análise' (inicial) e 'Cancelado'.
+
+## Sinais
+- status com outro texto: fora do domínio
+- linha de reserva toda vazia: cliente que ainda não reservou
+
+## Causa
+A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza.
+
+## Notas do modelo
+- [E1 · sin-12 · retificação de "cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza."] Corrigir a renderização para não exibir linhas com campos nulos quando o cliente não reservou. — Motivo: Este caso mostrou que a interface web exibe linhas incompletas, indicando uma falha na lógica de renderização quando os campos ausentes não são tratados adequadamente.
+- [E1 · semt-15 · retificação de "Status só admite 'Em Análise' (inicial) e 'Cancelado'."] Adicionar validação no backend para verificar se o status está dentro do domínio permitido. — Motivo: O caso mostrou que a API retorna um status inesperado, que não é tratado pelo frontend, causando o problema de reserva sem pessoas.
+- [E1 · semt-15 · retificação de "A leitura usa vw_tbpedidos, LEFT JOIN de tbusuarios (schema_completo.sql:57): cliente sem reserva vira linha com campos nulos, que reserva_cli.php renderiza."] Corrigir a lógica do LEFT JOIN para evitar linhas nulas quando o cliente não tem reserva. — Motivo: O caso mostrou que a API retorna linhas nulas para clientes sem reserva, que são renderizadas pelo frontend, causando o problema de reserva não alocada.
--- epoca-0/negocio/usuario-e-login.md
+++ epoca-2/negocio/usuario-e-login.md
@@ -0,0 +1,25 @@
+---
+# ! Alteração de IA - Revisar: verbete da biblioteca base da Fase 2-B (regra de negócio).
+# ! Motivo: o login do cliente É o CPF — sem isso o modelo não entende por que o campo
+# cpf da API vem de login_usuario nem por que nome/cpf trocados indicam junção errada.
+id: usuario-e-login
+titulo: Usuário, níveis e login
+sistema: Ambos
+entidade_principal: Usuario
+tipo: funcionamento
+status: ativo
+arquivos: [Programacao/CobaiaFront/admin/login.php, Programacao/CobaiaFront/admin/acesso_com.php, Programacao/CobaiaAPI/app/models.py]
+tabelas: [tbusuarios]
+sintomas: [reserva com nome de outro usuario, saudacao vazia]
+palavras_chave: [usuario, login, cpf, senha, nivel, sup, cli, administrador, cliente, sessao]
+causas_relacionadas: [chave_de_juncao_errada, nulo_inesperado]
+---
+## Resumo
+Conta em tbusuarios: login_usuario, senha_usuario, nivel_usuario ('sup' admin, 'cli' cliente). Para o cliente o login é o CPF, que vira o campo cpf da API.
+
+## Sinais
+- nome ou cpf de outra pessoa na reserva: junção por id trocada
+- saudação "Olá, !" sem nome: nome nulo vindo da view
+
+## Causa
+login.php:7 compara a senha em texto puro; 'sup' abre o painel, 'cli' abre cliente/index.php?cliente=<login>, falha vai a invasor.php.
```
