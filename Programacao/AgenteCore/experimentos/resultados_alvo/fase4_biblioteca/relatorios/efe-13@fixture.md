<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `efe-13`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/efe-13@fixture`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `dado_desatualizado` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,91)

**IMPACTO (declarado):** `O usuário vê o preço antigo do produto 3, R$ 69,90, mesmo após a atualização da API para R$ 74,90.`

Justificativa (gerada por molde): O agente respondeu dado_desatualizado no campo preco porque os verbetes estado_da_tela_divergente, contagem_inconsistente, corpo_vazio, atualizacao_imediata estavam entre os entregues ao modelo. A segunda causa, estado_da_tela_divergente, ficou com probabilidade 0,02. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

**Biblioteca:** 1 edição(ões) aplicada(s) ([estado_da_tela_divergente]), 0 para revisão humana, 1 recusada(s) (teto_verbetes_novos).

Justificativa (gerada por molde): O modelo propôs 2 edição(ões) para o caso efe-13. A proposta 1 (nota em [estado_da_tela_divergente], peso 1) passou pela validação da Fase 3 e pelos filtros e entrou no lote. A proposta 2 (novo_verbete em [cancelamento_via_redirect]) foi recusada por a validação da Fase 3 com o código teto_verbetes_novos: 6 verbetes novos nesta época (teto 6).

## 2. Evidência

Propostas de edição da biblioteca, na ordem em que o modelo as escreveu (o validador da Fase 3 decide primeiro; depois os filtros do P5):

| Proposta | Operação | Verbete | Validador da Fase 3 | Filtro do P5 | Resultado | Peso |
|---|---|---|---|---|---|---|
| 1 | nota | `estado_da_tela_divergente` | aceita | nenhum | **aplicada** | 1 |
| 2 | novo_verbete | `cancelamento_via_redirect` | recusada: `teto_verbetes_novos` | nenhum | recusada: `teto_verbetes_novos` |  |

Não houve interceptação nem poda nesta trilha: o caso entrou em texto. Como foi posto no prompt:

```text
REQUISIÇÃO: GET /api/produtos (chamado duas vezes em sequencia; a primeira resposta chegou depois da segunda)

STATUS HTTP: 200

CONTRATO ESPERADO PELA INTERFACE: id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano

CORPO DA RESPOSTA:
(primeira resposta: 14 itens, produto 3 a 69.9; segunda resposta: 14 itens, produto 3 a 74.9, apos alteracao no cadastro)

SINTOMA OBSERVADO: A tela mostra o preco antigo (R$ 69,90) do produto 3, embora a ultima resposta da API traga 74.9; nenhum erro no console.

