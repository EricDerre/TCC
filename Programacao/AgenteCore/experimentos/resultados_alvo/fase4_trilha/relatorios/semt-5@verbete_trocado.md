<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-5@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-5@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,89)

**IMPACTO (declarado):** `A saudação na área do cliente mostra "Ola, !" pois o campo nome é nulo, resultando em uma saudação genérica.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo nome porque o sinal nome: esperado texto, recebido nulo está presente na resposta HTTP e os verbetes formato_de_data_divergente, contrato-pedido, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,05. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 761): regras diff_contra_contrato; antes {"chars": 121}, depois {"chars": 121}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | texto | nulo |

Trecho podado (hash `83e91442cbd302d4`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": null, "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 0,89 contra 0,05; verbete(s) na evidência: formato_de_data_divergente, contrato-pedido, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,89 | sim |
| campo_ausente | 0,05 |  |
| campo_renomeado | 0,05 |  |
| formato_de_data_divergente | 0,01 |  |
| valor_fora_do_dominio | 0,01 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| resposta_truncada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[usuario-e-login]`; verbetes citados: `usuario-e-login`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `usuario-e-login` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `usuario-e-login` | confere | contexto: `formato_de_data_divergente`, `contrato-pedido`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `usuario-e-login` |
| fonte_formato_valido | `[usuario-e-login]` | confere | {"ids": ["usuario-e-login"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `usuario-e-login` | **não confere** | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-5 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 760 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:44:44 | caso semt-5@verbete_trocado |
| 761 | 2 | poda | programa | ao_vivo | 2026-11-04T23:44:44 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 762 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:44:44 | poda: escolha json/lista; nome:nulo_inesperado; divergência não |
| 763 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:44:44 | 3 de 39 verbetes entregues |
| 764 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:44:44 | recuperacao: escolha formato_de_data_divergente,contrato-pedido,usuario-e-login; divergência não |
| 765 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:44:44 | {"etapa": "diagnostico", "sha": "87ec6f20d954b3db", "prompt_sha256": "87ec6f20d954", "chars": 3361, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 766 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:44:44 | diagnostico: 16,5 s |
| 767 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:44:44 | causa_raiz: `nulo_inesperado` |
| 768 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:44:44 | campo: `nome` |
| 769 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:44:44 | impacto: `A saudação na área do cliente mostra "Ola, !" pois o campo nome é nulo, resultando em uma saudação genérica.` |
| 770 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:44:44 | fonte: `[usuario-e-login]` |
| 771 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:44:44 | fonte_citada: `usuario-e-login` |
| 772 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | quatro_linhas_presentes: confere |
| 773 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | rotulo_no_conjunto: confere |
| 774 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | fonte_existe_na_biblioteca: confere |
| 775 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | fonte_estava_no_contexto: confere |
| 776 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | campo_existe_no_caso: confere |
| 777 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 778 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | notas_nos_verbetes_citados: informativo |
| 779 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | impacto: nao_verificavel |
| 780 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | fonte_formato_valido: confere |
| 781 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:44:44 | fonte_contem_termo_da_causa: nao_confere |
| 782 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:44:44 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 762, `poda`: escolha `json/lista; nome:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 761 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nome (gen_ai: plan)
- evento 764, `recuperacao`: escolha `formato_de_data_divergente,contrato-pedido,usuario-e-login`; resultado verbetes_entregues; evidência: evento 763 (verbete_entregue, formato_de_data_divergente), evento 763 (verbete_entregue, contrato-pedido), evento 763 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, contrato-pedido, usuario-e-login (gen_ai: retrieval)
- evento 782, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 761 (sinal_em_codigo), evento 763 (verbete_entregue, formato_de_data_divergente), evento 763 (verbete_entregue, contrato-pedido), evento 763 (verbete_entregue, usuario-e-login), evento 766 (resposta), evento 771 (verbete_citado, usuario-e-login); divergência: não; falha: nenhuma; prov.used: formato_de_data_divergente, contrato-pedido, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 760 a 782 da trilha; hash dos eventos deste caso: `c1df09968a9bb038`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
