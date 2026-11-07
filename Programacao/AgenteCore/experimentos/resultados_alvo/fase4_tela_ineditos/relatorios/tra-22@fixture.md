<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-22`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/tra-22@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,81)

**IMPACTO (declarado):** `O usuário vê preços com valores muito altos, indicando um formato incorreto.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, escala_ou_unidade_errada, ficou com probabilidade 0,09. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,81); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 8, "nome": "Água Mineral", "resumo": "Garrafa 500ml, com ou sem gás", "tipo": "Bebidas", "preco": 600.0, "imagem": "agua.png", "destaque": false}, {"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4500.0, "imagem": "balde_cerveja.png", "destaque": true}]

SINTOMA OBSERVADO: Na grade de bebidas, a Agua Mineral aparece por 'R$ 600,00' e o Balde de Cerveja por 'R$ 4500,00'; nomes, categorias e fotos estao certos.

OBSERVAÇÃO ADICIONAL: Antes da falha, a mesma grade mostrava a Agua Mineral por 'R$ 6,00' e o Balde de Cerveja por 'R$ 45,00'.
```

## 3. Contraste com a segunda causa

tipo_divergente e não escala_ou_unidade_errada: a escolha tem probabilidade 0,81 contra 0,09; verbete(s) na evidência: entidade-produto, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,81 | sim |
| escala_ou_unidade_errada | 0,09 |  |
| valor_fora_do_dominio | 0,06 |  |
| formato_de_data_divergente | 0,04 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids tra-22 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1087 | 1 | entrada | programa | ao_vivo | 2026-11-06T12:08:02 | caso tra-22 |
| 1088 | 2 | candidatos | programa | ao_vivo | 2026-11-06T12:08:02 | 3 de 39 verbetes entregues |
| 1090 | 3 | prompt | programa | ao_vivo | 2026-11-06T12:08:02 | {"etapa": "diagnostico", "sha": "542035cd113c539d", "prompt_sha256": "542035cd113c", "chars": 3722, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1092 | 4 | inferencia | programa | ao_vivo | 2026-11-06T12:08:02 | diagnostico: 76,2 s |
| 1093 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T12:08:02 | causa_raiz: `tipo_divergente` |
| 1094 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T12:08:02 | campo: `preco` |
| 1095 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T12:08:02 | impacto: `O usuário vê preços com valores muito altos, indicando um formato incorreto.` |
| 1096 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T12:08:02 | fonte: `[entidade-produto], [contrato-produto]` |
| 1097 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T12:08:02 | fonte_citada: `entidade-produto` |
| 1098 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T12:08:02 | fonte_citada: `contrato-produto` |
| 1099 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | quatro_linhas_presentes: confere |
| 1100 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | rotulo_no_conjunto: confere |
| 1101 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_existe_na_biblioteca: confere |
| 1102 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_existe_na_biblioteca: confere |
| 1103 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_estava_no_contexto: confere |
| 1104 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_estava_no_contexto: confere |
| 1105 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | campo_existe_no_caso: confere |
| 1106 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1107 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | notas_nos_verbetes_citados: informativo |
| 1108 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | impacto: nao_verificavel |
| 1109 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_formato_valido: confere |
| 1110 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_contem_termo_da_causa: nao_confere |
| 1111 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T12:08:02 | fonte_contem_termo_da_causa: nao_confere |
| 1112 | 24 | decisao | programa | ao_vivo | 2026-11-06T12:08:02 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1112, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1088 (verbete_entregue, entidade-produto), evento 1088 (verbete_entregue, nulo_inesperado), evento 1088 (verbete_entregue, contrato-produto), evento 1092 (resposta), evento 1097 (verbete_citado, entidade-produto), evento 1098 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1087 a 1112 da trilha; hash dos eventos deste caso: `0c1e19ca903d4c06`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
