<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-22@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê todos os preços como 'R$ 0,00' porque os campos 'preco' estão retornando 'null', embora o contrato especifique que devem ser números.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo preco porque os verbetes nulo_inesperado, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 6, "nome": "Maminha", "resumo": "Corte macio grelhado na brasa", "tipo": "Carnes", "preco": null, "imagem": "maminha.jpg", "destaque": false}, {"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Carnes", "preco": null, "imagem": "cupim.jpg", "destaque": true}]

SINTOMA OBSERVADO: Todos os botoes de preco da grade mostram 'R$ 0,00'. Os nomes, as categorias e as fotos estao normais.
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-22 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 773 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:55:12 | caso semt-22 |
| 774 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:55:12 | 3 de 39 verbetes entregues |
| 776 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:55:12 | {"etapa": "diagnostico", "sha": "f37d5d35a5d5be0f", "prompt_sha256": "f37d5d35a5d5", "chars": 3546, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 778 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:55:12 | diagnostico: 43,7 s |
| 779 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:55:12 | causa_raiz: `nulo_inesperado` |
| 780 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:55:12 | campo: `preco` |
| 781 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:55:12 | impacto: `O usuário vê todos os preços como 'R$ 0,00' porque os campos 'preco' estão retornando 'null', embora o contrato especifique que devem ser números.` |
| 782 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:55:12 | fonte: `[nulo_inesperado]` |
| 783 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:55:12 | fonte_citada: `nulo_inesperado` |
| 784 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | quatro_linhas_presentes: confere |
| 785 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | rotulo_no_conjunto: confere |
| 786 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | fonte_existe_na_biblioteca: confere |
| 787 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | fonte_estava_no_contexto: confere |
| 788 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | campo_existe_no_caso: confere |
| 789 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 790 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | notas_nos_verbetes_citados: informativo |
| 791 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | impacto: nao_verificavel |
| 792 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | fonte_formato_valido: confere |
| 793 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:55:12 | fonte_contem_termo_da_causa: confere |
| 794 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:55:12 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 794, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 774 (verbete_entregue, nulo_inesperado), evento 774 (verbete_entregue, contrato-produto), evento 774 (verbete_entregue, entidade-produto), evento 778 (resposta), evento 783 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 773 a 794 da trilha; hash dos eventos deste caso: `d43945238533da38`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
