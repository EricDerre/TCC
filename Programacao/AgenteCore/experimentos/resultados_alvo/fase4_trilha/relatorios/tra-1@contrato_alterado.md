<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1@contrato_alterado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-1@contrato_alterado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário vê preços cem vezes maiores, como 'R$ 8.990,00' para a picanha, em vez dos valores corretos.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal id: esperado texto, recebido inteiro está presente na resposta HTTP e os verbetes entidade-produto, contrato-produto, escala_ou_unidade_errada estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,02 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 905): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| id | texto | inteiro |

Trecho podado (hash `aff3accfceebc5e4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,98 contra 0,02; verbete(s) na evidência: entidade-produto, contrato-produto, escala_ou_unidade_errada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,98 | sim |
| valor_fora_do_dominio | 0,02 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `escala_ou_unidade_errada` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `escala_ou_unidade_errada` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-1 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 904 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:51:43 | caso tra-1@contrato_alterado |
| 905 | 2 | poda | programa | ao_vivo | 2026-11-04T23:51:43 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 906 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:51:43 | poda: escolha json/lista; id:tipo_diferente; divergência não |
| 907 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:51:43 | 3 de 39 verbetes entregues |
| 908 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:51:43 | recuperacao: escolha entidade-produto,contrato-produto,escala_ou_unidade_errada; divergência não |
| 910 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:51:43 | {"etapa": "diagnostico", "sha": "69c22685ad02d7db", "prompt_sha256": "69c22685ad02", "chars": 3894, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 911 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:51:43 | diagnostico: 63,1 s |
| 912 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:43 | causa_raiz: `escala_ou_unidade_errada` |
| 913 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:43 | campo: `preco` |
| 914 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:43 | impacto: `O usuário vê preços cem vezes maiores, como 'R$ 8.990,00' para a picanha, em vez dos valores corretos.` |
| 915 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:43 | fonte: `[entidade-produto], [contrato-produto]` |
| 916 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:43 | fonte_citada: `entidade-produto` |
| 917 | 13 | declaracao | modelo | ao_vivo | 2026-11-04T23:51:43 | fonte_citada: `contrato-produto` |
| 918 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | quatro_linhas_presentes: confere |
| 919 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | rotulo_no_conjunto: confere |
| 920 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_existe_na_biblioteca: confere |
| 921 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_existe_na_biblioteca: confere |
| 922 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_estava_no_contexto: confere |
| 923 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_estava_no_contexto: confere |
| 924 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | campo_existe_no_caso: confere |
| 925 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 926 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | notas_nos_verbetes_citados: informativo |
| 927 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | impacto: nao_verificavel |
| 928 | 24 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_formato_valido: confere |
| 929 | 25 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_contem_termo_da_causa: nao_confere |
| 930 | 26 | verificacao | verificacao | ao_vivo | 2026-11-04T23:51:43 | fonte_contem_termo_da_causa: nao_confere |
| 931 | 27 | decisao | programa | ao_vivo | 2026-11-04T23:51:43 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 906, `poda`: escolha `json/lista; id:tipo_diferente`; resultado sinais_em_codigo; evidência: evento 905 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: id (gen_ai: plan)
- evento 908, `recuperacao`: escolha `entidade-produto,contrato-produto,escala_ou_unidade_errada`; resultado verbetes_entregues; evidência: evento 907 (verbete_entregue, entidade-produto), evento 907 (verbete_entregue, contrato-produto), evento 907 (verbete_entregue, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, escala_ou_unidade_errada (gen_ai: retrieval)
- evento 931, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 905 (sinal_em_codigo), evento 907 (verbete_entregue, entidade-produto), evento 907 (verbete_entregue, contrato-produto), evento 907 (verbete_entregue, escala_ou_unidade_errada), evento 911 (resposta), evento 916 (verbete_citado, entidade-produto), evento 917 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, escala_ou_unidade_errada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 904 a 931 da trilha; hash dos eventos deste caso: `eed746be783b0433`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
