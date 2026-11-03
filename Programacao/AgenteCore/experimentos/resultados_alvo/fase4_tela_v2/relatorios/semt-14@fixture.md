<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-14`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-14@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `tipo` · selo de probabilidade: **baixo** (p = 0,74)

**IMPACTO (declarado):** `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo tipo porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,25. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo tipo antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": 8, "nome": "Agua Mineral", "resumo": "500ml", "tipo": null, "preco": 6.0, "imagem": "agua.png", "destaque": false}]

SINTOMA OBSERVADO: O filtro por categoria deixa de listar alguns produtos que existem no cadastro.
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,74 contra 0,25; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,74 | sim |
| tipo_divergente | 0,25 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| valor_fora_do_dominio | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [nulo_inesperado]`; verbetes citados: `contrato-produto`, `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[contrato-produto], [nulo_inesperado]` | confere | {"ids": ["contrato-produto", "nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "nulo_inesperado"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-14 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1161 | 1 | entrada | programa | ao_vivo | 2026-11-01T14:53:13 | caso semt-14 |
| 1162 | 2 | candidatos | programa | ao_vivo | 2026-11-01T14:53:13 | 3 de 40 verbetes entregues |
| 1164 | 3 | prompt | programa | ao_vivo | 2026-11-01T14:53:13 | {"etapa": "diagnostico", "sha": "4f40cbe2904603c7", "prompt_sha256": "4f40cbe29046", "chars": 3495, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1166 | 4 | inferencia | programa | ao_vivo | 2026-11-01T14:53:13 | diagnostico: 48,9 s |
| 1167 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T14:53:13 | causa_raiz: `nulo_inesperado` |
| 1168 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T14:53:13 | campo: `tipo` |
| 1169 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T14:53:13 | impacto: `O filtro por categoria não exibe corretamente os produtos, pois alguns tipos estão ausentes na resposta.` |
| 1170 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T14:53:13 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 1171 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T14:53:13 | fonte_citada: `contrato-produto` |
| 1172 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T14:53:13 | fonte_citada: `nulo_inesperado` |
| 1173 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | quatro_linhas_presentes: confere |
| 1174 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | rotulo_no_conjunto: confere |
| 1175 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_existe_na_biblioteca: confere |
| 1176 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_existe_na_biblioteca: confere |
| 1177 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_estava_no_contexto: confere |
| 1178 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_estava_no_contexto: confere |
| 1179 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | campo_existe_no_caso: confere |
| 1180 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1181 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | notas_nos_verbetes_citados: informativo |
| 1182 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | impacto: nao_verificavel |
| 1183 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_formato_valido: confere |
| 1184 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_contem_termo_da_causa: nao_confere |
| 1185 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T14:53:13 | fonte_contem_termo_da_causa: confere |
| 1186 | 24 | decisao | programa | ao_vivo | 2026-11-01T14:53:13 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1186, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1162 (verbete_entregue, entidade-produto), evento 1162 (verbete_entregue, contrato-produto), evento 1162 (verbete_entregue, nulo_inesperado), evento 1166 (resposta), evento 1171 (verbete_citado, contrato-produto), evento 1172 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1161 a 1186 da trilha; hash dos eventos deste caso: `1f7ce7d16c3e6bf2`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
