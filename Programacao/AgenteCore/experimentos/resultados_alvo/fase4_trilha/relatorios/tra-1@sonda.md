<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-1@sonda`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/tra-1@sonda`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,98)

**IMPACTO (declarado):** `O usuário vê preços cem vezes maiores, como 'R$ 8.990,00' para a picanha.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, escala_ou_unidade_errada, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `corpo_http` (evento 851): regras diff_contra_contrato; antes {"chars": 149}, depois {"chars": 149}.

Trecho podado (hash `aff3accfceebc5e4`):

```text
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 8990, "imagem": "picanha_alho.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: entidade-produto, escala_ou_unidade_errada, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,98 | sim |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `entidade-produto`, `escala_ou_unidade_errada`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto`, `escala_ou_unidade_errada` |
| fonte_formato_valido | `[escala_ou_unidade_errada]` | confere | {"ids": ["escala_ou_unidade_errada"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids tra-1 --sem-seletor`

## 6. Árvore completa

<details><summary>23 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 850 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:49:56 | caso tra-1@sonda |
| 851 | 2 | poda | programa | ao_vivo | 2026-11-04T23:49:56 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 852 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:49:56 | poda: escolha json/lista; sem diferença; divergência não |
| 853 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:49:56 | 3 de 39 verbetes entregues |
| 854 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:49:56 | recuperacao: escolha entidade-produto,escala_ou_unidade_errada,contrato-produto; divergência não |
| 856 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:49:56 | {"etapa": "diagnostico", "sha": "ca40a5e181706955", "prompt_sha256": "ca40a5e18170", "chars": 4018, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 858 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:49:56 | diagnostico: 78,5 s |
| 859 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:49:56 | causa_raiz: `escala_ou_unidade_errada` |
| 860 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:49:56 | campo: `preco` |
| 861 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:49:56 | impacto: `O usuário vê preços cem vezes maiores, como 'R$ 8.990,00' para a picanha.` |
| 862 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:49:56 | fonte: `[escala_ou_unidade_errada]` |
| 863 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:49:56 | fonte_citada: `escala_ou_unidade_errada` |
| 864 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | quatro_linhas_presentes: confere |
| 865 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | rotulo_no_conjunto: confere |
| 866 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | fonte_existe_na_biblioteca: confere |
| 867 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | fonte_estava_no_contexto: confere |
| 868 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | campo_existe_no_caso: confere |
| 869 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 870 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | notas_nos_verbetes_citados: informativo |
| 871 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | impacto: nao_verificavel |
| 872 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | fonte_formato_valido: confere |
| 873 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:49:56 | fonte_contem_termo_da_causa: confere |
| 874 | 23 | decisao | programa | ao_vivo | 2026-11-04T23:49:56 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 852, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 851 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 854, `recuperacao`: escolha `entidade-produto,escala_ou_unidade_errada,contrato-produto`; resultado verbetes_entregues; evidência: evento 853 (verbete_entregue, entidade-produto), evento 853 (verbete_entregue, escala_ou_unidade_errada), evento 853 (verbete_entregue, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, escala_ou_unidade_errada, contrato-produto (gen_ai: retrieval)
- evento 874, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 853 (verbete_entregue, entidade-produto), evento 853 (verbete_entregue, escala_ou_unidade_errada), evento 853 (verbete_entregue, contrato-produto), evento 858 (resposta), evento 863 (verbete_citado, escala_ou_unidade_errada); divergência: não; falha: nenhuma; prov.used: entidade-produto, escala_ou_unidade_errada, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 850 a 874 da trilha; hash dos eventos deste caso: `2299f7d7f1cbac44`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
