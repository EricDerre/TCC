<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/lex-22@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `corpo_nao_e_json` · **CAMPO:** `nenhum` · selo de probabilidade: **medio** (p = 0,92)

**IMPACTO (declarado):** `A página Produtos exibe uma mensagem de erro e não carrega nenhum cartão de produto.`

Justificativa (gerada por molde): O agente respondeu corpo_nao_e_json porque os verbetes corpo_nao_e_json, mensagens-de-erro-do-codigo, corpo_vazio estavam entre os entregues ao modelo. A segunda causa, corpo_vazio, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
<html><body><h1>Erro</h1><p>Falha ao montar a resposta.</p></body></html>

SINTOMA OBSERVADO: A pagina Produtos (API) abre sem nenhum cartao. A linha de status acima da grade fica vermelha e mostra 'Erro ao carregar produtos da CobaiaAPI:' seguido de uma mensagem do navegador que cita o caractere inesperado '<' e diz que o texto nao e JSON valido. O status HTTP da resposta e 200.

OBSERVAÇÃO ADICIONAL: O Content-Type da resposta e text/html, nao application/json.
```

## 3. Contraste com a segunda causa

corpo_nao_e_json e não corpo_vazio: a escolha tem probabilidade 0,92 contra 0,00; verbete(s) na evidência: corpo_nao_e_json, mensagens-de-erro-do-codigo, corpo_vazio

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| corpo_nao_e_json | 0,92 | sim |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_nao_e_json]`; verbetes citados: `corpo_nao_e_json`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_nao_e_json` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_nao_e_json` | confere | contexto: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio` |
| Algum verbete do contexto trata da causa respondida | `corpo_nao_e_json` | confere | verbetes: `corpo_nao_e_json`, `mensagens-de-erro-do-codigo`, `corpo_vazio` |
| fonte_formato_valido | `[corpo_nao_e_json]` | confere | {"ids": ["corpo_nao_e_json"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `corpo_nao_e_json` | confere | {"termo": "corpo_nao_e_json"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids lex-22 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 43 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:29:08 | caso lex-22 |
| 44 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:29:08 | 3 de 39 verbetes entregues |
| 46 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:29:08 | {"etapa": "diagnostico", "sha": "c60ca336cb5a3ed8", "prompt_sha256": "c60ca336cb5a", "chars": 3820, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 48 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:29:08 | diagnostico: 64,1 s |
| 49 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:29:08 | causa_raiz: `corpo_nao_e_json` |
| 50 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:29:08 | campo: `nenhum` |
| 51 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:29:08 | impacto: `A página Produtos exibe uma mensagem de erro e não carrega nenhum cartão de produto.` |
| 52 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:29:08 | fonte: `[corpo_nao_e_json]` |
| 53 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:29:08 | fonte_citada: `corpo_nao_e_json` |
| 54 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | quatro_linhas_presentes: confere |
| 55 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | rotulo_no_conjunto: confere |
| 56 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | fonte_existe_na_biblioteca: confere |
| 57 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | fonte_estava_no_contexto: confere |
| 58 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | campo_existe_no_caso: nao_se_aplica |
| 59 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 60 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | notas_nos_verbetes_citados: informativo |
| 61 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | impacto: nao_verificavel |
| 62 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | fonte_formato_valido: confere |
| 63 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:29:08 | fonte_contem_termo_da_causa: confere |
| 64 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:29:08 | diagnostico: escolha corpo_nao_e_json; divergência não |

</details>

Nós de decisão:

- evento 64, `diagnostico`: escolha `corpo_nao_e_json`; resultado rotulo_emitido; evidência: evento 44 (verbete_entregue, corpo_nao_e_json), evento 44 (verbete_entregue, mensagens-de-erro-do-codigo), evento 44 (verbete_entregue, corpo_vazio), evento 48 (resposta), evento 53 (verbete_citado, corpo_nao_e_json); divergência: não; falha: nenhuma; prov.used: corpo_nao_e_json, mensagens-de-erro-do-codigo, corpo_vazio (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 43 a 64 da trilha; hash dos eventos deste caso: `1e3405e5d596a181`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
