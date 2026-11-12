<!-- ! Alteração de IA - Revisar: relatório DERIVADO (versão 3, Pós-Fase 4, pacote Q1), gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v3 a partir da trilha v2 do caso, no molde do relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (decisão 104); não editar à mão.
     ! Motivo: o que o código sabe vem preenchido da trilha, sem segunda chamada a modelo; severidade, prioridade e estado ficam para o analista (plano da Pós-Fase 4, seção 3.1); o hash no fim prova de que eventos ele saiu. -->
# Relatório de defeito: Valor fora do domínio em `GET /api/produtos`, campo `preco`

Caso `semt-20` da corrida `fase4_tela_v4`; modelo `qwen2.5:7b` no Ollama 0.40.14 (o programa que roda o modelo nesta máquina); Playwright 1.64.1 com o navegador 156.0.8078.4 (o Playwright controla o navegador, sem janela); trilha no esquema v2. Os onze primeiros blocos são os campos do relatório de defeitos do syllabus CTFL 4.0 do ISTQB (Certified Tester Foundation Level, a certificação de base em teste de software do International Software Testing Qualifications Board; seção 5.5); os seis seguintes são o que o agente fez, declarou e conferiu. Tudo o que está aqui saiu da trilha gravada; o que o modelo escreveu vem marcado como texto do modelo.

## 1. Identificador

`fase4_tela_v4/qwen2.5_7b/semt-20@tela`: o caso `semt-20` na corrida `fase4_tela_v4`; eventos 1730 a 1763 da trilha `trilha_tela.jsonl`, hash dos eventos `6e335cb32433f08a` (a impressão digital destes eventos: muda se um byte deles mudar).

## 2. Título

Valor fora do domínio em `GET /api/produtos`, campo `preco`

## 3. Data, organização e autor

Observado em 06/11/2026 10:57:09 (hora do primeiro evento do caso na trilha; a corrida foi de 06/11/2026 09:53:30 a 06/11/2026 11:12:59). Organização emissora: o projeto do TCC (agente de QA de ponta a ponta local; o programa que roda os casos é o harness `executar_fase4.py`, no modo `tela`). Autor: o agente (modelo `qwen2.5:7b`, biblioteca de produção `95af35290860`; o resto do ambiente está no bloco 4); nenhuma revisão humana registrada nesta trilha: o veredito final é do analista.

## 4. Objeto de teste e ambiente

A página `produtos_api.php` do site PHP (CobaiaFront), que chama a CobaiaAPI em `GET /api/produtos` (host localhost:8000).

Modelo `qwen2.5:7b` (quantização Q4_K_M: os pesos do modelo guardados com menos bits, para caber na memória) no Ollama 0.40.14, só CPU. Janela de contexto num_ctx 8192 tokens (os pedaços de texto que o modelo lê de uma vez) e temperatura 0,1 (quase nenhuma aleatoriedade na resposta). Playwright 1.64.1 com o navegador 156.0.8078.4 (canal chromium, sem janela). Biblioteca de produção `95af35290860`, índice da busca `11e763ba9cb1fdf4` e prompt fixo `2e42cf9c31826941` (o prompt é o texto que o modelo recebe; o fixo é a parte igual em todos os casos); 3 verbetes por consulta. As versões da máquina estão em `resultados_alvo/fase4/ambiente.json`.

## 5. Contexto

Roteiro `api-catalogo` da tela, com a falha injetada `valor_fora_do_dominio` (um valor vem fora do domínio permitido (número negativo, status desconhecido, booleano como texto)) no campo `preco`. O roteiro parou no passo 4 (conferir `#produtos-api-grid .thumbnail .btn-default`). Caso `semt-20`, de `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação); classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela).

## 6. Descrição para reproduzir

Passos do roteiro, na ordem em que o agente os executou (os tempos são os medidos):

1. Abrir `produtos_api.php` (0,1 s).
2. Esperar aparecer `#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger` (0,0 s).
3. Conferir `#produtos-api-grid .saiba-mais` (0,0 s).
4. Conferir `#produtos-api-grid .thumbnail .btn-default` (0,0 s): falhou aqui.

A página chamou `GET /api/produtos` em localhost:8000 e recebeu status 200 (a API respondeu sem código de erro), `application/json`, 2082 caracteres, em 16,1 ms.

A conferência do roteiro `preço do primeiro cartão` não confere: esperava texto no padrão ^R\$ \d+,\d{2}$ e observou R$ -90,90.
A outra conferência do roteiro confere (a tabela do bloco 7 a traz).

