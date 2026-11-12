<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Escala ou unidade errada em `GET /api/produtos`, campo `preco`

Caso `contrato-escala_ou_unidade_errada#1` da corrida `fase4_ensaio_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_ensaio_v4/qwen2.5_7b/contrato-escala_ou_unidade_errada#1`: o caso `contrato-escala_ou_unidade_errada#1` na corrida `fase4_ensaio_v4`; eventos 153 a 188 da trilha `trilha_cenarios.jsonl`, hash dos eventos `0551d025f198ae15` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Escala ou unidade errada em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 11:19:03 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 11:13:26 a 06/11/2026 11:26:54). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `cenarios`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `escala_ou_unidade_errada` (um valor numérico vem multiplicado por 100) no campo `preco`. Caso `contrato-escala_ou_unidade_errada#1`, de `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36); classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s).
5. Conferir `#produtos-api-status` (0,0 s).

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2096 caracteres, em 20,5 ms.

As 3 conferências do roteiro conferem (a tabela do bloco 7 traz cada uma).

Sintoma, como o código o descreveu para o agente:

> O campo preco veio diferente da referência em modo normal em 14 itens, por exemplo no id 1: 8990.0 em vez de 89.9. A tela mostra 14 linha(s) a menos e 14 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `1cf6e56bcb7be5a1`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 3 linha(s) da referência | 3 linha(s) novas |
| corpo de `GET /api/produtos`, campo `preco` | 89.9 (referência em modo normal) | 8990.0 em 14 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ 8990,00 |
| conferência do roteiro `sem mensagem de erro na carga` | texto no padrão ^$ |  |

A referência em modo normal desta corrida é a trilha `fase4_ensaio_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 4 (tradução: o mapeamento entre as camadas está errado); nível 2 (médio: status 200 e corpo válido, mas o contrato divergiu no tipo, no valor permitido ou no formato).

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 4 (tradução); nível 2 (médio). Confiança do agente: o agente tem dúvida entre causas vizinhas; confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `escala_ou_unidade_errada` (Escala ou unidade errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/escala_ou_unidade_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/escala_ou_unidade_errada.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `tempo_de_resposta_excedido` (Tempo de resposta excedido; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/tempo_de_resposta_excedido.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/tempo_de_resposta_excedido.md`).
- Caso escrito: `contrato-escala_ou_unidade_errada#1` em `cenarios_fase4.py` (catálogo dos dez cenários do ensaio da Fase 5, ficha 36).
- Trilha: `fase4_ensaio_v4/qwen2.5_7b/contrato-escala_ou_unidade_errada#1` em `trilha_cenarios.jsonl`, eventos 153 a 188, hash dos eventos `0551d025f198ae15`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/contrato-escala_ou_unidade_errada__r1.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `escala_ou_unidade_errada` (Escala ou unidade errada). Campo: `preco`. Confiança: o agente tem dúvida entre causas vizinhas; confira antes de agir (probabilidade 0,98 no rótulo; selo `medio` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê preços incorretos, com valores muito maiores do que o esperado, resultando em desconfiança sobre o preço real dos produtos.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu escala_ou_unidade_errada no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido 8990.0 em 14 itens está presente na resposta HTTP e os verbetes escala_ou_unidade_errada, entidade-produto, tempo_de_resposta_excedido estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,00. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 13. Evidência

Poda de `arvore` (evento 165), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `b68e52486de88711`):

