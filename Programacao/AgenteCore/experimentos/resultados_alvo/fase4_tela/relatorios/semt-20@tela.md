<!-- ! Alteração de IA - Revisar: relatório DERIVADO, gerado por gerar_relatorio_raciocinio.relatorio_do_caso_v2 a partir da trilha v2 do caso; não editar à mão.
     ! Motivo: o relatório para humanos sai por script do arquivo bruto, sem segunda chamada a modelo, na ordem fixa da especificação (seção 11); o hash no fim prova de que eventos ele saiu. -->
# Caso `semt-20`: o que o agente fez, declarou e conferiu

Trilha `fase4_tela/qwen2.5_7b/semt-20@tela`; modelo `qwen2.5:7b`, Ollama 0.40.2, Playwright 1.64.1 com navegador 156.0.8078.4; esquema v2. Origem dos eventos: ao_vivo.

## 1. Veredito

**CAUSA_RAIZ:** `tipo_divergente` · **CAMPO:** `preco` · selo de probabilidade: **medio** (p = 0,88)

**IMPACTO (declarado):** `O usuário vê preços negativos e formatados incorretamente, o que causa confusão e possíveis erros na interação com o sistema.`

Justificativa (gerada por molde): O agente respondeu tipo_divergente no campo preco porque o sinal arvore: esperado 3 linha(s) da referência, recebido 3 linha(s) novas está presente na tela e os verbetes entidade-produto, tipo_divergente, pagina-produtos-api estavam entre os entregues ao modelo. A segunda causa, valor_fora_do_dominio, ficou com probabilidade 0,08. A FONTE cita 2 verbete(s), todos presentes no contexto. O que não dá para conferir por código: a frase de impacto.

## 2. Evidência

Poda de `arvore` (evento 1803): regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos; antes {"nos": 193}, depois {"linhas": 39}.

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

Poda de `corpo_http` (evento 1805): regras diff_contra_contrato; antes {"chars": 2082}, depois {"chars": 175}.

Trecho podado (hash `2f5584eefe6d4bf2`):

```text
{"id": 1, "nome": "Picanha ao Alho", "resumo": "Picanha grelhada com alho laminado na brasa", "tipo": "Carnes", "preco": -90.9, "imagem": "picanha_alho.jpg", "destaque": true}
```

Interceptação (evento 1799): `GET /api/produtos` status 200; corpo `6adc357553572583`, árvore `None`.

## 3. Contraste com a segunda causa

tipo_divergente e não valor_fora_do_dominio: a escolha tem probabilidade 0,88 contra 0,08; verbete(s) na evidência: entidade-produto, tipo_divergente, pagina-produtos-api

| Alternativa | Probabilidade ou escore | Escolhida |
|---|---|---|
| tipo_divergente | 0,88 | sim |
| valor_fora_do_dominio | 0,08 |  |
| formato_de_data_divergente | 0,03 |  |
| colecao_no_lugar_de_objeto | 0,00 |  |
| resposta_truncada | 0,00 |  |
| campo_ausente | 0,00 |  |
| campo_renomeado | 0,00 |  |
| corpo_nao_e_json | 0,00 |  |
| corpo_vazio | 0,00 |  |
| escala_ou_unidade_errada | 0,00 |  |
| estrutura_aninhada_divergente | 0,00 |  |

## 4. FONTE declarada e conferida

Linha FONTE como veio: `[tipo_divergente] [entidade-produto]`; verbetes citados: `tipo_divergente`, `entidade-produto`.

| Conferência | Sobre | Resultado | Evidência |
|---|---|---|---|
| O verbete citado existe na biblioteca | `tipo_divergente` | confere |  |
| O verbete citado existe na biblioteca | `entidade-produto` | confere |  |
| O verbete citado estava no contexto entregue ao modelo | `tipo_divergente` | confere | contexto: `entidade-produto`, `tipo_divergente`, `pagina-produtos-api` |
| O verbete citado estava no contexto entregue ao modelo | `entidade-produto` | confere | contexto: `entidade-produto`, `tipo_divergente`, `pagina-produtos-api` |
| Algum verbete do contexto trata da causa respondida | `tipo_divergente` | confere | verbetes: `entidade-produto`, `tipo_divergente`, `pagina-produtos-api` |
| fonte_formato_valido | `[tipo_divergente] [entidade-produto]` | confere | {"ids": ["tipo_divergente", "entidade-produto"], "formato": "[id] separados por vírgula, ponto e vírgula ou 'e', sem texto livre"} |
| fonte_contem_termo_da_causa | `tipo_divergente` | confere | {"termo": "tipo_divergente"} |
| fonte_contem_termo_da_causa | `entidade-produto` | **não confere** | {"termo": "tipo_divergente"} |

Nenhuma intervenção rodou neste caso: a FONTE fica como declarada, não verificada.

## 5. Linha de ação

Confira o campo `preco` em `GET /api/produtos` e compare com o contrato esperado pela interface.

Comando para reexecutar o caso: `RESULTADOS_DIR=resultados_alvo python executar_fase4.py --modo tela --saida fase4_tela_reexec --ids semt-20 --k 3`

## 6. Árvore completa

<details><summary>33 eventos da trilha, na ordem em que aconteceram (camadas programa, modelo e verificação separadas)</summary>

