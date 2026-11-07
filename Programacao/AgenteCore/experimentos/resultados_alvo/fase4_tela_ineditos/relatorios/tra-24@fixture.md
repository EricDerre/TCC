<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-24`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-24@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,92)

**IMPACTO (declarado):** `O usuário vê categorias incorretas para alguns produtos na grade.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo tipo porque os verbetes entidade-produto, contrato-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,04. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 7, "nome": "Cupim", "resumo": "Cupim assado lentamente, bem macio", "tipo": "Bebidas", "preco": 76.9, "imagem": "cupim.jpg", "destaque": true}, {"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 6.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 45.0, "imagem": "balde_cerveja.png", "destaque": true}, {"id": 10, "nome": "Refrigerante", "resumo": "Lata 350ml, diversos sabores", "tipo": "Acompanhamentos", "preco": 7.0, "imagem": "refrigerante.png", "destaque": false}]

SINTOMA OBSERVADO: Na grade, o Cupim aparece com a categoria 'Bebidas' e o Refrigerante com 'Acompanhamentos'; a Agua Mineral e o Balde de Cerveja aparecem com 'Bebidas'. Os nomes, os precos e as fotos estao certos.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 7 a 10; a lista completa tem 14.
```

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não tipo_divergente: a escolha tem probabilidade 0,92 contra 0,04; verbete(s) na evidência: entidade-produto, contrato-produto, chave_de_juncao_errada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 0,92 | sim |
| tipo_divergente | 0,04 |  |
| colecao_no_lugar_de_objeto | 0,02 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[chave_de_juncao_errada]`; verbetes citados: `chave_de_juncao_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `chave_de_juncao_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `chave_de_juncao_errada` | confere | contexto: `entidade-produto`, `contrato-produto`, `chave_de_juncao_errada` |
| Algum verbete do contexto trata da causa respondida | `chave_de_juncao_errada` | confere | verbetes: `entidade-produto`, `chave_de_juncao_errada` |
| fonte_formato_valido | `[chave_de_juncao_errada]` | confere | {"ids": ["chave_de_juncao_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `chave_de_juncao_errada` | confere | {"termo": "chave_de_juncao_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-24 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1150 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:10:50 | caso tra-24 |
| 1151 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:10:50 | 3 de 39 verbetes entregues |
| 1153 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:10:50 | {"etapa": "diagnostico", "sha": "53c404d400f96e17", "prompt_sha256": "53c404d400f9", "chars": 4674, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1155 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:10:50 | diagnostico: 72,7 s |
| 1156 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:10:50 | causa_raiz: `chave_de_juncao_errada` |
| 1157 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:10:50 | campo: `tipo` |
| 1158 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:10:50 | impacto: `O usuário vê categorias incorretas para alguns produtos na grade.` |
| 1159 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:10:50 | fonte: `[chave_de_juncao_errada]` |
| 1160 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:10:50 | fonte_citada: `chave_de_juncao_errada` |
| 1161 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | quatro_linhas_presentes: confere |
| 1162 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | rotulo_no_conjunto: confere |
| 1163 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | fonte_existe_na_biblioteca: confere |
| 1164 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | fonte_estava_no_contexto: confere |
| 1165 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | campo_existe_no_caso: confere |
| 1166 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1167 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | notas_nos_verbetes_citados: informativo |
| 1168 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | impacto: nao_verificavel |
| 1169 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | fonte_formato_valido: confere |
| 1170 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:10:50 | fonte_contem_termo_da_causa: confere |
| 1171 | 20 | decisao | programa | ao_vivo | 2026-11-06T12:10:50 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 1171, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 1151 (verbete_entregue, entidade-produto), evento 1151 (verbete_entregue, contrato-produto), evento 1151 (verbete_entregue, chave_de_juncao_errada), evento 1155 (resposta), evento 1160 (verbete_citado, chave_de_juncao_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, chave_de_juncao_errada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1150 a 1171 da trilha; hash dos eventos deste caso: `daefec433076d24d`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
