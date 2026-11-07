<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-21`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_v4/qwen2.5_7b/semt-21@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_ausente` · **CAMPO:** `nome` · selo de probabilidade: **medio** (p = 0,96)

**IMPACTO (declarado):** `O usuário vê "(sem nome)" em vez do nome do produto.`

Justificativa (gerada por molde): O agente respondeu campo_ausente no campo nome porque os verbetes contrato-produto, entidade-produto, tipo_divergente estavam entre os entregues ao modelo. A segunda causa, campo_renomeado, ficou com probabilidade 0,28. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 1, "nome": "", "resumo": "Picanha grelhada", "tipo": "Carnes", "preco": 89.9, "imagem": "picanha_alho.jpg", "destaque": true}]

SINTOMA OBSERVADO: O card mostra o texto literal '(sem nome)' no lugar do nome do produto; o campo nome e do tipo certo (texto), so que vazio.
```

## 3. Contraste com a segunda causa

campo_ausente e não campo_renomeado: a escolha tem probabilidade 0,96 contra 0,28; verbete(s) na evidência: contrato-produto, entidade-produto, tipo_divergente

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_ausente | 0,96 | sim |
| campo_renomeado | 0,28 |  |
| corpo_nao_e_json | 0,03 |  |
| corpo_vazio | 0,03 |  |
| valor_fora_do_dominio | 0,00 |  |
| tipo_divergente | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |
| nulo_inesperado | 0,00 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| resposta_truncada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `tipo_divergente` |
| Algum verbete do contexto trata da causa respondida | `campo_ausente` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_ausente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-21 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1829 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:00:05 | caso semt-21 |
| 1830 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:00:05 | 3 de 39 verbetes entregues |
| 1832 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:00:05 | {"etapa": "diagnostico", "sha": "d02db45ad77fc903", "prompt_sha256": "d02db45ad77f", "chars": 3591, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1834 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:00:05 | diagnostico: 51,5 s |
| 1835 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | causa_raiz: `campo_ausente` |
| 1836 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | campo: `nome` |
| 1837 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | impacto: `O usuário vê "(sem nome)" em vez do nome do produto.` |
| 1838 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | fonte: `[contrato-produto]` |
| 1839 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:00:05 | fonte_citada: `contrato-produto` |
| 1840 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | quatro_linhas_presentes: confere |
| 1841 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | rotulo_no_conjunto: confere |
| 1842 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_existe_na_biblioteca: confere |
| 1843 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_estava_no_contexto: confere |
| 1844 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | campo_existe_no_caso: confere |
| 1845 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1846 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | notas_nos_verbetes_citados: informativo |
| 1847 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | impacto: nao_verificavel |
| 1848 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_formato_valido: confere |
| 1849 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:00:05 | fonte_contem_termo_da_causa: nao_confere |
| 1850 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:00:05 | diagnostico: escolha campo_ausente; divergência não |

</details>

Nós de decisão:

- evento 1850, `diagnostico`: escolha `campo_ausente`; resultado rotulo_emitido; evidência: evento 1830 (verbete_entregue, contrato-produto), evento 1830 (verbete_entregue, entidade-produto), evento 1830 (verbete_entregue, tipo_divergente), evento 1834 (resposta), evento 1839 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, tipo_divergente (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1829 a 1850 da trilha; hash dos eventos deste caso: `b89d6b5af635bb48`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