OBSERVAÇÃO ADICIONAL: A pagina substitui o grid inteiro a cada resposta recebida; a resposta mais antiga chegou por ultimo e sobrescreveu a mais nova.
```

## 3. Contraste com a segunda causa

dado_desatualizado e não estado_da_tela_divergente: a escolha tem probabilidade 0,91 contra 0,02; verbete(s) na evidência: estado_da_tela_divergente, contagem_inconsistente, corpo_vazio, atualizacao_imediata

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| dado_desatualizado | 0,91 | sim |
| estado_da_tela_divergente | 0,02 |  |
| valor_fora_do_dominio | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| registro_duplicado | 0,00 |  |
| tempo_de_resposta_excedido | 0,00 |  |
| resposta_truncada | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| tipo_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[corpo_vazio] [atualizacao_imediata]`; verbetes citados: `corpo_vazio`, `atualizacao_imediata`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `corpo_vazio` | confere |  |
| O verbete citado existe na biblioteca | `atualizacao_imediata` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `corpo_vazio` | confere | contexto: `estado_da_tela_divergente`, `contagem_inconsistente`, `corpo_vazio`, `atualizacao_imediata` |
| O verbete citado estava no contexto entregue ao modelo | `atualizacao_imediata` | confere | contexto: `estado_da_tela_divergente`, `contagem_inconsistente`, `corpo_vazio`, `atualizacao_imediata` |
| Algum verbete do contexto trata da causa respondida | `dado_desatualizado` | confere | verbetes: `estado_da_tela_divergente`, `contagem_inconsistente` |
| fonte_formato_valido | `[corpo_vazio] [atualizacao_imediata]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["corpo_vazio", "atualizacao_imediata"]} |
| fonte_contem_termo_da_causa | `corpo_vazio` | **não confere** | {"termo": "dado_desatualizado"} |
| fonte_contem_termo_da_causa | `atualizacao_imediata` | **não confere** | {"termo": "dado_desatualizado"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>28 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1829 | 1 | entrada | programa | ao_vivo | 2026-11-04T00:19:10 | caso efe-13 |
| 1830 | 2 | candidatos | programa | ao_vivo | 2026-11-04T00:19:10 | 3 de 40 verbetes entregues |
| 1832 | 3 | prompt | programa | ao_vivo | 2026-11-04T00:19:10 | {"chars": 3775, "etapa": "diagnostico", "hash_prompt_fixo": "2e42cf9c31826941", "prompt_sha256": "a322a3834c03", "sha": "a322a3834c030b98"} |
| 1834 | 4 | inferencia | programa | ao_vivo | 2026-11-04T00:19:10 | diagnostico: 75,7 s |
| 1835 | 5 | declaracao | modelo | ao_vivo | 2026-11-04T00:19:10 | causa_raiz: `dado_desatualizado` |
| 1836 | 6 | declaracao | modelo | ao_vivo | 2026-11-04T00:19:10 | campo: `preco` |
| 1837 | 7 | declaracao | modelo | ao_vivo | 2026-11-04T00:19:10 | impacto: `O usuário vê o preço antigo do produto 3, R$ 69,90, mesmo após a atualização da API para R$ 74,90.` |
| 1838 | 8 | declaracao | modelo | ao_vivo | 2026-11-04T00:19:10 | fonte: `[corpo_vazio] [atualizacao_imediata]` |
| 1839 | 9 | declaracao | modelo | ao_vivo | 2026-11-04T00:19:10 | fonte_citada: `corpo_vazio` |
| 1840 | 10 | declaracao | modelo | ao_vivo | 2026-11-04T00:19:10 | fonte_citada: `atualizacao_imediata` |
| 1841 | 11 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | quatro_linhas_presentes: confere |
| 1842 | 12 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | rotulo_no_conjunto: confere |
| 1843 | 13 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_existe_na_biblioteca: confere |
| 1844 | 14 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_existe_na_biblioteca: confere |
| 1845 | 15 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_estava_no_contexto: confere |
| 1846 | 16 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_estava_no_contexto: confere |
| 1847 | 17 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | campo_existe_no_caso: confere |
| 1848 | 18 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1849 | 19 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | notas_nos_verbetes_citados: informativo |
| 1850 | 20 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | impacto: nao_verificavel |
| 1851 | 21 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_formato_valido: confere |
| 1852 | 22 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_contem_termo_da_causa: nao_confere |
| 1853 | 23 | verificacao | verificacao | ao_vivo | 2026-11-04T00:19:10 | fonte_contem_termo_da_causa: nao_confere |
| 1854 | 24 | decisao | programa | ao_vivo | 2026-11-04T00:19:10 | diagnostico: escolha dado_desatualizado; divergência não |
| 1857 | 25 | inferencia | programa | ao_vivo | 2026-11-04T00:20:30 | proposta: 142,0 s |
| 1859 | 26 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:20:30 | proposta 1: nota em [estado_da_tela_divergente]: aplicada |
| 1861 | 27 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T00:20:30 | proposta 2: novo_verbete em [cancelamento_via_redirect]: recusada: teto_verbetes_novos |
| 1862 | 28 | decisao | programa | ao_vivo | 2026-11-04T00:20:30 | edicao_biblioteca: escolha proposta_1; divergência sim |

</details>

Nós de decisão:

- evento 1854, `diagnostico`: escolha `dado_desatualizado`; resultado rotulo_emitido; evidência: evento 1830 (verbete_entregue, estado_da_tela_divergente), evento 1830 (verbete_entregue, contagem_inconsistente), evento 1830 (verbete_entregue, corpo_vazio), evento 1830 (verbete_entregue, atualizacao_imediata), evento 1834 (resposta), evento 1839 (verbete_citado, corpo_vazio), evento 1840 (verbete_citado, atualizacao_imediata); divergência: não; falha: nenhuma; prov.used: estado_da_tela_divergente, contagem_inconsistente, corpo_vazio, atualizacao_imediata (gen_ai: chat)
- evento 1862, `edicao_biblioteca`: escolha `proposta_1`; resultado lote; evidência: evento 1834 (resposta), evento 1857 (resposta), evento 1859 (verbete_entregue, estado_da_tela_divergente); divergência: sim; falha: nenhuma; prov.used: atualizacao_imediata, contagem_inconsistente, corpo_vazio, estado_da_tela_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1829 a 1862 da trilha; hash dos eventos deste caso: `dc7fd1f9a10b8aa7`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
