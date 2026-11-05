<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `run-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/run-20@lote`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `dado_desatualizado` · **CAMPO:** `preco` · selo de probabilidade: **alto** (p = 1,00)

**IMPACTO (declarado):** `O usuário vê o preço antigo da Fraldinha, R$ 69,90, mesmo após a atualização no painel.`

Justificativa (gerada por molde): O agente respondeu dado_desatualizado no campo preco porque os verbetes dado_desatualizado, entidade-produto, contrato-produto estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,00 e nenhum verbete entregue a sustenta. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: admin atualiza preco da Fraldinha para R$ 74,90 -> GET /api/produtos

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
GET devolveu {"id": 3, "nome": "Fraldinha", "resumo": "Corte grelhado na brasa, fatiado na hora", "tipo": "Carnes", "preco": 69.9, "imagem": "fraldinha.jpg", "destaque": false} — o preco antigo, mesmo apos a atualizacao confirmada no painel.

SINTOMA OBSERVADO: Depois de o administrador mudar o preco da Fraldinha pra R$ 74,90 no painel, GET /api/produtos continua devolvendo 69.9 por varios minutos.

OBSERVAÇÃO ADICIONAL: tbprodutos e a mesma tabela do painel PHP e da CobaiaAPI; listar_produtos le do banco a cada chamada, sem cache proprio — a defasagem apontaria pra um cache fora da CobaiaAPI.
```

## 3. Contraste com a segunda causa

dado_desatualizado e não valor_fora_do_dominio: a escolha tem probabilidade 1,00 contra 0,00; verbete(s) na evidência: dado_desatualizado, entidade-produto, contrato-produto

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| dado_desatualizado | 1,00 | sim |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| registro_duplicado | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| chave_de_juncao_errada | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[dado_desatualizado]`; verbetes citados: `dado_desatualizado`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `dado_desatualizado` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `dado_desatualizado` | confere | contexto: `dado_desatualizado`, `entidade-produto`, `contrato-produto` |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | confere | verbetes: `dado_desatualizado` |
| fonte_formato_valido | `[dado_desatualizado]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["dado_desatualizado"]} |
| fonte_contem_termo_da_causa | `dado_desatualizado` | confere | {"termo": "dado_desatualizado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>20 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 2669 | 1 | entrada | programa | ao_vivo | 2026-11-04T01:09:21 | caso run-20 |
| 2670 | 2 | candidatos | programa | ao_vivo | 2026-11-04T01:09:21 | 3 de 46 verbetes entregues |
| 2672 | 3 | prompt | programa | ao_vivo | 2026-11-04T01:09:21 | {"chars": 3805, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "e9c0245105cf", "sha": "e9c0245105cf8f91"} |
| 2674 | 4 | inferencia | programa | ao_vivo | 2026-11-04T01:09:21 | diagnostico: 74,8 s |
| 2675 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T01:09:21 | causa_raiz: `dado_desatualizado` |
| 2676 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T01:09:21 | campo: `preco` |
| 2677 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T01:09:21 | impacto: `O usuário vê o preço antigo da Fraldinha, R$ 69,90, mesmo após a atualização no painel.` |
| 2678 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T01:09:21 | fonte: `[dado_desatualizado]` |
| 2679 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T01:09:21 | fonte_citada: `dado_desatualizado` |
| 2680 | 10 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | quatro_linhas_presentes: confere |
| 2681 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | rotulo_no_conjunto: confere |
| 2682 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | fonte_existe_na_biblioteca: confere |
| 2683 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | fonte_estava_no_contexto: confere |
| 2684 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | campo_existe_no_caso: confere |
| 2685 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 2686 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | notas_nos_verbetes_citados: informativo |
| 2687 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | impacto: nao_verificavel |
| 2688 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | fonte_formato_valido: confere |
| 2689 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T01:09:21 | fonte_contem_termo_da_causa: confere |
| 2690 | 20 | decisao | programa | ao_vivo | 2026-11-04T01:09:21 | diagnostico: escolha dado_desatualizado; divergência não |

</details>

Nós de decisão:

- evento 2690, `diagnostico`: escolha `dado_desatualizado`; resultado rotulo_emitido; evidência: evento 2670 (verbete_entregue, dado_desatualizado), evento 2670 (verbete_entregue, entidade-produto), evento 2670 (verbete_entregue, contrato-produto), evento 2674 (resposta), evento 2679 (verbete_citado, dado_desatualizado); divergência: não; falha: nenhuma; prov.used: dado_desatualizado, entidade-produto, contrato-produto (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 2669 a 2690 da trilha; hash dos eventos deste caso: `46cc7c11a9ffecdf`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
