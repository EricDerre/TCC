<!-- ! Alteração de IA - Revisar: arquivo novo (11/11/2026) com a origem do CobaiaFront: o projeto de onde o site veio, o autor, o que este trabalho acrescentou e mudou nele, a diferença contra o repositório público de origem e como citar.
     ! Motivo: o Eric pediu, em 11/11/2026, a citação correta do Projeto CHULETA, que é a parte PHP da cobaia. Até esta data nenhum arquivo do repositório dizia de onde o site veio, e a licença MIT daqui, sozinha, dava a entender que o site tinha sido escrito para este trabalho. Nenhum arquivo do site foi alterado para isto: só esta nota entrou na pasta. As listas vêm do histórico do Git deste repositório e da árvore de arquivos do repositório de origem, lida pela API do GitHub nesta data. -->
# Origem do CobaiaFront

O site desta pasta é o **Projeto CHULETA**, de Pedro Henrique Torres Gonçalves, integrante do grupo deste trabalho. Ele foi cedido pelo autor para servir de sistema sob teste: é o sistema antigo, em PHP, que o agente usa pela tela.

- Repositório de origem: https://github.com/pedrohtgoncalvesgit/Projeto-CHULETA
- Autor: Pedro Henrique Torres Gonçalves (no GitHub, `pedrohtgoncalvesgit`)
- Datas no repositório de origem: criado em 17/09/2024, com três commits nesse dia
- Licença: o repositório de origem não traz arquivo de licença. Aqui, o site é distribuído sob a [licença MIT](../../LICENSE) deste repositório, da qual o autor do site é um dos titulares. As bibliotecas que o site usa mantêm as licenças delas (Bootstrap e jQuery, MIT; PHPMailer, LGPL 2.1, com o texto em `PHPMailer/LICENSE`).

## Como citar

> GONÇALVES, Pedro Henrique Torres. **Projeto CHULETA.** 2024. Disponível em: https://github.com/pedrohtgoncalvesgit/Projeto-CHULETA. Acesso em: 11 nov. 2026.

## O que este trabalho acrescentou e mudou

O site entrou neste repositório em 31/08/2026, no commit `e854a0eb`, com 197 arquivos, como foi clonado. Depois disso, este trabalho acrescentou quatro arquivos e alterou quatro. O resto ficou como veio.

| O que | Arquivos | Para quê |
|---|---|---|
| Acrescentado em 31/08/2026 | `produtos_api.php`, `banco/schema_completo.sql`, `banco/seed.sql` | A aba que lê os produtos pela CobaiaAPI, e o banco de dados reconstruído a partir das consultas do próprio site |
| Acrescentado em 03/11/2026 | `quebra.php` | A variante que troca o localizador de um elemento da tela, ligada só por parâmetro de URL, para medir a cura de seletor |
| Alterado | `menu_publico.php`, `admin/login.php`, `admin/produtos_lista.php`, `cliente/registrar_reserva.php` | O item de menu da aba nova e os pontos em que a variante de `quebra.php` entra |

## Diferença contra o repositório público de origem

A comparação é pelo caminho dos arquivos, feita em 11/11/2026 contra o ramo `main` do repositório de origem. Ela não compara o conteúdo de cada arquivo.

| | Quantos | Quais |
|---|---|---|
| Nos dois lugares | 196 | As páginas do site, `PHPMailer/`, `js/`, `css/`, `fonts/` e `images/` |
| Só nesta pasta | 5 | Os quatro arquivos acrescentados por este trabalho e `css/estilo-login.css`, que já veio na cópia clonada em 31/08/2026 |
| Só no repositório de origem | 10 | `README.md`, `faixa_reserva.php`, `reservado.php`, `reservas.php`, `admin/reservas_concluir.php`, `admin/reservas_info.php`, `admin/reservas_lista.php`, `banco/bancoexport.sql`, `banco/dumpbanco.sql`, `banco/script.sql` |

A cópia que este trabalho recebeu não é, portanto, idêntica ao que está publicado no repositório de origem: ela tem um arquivo de estilo a mais e não tem as páginas de reserva da raiz e do painel administrativo.
