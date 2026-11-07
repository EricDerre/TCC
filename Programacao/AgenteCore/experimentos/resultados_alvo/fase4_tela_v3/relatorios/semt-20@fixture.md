<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v3/qwen2.5_7b/semt-20@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,53)

**IMPACTO (declarado):** `O usuário vê um preço negativo, 'R$ -10,00', que não faz sentido para um produto.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,46. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,53); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": -10, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O botao de preco da Picanha ao Alho mostra 'R$ -10,00'; o tipo do campo esta certo (numero), so o valor que nao faz sentido pra um preco.
```

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,53 contra 0,46; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,53 | sim |
| valor_fora_do_dominio | 0,46 |  |
| escala_ou_unidade_errada | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [entidade-produto]`; verbetes citados: `contrato-produto`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto` |
| fonte_formato_valido | `[contrato-produto], [entidade-produto]` | confere | {"ids": ["contrato-produto", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v3_reexec --ids semt-20 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1774 | 1 | entrada | programa | ao_vivo | 2026-11-05T19:42:29 | caso semt-20 |
| 1775 | 2 | candidatos | programa | ao_vivo | 2026-11-05T19:42:29 | 3 de 39 verbetes entregues |
| 1777 | 3 | prompt | programa | ao_vivo | 2026-11-05T19:42:29 | {"etapa": "diagnostico", "sha": "7e7f576ac385b1bd", "prompt_sha256": "7e7f576ac385", "chars": 3429, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1779 | 4 | inferencia | programa | ao_vivo | 2026-11-05T19:42:29 | diagnostico: 36,1 s |
| 1780 | 5 | declaracao | modelo | ao_vivo | 2026-11-05T19:42:29 | causa_raiz: `tipo_divergente` |
| 1781 | 6 | declaracao | modelo | ao_vivo | 2026-11-05T19:42:29 | campo: `preco` |
| 1782 | 7 | declaracao | modelo | ao_vivo | 2026-11-05T19:42:29 | impacto: `O usuário vê um preço negativo, 'R$ -10,00', que não faz sentido para um produto.` |
| 1783 | 8 | declaracao | modelo | ao_vivo | 2026-11-05T19:42:29 | fonte: `[contrato-produto], [entidade-produto]` |
| 1784 | 9 | declaracao | modelo | ao_vivo | 2026-11-05T19:42:29 | fonte_citada: `contrato-produto` |
| 1785 | 10 | declaracao | modelo | ao_vivo | 2026-11-05T19:42:29 | fonte_citada: `entidade-produto` |
| 1786 | 11 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | quatro_linhas_presentes: confere |
| 1787 | 12 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | rotulo_no_conjunto: confere |
| 1788 | 13 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_existe_na_biblioteca: confere |
| 1789 | 14 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_existe_na_biblioteca: confere |
| 1790 | 15 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_estava_no_contexto: confere |
| 1791 | 16 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_estava_no_contexto: confere |
| 1792 | 17 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | campo_existe_no_caso: confere |
| 1793 | 18 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1794 | 19 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | notas_nos_verbetes_citados: informativo |
| 1795 | 20 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | impacto: nao_verificavel |
| 1796 | 21 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_formato_valido: confere |
| 1797 | 22 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_contem_termo_da_causa: nao_confere |
| 1798 | 23 | verificacao | verificacao | ao_vivo | 2026-11-05T19:42:29 | fonte_contem_termo_da_causa: nao_confere |
| 1799 | 24 | decisao | programa | ao_vivo | 2026-11-05T19:42:29 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1799, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1775 (verbete_entregue, entidade-produto), evento 1775 (verbete_entregue, contrato-produto), evento 1775 (verbete_entregue, nulo_inesperado), evento 1779 (resposta), evento 1784 (verbete_citado, contrato-produto), evento 1785 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1774 a 1799 da trilha; hash dos eventos deste caso: `a0928feae8db0dab`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
