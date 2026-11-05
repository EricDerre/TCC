<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/semt-17@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `id` · selo de probabilidade: **medio** (p = 0,91)

**IMPACTO (declarado):** `O usuário vê um botão com `data-id="null"` ao clicar, o modal exibe um erro, pois o `id` nulo não pode ser usado para buscar detalhes do produto.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo id porque os verbetes entidade-produto, contrato-produto, nulo_inesperado estavam entre os entregues ao modelo. A segunda causa, colecao_no_lugar_de_objeto, ficou com probabilidade 0,06. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}, {"id": null, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false}]

SINTOMA OBSERVADO: O card da Fraldinha mostra nome, preco e imagem certos, mas o botao 'Saiba Mais...' fica com data-id="null"; ao clicar, o modal abre mostrando 'Erro'.
```

## 3. Contraste com a segunda causa

nulo_inesperado e não colecao_no_lugar_de_objeto: a escolha tem probabilidade 0,91 contra 0,06; verbete(s) na evidência: entidade-produto, contrato-produto, nulo_inesperado

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 0,91 | sim |
| colecao_no_lugar_de_objeto | 0,06 |  |
| campo_ausente | 0,01 |  |
| campo_renomeado | 0,01 |  |
| corpo_nao_e_json | 0,01 |  |
| corpo_vazio | 0,01 |  |
| tipo_divergente | 0,01 |  |
| resposta_truncada | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto], [nulo_inesperado]`; verbetes citados: `contrato-produto`, `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `entidade-produto`, `contrato-produto`, `nulo_inesperado` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado` |
| fonte_formato_valido | `[contrato-produto], [nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["contrato-produto", "nulo_inesperado"]} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "nulo_inesperado"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2296 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:53:06 | caso semt-17 |
| 2297 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:53:06 | 3 de 46 verbetes entregues |
| 2299 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:53:06 | {"chars": 3611, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "fcf716127e39", "sha": "fcf716127e39a8c0"} |
| 2301 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:53:06 | diagnostico: 58,6 s |
| 2302 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:53:06 | causa_raiz: `nulo_inesperado` |
| 2303 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:53:06 | campo: `id` |
| 2304 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:53:06 | impacto: `O usuário vê um botão com `data-id="null"` ao clicar, o modal exibe um erro, pois o `id` nulo não pode ser usado para buscar detalhes do produto.` |
| 2305 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:53:06 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 2306 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:53:06 | fonte_citada: `contrato-produto` |
| 2307 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:53:06 | fonte_citada: `nulo_inesperado` |
| 2308 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | quatro_linhas_presentes: confere |
| 2309 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | rotulo_no_conjunto: confere |
| 2310 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_existe_na_biblioteca: confere |
| 2311 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_existe_na_biblioteca: confere |
| 2312 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_estava_no_contexto: confere |
| 2313 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_estava_no_contexto: confere |
| 2314 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | campo_existe_no_caso: confere |
| 2315 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2316 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | notas_nos_verbetes_citados: informativo |
| 2317 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | impacto: nao_verificavel |
| 2318 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_formato_valido: confere |
| 2319 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_contem_termo_da_causa: nao_confere |
| 2320 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:53:06 | fonte_contem_termo_da_causa: confere |
| 2321 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:53:06 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 2321, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 2297 (verbete_entregue, entidade-produto), evento 2297 (verbete_entregue, contrato-produto), evento 2297 (verbete_entregue, nulo_inesperado), evento 2301 (resposta), evento 2306 (verbete_citado, contrato-produto), evento 2307 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2296 a 2321 da trilha; hash dos eventos deste caso: `6d61a23acc67a23c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
