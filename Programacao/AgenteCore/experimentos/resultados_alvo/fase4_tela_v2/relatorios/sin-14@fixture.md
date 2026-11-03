<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/sin-14@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `colecao_no_lugar_de_objeto` · **CAMPO:** `imagem_url` · selo de probabilidade: **baixo** (p = 0,31)

**IMPACTO (declarado):** `O ícone de imagem quebrado indica que o campo `imagem_url` está presente em uma coleção onde se esperava um objeto, causando a exibição incorreta.`

Justificativa (gerada por molde): O agente respondeu colecao_no_lugar_de_objeto no campo imagem_url porque os verbetes entidade-produto, contrato-produto, campo_renomeado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,17. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,31); trate como hipótese e confira o campo imagem_url antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem_url": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: Todos os cartoes mostram icone de imagem quebrada; o resto do dado esta certo.
```

## 3. Contraste com a segunda causa

colecao_no_lugar_de_objeto e não tipo_divergente: a escolha tem probabilidade 0,31 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, campo_renomeado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| colecao_no_lugar_de_objeto | 0,31 | sim |
| tipo_divergente | 0,17 |  |
| resposta_truncada | 0,16 |  |
| formato_de_data_divergente | 0,14 |  |
| campo_ausente | 0,09 |  |
| campo_renomeado | 0,09 |  |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `campo_renomeado` |
| Algum verbete do contexto trata da causa respondida | `colecao_no_lugar_de_objeto` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "colecao_no_lugar_de_objeto"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem_url` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids sin-14 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 977 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:45:55 | caso sin-14 |
| 978 | 2 | candidatos | programa | ao_vivo | 2026-11-01T14:45:55 | 3 de 40 verbetes entregues |
| 980 | 3 | prompt | programa | ao_vivo | 2026-11-01T14:45:55 | {"etapa": "diagnostico", "sha": "f827f5e0b766d79a", "prompt_sha256": "f827f5e0b766", "chars": 3588, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 982 | 4 | inferencia | programa | ao_vivo | 2026-11-01T14:45:55 | diagnostico: 51,1 s |
| 983 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T14:45:55 | causa_raiz: `colecao_no_lugar_de_objeto` |
| 984 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T14:45:55 | campo: `imagem_url` |
| 985 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T14:45:55 | impacto: `O ícone de imagem quebrado indica que o campo `imagem_url` está presente em uma coleção onde se esperava um objeto, causando a exibição incorreta.` |
| 986 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T14:45:55 | fonte: `[contrato-produto]` |
| 987 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T14:45:55 | fonte_citada: `contrato-produto` |
| 988 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | quatro_linhas_presentes: confere |
| 989 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | rotulo_no_conjunto: confere |
| 990 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | fonte_existe_na_biblioteca: confere |
| 991 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | fonte_estava_no_contexto: confere |
| 992 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | campo_existe_no_caso: confere |
| 993 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 994 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | notas_nos_verbetes_citados: informativo |
| 995 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | impacto: nao_verificavel |
| 996 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | fonte_formato_valido: confere |
| 997 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T14:45:55 | fonte_contem_termo_da_causa: nao_confere |
| 998 | 20 | decisao | programa | ao_vivo | 2026-11-01T14:45:55 | diagnostico: escolha colecao_no_lugar_de_objeto; divergência não |

</details>

Nós de decisão:

- evento 998, `diagnostico`: escolha `colecao_no_lugar_de_objeto`; resultado rotulo_emitido; evidência: evento 978 (verbete_entregue, entidade-produto), evento 978 (verbete_entregue, contrato-produto), evento 978 (verbete_entregue, campo_renomeado), evento 982 (resposta), evento 987 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, campo_renomeado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 977 a 998 da trilha; hash dos eventos deste caso: `f3d983a7364c3bc4`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
