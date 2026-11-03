<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-3`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/efe-3@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,58)

**IMPACTO (declarado):** `Os cartões aparecem sem foto nenhuma, pois o campo "imagem" está ausente na resposta da API.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo imagem porque os verbetes entidade-produto, contrato-produto, campo_ausente estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,23. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,58); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "destaque": true}]

SINTOMA OBSERVADO: Os cartoes aparecem sem foto nenhuma (nem o espaco da imagem e desenhado), mas nome e preco corretos.
```

## 3. Contraste com a segunda causa

campo_ausente e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,58 contra 0,23; verbete(s) na evidência: entidade-produto, contrato-produto, campo_ausente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,58 | sim |
| colecao_no_lugar_de_objeto | 0,23 |  |
| resposta_truncada | 0,10 |  |
| tipo_divergente | 0,04 |  |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| formato_de_data_divergente | 0,01 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [campo_ausente]`; verbetes citados: `contrato-produto`, `campo_ausente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `campo_ausente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| O verbete citado estava no contexto entregue ao modelo | `campo_ausente` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_ausente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto`, `campo_ausente` |
| fonte_formato_valido | `[contrato-produto] [campo_ausente]` | confere | {"ids": ["contrato-produto", "campo_ausente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |
| fonte_contem_termo_da_causa | `campo_ausente` | confere | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids efe-3 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 607 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:33:46 | caso efe-3 |
| 608 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:33:46 | 3 de 40 verbetes entregues |
| 610 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:33:46 | {"etapa": "diagnostico", "sha": "11a3fe94e7df2dcc", "prompt_sha256": "11a3fe94e7df", "chars": 3419, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 612 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:33:46 | diagnostico: 31,9 s |
| 613 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:33:46 | causa_raiz: `campo_ausente` |
| 614 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:33:46 | campo: `imagem` |
| 615 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:33:46 | impacto: `Os cartões aparecem sem foto nenhuma, pois o campo "imagem" está ausente na resposta da API.` |
| 616 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:33:46 | fonte: `[contrato-produto] [campo_ausente]` |
| 617 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:33:46 | fonte_citada: `contrato-produto` |
| 618 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T11:33:46 | fonte_citada: `campo_ausente` |
| 619 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | quatro_linhas_presentes: confere |
| 620 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | rotulo_no_conjunto: confere |
| 621 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_existe_na_biblioteca: confere |
| 622 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_existe_na_biblioteca: confere |
| 623 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_estava_no_contexto: confere |
| 624 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_estava_no_contexto: confere |
| 625 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | campo_existe_no_caso: confere |
| 626 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 627 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | notas_nos_verbetes_citados: informativo |
| 628 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | impacto: nao_verificavel |
| 629 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_formato_valido: confere |
| 630 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_contem_termo_da_causa: nao_confere |
| 631 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T11:33:46 | fonte_contem_termo_da_causa: confere |
| 632 | 24 | decisao | programa | ao_vivo | 2026-11-01T11:33:46 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 632, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 608 (verbete_entregue, entidade-produto), evento 608 (verbete_entregue, contrato-produto), evento 608 (verbete_entregue, campo_ausente), evento 612 (resposta), evento 617 (verbete_citado, contrato-produto), evento 618 (verbete_citado, campo_ausente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_ausente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 607 a 632 da trilha; hash dos eventos deste caso: `c8676db5255709d9`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
