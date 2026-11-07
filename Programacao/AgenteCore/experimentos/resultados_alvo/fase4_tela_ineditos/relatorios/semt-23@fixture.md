<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-23`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/semt-23@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,91)

**IMPACTO (declarado):** `Os usuários vêem valores de preço negativos, que são incorretos e não fazem sentido no contexto do negócio.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,06. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": -80.9, "imagem": "costelona.jpg", "destaque": true}, {"id": 5, "nome": "Alcatra na Pedra", "resumo": "Alcatra grelhada servida na pedra quente", "tipo": "Carnes", "preco": -75.9, "imagem": "alcatra_pedra.jpg", "destaque": false}]

SINTOMA OBSERVADO: Os botoes de preco da grade mostram valores negativos, por exemplo 'R$ -80,90' na Costelona e 'R$ -75,90' na Alcatra na Pedra.
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,91 contra 0,06; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,91 | sim |
| valor_fora_do_dominio | 0,06 |  |
| colecao_no_lugar_de_objeto | 0,02 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
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

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids semt-23 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 831 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:57:26 | caso semt-23 |
| 832 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:57:26 | 3 de 39 verbetes entregues |
| 834 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:57:26 | {"etapa": "diagnostico", "sha": "674b9e1275955f45", "prompt_sha256": "674b9e127595", "chars": 3797, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 836 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:57:26 | diagnostico: 59,5 s |
| 837 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:57:26 | causa_raiz: `tipo_divergente` |
| 838 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:57:26 | campo: `preco` |
| 839 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:57:26 | impacto: `Os usuários vêem valores de preço negativos, que são incorretos e não fazem sentido no contexto do negócio.` |
| 840 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:57:26 | fonte: `[entidade-produto], [contrato-produto]` |
| 841 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:57:26 | fonte_citada: `entidade-produto` |
| 842 | 10 | declaracao | modelo | ao_vivo | 2026-11-06T11:57:26 | fonte_citada: `contrato-produto` |
| 843 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | quatro_linhas_presentes: confere |
| 844 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | rotulo_no_conjunto: confere |
| 845 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_existe_na_biblioteca: confere |
| 846 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_existe_na_biblioteca: confere |
| 847 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_estava_no_contexto: confere |
| 848 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_estava_no_contexto: confere |
| 849 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | campo_existe_no_caso: confere |
| 850 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 851 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | notas_nos_verbetes_citados: informativo |
| 852 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | impacto: nao_verificavel |
| 853 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_formato_valido: confere |
| 854 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_contem_termo_da_causa: nao_confere |
| 855 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:57:26 | fonte_contem_termo_da_causa: nao_confere |
| 856 | 24 | decisao | programa | ao_vivo | 2026-11-06T11:57:26 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 856, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 832 (verbete_entregue, entidade-produto), evento 832 (verbete_entregue, contrato-produto), evento 832 (verbete_entregue, tipo_divergente), evento 836 (resposta), evento 841 (verbete_citado, entidade-produto), evento 842 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 831 a 856 da trilha; hash dos eventos deste caso: `98089b037db20f4c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
