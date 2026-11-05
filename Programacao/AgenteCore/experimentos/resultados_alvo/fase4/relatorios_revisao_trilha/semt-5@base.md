<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-5`: o que o agente fez, declarou e conferiu

Trilha `fase4_trilha/qwen2.5_7b/semt-5@base`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `nulo_inesperado` · **CAMPO:** `nome` · selo de probabilidade: **alto** (p = 1,00) · **CONFLITO**: a inferência sem documentação mudou a resposta de nulo_inesperado para campo_ausente

**IMPACTO (declarado):** `A saudação na área do cliente mostra 'Olá, !', indicando que o nome do cliente é nulo na resposta da API.`

Justificativa (gerada por molde): O agente respondeu nulo_inesperado no campo nome porque o sinal nome: esperado texto, recebido nulo está presente na resposta HTTP e os verbetes nulo_inesperado, contrato-pedido, usuario-e-login estavam entre os entregues ao modelo. A segunda causa, campo_ausente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. A remoção do verbete nulo_inesperado não mudou a resposta: sem efeito medido do contexto. A troca do verbete nulo_inesperado por um verbete errado não mudou a resposta: sem efeito medido do contexto. A inferência sem documentação mudou a resposta (de nulo_inesperado para campo_ausente). A repetição da inferência de base não mudou a resposta. O que não dá para conferir por código: a frase de impacto. O que o modelo declarou diverge do que o código mediu (entre modelo e verificacao): a inferência sem documentação mudou a resposta de nulo_inesperado para campo_ausente.

## 2. Evidência

O caso, como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/pedidos?login=11122233344

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id_pedido: inteiro | pessoas: inteiro | data_pedido: data ISO (AAAA-MM-DD) | status: texto ('Em Analise' ou 'Cancelado') | nome: texto | cpf: texto

CORPO DA RESPOSTA:
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": null, "cpf": "11122233344"}]

SINTOMA OBSERVADO: A saudacao da area do cliente mostra 'Ola, !' — o restante da pagina carrega.
```

Poda de `corpo_http` (evento 696): regras diff_contra_contrato; antes {"chars": 121}, depois {"chars": 121}.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| nome | texto | nulo |

Trecho podado (hash `83e91442cbd302d4`):

```text
[{"id_pedido": 7, "pessoas": 4, "data_pedido": "2026-09-10", "status": "Em Analise", "nome": null, "cpf": "11122233344"}]
```

## 3. Contraste com a segunda causa

nulo_inesperado e não campo_ausente: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: nulo_inesperado, contrato-pedido, usuario-e-login

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| nulo_inesperado | 1,00 | sim |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| tipo_divergente | 0,00 |  |
| formato_de_data_divergente | 0,00 |  |
| valor_fora_do_dominio | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[nulo_inesperado]`; verbetes citados: `nulo_inesperado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `nulo_inesperado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `nulo_inesperado` | confere | contexto: `nulo_inesperado`, `contrato-pedido`, `usuario-e-login` |
| Algum verbete do contexto trata da causa respondida | `nulo_inesperado` | confere | verbetes: `nulo_inesperado`, `usuario-e-login` |
| fonte_formato_valido | `[nulo_inesperado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["nulo_inesperado"]} |
| fonte_contem_termo_da_causa | `nulo_inesperado` | confere | {"termo": "nulo_inesperado"} |

| Intervenção | Verbete | Rótulo antes | Rótulo depois | p antes | p depois | Efeito |
|---|---|---|---|---|---|---|
| remocao | `nulo_inesperado` | nulo_inesperado | nulo_inesperado | 1,00 | 0,80 | sem efeito medido do contexto |
| troca | `nulo_inesperado` | nulo_inesperado | nulo_inesperado | 1,00 | 0,83 | sem efeito medido do contexto |
| sem_documentacao | não se aplica | nulo_inesperado | campo_ausente | 1,00 | 0,45 | sem documentação a resposta muda: a documentação pesou na decisão |
| repeticao_da_base | não se aplica | nulo_inesperado | nulo_inesperado | 1,00 | 1,00 | o mesmo prompt manteve o rótulo |

## 5. Linha de ação