Sintoma, como o código o descreveu para o agente:

> A conferência 'preço do primeiro cartão' falhou: esperava texto no padrão ^R\$ \d+,\d{2}$; viu R$ -90,90. O campo preco veio diferente da referência em modo normal em 14 itens, por exemplo no id 1: -90.9 em vez de 89.9. A tela mostra 14 linha(s) a menos e 14 a mais que a referência.

Trecho da resposta, como a poda em código deixou para o agente (hash `27ade78311a661e6`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": -90.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-20 --k 3`

## 7. Resultado esperado e resultado real

Contrato esperado pela interface: `id: inteiro | nome: texto | resumo: texto|nulo | tipo: texto | preco: numero | imagem: texto|nulo | destaque: booleano`.

O diff que a poda e o caso ao vivo calculam em código (o que o contrato e a referência em modo normal esperam, contra o que veio):

| Onde | Esperado | Recebido |
|---|---|---|
| tela (árvore de acessibilidade, contra a referência em modo normal) | 3 linha(s) da referência | 3 linha(s) novas |
| corpo de `GET /api/produtos`, campo `preco` | 89.9 (referência em modo normal) | -90.9 em 14 itens |
| conferência do roteiro `grid com 14 cartões` | 14 elementos | 14 elementos |
| conferência do roteiro `preço do primeiro cartão` | texto no padrão ^R\$ \d+,\d{2}$ | R$ -90,90 |

A referência em modo normal desta corrida é a trilha `fase4_tela_v4/referencia/api-catalogo@normal`: é contra ela que a poda comparou a tela e o corpo.

## 8. Severidade

em branco: preenche o analista. Para ajudar a decidir, o que o código sabe: classe 3 (semântica: os tipos ou os domínios dos valores não fazem sentido); nível 3 (difícil: status 200, corpo válido e tipos certos; a falha é de lógica ou de estado e só aparece cruzando duas requisições, ou a requisição com a tela); o roteiro parou no passo 4.

## 9. Prioridade

em branco: preenche o analista. A classe e o nível estão na severidade: classe 3 (semântica); nível 3 (difícil). Confiança do agente: o agente não está seguro desta causa; trate como hipótese e confira antes de agir.

## 10. Estado

aberto (estado inicial, dado pelo código; o analista muda no hub).

## 11. Referências

- Verbetes citados pelo agente na linha FONTE: `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`).
- Verbetes entregues pela busca e não citados: `entidade-produto` (Produto e sua categoria; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/entidade-produto.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/entidade-produto.md`); `fluxo-reserva-e-cancelamento` (Fluxo de reservar e cancelar; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/negocio/fluxo-reserva-e-cancelamento.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/negocio/fluxo-reserva-e-cancelamento.md`).
- Caso escrito: `semt-20` em `banco_casos.py` ou `banco_casos_extra.py` (os 72 casos de avaliação).
- Trilha: `fase4_tela_v4/qwen2.5_7b/semt-20@tela` em `trilha_tela.jsonl`, eventos 1730 a 1763, hash dos eventos `6e335cb32433f08a`.
- Relatório v2 do mesmo caso (seis seções, formato da Fase 4): `../relatorios/semt-20@tela.md`.
- Comando de reexecução: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-20 --k 3`.
- Molde: relatório de defeitos da seção 5.5 do syllabus CTFL 4.0 (ISTQB, 2023, p. 50), adotado pela decisão 104.

## 12. Veredito do agente

Causa respondida: `valor_fora_do_dominio` (Valor fora do domínio). Campo: `preco`. Confiança: o agente não está seguro desta causa; trate como hipótese e confira antes de agir (probabilidade 0,64 no rótulo; selo `baixo` pelos limiares da calibração).

Impacto, nas palavras do modelo (texto do modelo, não conferido por código): `O usuário vê preços negativos na interface, o que é incoerente e pode levar a confusão.`.

Justificativa (gerada por molde na corrida, como está na trilha):

> O agente respondeu valor_fora_do_dominio no campo preco porque o sinal preco: esperado 89.9 (referência em modo normal), recebido -90.9 em 14 itens está presente na resposta HTTP e os verbetes valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento estavam entre os entregues ao modelo. A segunda causa, tipo_divergente, ficou com probabilidade 0,35. A FONTE cita 1 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto. O agente não está seguro desta causa (probabilidade 0,64); trate como hipótese e confira o campo preco antes de agir.

## 13. Evidência

Poda de `arvore` (evento 1740), feita em código antes de montar o prompt: 193 nós antes, 39 linhas depois. Regras aplicadas: `cartoes_omitidos` 11, `decoracao_removida` 1, `headings_removidos` 1, `imagens_removidas` 16, `interativos_sem_nome_removidos` 8, `listas_achatadas` 14, `textos_sem_letra_removidos` 3.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| arvore | 3 linha(s) da referência | 3 linha(s) novas |

Trecho podado (hash `549519a6e88e6100`):

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
      button "R$ -90,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="1"
    group
      heading "Picanha Simples" level=3
      text "Carnes"
      text "Corte nobre grelhado no ponto"
      text "destaque: Não"
      button "R$ -85,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="2"
    group
      heading "Fraldinha" level=3
      text "Carnes"
      text "Corte grelhado na brasa, fatiado na hora"
      text "destaque: Não"
      button "R$ -70,90" class="btn btn-default disable"
      button "Saiba Mais..." class="btn btn-info btn-xs saiba-mais" data-id="3"
    text "(mais 11 cartões omitidos pela poda)"
    heading "Links" level=4
    heading "Contato" level=4
    textbox "Digite seu nome" name="nome_contato" class="form-control"
    textbox "Digite seu email" name="email_contato" class="form-control"
    textbox "Digite seu comentario" name="comentario_contato" class="form-control"
    button "enviar" class="btn btn-danger btn-block"

```

