<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-1@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,93)

**IMPACTO (declarado):** `A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, tipo_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,05. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": "89.90", "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A ordenacao por preco fica errada: 'R$ 9,90' aparece depois de 'R$ 89,90'.
```

## 3. Contraste com a segunda causa

tipo_divergente e não formato_de_data_divergente: a escolha tem probabilidade 0,93 contra 0,05; verbete(s) na evidência: entidade-produto, tipo_divergente, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,93 | sim |
| formato_de_data_divergente | 0,05 |  |
| valor_fora_do_dominio | 0,02 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `contrato-produto` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-1 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 290 | 1 | entrada | programa | ao_vivo | 2026-11-05T18:50:12 | caso semt-1 |
| 291 | 2 | candidatos | programa | ao_vivo | 2026-11-05T18:50:12 | 3 de 39 verbetes entregues |
| 293 | 3 | prompt | programa | ao_vivo | 2026-11-05T18:50:12 | {"etapa": "diagnostico", "sha": "9cbbd5d7decc1a4a", "prompt_sha256": "9cbbd5d7decc", "chars": 3560, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 295 | 4 | inferencia | programa | ao_vivo | 2026-11-05T18:50:12 | diagnostico: 72,7 s |
| 296 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T18:50:12 | causa_raiz: `tipo_divergente` |
| 297 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T18:50:12 | campo: `preco` |
| 298 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T18:50:12 | impacto: `A ordenação por preço fica errada, com 'R$ 9,90' aparecendo depois de 'R$ 89,90'.` |
| 299 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T18:50:12 | fonte: `[tipo_divergente]` |
| 300 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T18:50:12 | fonte_citada: `tipo_divergente` |
| 301 | 10 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | quatro_linhas_presentes: confere |
| 302 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | rotulo_no_conjunto: confere |
| 303 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | fonte_existe_na_biblioteca: confere |
| 304 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | fonte_estava_no_contexto: confere |
| 305 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | campo_existe_no_caso: confere |
| 306 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 307 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | notas_nos_verbetes_citados: informativo |
| 308 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | impacto: nao_verificavel |
| 309 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | fonte_formato_valido: confere |
| 310 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T18:50:12 | fonte_contem_termo_da_causa: confere |
| 311 | 20 | decisao | programa | ao_vivo | 2026-11-05T18:50:12 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 311, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 291 (verbete_entregue, entidade-produto), evento 291 (verbete_entregue, tipo_divergente), evento 291 (verbete_entregue, contrato-produto), evento 295 (resposta), evento 300 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 290 a 311 da trilha; hash dos eventos deste caso: `b8462adc8fe13695`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
