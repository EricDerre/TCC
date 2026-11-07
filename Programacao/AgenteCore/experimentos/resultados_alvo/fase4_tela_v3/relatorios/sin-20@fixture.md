<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/sin-20@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `id` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê um botão 'Saiba Mais...' sem identificador, resultando em uma ação sem efeito.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo id porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, resposta_truncada, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]

SINTOMA OBSERVADO: O card da Fraldinha aparece normal, com nome, preco e imagem certos, mas o botao 'Saiba Mais...' fica com data-id="undefined"; clicar nele abre o modal mostrando 'Erro'.

OBSERVAÇÃO ADICIONAL: So o segundo item da resposta nao traz id; o primeiro (Picanha ao Alho) esta completo.
```

## 3. Contraste com a segunda causa

campo_ausente e não resposta_truncada: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 1,00 | sim |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| tipo_divergente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[campo_ausente]`; verbetes citados: `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[campo_ausente]` | confere | {"ids": ["campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids sin-20 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1524 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:35:04 | caso sin-20 |
| 1525 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:35:04 | 3 de 39 verbetes entregues |
| 1527 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:35:04 | {"etapa": "diagnostico", "sha": "b01dc9310b7c2384", "prompt_sha256": "b01dc9310b7c", "chars": 3783, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1529 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:35:04 | diagnostico: 45,4 s |
| 1530 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:35:04 | causa_raiz: `campo_ausente` |
| 1531 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:35:04 | campo: `id` |
| 1532 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:35:04 | impacto: `O usuário vê um botão 'Saiba Mais...' sem identificador, resultando em uma ação sem efeito.` |
| 1533 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:35:04 | fonte: `[campo_ausente]` |
| 1534 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:35:04 | fonte_citada: `campo_ausente` |
| 1535 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | quatro_linhas_presentes: confere |
| 1536 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | rotulo_no_conjunto: confere |
| 1537 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | fonte_existe_na_biblioteca: confere |
| 1538 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | fonte_estava_no_contexto: confere |
| 1539 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | campo_existe_no_caso: confere |
| 1540 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1541 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | notas_nos_verbetes_citados: informativo |
| 1542 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | impacto: nao_verificavel |
| 1543 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | fonte_formato_valido: confere |
| 1544 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:35:04 | fonte_contem_termo_da_causa: confere |
| 1545 | 20 | decisao | programa | ao_vivo | 2026-11-05T19:35:04 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1545, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1525 (verbete_entregue, entidade-produto), evento 1525 (verbete_entregue, contrato-produto), evento 1525 (verbete_entregue, campo_ausente), evento 1529 (resposta), evento 1534 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1524 a 1545 da trilha; hash dos eventos deste caso: `a02fc1549b574601`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
