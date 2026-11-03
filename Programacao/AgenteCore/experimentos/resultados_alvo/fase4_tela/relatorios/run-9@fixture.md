<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-9`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/run-9@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tempo_de_resposta_excedido` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário percebeu uma demora significativa na resposta da API, impactando a experiência de uso.`

Justificativa (gerada por molde): O agente respondeu tempo_de_resposta_excedido porque os verbetes entidade-produto, contrato-produto, resposta_truncada estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}] (recebido apos 9,4 s)

SINTOMA OBSERVADO: A listagem carrega, mas demora quase 10 segundos.

OBSERVAÇÃO ADICIONAL: O mesmo endpoint respondia em 120 ms na semana anterior.
```

## 3. Contraste com a segunda causa

tempo_de_resposta_excedido e não tipo_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: entidade-produto, contrato-produto, resposta_truncada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tempo_de_resposta_excedido | 1,00 | sim |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[resposta_truncada]`; verbetes citados: `resposta_truncada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `resposta_truncada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `resposta_truncada` | confere | contexto: `entidade-produto`, `contrato-produto`, `resposta_truncada` |
| Algum verbete do contexto trata da causa respondida | `tempo_de_resposta_excedido` | confere | verbetes: `resposta_truncada` |
| fonte_formato_valido | `[resposta_truncada]` | confere | {"ids": ["resposta_truncada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `resposta_truncada` | **não confere** | {"termo": "tempo_de_resposta_excedido"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nenhum` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids run-9 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1326 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:00:44 | caso run-9 |
| 1327 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:00:44 | 3 de 40 verbetes entregues |
| 1329 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:00:44 | {"etapa": "diagnostico", "sha": "732550e48ff82416", "prompt_sha256": "732550e48ff8", "chars": 3750, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1331 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:00:44 | diagnostico: 51,1 s |
| 1332 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:00:44 | causa_raiz: `tempo_de_resposta_excedido` |
| 1333 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:00:44 | campo: `nenhum` |
| 1334 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:00:44 | impacto: `O usuário percebeu uma demora significativa na resposta da API, impactando a experiência de uso.` |
| 1335 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:00:44 | fonte: `[resposta_truncada]` |
| 1336 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:00:44 | fonte_citada: `resposta_truncada` |
| 1337 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | quatro_linhas_presentes: confere |
| 1338 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | rotulo_no_conjunto: confere |
| 1339 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | fonte_existe_na_biblioteca: confere |
| 1340 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | fonte_estava_no_contexto: confere |
| 1341 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | campo_existe_no_caso: nao_se_aplica |
| 1342 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1343 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | notas_nos_verbetes_citados: informativo |
| 1344 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | impacto: nao_verificavel |
| 1345 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | fonte_formato_valido: confere |
| 1346 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:00:44 | fonte_contem_termo_da_causa: nao_confere |
| 1347 | 20 | decisao | programa | ao_vivo | 2026-11-01T12:00:44 | diagnostico: escolha tempo_de_resposta_excedido; divergência não |

</details>

Nós de decisão:

- evento 1347, `diagnostico`: escolha `tempo_de_resposta_excedido`; resultado rotulo_emitido; evidência: evento 1327 (verbete_entregue, entidade-produto), evento 1327 (verbete_entregue, contrato-produto), evento 1327 (verbete_entregue, resposta_truncada), evento 1331 (resposta), evento 1336 (verbete_citado, resposta_truncada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, resposta_truncada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1326 a 1347 da trilha; hash dos eventos deste caso: `e74aebc3e118f851`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
