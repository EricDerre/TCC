<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v2/qwen2.5_7b/semt-17@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

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
| fonte_formato_valido | `[contrato-produto], [nulo_inesperado]` | confere | {"ids": ["contrato-produto", "nulo_inesperado"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "nulo_inesperado"} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `id` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v2_reexec --ids semt-17 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1778 | 1 | entrada | programa | ao_vivo | 2026-11-01T15:16:30 | caso semt-17 |
| 1779 | 2 | candidatos | programa | ao_vivo | 2026-11-01T15:16:30 | 3 de 40 verbetes entregues |
| 1781 | 3 | prompt | programa | ao_vivo | 2026-11-01T15:16:30 | {"etapa": "diagnostico", "sha": "fcf716127e39a8c0", "prompt_sha256": "fcf716127e39", "chars": 3611, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1783 | 4 | inferencia | programa | ao_vivo | 2026-11-01T15:16:30 | diagnostico: 54,9 s |
| 1784 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T15:16:30 | causa_raiz: `nulo_inesperado` |
| 1785 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T15:16:30 | campo: `id` |
| 1786 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T15:16:30 | impacto: `O usuário vê um botão com `data-id="null"` ao clicar, o modal exibe um erro, pois o `id` nulo não pode ser usado para buscar detalhes do produto.` |
| 1787 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T15:16:30 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 1788 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T15:16:30 | fonte_citada: `contrato-produto` |
| 1789 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T15:16:30 | fonte_citada: `nulo_inesperado` |
| 1790 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | quatro_linhas_presentes: confere |
| 1791 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | rotulo_no_conjunto: confere |
| 1792 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_existe_na_biblioteca: confere |
| 1793 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_existe_na_biblioteca: confere |
| 1794 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_estava_no_contexto: confere |
| 1795 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_estava_no_contexto: confere |
| 1796 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | campo_existe_no_caso: confere |
| 1797 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1798 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | notas_nos_verbetes_citados: informativo |
| 1799 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | impacto: nao_verificavel |
| 1800 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_formato_valido: confere |
| 1801 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_contem_termo_da_causa: nao_confere |
| 1802 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T15:16:30 | fonte_contem_termo_da_causa: confere |
| 1803 | 24 | decisao | programa | ao_vivo | 2026-11-01T15:16:30 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1803, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1779 (verbete_entregue, entidade-produto), evento 1779 (verbete_entregue, contrato-produto), evento 1779 (verbete_entregue, nulo_inesperado), evento 1783 (resposta), evento 1788 (verbete_citado, contrato-produto), evento 1789 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1778 a 1803 da trilha; hash dos eventos deste caso: `e67058b695964e92`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
