<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-1@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,74) · **CONFLITO**: a FONTE cita o verbete valor_produto, que não existe na biblioteca; a FONTE cita o verbete valor_produto, fora do contexto entregue

**IMPACTO (declarado):** `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, estrutura_aninhada_divergente, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,17 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), 1 fora do contexto entregue (valor_produto). O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a FONTE cita o verbete valor_produto, que não existe na biblioteca; a FONTE cita o verbete valor_produto, fora do contexto entregue. Este nó está marcado com a falha citacao_inexistente (origem: modelo). O agente não está seguro desta causa (probabilidade 0,74); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Poda de `corpo_http` (evento 876): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

Trecho podado (hash `aff3accfceebc5e4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,74 contra 0,17; verbete(s) na evidência: entidade-produto, estrutura_aninhada_divergente, contrato-produto, valor_produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,74 | sim |
| valor_fora_do_dominio | 0,17 |  |
| formato_de_data_divergente | 0,05 |  |
| tipo_divergente | 0,04 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[valor_produto], [contrato-produto]`; verbetes citados: `valor_produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_produto` | **não confere** |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_produto` | **não confere** | contexto: `entidade-produto`, `estrutura_aninhada_divergente`, `contrato-produto` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `estrutura_aninhada_divergente`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto` |
| fonte_formato_valido | `[valor_produto], [contrato-produto]` | confere | {"ids": ["valor_produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `valor_produto` | não se aplica | verbete não encontrado na biblioteca |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-1 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 875 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:51:19 | caso tra-1@verbete_trocado |
| 876 | 2 | poda | programa | ao_vivo | 2026-11-04T23:51:19 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 877 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:51:19 | poda: escolha json/lista; sem diferença; divergência não |
| 878 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:51:19 | 3 de 39 verbetes entregues |
| 879 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:51:19 | recuperacao: escolha entidade-produto,estrutura_aninhada_divergente,contrato-produto; divergência não |
| 880 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:51:19 | {"etapa": "diagnostico", "sha": "c734594537a3e729", "prompt_sha256": "c734594537a3", "chars": 3712, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 882 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:51:19 | diagnostico: 19,7 s |
| 883 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:19 | causa_raiz: `escala_ou_unidade_errada` |
| 884 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:19 | campo: `preco` |
| 885 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:19 | impacto: `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.` |
| 886 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:19 | fonte: `[valor_produto], [contrato-produto]` |
| 887 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:19 | fonte_citada: `valor_produto` |
| 888 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:19 | fonte_citada: `contrato-produto` |
| 889 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | quatro_linhas_presentes: confere |
| 890 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | rotulo_no_conjunto: confere |
| 891 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_existe_na_biblioteca: nao_confere |
| 892 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_existe_na_biblioteca: confere |
| 893 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_estava_no_contexto: nao_confere |
| 894 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_estava_no_contexto: confere |
| 895 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | campo_existe_no_caso: confere |
| 896 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 897 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | notas_nos_verbetes_citados: informativo |
| 898 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | impacto: nao_verificavel |
| 899 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_formato_valido: confere |
| 900 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_contem_termo_da_causa: nao_se_aplica |
| 901 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:19 | fonte_contem_termo_da_causa: nao_confere |
| 902 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:51:19 | diagnostico: escolha escala_ou_unidade_errada; divergência sim |

</details>

Nós de decisão:

- evento 877, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 876 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 879, `recuperacao`: escolha `entidade-produto,estrutura_aninhada_divergente,contrato-produto`; resultado verbetes_entregues; evidência: evento 878 (verbete_entregue, entidade-produto), evento 878 (verbete_entregue, estrutura_aninhada_divergente), evento 878 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, estrutura_aninhada_divergente, contrato-produto (gen_ai: retrieval)
- evento 902, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 878 (verbete_entregue, entidade-produto), evento 878 (verbete_entregue, estrutura_aninhada_divergente), evento 878 (verbete_entregue, contrato-produto), evento 882 (resposta), evento 887 (verbete_citado, valor_produto), evento 888 (verbete_citado, contrato-produto); divergência: sim; falha: citacao_inexistente; prov.used: entidade-produto, estrutura_aninhada_divergente, contrato-produto, valor_produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 875 a 902 da trilha; hash dos eventos deste caso: `d98c3f60dfd6d760`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
