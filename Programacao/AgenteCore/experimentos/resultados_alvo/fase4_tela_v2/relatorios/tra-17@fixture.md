<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/tra-17@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,95)

**IMPACTO (declarado):** `O usuário vê a categoria como 'CAR' em vez de 'Carnes'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, chave_de_juncao_errada, ficou com probabilidade 0,03. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "CAR", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria da Picanha ao Alho aparece como 'CAR' no card, em vez de 'Carnes'.

OBSERVAÇÃO ADICIONAL: tbtipos.id 1 tem sigla_tipo='CAR' e rotulo_tipo='Carnes'; o contrato usa o rotulo, nao a sigla.
```

## 3. Contraste com a segunda causa

tipo_divergente e não chave_de_juncao_errada: a escolha tem probabilidade 0,95 contra 0,03; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,95 | sim |
| chave_de_juncao_errada | 0,03 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids tra-17 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1975 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:23:22 | caso tra-17 |
| 1976 | 2 | candidatos | programa | ao_vivo | 2026-11-01T15:23:22 | 3 de 40 verbetes entregues |
| 1978 | 3 | prompt | programa | ao_vivo | 2026-11-01T15:23:22 | {"etapa": "diagnostico", "sha": "70f4952363c0a22b", "prompt_sha256": "70f4952363c0", "chars": 3519, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1980 | 4 | inferencia | programa | ao_vivo | 2026-11-01T15:23:22 | diagnostico: 33,9 s |
| 1981 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T15:23:22 | causa_raiz: `tipo_divergente` |
| 1982 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T15:23:22 | campo: `tipo` |
| 1983 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T15:23:22 | impacto: `O usuário vê a categoria como 'CAR' em vez de 'Carnes'.` |
| 1984 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T15:23:22 | fonte: `[entidade-produto], [contrato-produto]` |
| 1985 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T15:23:22 | fonte_citada: `entidade-produto` |
| 1986 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T15:23:22 | fonte_citada: `contrato-produto` |
| 1987 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | quatro_linhas_presentes: confere |
| 1988 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | rotulo_no_conjunto: confere |
| 1989 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_existe_na_biblioteca: confere |
| 1990 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_existe_na_biblioteca: confere |
| 1991 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_estava_no_contexto: confere |
| 1992 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_estava_no_contexto: confere |
| 1993 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | campo_existe_no_caso: confere |
| 1994 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1995 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | notas_nos_verbetes_citados: informativo |
| 1996 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | impacto: nao_verificavel |
| 1997 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_formato_valido: confere |
| 1998 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_contem_termo_da_causa: nao_confere |
| 1999 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:23:22 | fonte_contem_termo_da_causa: nao_confere |
| 2000 | 24 | decisao | programa | ao_vivo | 2026-11-01T15:23:22 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 2000, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1976 (verbete_entregue, entidade-produto), evento 1976 (verbete_entregue, contrato-produto), evento 1976 (verbete_entregue, tipo_divergente), evento 1980 (resposta), evento 1985 (verbete_citado, entidade-produto), evento 1986 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1975 a 2000 da trilha; hash dos eventos deste caso: `f9a202e0352450b0`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
