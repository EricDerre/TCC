<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-1@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 0,99)

**IMPACTO (declarado):** `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, escala_ou_unidade_errada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete escala_ou_unidade_errada não mudou a resposta: sem efeito medido do contexto. A troca do verbete escala_ou_unidade_errada por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação não mudou a resposta. A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 812): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

Trecho podado (hash `aff3accfceebc5e4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,99 contra 0,00; verbete(s) na evidência: entidade-produto, escala_ou_unidade_errada, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,99 | sim |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| fonte_formato_valido | `[escala_ou_unidade_errada]` | confere | {"ids": ["escala_ou_unidade_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `escala_ou_unidade_errada` | escala_ou_unidade_errada | escala_ou_unidade_errada | 0,99 | 0,81 | sem efeito medido do contexto |
| troca | `escala_ou_unidade_errada` | escala_ou_unidade_errada | escala_ou_unidade_errada | 0,99 | 0,65 | sem efeito medido do contexto |
| sem_documentacao | `` | escala_ou_unidade_errada | escala_ou_unidade_errada | 0,99 | 0,96 | sem efeito medido do contexto |
| repeticao_da_base | `` | escala_ou_unidade_errada | escala_ou_unidade_errada | 0,99 | 1,00 | sem efeito medido do contexto |

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-1 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 810 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:45:48 | caso tra-1 |
| 812 | 2 | poda | programa | ao_vivo | 2026-11-04T23:45:48 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 813 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:45:48 | poda: escolha json/lista; sem diferença; divergência não |
| 814 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:45:48 | 3 de 39 verbetes entregues |
| 815 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:45:48 | recuperacao: escolha entidade-produto,escala_ou_unidade_errada,contrato-produto; divergência não |
| 817 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:45:48 | {"etapa": "diagnostico", "sha": "d3ee8627b360f3f2", "prompt_sha256": "d3ee8627b360", "chars": 3896, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 819 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:45:48 | diagnostico: 80,2 s |
| 820 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:48 | causa_raiz: `escala_ou_unidade_errada` |
| 821 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:48 | campo: `preco` |
| 822 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:48 | impacto: `O usuário vê preços cem vezes maiores do que o esperado, como 'R$ 8.990,00' para a picanha.` |
| 823 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:48 | fonte: `[escala_ou_unidade_errada]` |
| 824 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:45:48 | fonte_citada: `escala_ou_unidade_errada` |
| 825 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | quatro_linhas_presentes: confere |
| 826 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | rotulo_no_conjunto: confere |
| 827 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | fonte_existe_na_biblioteca: confere |
| 828 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | fonte_estava_no_contexto: confere |
| 829 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | campo_existe_no_caso: confere |
| 830 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 831 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | notas_nos_verbetes_citados: informativo |
| 832 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | impacto: nao_verificavel |
| 833 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | fonte_formato_valido: confere |
| 834 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:45:48 | fonte_contem_termo_da_causa: confere |
| 837 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:45:48 | intervencao:remocao: 41,0 s |
| 838 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:45:48 | remocao de escala_ou_unidade_errada: rótulo escala_ou_unidade_errada para escala_ou_unidade_errada |
| 841 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:45:48 | intervencao:troca: 67,4 s |
| 842 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:45:48 | troca de escala_ou_unidade_errada: rótulo escala_ou_unidade_errada para escala_ou_unidade_errada |
| 845 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:45:48 | intervencao:sem_documentacao: 35,8 s |
| 846 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:45:48 | sem_documentacao de None: rótulo escala_ou_unidade_errada para escala_ou_unidade_errada |
| 847 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:45:48 | intervencao:repeticao_da_base: 19,8 s |
| 848 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:45:48 | repeticao_da_base de None: rótulo escala_ou_unidade_errada para escala_ou_unidade_errada |
| 849 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:45:48 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 813, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 812 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 815, `recuperacao`: escolha `entidade-produto,escala_ou_unidade_errada,contrato-produto`; resultado verbetes_entregues; evidência: evento 814 (verbete_entregue, entidade-produto), evento 814 (verbete_entregue, escala_ou_unidade_errada), evento 814 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, escala_ou_unidade_errada, contrato-produto (gen_ai: retrieval)
- evento 849, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 814 (verbete_entregue, entidade-produto), evento 814 (verbete_entregue, escala_ou_unidade_errada), evento 814 (verbete_entregue, contrato-produto), evento 819 (resposta), evento 824 (verbete_citado, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, escala_ou_unidade_errada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 810 a 849 da trilha; hash dos eventos deste caso: `8c65b0cfa30ae6f2`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
