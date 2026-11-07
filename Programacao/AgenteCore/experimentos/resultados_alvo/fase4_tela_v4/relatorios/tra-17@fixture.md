<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `tra-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/tra-17@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `tipo` · selo de probabilidade: **medio** (p = 0,88)

**IMPACTO (declarado):** `O usuário vê a categoria como 'CAR' em vez de 'Carnes'.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo tipo porque os verbetes entidade-produto, contrato-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,07. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "CAR", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: A categoria da Picanha ao Alho aparece como 'CAR' no card, em vez de 'Carnes'.

OBSERVAÇÃO ADICIONAL: tbtipos.id 1 tem sigla_tipo='CAR' e rotulo_tipo='Carnes'; o contrato usa o rotulo, nao a sigla.
```

## 3. Contraste com a segunda causa

tipo_divergente e não campo_ausente: a escolha tem probabilidade 0,88 contra 0,07; verbete(s) na evidência: entidade-produto, contrato-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,88 | sim |
| campo_ausente | 0,07 |  |
| campo_renomeado | 0,07 |  |
| chave_de_juncao_errada | 0,04 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente]`; verbetes citados: `tipo_divergente`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `contrato-produto`, `tipo_divergente` |
| fonte_formato_valido | `[tipo_divergente]` | confere | {"ids": ["tipo_divergente"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `tipo` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids tra-17 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1888 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:02:31 | caso tra-17 |
| 1889 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:02:31 | 3 de 39 verbetes entregues |
| 1891 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:02:31 | {"etapa": "diagnostico", "sha": "4b800f6d5d93bb1c", "prompt_sha256": "4b800f6d5d93", "chars": 3677, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1893 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:02:31 | diagnostico: 35,3 s |
| 1894 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:02:31 | causa_raiz: `tipo_divergente` |
| 1895 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:02:31 | campo: `tipo` |
| 1896 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:02:31 | impacto: `O usuário vê a categoria como 'CAR' em vez de 'Carnes'.` |
| 1897 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:02:31 | fonte: `[tipo_divergente]` |
| 1898 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:02:31 | fonte_citada: `tipo_divergente` |
| 1899 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | quatro_linhas_presentes: confere |
| 1900 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | rotulo_no_conjunto: confere |
| 1901 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | fonte_existe_na_biblioteca: confere |
| 1902 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | fonte_estava_no_contexto: confere |
| 1903 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | campo_existe_no_caso: confere |
| 1904 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1905 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | notas_nos_verbetes_citados: informativo |
| 1906 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | impacto: nao_verificavel |
| 1907 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | fonte_formato_valido: confere |
| 1908 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:02:31 | fonte_contem_termo_da_causa: confere |
| 1909 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:02:31 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1909, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1889 (verbete_entregue, entidade-produto), evento 1889 (verbete_entregue, contrato-produto), evento 1889 (verbete_entregue, tipo_divergente), evento 1893 (resposta), evento 1898 (verbete_citado, tipo_divergente); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1888 a 1909 da trilha; hash dos eventos deste caso: `b15a8c1f3c4a51b7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
