<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-17`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-17@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

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

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-17 --k 3`

## 6. Árvore completa

<details><summary>24 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1766 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:17:36 | caso semt-17 |
| 1767 | 2 | candidatos | programa | ao_vivo | 2026-11-01T12:17:36 | 3 de 40 verbetes entregues |
| 1769 | 3 | prompt | programa | ao_vivo | 2026-11-01T12:17:36 | {"etapa": "diagnostico", "sha": "fcf716127e39a8c0", "prompt_sha256": "fcf716127e39", "chars": 3611, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1771 | 4 | inferencia | programa | ao_vivo | 2026-11-01T12:17:36 | diagnostico: 56,2 s |
| 1772 | 5 | declaracao | modelo | ao_vivo | 2026-11-01T12:17:36 | causa_raiz: `nulo_inesperado` |
| 1773 | 6 | declaracao | modelo | ao_vivo | 2026-11-01T12:17:36 | campo: `id` |
| 1774 | 7 | declaracao | modelo | ao_vivo | 2026-11-01T12:17:36 | impacto: `O usuário vê um botão com `data-id="null"` ao clicar, o modal exibe um erro, pois o `id` nulo não pode ser usado para buscar detalhes do produto.` |
| 1775 | 8 | declaracao | modelo | ao_vivo | 2026-11-01T12:17:36 | fonte: `[contrato-produto], [nulo_inesperado]` |
| 1776 | 9 | declaracao | modelo | ao_vivo | 2026-11-01T12:17:36 | fonte_citada: `contrato-produto` |
| 1777 | 10 | declaracao | modelo | ao_vivo | 2026-11-01T12:17:36 | fonte_citada: `nulo_inesperado` |
| 1778 | 11 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | quatro_linhas_presentes: confere |
| 1779 | 12 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | rotulo_no_conjunto: confere |
| 1780 | 13 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_existe_na_biblioteca: confere |
| 1781 | 14 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_existe_na_biblioteca: confere |
| 1782 | 15 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_estava_no_contexto: confere |
| 1783 | 16 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_estava_no_contexto: confere |
| 1784 | 17 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | campo_existe_no_caso: confere |
| 1785 | 18 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1786 | 19 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | notas_nos_verbetes_citados: informativo |
| 1787 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | impacto: nao_verificavel |
| 1788 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_formato_valido: confere |
| 1789 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_contem_termo_da_causa: nao_confere |
| 1790 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:17:36 | fonte_contem_termo_da_causa: confere |
| 1791 | 24 | decisao | programa | ao_vivo | 2026-11-01T12:17:36 | diagnostico: escolha nulo_inesperado; divergência não |

</details>

Nós de decisão:

- evento 1791, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 1767 (verbete_entregue, entidade-produto), evento 1767 (verbete_entregue, contrato-produto), evento 1767 (verbete_entregue, nulo_inesperado), evento 1771 (resposta), evento 1776 (verbete_citado, contrato-produto), evento 1777 (verbete_citado, nulo_inesperado); divergência: não; falha: nenhuma; prov.used: entidade-produto, contrato-produto, nulo_inesperado (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1766 a 1791 da trilha; hash dos eventos deste caso: `f840c47772ccad03`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