```text
document "Churrascaria Fornalha - Produtos (API)"
  navigation
    link "Logotipo Fornalha"
    link "DESTAQUES" href="index.php#destaques"
    link "PRODUTOS" href="index.php#produtos"
    link "PRODUTOS (API)" href="produtos_api.php"
    button "TIPOS" class="dropdown-toggle"
    link "CONTATO" href="index.php#contato"
    searchbox "search" id="buscar" name="buscar" class="form-control"
  main
    heading "Produtos via API" level=2
    group
      heading "Picanha ao Alho" level=3
      text "Carnes"
      text "Picanha grelhada com alho laminado na brasa"
      text "destaque: Sim"
      button "R$ 8990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ 8490,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ 6990,00" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Também podado em código o `corpo_http` (evento 167): de 2096 caracteres para 270 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | 8990.0 em 14 itens |

O que sobrou desta poda (hash `1cf6e56bcb7be5a1`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": 8990.0, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 160): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `61ba8740c5fc1841`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> escala_ou_unidade_errada e não tipo_divergente: a escolha tem probabilidade 0,98 contra 0,00; verbete(s) na evidência: escala_ou_unidade_errada, entidade-produto, tempo_de_resposta_excedido

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `escala_ou_unidade_errada` (Escala ou unidade errada) | 0,98 | sim |
| `tipo_divergente` (Tipo divergente) | 0,00 |  |
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,00 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `estado_da_tela_divergente` (Estado da tela divergente da resposta) | 0,00 |  |
| `estrutura_aninhada_divergente` (Estrutura aninhada divergente) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[escala_ou_unidade_errada]`; verbetes citados: `escala_ou_unidade_errada` (Escala ou unidade errada; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/escala_ou_unidade_errada.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/escala_ou_unidade_errada.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `escala_ou_unidade_errada` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `escala_ou_unidade_errada` | confere | contexto: `escala_ou_unidade_errada`, `entidade-produto`, `tempo_de_resposta_excedido` |
| Algum verbete do contexto trata da causa respondida | `escala_ou_unidade_errada` | confere | verbetes: `escala_ou_unidade_errada`, `entidade-produto` |
| A linha FONTE só tem identificadores, no formato pedido | `[escala_ou_unidade_errada]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["escala_ou_unidade_errada"]} |
| O verbete citado fala da causa respondida | `escala_ou_unidade_errada` | confere | {"termo": "escala_ou_unidade_errada"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo cenarios --saida fase4_ensaio_v4_reexec --repeticoes 1`

## 17. Árvore completa

<details><summary>31 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 153 | 1 | entrada | programa | ao_vivo | 2026-11-06T11:19:03 | caso contrato-escala_ou_unidade_errada#1 |
| 154 | 2 | acao | programa | ao_vivo | 2026-11-06T11:19:03 | passo 1: abrir produtos_api.php |
| 155 | 3 | acao | programa | ao_vivo | 2026-11-06T11:19:03 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 156 | 4 | acao | programa | ao_vivo | 2026-11-06T11:19:03 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 157 | 5 | acao | programa | ao_vivo | 2026-11-06T11:19:03 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default |
| 158 | 6 | acao | programa | ao_vivo | 2026-11-06T11:19:03 | passo 5: conferir #produtos-api-status |
| 160 | 7 | interceptacao | programa | ao_vivo | 2026-11-06T11:19:03 | GET /api/produtos 200 |
| 161 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | conferencia_do_roteiro: confere |
| 162 | 9 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | conferencia_do_roteiro: confere |
| 163 | 10 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | conferencia_do_roteiro: confere |
| 165 | 11 | poda | programa | ao_vivo | 2026-11-06T11:19:03 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 167 | 12 | poda | programa | ao_vivo | 2026-11-06T11:19:03 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 168 | 13 | candidatos | programa | ao_vivo | 2026-11-06T11:19:03 | 3 de 39 verbetes entregues |
| 170 | 14 | prompt | programa | ao_vivo | 2026-11-06T11:19:03 | diagnostico: 4196 caracteres; verbetes escala_ou_unidade_errada, entidade-produto, tempo_de_resposta_excedido |
| 172 | 15 | inferencia | programa | ao_vivo | 2026-11-06T11:19:03 | diagnostico: 89,1 s |
| 173 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T11:19:03 | causa_raiz: `escala_ou_unidade_errada` |
| 174 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T11:19:03 | campo: `preco` |
| 175 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T11:19:03 | impacto: `O usuário vê preços incorretos, com valores muito maiores do que o esperado, resultando em desconfiança sobre o preço real dos produtos.` |
| 176 | 19 | declaracao | modelo | ao_vivo | 2026-11-06T11:19:03 | fonte: `[escala_ou_unidade_errada]` |
| 177 | 20 | declaracao | modelo | ao_vivo | 2026-11-06T11:19:03 | fonte_citada: `escala_ou_unidade_errada` |
| 178 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | quatro_linhas_presentes: confere |
| 179 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | rotulo_no_conjunto: confere |
| 180 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | fonte_existe_na_biblioteca: confere |
| 181 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | fonte_estava_no_contexto: confere |
| 182 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | campo_existe_no_caso: confere |
| 183 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 184 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | notas_nos_verbetes_citados: informativo |
| 185 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | impacto: nao_verificavel |
| 186 | 29 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | fonte_formato_valido: confere |
| 187 | 30 | verificacao | verificacao | ao_vivo | 2026-11-06T11:19:03 | fonte_contem_termo_da_causa: confere |
| 188 | 31 | decisao | programa | ao_vivo | 2026-11-06T11:19:03 | diagnostico: escolha escala_ou_unidade_errada; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 188, decisão `diagnostico`: escolha `escala_ou_unidade_errada`; resultado rotulo_emitido.
  - Evidência: evento 167 (sinal_em_codigo); evento 165 (arvore_podada); evento 160 (corpo_http); evento 168 (verbete_entregue: `escala_ou_unidade_errada`, `entidade-produto`, `tempo_de_resposta_excedido`); evento 172 (resposta); evento 177 (verbete_citado: `escala_ou_unidade_errada`).
  - Usou: `escala_ou_unidade_errada`, `entidade-produto`, `tempo_de_resposta_excedido`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 153 a 188 da trilha; hash dos eventos deste caso: `0551d025f198ae15`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
