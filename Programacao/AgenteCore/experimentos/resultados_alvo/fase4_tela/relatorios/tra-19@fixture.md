<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-19`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/tra-19@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `escala_ou_unidade_errada` · **CAMPO:** `preco` · selo de probabilidade: **baixo** (p = 0,61)

**IMPACTO (declarado):** `O usuário vê o preço do Balde de Cerveja como R$ 4,50, quando na verdade é R$ 45,00.`

Justificativa (gerada por molde): O agente respondeu escala_ou_unidade_errada no campo preco porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,17. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,61); trate como hipótese e confira o campo preco antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 9, "nome": "Balde de Cerveja", "resumo": "5 long necks geladas", "tipo": "Bebidas", "preco": 4.5, "imagem": "balde_cerveja.png", "destaque": true}]

SINTOMA OBSERVADO: O Balde de Cerveja aparece por 'R$ 4,50'; no cadastro custa R$ 45,00 — dez vezes mais.

OBSERVAÇÃO ADICIONAL: tbprodutos.valor_produto do id 9 vale 45.00.
```

## 3. Contraste com a segunda causa

escala_ou_unidade_errada e não valor_fora_do_dominio: a escolha tem probabilidade 0,61 contra 0,17; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| escala_ou_unidade_errada | 0,61 | sim |
| valor_fora_do_dominio | 0,17 |  |
| formato_de_data_divergente | 0,13 |  |
| tipo_divergente | 0,09 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| nulo_inesperado | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[entidade-produto], [contrato-produto]`; verbetes citados: `entidade-produto`, `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `entidade-produto` |
| fonte_formato_valido | `[entidade-produto], [contrato-produto]` | confere | {"ids": ["entidade-produto", "contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids tra-19 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2016 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:24:50 | caso tra-19 |
| 2017 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:24:50 | 3 de 40 verbetes entregues |
| 2019 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:24:50 | {"etapa": "diagnostico", "sha": "e6f3071ea65acb7b", "prompt_sha256": "e6f3071ea65a", "chars": 3453, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 2021 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:24:50 | diagnostico: 39,2 s |
| 2022 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:50 | causa_raiz: `escala_ou_unidade_errada` |
| 2023 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:50 | campo: `preco` |
| 2024 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:50 | impacto: `O usuário vê o preço do Balde de Cerveja como R$ 4,50, quando na verdade é R$ 45,00.` |
| 2025 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:50 | fonte: `[entidade-produto], [contrato-produto]` |
| 2026 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:50 | fonte_citada: `entidade-produto` |
| 2027 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T12:24:50 | fonte_citada: `contrato-produto` |
| 2028 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | quatro_linhas_presentes: confere |
| 2029 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | rotulo_no_conjunto: confere |
| 2030 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_existe_na_biblioteca: confere |
| 2031 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_existe_na_biblioteca: confere |
| 2032 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_estava_no_contexto: confere |
| 2033 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_estava_no_contexto: confere |
| 2034 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | campo_existe_no_caso: confere |
| 2035 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2036 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | notas_nos_verbetes_citados: informativo |
| 2037 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | impacto: nao_verificavel |
| 2038 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_formato_valido: confere |
| 2039 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_contem_termo_da_causa: nao_confere |
| 2040 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:24:50 | fonte_contem_termo_da_causa: nao_confere |
| 2041 | 24 | decisao | programa | ao_vivo | 2026-11-01T12:24:50 | diagnostico: escolha escala_ou_unidade_errada; divergência não |

</details>

Nós de decisão:

- evento 2041, `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido; evidência: evento 2017 (verbete_entregue, entidade-produto), evento 2017 (verbete_entregue, contrato-produto), evento 2017 (verbete_entregue, nulo_inesperado), evento 2021 (resposta), evento 2026 (verbete_citado, entidade-produto), evento 2027 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2016 a 2041 da trilha; hash dos eventos deste caso: `b60edf5912191f32`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
