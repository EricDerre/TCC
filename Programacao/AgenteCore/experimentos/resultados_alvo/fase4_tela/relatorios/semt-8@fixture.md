<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-8`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-8@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,85)

**IMPACTO (declarado):** `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo preco porque os verbetes entidade-produto, nulo_inesperado, contrato-produto estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,08. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": null, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O cartao exibe 'R$ 0,00' para um produto que custa 89,90.
```

## 3. Contraste com a segunda causa

nulo_inesperado e não tipo_divergente: a escolha tem probabilidade 0,85 contra 0,08; verbete(s) na evidência: entidade-produto, nulo_inesperado, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,85 | sim |
| tipo_divergente | 0,08 |  |
| valor_fora_do_dominio | 0,05 |  |
| formato_de_data_divergente | 0,01 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `nulo_inesperado`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-8 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1029 | 1 | entrada | programa | ao_vivo | 2026-11-01T11:49:38 | caso semt-8 |
| 1030 | 2 | candidatos | programa | ao_vivo | 2026-11-01T11:49:38 | 3 de 40 verbetes entregues |
| 1032 | 3 | prompt | programa | ao_vivo | 2026-11-01T11:49:38 | {"etapa": "diagnostico", "sha": "c24829ec7be8e8b1", "prompt_sha256": "c24829ec7be8", "chars": 3350, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1034 | 4 | inferencia | programa | ao_vivo | 2026-11-01T11:49:38 | diagnostico: 63,9 s |
| 1035 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T11:49:38 | causa_raiz: `nulo_inesperado` |
| 1036 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T11:49:38 | campo: `preco` |
| 1037 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T11:49:38 | impacto: `O usuário vê 'R$ 0,00' em vez do preço correto de R$ 89,90.` |
| 1038 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T11:49:38 | fonte: `[nulo_inesperado]` |
| 1039 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T11:49:38 | fonte_citada: `nulo_inesperado` |
| 1040 | 10 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | quatro_linhas_presentes: confere |
| 1041 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | rotulo_no_conjunto: confere |
| 1042 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | fonte_existe_na_biblioteca: confere |
| 1043 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | fonte_estava_no_contexto: confere |
| 1044 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | campo_existe_no_caso: confere |
| 1045 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1046 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | notas_nos_verbetes_citados: informativo |
| 1047 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | impacto: nao_verificavel |
| 1048 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | fonte_formato_valido: confere |
| 1049 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T11:49:38 | fonte_contem_termo_da_causa: confere |
| 1050 | 20 | decisao | programa | ao_vivo | 2026-11-01T11:49:38 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1050, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1030 (verbete_entregue, entidade-produto), evento 1030 (verbete_entregue, nulo_inesperado), evento 1030 (verbete_entregue, contrato-produto), evento 1034 (resposta), evento 1039 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, nulo_inesperado, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1029 a 1050 da trilha; hash dos eventos deste caso: `03fc14721e334704`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
