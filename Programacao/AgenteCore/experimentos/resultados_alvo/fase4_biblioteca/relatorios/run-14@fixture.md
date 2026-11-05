<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-14@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `dado_desatualizado` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê uma lista de produtos que não inclui o produto recém-cadastrado, enquanto o painel PHP já exibe o produto imediatamente.`

Justificativa (gerada por molde): O agente respondeu dado_desatualizado porque os verbetes dado_desatualizado, contagem_inconsistente, colecao_no_lugar_de_objeto estavam entre os entregues ao modelo. A segunda causa, tempo_de_resposta_excedido, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 0 edição(ões) aplicada(s), 0 para revisão humana, 1 recusada(s) (palavra_chave_invalida) · falha: `acrescimo_recusado_pela_validacao`.

Justificativa (gerada por molde): O modelo propôs 1 edição(ões) para o caso run-14. A proposta 1 (nota em [dado_desatualizado]) foi recusada por a validação da Fase 3 com o código palavra_chave_invalida: item de lista inválido: 'produto recem-cadastrado nao aparece na api por minutos'.

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `dado_desatualizado` | recusada: `palavra_chave_invalida` | nenhum | recusada: `palavra_chave_invalida` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: POST admin cadastra produto -> GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
GET devolveu 14 itens; o produto recem-cadastrado (id 15) nao esta na lista.

SINTOMA OBSERVADO: Produto cadastrado pelo painel nao aparece na aba de API por varios minutos.

OBSERVAÇÃO ADICIONAL: O painel PHP mostra o produto imediatamente; so a API atrasa.
```

## 3. Contraste com a segunda causa

dado_desatualizado e não tempo_de_resposta_excedido: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: dado_desatualizado, contagem_inconsistente, colecao_no_lugar_de_objeto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| dado_desatualizado | 1,00 | sim |
| tempo_de_resposta_excedido | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| registro_duplicado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[dado_desatualizado]`; verbetes citados: `dado_desatualizado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `dado_desatualizado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `dado_desatualizado` | confere | contexto: `dado_desatualizado`, `contagem_inconsistente`, `colecao_no_lugar_de_objeto` |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | confere | verbetes: `dado_desatualizado`, `contagem_inconsistente` |
| fonte_formato_valido | `[dado_desatualizado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["dado_desatualizado"]} |
| fonte_contem_termo_da_causa | `dado_desatualizado` | confere | {"termo": "dado_desatualizado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1565 | 1 | entrada | programa | ao_vivo | 2026-11-03T23:47:15 | caso run-14 |
| 1566 | 2 | candidatos | programa | ao_vivo | 2026-11-03T23:47:15 | 3 de 40 verbetes entregues |
| 1568 | 3 | prompt | programa | ao_vivo | 2026-11-03T23:47:15 | {"chars": 3503, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "69a3020da0ff", "sha": "69a3020da0ff3be3"} |
| 1570 | 4 | inferencia | programa | ao_vivo | 2026-11-03T23:47:15 | diagnostico: 69,1 s |
| 1571 | 5 | declaracao | modelo | ao_vivo | 2026-11-03T23:47:15 | causa_raiz: `dado_desatualizado` |
| 1572 | 6 | declaracao | modelo | ao_vivo | 2026-11-03T23:47:15 | campo: `nenhum` |
| 1573 | 7 | declaracao | modelo | ao_vivo | 2026-11-03T23:47:15 | impacto: `O usuário vê uma lista de produtos que não inclui o produto recém-cadastrado, enquanto o painel PHP já exibe o produto imediatamente.` |
| 1574 | 8 | declaracao | modelo | ao_vivo | 2026-11-03T23:47:15 | fonte: `[dado_desatualizado]` |
| 1575 | 9 | declaracao | modelo | ao_vivo | 2026-11-03T23:47:15 | fonte_citada: `dado_desatualizado` |
| 1576 | 10 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | quatro_linhas_presentes: confere |
| 1577 | 11 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | rotulo_no_conjunto: confere |
| 1578 | 12 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | fonte_existe_na_biblioteca: confere |
| 1579 | 13 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | fonte_estava_no_contexto: confere |
| 1580 | 14 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | campo_existe_no_caso: nao_se_aplica |
| 1581 | 15 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1582 | 16 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | notas_nos_verbetes_citados: informativo |
| 1583 | 17 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | impacto: nao_verificavel |
| 1584 | 18 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | fonte_formato_valido: confere |
| 1585 | 19 | verificacao | verificacao | ao_vivo | 2026-11-03T23:47:15 | fonte_contem_termo_da_causa: confere |
| 1586 | 20 | decisao | programa | ao_vivo | 2026-11-03T23:47:15 | diagnostico: escolha dado_desatualizado; divergência não |
| 1589 | 21 | inferencia | programa | ao_vivo | 2026-11-03T23:48:28 | proposta: 110,8 s |
| 1591 | 22 | edicao_biblioteca | programa | ao_vivo | 2026-11-03T23:48:28 | proposta 1: nota em [dado_desatualizado]: recusada: palavra_chave_invalida |
| 1592 | 23 | decisao | programa | ao_vivo | 2026-11-03T23:48:28 | edicao_biblioteca: escolha nenhuma; divergência sim |

</details>

Nós de decisão:

- evento 1586, `diagnostico`: escolha `dado_desatualizado`; resultado rotulo_emitido; evidência: evento 1566 (verbete_entregue, dado_desatualizado), evento 1566 (verbete_entregue, contagem_inconsistente), evento 1566 (verbete_entregue, colecao_no_lugar_de_objeto), evento 1570 (resposta), evento 1575 (verbete_citado, dado_desatualizado); divergência: não; falha: nenhuma; prov.used: dado_desatualizado, contagem_inconsistente, colecao_no_lugar_de_objeto (gen_ai: chat)
- evento 1592, `edicao_biblioteca`: escolha `nenhuma`; resultado recusada; evidência: evento 1570 (resposta), evento 1589 (resposta), evento 1591 (verbete_entregue, dado_desatualizado); divergência: sim; falha: acrescimo_recusado_pela_validacao; prov.used: colecao_no_lugar_de_objeto, contagem_inconsistente, dado_desatualizado

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1565 a 1592 da trilha; hash dos eventos deste caso: `10717ecd5130cbef`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
