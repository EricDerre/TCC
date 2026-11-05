<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_biblioteca/qwen2.5_7b/sin-13@correcao`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/sin-13@correcao`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** **a linha não está na resposta** · **CAMPO:** **a linha não está na resposta** · selo de probabilidade: **sem selo**

**IMPACTO (declarado):** **a linha não está na resposta**

Nenhum nó de decisão de diagnóstico nesta trilha.

**Biblioteca (ciclo de correção):** corrigido: [estrutura_aninhada_divergente] nao_corrigido para corrigido.

Justificativa (gerada por molde): O caso sin-13 foi reapresentado com o modo de falha desligado: o roteiro passou e o fio e a árvore mudaram entre a corrida que falhava e a que passou. Os verbetes estrutura_aninhada_divergente passaram a corrigido, com a solução sugerida (o texto do modelo) e a solução aplicada (o molde da evidência).

## 2. Evidência

Ciclo de correção do verbete [estrutura_aninhada_divergente] pelo caso sin-13: estado nao_corrigido para corrigido; evidência: reexecução passou, fio mudou, árvore mudou.

Não houve interceptação nem poda nesta trilha: o caso entrou em texto.

## 3. Contraste com a segunda causa

Sem nó de diagnóstico, não há contraste.

## 4. FONTE declarada e conferida

Linha FONTE como veio: **a linha não está na resposta**; verbetes citados: nenhum.

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira a resposta no caso de entrada e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo biblioteca --saida fase4_biblioteca_reexec --casos 1 --sem-sonda --sem-correcao`

## 6. Árvore completa

<details><summary>2 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 3006 | 1 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T16:25:03 | correção de [estrutura_aninhada_divergente] pelo caso sin-13: nao_corrigido para corrigido |
| 3007 | 2 | decisao | programa | ao_vivo | 2026-11-04T16:25:03 | edicao_biblioteca: escolha corrigido; divergência não |

</details>

Nós de decisão:

- evento 3007, `edicao_biblioteca`: escolha `corrigido`; resultado correcao_registrada; evidência: evento 2992 (sinal_em_codigo), evento 2991 (arvore_podada), evento 3005 (sinal_em_codigo), evento 3004 (arvore_podada); divergência: não; falha: nenhuma; prov.used: estrutura_aninhada_divergente

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3006 a 3007 da trilha; hash dos eventos deste caso: `5e7e17f26ba123cd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
