<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `lex-8@verbete_trocado`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/lex-8@verbete_trocado`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `codificacao_incorreta` · **CAMPO:** `nenhum` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: nenhum verbete entregue trata da causa respondida codificacao_incorreta

**IMPACTO (declarado):** `A descrição da costelona aparece com símbolos inválidos no lugar dos acentos.`

Justificativa (gerada por molde): O agente respondeu codificacao_incorreta porque os verbetes estado_da_tela_divergente, contrato-produto, entidade-produto estavam entre os entregues ao modelo. A segunda causa, formato_de_data_divergente, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): nenhum verbete entregue trata da causa respondida codificacao_incorreta. Este nó está marcado com a falha causa_sem_verbete_que_a_trate (origem: modelo).

## 2. Evidência

Poda de `corpo_http` (evento 1843): regras diff_contra_contrato; antes {"chars": 159}, depois {"chars": 159}.

Trecho podado (hash `cd0b56c99381d9a7`):

```text
[{"id": 4, "nome": "Costelona", "resumo": "Costela assada lentamente por horas", "tipo": "Carnes", "preco": 79.9, "imagem": "costelona.jpg", "destaque": true}]
```

## 3. Contraste com a segunda causa

codificacao_incorreta e não formato_de_data_divergente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: estado_da_tela_divergente, contrato-produto, entidade-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| codificacao_incorreta | 1,00 | sim |
| formato_de_data_divergente | 0,00 |  |
| tipo_divergente | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto] [estado_da_tela_divergente]`; verbetes citados: `contrato-produto`, `estado_da_tela_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `estado_da_tela_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `estado_da_tela_divergente`, `contrato-produto`, `entidade-produto` |
| O verbete citado estava no contexto entregue ao modelo | `estado_da_tela_divergente` | confere | contexto: `estado_da_tela_divergente`, `contrato-produto`, `entidade-produto` |
| Algum verbete do contexto trata da causa respondida | `codificacao_incorreta` | **não confere** | nenhum verbete do contexto trata dessa causa |
| fonte_formato_valido | `[contrato-produto] [estado_da_tela_divergente]` | confere | {"ids": ["contrato-produto", "estado_da_tela_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "codificacao_incorreta"} |
| fonte_contem_termo_da_causa | `estado_da_tela_divergente` | **não confere** | {"termo": "codificacao_incorreta"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids lex-8 --sem-seletor`

## 6. Árvore completa

<details><summary>27 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1842 | 1 | entrada | programa | ao_vivo | 2026-11-05T00:50:02 | caso lex-8@verbete_trocado |
| 1843 | 2 | poda | programa | ao_vivo | 2026-11-05T00:50:02 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1844 | 3 | decisao | programa | ao_vivo | 2026-11-05T00:50:02 | poda: escolha json/lista; sem diferença; divergência não |
| 1845 | 4 | candidatos | programa | ao_vivo | 2026-11-05T00:50:02 | 3 de 39 verbetes entregues |
| 1846 | 5 | decisao | programa | ao_vivo | 2026-11-05T00:50:02 | recuperacao: escolha estado_da_tela_divergente,contrato-produto,entidade-produto; divergência não |
| 1847 | 6 | prompt | programa | ao_vivo | 2026-11-05T00:50:02 | {"etapa": "diagnostico", "sha": "512add1813db47c9", "prompt_sha256": "512add1813db", "chars": 3578, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1849 | 7 | inferencia | programa | ao_vivo | 2026-11-05T00:50:02 | diagnostico: 17,2 s |
| 1850 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:02 | causa_raiz: `codificacao_incorreta` |
| 1851 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:02 | campo: `nenhum` |
| 1852 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:02 | impacto: `A descrição da costelona aparece com símbolos inválidos no lugar dos acentos.` |
| 1853 | 11 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:02 | fonte: `[contrato-produto] [estado_da_tela_divergente]` |
| 1854 | 12 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:02 | fonte_citada: `contrato-produto` |
| 1855 | 13 | declaracao | modelo | ao_vivo | 2026-11-05T00:50:02 | fonte_citada: `estado_da_tela_divergente` |
| 1856 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | quatro_linhas_presentes: confere |
| 1857 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | rotulo_no_conjunto: confere |
| 1858 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_existe_na_biblioteca: confere |
| 1859 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_existe_na_biblioteca: confere |
| 1860 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_estava_no_contexto: confere |
| 1861 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_estava_no_contexto: confere |
| 1862 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | campo_existe_no_caso: nao_se_aplica |
| 1863 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | rotulo_sustentado_por_verbete_do_contexto: nao_confere |
| 1864 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | notas_nos_verbetes_citados: informativo |
| 1865 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | impacto: nao_verificavel |
| 1866 | 24 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_formato_valido: confere |
| 1867 | 25 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_contem_termo_da_causa: nao_confere |
| 1868 | 26 | verificacao | verificacao | ao_vivo | 2026-11-05T00:50:02 | fonte_contem_termo_da_causa: nao_confere |
| 1869 | 27 | decisao | programa | ao_vivo | 2026-11-05T00:50:02 | diagnostico: escolha codificacao_incorreta; divergência sim |

</details>

Nós de decisão:

- evento 1844, `poda`: escolha `json/lista; sem diferença`; resultado sinais_em_codigo; evidência: evento 1843 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nenhum (gen_ai: plan)
- evento 1846, `recuperacao`: escolha `estado_da_tela_divergente,contrato-produto,entidade-produto`; resultado verbetes_entregues; evidência: evento 1845 (verbete_entregue, estado_da_tela_divergente), evento 1845 (verbete_entregue, contrato-produto), evento 1845 (verbete_entregue, entidade-produto); divergência: não; falha: nenhuma; prov.used: estado_da_tela_divergente, contrato-produto, entidade-produto (gen_ai: retrieval)
- evento 1869, `diagnostico`: escolha `codificacao_incorreta`; resultado rotulo_emitido; evidência: evento 1845 (verbete_entregue, estado_da_tela_divergente), evento 1845 (verbete_entregue, contrato-produto), evento 1845 (verbete_entregue, entidade-produto), evento 1849 (resposta), evento 1854 (verbete_citado, contrato-produto), evento 1855 (verbete_citado, estado_da_tela_divergente); divergência: sim; falha: causa_sem_verbete_que_a_trate; prov.used: estado_da_tela_divergente, contrato-produto, entidade-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1842 a 1869 da trilha; hash dos eventos deste caso: `13333c03657b6462`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
