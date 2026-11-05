<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-10`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-10@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `valor_fora_do_dominio` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,62) · **CONFLITO**: nenhum verbete entregue trata da causa respondida valor_fora_do_dominio

**IMPACTO (declarado):** `O usuário vê um preço diferente do retornado pela API, exibindo 'R$ 79,90' em vez de 'R$ 84,90'.`

Justificativa (gerada por molde): O agente respondeu valor_fora_do_dominio no campo preco porque os verbetes contrato-produto, entidade-produto, estado_da_tela_divergente, interface-frontend estavam entre os entregues ao modelo. A segunda causa, dado_desatualizado, ficou com probabilidade 0,19. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida valor_fora_do_dominio. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo). O agente não está seguro desta causa (probabilidade 0,62); trate como hipótese e confira o campo preco antes de agir.

**Biblioteca:** 1 edição(ões) aplicada(s) ([interface-frontend]), 0 para revisão humana, 1 recusada(s) (trecho_nao_encontrado).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-10. A proposta 1 (nota em [interface-frontend], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (retificacao em [contrato-produto]) foi recusada por a validação da Fase 3 com o código trecho_nao_encontrado: 'Notas: Notar que o contrato especifica a estrutura do JSON e' não aparece em [contrato-produto].

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `interface-frontend` | aceita | nenhum | **aplicada** | 1 |
| 2 | retificacao | `contrato-produto` | recusada: `trecho_nao_encontrado` | nenhum | recusada: `trecho_nao_encontrado` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (consultado agora, com a pagina aberta desde antes da alteracao do cadastro)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 84.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: A API, consultada agora, devolve preco 84.9 para a Costelona, mas o cartao na tela continua exibindo 'R$ 79,90'; nenhum erro no console.

OBSERVAÇÃO ADICIONAL: A pagina foi carregada antes de o administrador alterar o preco no cadastro e nao foi recarregada; a grade so e redesenhada quando carregarProdutos() roda.
```

## 3. Contraste com a segunda causa

valor_fora_do_dominio e não dado_desatualizado: a escolha tem probabilidade 0,62 contra 0,19; verbete(s) na evidência: contrato-produto, entidade-produto, estado_da_tela_divergente, interface-frontend

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| valor_fora_do_dominio | 0,62 | sim |
| dado_desatualizado | 0,19 |  |
| tipo_divergente | 0,07 |  |
| escala_ou_unidade_errada | 0,05 |  |
| campo_ausente | 0,04 |  |
| campo_renomeado | 0,04 |  |
| formato_de_data_divergente | 0,02 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente`, `interface-frontend` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `estado_da_tela_divergente`, `interface-frontend` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto], [entidade-produto]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "entidade-produto"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "valor_fora_do_dominio"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>28 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1732 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:06:39 | caso efe-10 |
| 1733 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:06:39 | 3 de 40 verbetes entregues |
| 1735 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:06:39 | {"chars": 3899, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "910f7fd8598d", "sha": "910f7fd8598d7e86"} |
| 1737 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:06:39 | diagnostico: 77,3 s |
| 1738 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:06:39 | causa_raiz: `valor_fora_do_dominio` |
| 1739 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:06:39 | campo: `preco` |
| 1740 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:06:39 | impacto: `O usuário vê um preço diferente do retornado pela API, exibindo 'R$ 79,90' em vez de 'R$ 84,90'.` |
| 1741 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:06:39 | fonte: `[contrato-produto], [entidade-produto]` |
| 1742 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:06:39 | fonte_citada: `contrato-produto` |
| 1743 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:06:39 | fonte_citada: `entidade-produto` |
| 1744 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | quatro_linhas_presentes: confere |
| 1745 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | rotulo_no_conjunto: confere |
| 1746 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_existe_na_biblioteca: confere |
| 1747 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_existe_na_biblioteca: confere |
| 1748 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_estava_no_contexto: confere |
| 1749 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_estava_no_contexto: confere |
| 1750 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | campo_existe_no_caso: confere |
| 1751 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1752 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | notas_nos_verbetes_citados: informativo |
| 1753 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | impacto: nao_verificavel |
| 1754 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_formato_valido: confere |
| 1755 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_contem_termo_da_causa: nao_confere |
| 1756 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:06:39 | fonte_contem_termo_da_causa: nao_confere |
| 1757 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:06:39 | diagnostico: escolha valor_fora_do_dominio; divergência sim |
| 1760 | 25 | inferencia | programa | ao_vivo | 2026-11-04T00:08:01 | proposta: 159,0 s |
| 1762 | 26 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:08:01 | proposta 1: nota em [interface-frontend]: aplicada |
| 1764 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:08:01 | proposta 2: retificacao em [contrato-produto]: recusada: trecho_nao_encontrado |
| 1765 | 28 | decisao | programa | ao_vivo | 2026-11-04T00:08:01 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 1757, `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido; evidência: evento 1733 (verbete_entregue, contrato-produto), evento 1733 (verbete_entregue, entidade-produto), evento 1733 (verbete_entregue, estado_da_tela_divergente), evento 1733 (verbete_entregue, interface-frontend), evento 1737 (resposta), evento 1742 (verbete_citado, contrato-produto), evento 1743 (verbete_citado, entidade-produto); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: contrato-produto, entidade-produto, estado_da_tela_divergente, interface-frontend (gen_ai: chat)
- evento 1765, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 1737 (resposta), evento 1760 (resposta), evento 1762 (verbete_entregue, interface-frontend), evento 1764 (verbete_entregue, contrato-produto); divergência: sim; falha: nenhuma; prov.used: contrato-produto, entidade-produto, estado_da_tela_divergente, interface-frontend

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1732 a 1765 da trilha; hash dos eventos deste caso: `12f344fd5d7acb21`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