| seq | passo | Tipo | Camada | Origem | Quando | Resumo |
|---|---|---|---|---|---|---|
| 1793 | 1 | entrada | programa | ao_vivo | 2026-11-01T12:18:36 | caso semt-20 |
| 1794 | 2 | acao | programa | ao_vivo | 2026-11-01T12:18:37 | {"passo": 1, "acao": "abrir", "seletor": null, "url": "produtos_api.php", "tempo_ms": 124.8, "falhou": false} |
| 1795 | 3 | acao | programa | ao_vivo | 2026-11-01T12:18:37 | {"passo": 2, "acao": "esperar", "seletor": "#produtos-api-grid .saiba-mais, #produtos-api-status.text-danger", "url": null, "tempo_ms": 10.0, "falhou": false} |
| 1796 | 4 | acao | programa | ao_vivo | 2026-11-01T12:18:37 | {"passo": 3, "acao": "conferir", "seletor": "#produtos-api-grid .saiba-mais", "url": null, "tempo_ms": 12.8, "falhou": false} |
| 1797 | 5 | acao | programa | ao_vivo | 2026-11-01T12:18:37 | {"passo": 4, "acao": "conferir", "seletor": "#produtos-api-grid .thumbnail .btn-default", "url": null, "tempo_ms": 4.0, "falhou": true} |
| 1799 | 6 | interceptacao | programa | ao_vivo | 2026-11-01T12:18:37 | GET /api/produtos 200 |
| 1800 | 7 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | conferencia_do_roteiro: confere |
| 1801 | 8 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | conferencia_do_roteiro: nao_confere |
| 1803 | 9 | poda | programa | ao_vivo | 2026-11-01T12:18:37 | arvore: 1 diferença(s) contra o contrato; regras cartoes_omitidos, imagens_removidas, decoracao_removida, listas_achatadas, textos_sem_letra_removidos, interativos_sem_nome_removidos, headings_removidos |
| 1805 | 10 | poda | programa | ao_vivo | 2026-11-01T12:18:37 | corpo_http: 0 diferença(s) contra o contrato; regras diff_contra_contrato |
| 1806 | 11 | candidatos | programa | ao_vivo | 2026-11-01T12:18:37 | 3 de 40 verbetes entregues |
| 1808 | 12 | prompt | programa | ao_vivo | 2026-11-01T12:18:37 | {"etapa": "diagnostico", "sha": "0ff778fb8fb6676d", "prompt_sha256": "0ff778fb8fb6", "chars": 5400, "hash_prompt_fixo": "2e42cf9c31826941"} |
| 1810 | 13 | inferencia | programa | ao_vivo | 2026-11-01T12:18:37 | diagnostico: 85,2 s |
| 1811 | 14 | declaracao | modelo | ao_vivo | 2026-11-01T12:18:37 | causa_raiz: `tipo_divergente` |
| 1812 | 15 | declaracao | modelo | ao_vivo | 2026-11-01T12:18:37 | campo: `preco` |
| 1813 | 16 | declaracao | modelo | ao_vivo | 2026-11-01T12:18:37 | impacto: `O usuário vê preços negativos e formatados incorretamente, o que causa confusão e possíveis erros na interação com o sistema.` |
| 1814 | 17 | declaracao | modelo | ao_vivo | 2026-11-01T12:18:37 | fonte: `[tipo_divergente] [entidade-produto]` |
| 1815 | 18 | declaracao | modelo | ao_vivo | 2026-11-01T12:18:37 | fonte_citada: `tipo_divergente` |
| 1816 | 19 | declaracao | modelo | ao_vivo | 2026-11-01T12:18:37 | fonte_citada: `entidade-produto` |
| 1817 | 20 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | quatro_linhas_presentes: confere |
| 1818 | 21 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | rotulo_no_conjunto: confere |
| 1819 | 22 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_existe_na_biblioteca: confere |
| 1820 | 23 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_existe_na_biblioteca: confere |
| 1821 | 24 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_estava_no_contexto: confere |
| 1822 | 25 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_estava_no_contexto: confere |
| 1823 | 26 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | campo_existe_no_caso: confere |
| 1824 | 27 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | rotulo_sustentado_por_verbete_do_contexto: confere |
| 1825 | 28 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | notas_nos_verbetes_citados: informativo |
| 1826 | 29 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | impacto: nao_verificavel |
| 1827 | 30 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_formato_valido: confere |
| 1828 | 31 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_contem_termo_da_causa: confere |
| 1829 | 32 | verificacao | verificacao | ao_vivo | 2026-11-01T12:18:37 | fonte_contem_termo_da_causa: nao_confere |
| 1830 | 33 | decisao | programa | ao_vivo | 2026-11-01T12:18:37 | diagnostico: escolha tipo_divergente; divergência não |

</details>

Nós de decisão:

- evento 1830, `diagnostico`: escolha `tipo_divergente`; resultado rotulo_emitido; evidência: evento 1805 (sinal_em_codigo), evento 1803 (arvore_podada), evento 1799 (corpo_http), evento 1806 (verbete_entregue, entidade-produto), evento 1806 (verbete_entregue, tipo_divergente), evento 1806 (verbete_entregue, pagina-produtos-api), evento 1810 (resposta), evento 1815 (verbete_citado, tipo_divergente), evento 1816 (verbete_citado, entidade-produto); divergência: não; falha: nenhuma; prov.used: entidade-produto, tipo_divergente, pagina-produtos-api (gen_ai: chat)

Sem gabarito: o agente não teve a resposta certa deste caso; tudo acima é o que ele pôde mostrar sozinho.

## Rastro

Gerado dos eventos 1793 a 1830 da trilha; hash dos eventos deste caso: `27f64dc497a0c0da`. Origem de cada evento: `ao_vivo` (emitido pelo agente na hora), `registro`, `recalculado` ou `humano`.