Confira o campo `nome` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo avaliacao_trilha --saida fase4_trilha_reexec --ids semt-5 --sem-seletor`

## 6. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 694 | 1 | entrada | programa | ao_vivo | 2026-11-04T23:39:30 | caso semt-5 |
| 696 | 2 | poda | programa | ao_vivo | 2026-11-04T23:39:30 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato |
| 697 | 3 | decisao | programa | ao_vivo | 2026-11-04T23:39:30 | poda: escolha json/lista; nome:nulo_inesperado; divergência não |
| 698 | 4 | candidatos | programa | ao_vivo | 2026-11-04T23:39:30 | 3 de 39 verbetes entregues |
| 699 | 5 | decisao | programa | ao_vivo | 2026-11-04T23:39:30 | recuperacao: escolha nulo_inesperado,contrato-pedido,usuario-e-login; divergência não |
| 701 | 6 | prompt | programa | ao_vivo | 2026-11-04T23:39:30 | {"chars": 3318, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "be432bd462d6", "sha": "be432bd462d60a1a"} |
| 703 | 7 | inferencia | programa | ao_vivo | 2026-11-04T23:39:30 | diagnostico: 66,5 s |
| 704 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T23:39:30 | causa_raiz: `nulo_inesperado` |
| 705 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T23:39:30 | campo: `nome` |
| 706 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T23:39:30 | impacto: `A saudação na área do cliente mostra 'Olá, !', indicando que o nome do cliente é nulo na resposta da API.` |
| 707 | 11 | declaracao | modelo | ao_vivo | 2026-11-04T23:39:30 | fonte: `[nulo_inesperado]` |
| 708 | 12 | declaracao | modelo | ao_vivo | 2026-11-04T23:39:30 | fonte_citada: `nulo_inesperado` |
| 709 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | quatro_linhas_presentes: confere |
| 710 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | rotulo_no_conjunto: confere |
| 711 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | fonte_existe_na_biblioteca: confere |
| 712 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | fonte_estava_no_contexto: confere |
| 713 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | campo_existe_no_caso: confere |
| 714 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 715 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | notas_nos_verbetes_citados: informativo |
| 716 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | impacto: nao_verificavel |
| 717 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | fonte_formato_valido: confere |
| 718 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T23:39:30 | fonte_contem_termo_da_causa: confere |
| 721 | 23 | inferencia | programa | ao_vivo | 2026-11-04T23:39:30 | intervencao:remocao: 61,4 s |
| 722 | 24 | intervencao | verificacao | ao_vivo | 2026-11-04T23:39:30 | remocao de nulo_inesperado: rótulo nulo_inesperado para nulo_inesperado |
| 725 | 25 | inferencia | programa | ao_vivo | 2026-11-04T23:39:30 | intervencao:troca: 68,4 s |
| 726 | 26 | intervencao | verificacao | ao_vivo | 2026-11-04T23:39:30 | troca de nulo_inesperado: rótulo nulo_inesperado para nulo_inesperado |
| 729 | 27 | inferencia | programa | ao_vivo | 2026-11-04T23:39:30 | intervencao:sem_documentacao: 34,9 s |
| 730 | 28 | intervencao | verificacao | ao_vivo | 2026-11-04T23:39:30 | sem_documentacao de None: rótulo nulo_inesperado para campo_ausente |
| 732 | 29 | inferencia | programa | ao_vivo | 2026-11-04T23:39:30 | intervencao:repeticao_da_base: 17,7 s |
| 733 | 30 | intervencao | verificacao | ao_vivo | 2026-11-04T23:39:30 | repeticao_da_base de None: rótulo nulo_inesperado para nulo_inesperado |
| 734 | 31 | decisao | programa | ao_vivo | 2026-11-04T23:39:30 | diagnostico: escolha nulo_inesperado; divergência sim |

</details>

Nós de decisão:

- evento 697, `poda`: escolha `json/lista; nome:nulo_inesperado`; resultado sinais_em_codigo; evidência: evento 696 (sinal_em_codigo); divergência: não; falha: nenhuma; prov.used: nome (gen_ai: plan)
- evento 699, `recuperacao`: escolha `nulo_inesperado,contrato-pedido,usuario-e-login`; resultado verbetes_entregues; evidência: evento 698 (verbete_entregue, nulo_inesperado), evento 698 (verbete_entregue, contrato-pedido), evento 698 (verbete_entregue, usuario-e-login); divergência: não; falha: nenhuma; prov.used: nulo_inesperado, contrato-pedido, usuario-e-login (gen_ai: retrieval)
- evento 734, `diagnostico`: escolha `nulo_inesperado`; resultado rotulo_emitido; evidência: evento 696 (sinal_em_codigo), evento 698 (verbete_entregue, nulo_inesperado), evento 698 (verbete_entregue, contrato-pedido), evento 698 (verbete_entregue, usuario-e-login), evento 703 (resposta), evento 708 (verbete_citado, nulo_inesperado); divergência: sim; falha: nenhuma; prov.used: nulo_inesperado, contrato-pedido, usuario-e-login (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 694 a 734 da trilha; hash dos eventos deste caso: `0602b2b9e8693e53`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
