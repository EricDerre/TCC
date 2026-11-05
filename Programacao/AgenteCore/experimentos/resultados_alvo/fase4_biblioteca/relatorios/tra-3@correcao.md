<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `fase4_biblioteca/qwen2.5_7b/tra-3@correcao`: o que o agente fez, declarou e conferiu

Trilha `fase4_biblioteca/qwen2.5_7b/tra-3@correcao`; modelo `qwen2.5:7b`, Ollama 0.40.14, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** **a linha não está na resposta** · **CAMPO:** **a linha não está na resposta** · selo de probabilidade: **sem selo**

**IMPACTO (declarado):** **a linha não está na resposta**

Nenhum nó de decisão de diagnóstico nesta trilha.

**Biblioteca (ciclo de correção):** não corrigido: nenhum verbete mudou de estado.

Justificativa (gerada por molde): O caso tra-3 foi reapresentado com o modo de falha desligado: o roteiro passou, mas nada mudou no fio (corpo e tempo da chamada iguais): sem evidência de correção. Nenhum verbete mudou de estado.

## 2. Evidência

Ciclo de correção do verbete [chave_de_juncao_errada] pelo caso tra-3: estado nao_corrigido para sem mudança; evidência: reexecução passou, fio igual, árvore igual.

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
| 3118 | 1 | edicao_biblioteca | programa | ao_vivo | 2026-11-04T16:25:06 | correção de [chave_de_juncao_errada] pelo caso tra-3: nao_corrigido para sem mudança |
| 3119 | 2 | decisao | programa | ao_vivo | 2026-11-04T16:25:06 | edicao_biblioteca: escolha nao_corrigido; divergência não |

</details>

Nós de decisão:

- evento 3119, `edicao_biblioteca`: escolha `nao_corrigido`; resultado sem_correcao; evidência: evento 3104 (sinal_em_codigo), evento 3103 (arvore_podada), evento 3117 (sinal_em_codigo), evento 3116 (arvore_podada); divergência: não; falha: nenhuma; prov.used: chave_de_juncao_errada

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 3118 a 3119 da trilha; hash dos eventos deste caso: `11707728f95002fd`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
