<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-5@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-5@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `A saudação na área do cliente mostra "Olá, !" pois o campo nome é nulo na resposta da API.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo nome porque o sinal nome: esperado texto, recebido nulo está presente na resposta HTTP e os verbetes nulo_inesperado, contrato-pedido, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 736): regras diff_contra_contrato; antes {"chars": 121}, depois {"chars": 121}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | texto | nulo |

Trecho podado (hash `83e91442cbd302d4`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": null, "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-pedido, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `contrato-pedido`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado`, `usuario-e-login` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"ids": ["nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-5 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 735 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:43:43 | caso semt-5@sonda |
| 736 | 2 | poda | programa | ao_vivo | 2026-11-04T23:43:43 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 737 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:43:43 | poda: escolha json/lista; nome:nulo_inesperado; divergência não |
| 738 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:43:43 | 3 de 39 verbetes entregues |
| 739 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:43:43 | recuperacao: escolha nulo_inesperado,contrato-pedido,usuario-e-login; divergência não |
| 741 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:43:43 | {"etapa": "diagnostico", "sha": "04a04c2dcc8c1e4d", "prompt_sha256": "04a04c2dcc8c", "chars": 3431, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 743 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:43:43 | diagnostico: 57,0 s |
| 744 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:43:43 | causa_raiz: `nulo_inesperado` |
| 745 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:43:43 | campo: `nome` |
| 746 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:43:43 | impacto: `A saudação na área do cliente mostra "Olá, !" pois o campo nome é nulo na resposta da API.` |
| 747 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:43:43 | fonte: `[nulo_inesperado]` |
| 748 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:43:43 | fonte_citada: `nulo_inesperado` |
| 749 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | quatro_linhas_presentes: confere |
| 750 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | rotulo_no_conjunto: confere |
| 751 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | fonte_existe_na_biblioteca: confere |
| 752 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | fonte_estava_no_contexto: confere |
| 753 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | campo_existe_no_caso: confere |
| 754 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 755 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | notas_nos_verbetes_citados: informativo |
| 756 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | impacto: nao_verificavel |
| 757 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | fonte_formato_valido: confere |
| 758 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:43:43 | fonte_contem_termo_da_causa: confere |
| 759 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:43:43 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 737, `poda`: escolha `json/lista; nome:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 736 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nome (gen_ai: plan)
- evento 739, `recuperacao`: escolha `nulo_inesperado,contrato-pedido,usuario-e-login`; resultado verbetes_entregues; evidência: evento 738 (verbete_entregue, nulo_inesperado), evento 738 (verbete_entregue, contrato-pedido), evento 738 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-pedido, usuario-e-login (gen_ai: retrieval)
- evento 759, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 736 (sinal_em_codigo), evento 738 (verbete_entregue, nulo_inesperado), evento 738 (verbete_entregue, contrato-pedido), evento 738 (verbete_entregue, usuario-e-login), evento 743 (resposta), evento 748 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-pedido, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 735 a 759 da trilha; hash dos eventos deste caso: `a63de6adf06e13ec`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
