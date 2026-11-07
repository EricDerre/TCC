<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/tra-20@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `chave_de_juncao_errada` · **CAMPO:** `tipo` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.`

Justificativa (gerada por molde): O agente respondeu chave_de_juncao_errada no campo tipo porque os verbetes entidade-produto, contrato-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Sobremesas", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}, {"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Sobremesas", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]

SINTOMA OBSERVADO: Fraldinha e Costelona (os dois cortes de carne) aparecem na categoria Sobremesas; os demais produtos de carne da listagem continuam certos em Carnes.

OBSERVAÇÃO ADICIONAL: tbprodutos.id_tipo_produto de id 3 e id 4 aponta pra 1 (Carnes) no banco; so esses dois produtos vem errados na resposta, o que sugere troca pontual de id_tipo_produto pra 4 (Sobremesas) nesses dois registros, nao um bug geral de juncao.
```

## 3. Contraste com a segunda causa

chave_de_juncao_errada e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, chave_de_juncao_errada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| chave_de_juncao_errada | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| registro_duplicado | 0,00 |  |

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-20 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2003 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:04:42 | caso tra-20 |
| 2004 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:04:42 | 3 de 39 verbetes entregues |
| 2006 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:04:42 | {"etapa": "diagnostico", "sha": "25eb4bf32d3b0341", "prompt_sha256": "25eb4bf32d3b", "chars": 4504, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2008 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:04:42 | diagnostico: 71,2 s |
| 2009 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | causa_raiz: `chave_de_juncao_errada` |
| 2010 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | campo: `tipo` |
| 2011 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | impacto: `Os produtos Fraldinha e Costelona, que são cortes de carne, aparecem incorretamente na categoria Sobremesas na interface web.` |
| 2012 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | fonte: `[chave_de_juncao_errada]` |
| 2013 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:04:42 | fonte_citada: `chave_de_juncao_errada` |
| 2014 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | quatro_linhas_presentes: confere |
| 2015 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | rotulo_no_conjunto: confere |
| 2016 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_existe_na_biblioteca: confere |
| 2017 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_estava_no_contexto: confere |
| 2018 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | campo_existe_no_caso: confere |
| 2019 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2020 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | notas_nos_verbetes_citados: informativo |
| 2021 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | impacto: nao_verificavel |
| 2022 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_formato_valido: confere |
| 2023 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:04:42 | fonte_contem_termo_da_causa: confere |
| 2024 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:04:42 | diagnostico: escolha chave_de_juncao_errada; divergência não |

</details>

Nós de decisão:

- evento 2024, `diagnostico`: escolha `chave_de_juncao_errada`; resultado rotulo_emitido; evidência: evento 2004 (verbete_entregue, entidade-produto), evento 2004 (verbete_entregue, contrato-produto), evento 2004 (verbete_entregue, chave_de_juncao_errada), evento 2008 (resposta), evento 2013 (verbete_citado, chave_de_juncao_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, chave_de_juncao_errada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2003 a 2024 da trilha; hash dos eventos deste caso: `b38bacc68d54d8f3`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