Também podado em código o `corpo_http` (evento 1742): de 2082 caracteres para 269 caracteres, pelas regras `diff_contra_contrato`, `diff_contra_referencia`.

| Campo do contrato | Esperado | Recebido |
|---|---|---|
| preco | 89.9 (referência em modo normal) | -90.9 em 14 itens |

O que sobrou desta poda (hash `27ade78311a661e6`):

```text
lista com 14 itens (referência em modo normal: 14); preco diferente em 14 itens; por exemplo: {"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": -90.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1736): `GET /api/produtos`, status 200 (a API respondeu sem código de erro); corpo guardado com o hash `6adc357553572583`.

## 14. Contraste com a segunda causa

O contraste registrado na trilha (molde da corrida):

> valor_fora_do_dominio e não tipo_divergente: a escolha tem probabilidade 0,64 contra 0,35; verbete(s) na evidência: valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento

| Alternativa | Probabilidade lida no rótulo | Escolhida |
|---|---|---|
| `valor_fora_do_dominio` (Valor fora do domínio) | 0,64 | sim |
| `tipo_divergente` (Tipo divergente) | 0,35 |  |
| `formato_de_data_divergente` (Formato de data divergente) | 0,00 |  |
| `campo_ausente` (Campo ausente) | 0,00 |  |
| `campo_renomeado` (Campo renomeado) | 0,00 |  |
| `colecao_no_lugar_de_objeto` (Coleção no lugar de objeto (ou o inverso)) | 0,00 |  |

## 15. FONTE declarada e conferida

Linha FONTE como veio: `[valor_fora_do_dominio]`; verbetes citados: `valor_fora_do_dominio` (Valor fora do domínio; leitura: `Programacao/AgenteCore/biblioteca_producao_leitura/erros/valor_fora_do_dominio.md`; verbete: `Programacao/AgenteCore/biblioteca_producao/erros/valor_fora_do_dominio.md`).

| Conferência em código | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `valor_fora_do_dominio` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `valor_fora_do_dominio` | confere | contexto: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento` |
| Algum verbete do contexto trata da causa respondida | `valor_fora_do_dominio` | confere | verbetes: `valor_fora_do_dominio`, `fluxo-reserva-e-cancelamento` |
| A linha FONTE só tem identificadores, no formato pedido | `[valor_fora_do_dominio]` | confere | {"formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre", "ids": ["valor_fora_do_dominio"]} |
| O verbete citado fala da causa respondida | `valor_fora_do_dominio` | confere | {"termo": "valor_fora_do_dominio"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, conferida só pelas regras em código acima.

## 16. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_v4_reexec --ids semt-20 --k 3`

## 17. Árvore completa

<details><summary>29 eventos da trilha, na ordem em que aconteceram (o que o programa fez, o que o modelo declarou e o que o código conferiu, em camadas separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1730 | 1 | entrada | programa | ao_vivo | 2026-11-06T10:57:09 | caso semt-20 |
| 1731 | 2 | acao | programa | ao_vivo | 2026-11-06T10:57:10 | passo 1: abrir produtos_api.php |
| 1732 | 3 | acao | programa | ao_vivo | 2026-11-06T10:57:10 | passo 2: esperar aparecer #produtos-api-grid .saiba-mais, #produtos-api-status.text-danger |
| 1733 | 4 | acao | programa | ao_vivo | 2026-11-06T10:57:10 | passo 3: conferir #produtos-api-grid .saiba-mais |
| 1734 | 5 | acao | programa | ao_vivo | 2026-11-06T10:57:10 | passo 4: conferir #produtos-api-grid .thumbnail .btn-default (falhou) |
| 1736 | 6 | interceptacao | programa | ao_vivo | 2026-11-06T10:57:10 | GET /api/produtos 200 |
| 1737 | 7 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | conferencia_do_roteiro: confere |
| 1738 | 8 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | conferencia_do_roteiro: nao_confere |
| 1740 | 9 | poda | programa | ao_vivo | 2026-11-06T10:57:10 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, decoracao_removida, headings_removidos, imagens_removidas, interativos_sem_nome_removidos, listas_achatadas, textos_sem_letra_removidos |
| 1742 | 10 | poda | programa | ao_vivo | 2026-11-06T10:57:10 | corpo_http: 1 diferença(s) contra o contrato; regras diff_contra_contrato, diff_contra_referencia |
| 1743 | 11 | candidatos | programa | ao_vivo | 2026-11-06T10:57:10 | 3 de 39 verbetes entregues |
| 1745 | 12 | prompt | programa | ao_vivo | 2026-11-06T10:57:10 | diagnostico: 3971 caracteres; verbetes valor_fora_do_dominio, entidade-produto, fluxo-reserva-e-cancelamento |
| 1747 | 13 | inferencia | programa | ao_vivo | 2026-11-06T10:57:10 | diagnostico: 81,5 s |
| 1748 | 14 | declaracao | modelo | ao_vivo | 2026-11-06T10:57:10 | causa_raiz: `valor_fora_do_dominio` |
| 1749 | 15 | declaracao | modelo | ao_vivo | 2026-11-06T10:57:10 | campo: `preco` |
| 1750 | 16 | declaracao | modelo | ao_vivo | 2026-11-06T10:57:10 | impacto: `O usuário vê preços negativos na interface, o que é incoerente e pode levar a confusão.` |
| 1751 | 17 | declaracao | modelo | ao_vivo | 2026-11-06T10:57:10 | fonte: `[valor_fora_do_dominio]` |
| 1752 | 18 | declaracao | modelo | ao_vivo | 2026-11-06T10:57:10 | fonte_citada: `valor_fora_do_dominio` |
| 1753 | 19 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | quatro_linhas_presentes: confere |
| 1754 | 20 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | rotulo_no_conjunto: confere |
| 1755 | 21 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | fonte_existe_na_biblioteca: confere |
| 1756 | 22 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | fonte_estava_no_contexto: confere |
| 1757 | 23 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | campo_existe_no_caso: confere |
| 1758 | 24 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1759 | 25 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | notas_nos_verbetes_citados: informativo |
| 1760 | 26 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | impacto: nao_verificavel |
| 1761 | 27 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | fonte_formato_valido: confere |
| 1762 | 28 | verificacao | verificacao | ao_vivo | 2026-11-06T10:57:10 | fonte_contem_termo_da_causa: confere |
| 1763 | 29 | decisao | programa | ao_vivo | 2026-11-06T10:57:10 | diagnostico: escolha valor_fora_do_dominio; divergência entre o declarado e o medido: não |

</details>

Nós de decisão, na ordem:

- evento 1763, decisão `diagnostico`: escolha `valor_fora_do_dominio`; resultado rotulo_emitido.
  - Evidência: evento 1742 (sinal_em_codigo); evento 1740 (arvore_podada); evento 1736 (corpo_http); evento 1743 (verbete_entregue: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento`); evento 1747 (resposta); evento 1752 (verbete_citado: `valor_fora_do_dominio`).
  - Usou: `valor_fora_do_dominio`, `entidade-produto`, `fluxo-reserva-e-cancelamento`.
Nenhum nó registrou divergência entre o declarado e o medido, nem falha.

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1730 a 1763 da trilha; hash dos eventos deste caso: `6e335cb32433f08a`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
