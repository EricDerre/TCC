<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `sin-27`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela_ineditos/qwen2.5_7b/sin-27@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `campo_renomeado` · **CAMPO:** `imagem` · selo de probabilidade: **baixo** (p = 0,41)

**IMPACTO (declarado):** `Os usuários não veem as imagens corretas ou nenhuma imagem para alguns produtos.`

Justificativa (gerada por molde): O agente respondeu campo_renomeado no campo imagem porque os verbetes contrato-produto, entidade-produto, chave_de_juncao_errada estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,16. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,41); trate como hipótese e confira o campo imagem antes de agir.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
[{"id": 12, "nome": "Queijo Coalho", "resumo": "Queijo coalho grelhado com mel", "tipo": "Acompanhamentos", "preco": 22.9, "destaque": true, "imagem_v2": "queijo.png"}, {"id": 13, "nome": "Hambúrguer Artesanal", "resumo": "Blend da casa, pão brioche", "tipo": "Acompanhamentos", "preco": 32.9, "imagem": "hamburger.png", "destaque": false}, {"id": 14, "nome": "Abacaxi na Brasa", "resumo": "Com canela e açúcar", "tipo": "Sobremesas", "preco": 14.9, "destaque": false, "imagem_v2": "abacaxi.jpg"}]

SINTOMA OBSERVADO: Na grade, o Queijo Coalho e o Abacaxi na Brasa aparecem sem foto, enquanto o Hamburguer Artesanal mostra a foto normalmente. Nome, categoria, preco e botoes estao certos nos tres. Ao recarregar a pagina, os cartoes sem foto mudam.

OBSERVAÇÃO ADICIONAL: O corpo mostra so os itens de id 12 a 14; a lista completa tem 14.
```

## 3. Contraste com a segunda causa

campo_renomeado e não valor_fora_do_dominio: a escolha tem probabilidade 0,41 contra 0,16; verbete(s) na evidência: contrato-produto, entidade-produto, chave_de_juncao_errada

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| campo_renomeado | 0,41 | sim |
| valor_fora_do_dominio | 0,16 |  |
| tipo_divergente | 0,10 |  |
| chave_de_juncao_errada | 0,10 |  |
| formato_de_data_divergente | 0,07 |  |
| colecao_no_lugar_de_objeto | 0,06 |  |
| escala_ou_unidade_errada | 0,05 |  |
| estrutura_aninhada_divergente | 0,01 |  |
| campo_ausente | 0,01 |  |
| nulo_inesperado | 0,00 |  |
| resposta_truncada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| estado_da_tela_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[contrato-produto]`; verbetes citados: `contrato-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `contrato-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `contrato-produto` | confere | contexto: `contrato-produto`, `entidade-produto`, `chave_de_juncao_errada` |
| Algum verbete do contexto trata da causa respondida | `campo_renomeado` | confere | verbetes: `contrato-produto` |
| fonte_formato_valido | `[contrato-produto]` | confere | {"ids": ["contrato-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `contrato-produto` | **não confere** | {"termo": "campo_renomeado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `imagem` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_ineditos_reexec --ids sin-27 --k 3`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 713 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:52:46 | caso sin-27 |
| 714 | 2 | candidatos | programa | ao_vivo | 2026-11-06T11:52:46 | 3 de 39 verbetes entregues |
| 716 | 3 | prompt | programa | ao_vivo | 2026-11-06T11:52:46 | {"etapa": "diagnostico", "sha": "c030e138e029c270", "prompt_sha256": "c030e138e029", "chars": 4579, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 718 | 4 | inferencia | programa | ao_vivo | 2026-11-06T11:52:46 | diagnostico: 69,6 s |
| 719 | 5 | declaracao | modelo | ao_vivo | 2026-11-06T11:52:46 | causa_raiz: `campo_renomeado` |
| 720 | 6 | declaracao | modelo | ao_vivo | 2026-11-06T11:52:46 | campo: `imagem` |
| 721 | 7 | declaracao | modelo | ao_vivo | 2026-11-06T11:52:46 | impacto: `Os usuários não veem as imagens corretas ou nenhuma imagem para alguns produtos.` |
| 722 | 8 | declaracao | modelo | ao_vivo | 2026-11-06T11:52:46 | fonte: `[contrato-produto]` |
| 723 | 9 | declaracao | modelo | ao_vivo | 2026-11-06T11:52:46 | fonte_citada: `contrato-produto` |
| 724 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | quatro_linhas_presentes: confere |
| 725 | 11 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | rotulo_no_conjunto: confere |
| 726 | 12 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | fonte_existe_na_biblioteca: confere |
| 727 | 13 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | fonte_estava_no_contexto: confere |
| 728 | 14 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | campo_existe_no_caso: confere |
| 729 | 15 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 730 | 16 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | notas_nos_verbetes_citados: informativo |
| 731 | 17 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | impacto: nao_verificavel |
| 732 | 18 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | fonte_formato_valido: confere |
| 733 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T11:52:46 | fonte_contem_termo_da_causa: nao_confere |
| 734 | 20 | decisao | programa | ao_vivo | 2026-11-06T11:52:46 | diagnostico: escolha campo_renomeado; divergência não |

</details>

Nós de decisão:

- evento 734, `diagnostico`: escolha `campo_renomeado`; resultado rotulo_emitido; evidência: evento 714 (verbete_entregue, contrato-produto), evento 714 (verbete_entregue, entidade-produto), evento 714 (verbete_entregue, chave_de_juncao_errada), evento 718 (resposta), evento 723 (verbete_citado, contrato-produto); divergência: não; falha: nenhuma; prov.used: contrato-produto, entidade-produto, chave_de_juncao_errada (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 713 a 734 da trilha; hash dos eventos deste caso: `5ee32df76a0a952c`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
