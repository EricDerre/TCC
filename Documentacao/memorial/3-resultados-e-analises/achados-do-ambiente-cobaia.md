<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Achados experimentais — ambiente cobaia (4.1 a 4.11)

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 4. Achados experimentais

Esta é a seção com maior valor para o relatório: são resultados obtidos executando, não deduções. Vários contradizem a expectativa inicial.

### 4.1 O objeto de estudo não existia no material de partida
O site cedido não faz nenhuma requisição JSON. Toda a premissa de interceptar quebra de contrato dependia de construir essa fronteira. **Implicação metodológica:** a "aplicação-alvo determinística" que o projeto de pesquisa menciona no plural precisou ser, em parte, construída.

### 4.2 Schema incompleto e conta de cliente impossível
Além das duas estruturas ausentes, `tbusuarios` não tinha as colunas `nome` e `cpf` que a view exige, e seu ENUM de nível só admitia `'sup'` — ou seja, **uma conta de cliente era fisicamente impossível de existir**, e o fluxo de reservas era código morto. Reconstruído por engenharia reversa das consultas reais do código, sem alterar nenhum arquivo PHP.

### 4.3 A extensão `mbstring` era obrigatória, não opcional
`mb_strimwidth()` é usada em 5 páginas de produtos, incluindo a home. Sem a extensão carregada é **erro fatal**, não aviso. Só apareceu ao inspecionar a página inteira — um teste superficial buscando uma string passava, porque o conteúdo anterior ao ponto de falha ainda era emitido.

### 4.4 `output_buffering` mascarava um bug pré-existente de sessão
`cliente/index.php` emite HTML antes de `reserva_cli.php` incluir `acesso_com.php`, que só então chama `session_start()`. Sem buffer de saída, isso vira "headers already sent", a sessão do login não é retomada e a página **trunca logo após a saudação**. Um XAMPP típico traz `output_buffering` ligado por padrão, o que esconde o defeito. Resolvido por configuração do PHP, sem tocar no código.

### 4.5 `INNER JOIN` apagava clientes sem reserva
A primeira versão da view `vw_tbpedidos` usava junção interna a partir de `tbpedido_reserva`: um cliente recém-criado, ainda sem reservas, sumia inteiramente da view e a saudação quebrava. Corrigido com `LEFT JOIN` a partir de `tbusuarios`.

### 4.6 O MariaDB do winget não registra serviço no Windows
Instalado sem privilégios de administrador, os binários e o diretório de dados são criados, mas **nenhum serviço do Windows é registrado**. Por isso o banco passou a ser gerenciado como subprocesso comum, igual ao servidor PHP e ao uvicorn — o que, de quebra, eliminou a necessidade de elevação em toda a instalação.

### 4.7 O `extension_dir` do PHP vem apontando para o lugar errado
O build Windows aponta por padrão para `C:\php\ext`, que não corresponde ao caminho real de instalação via winget. Sem sobrescrever explicitamente, as extensões falham a carregar **silenciosamente**.

### 4.8 Um executável PyInstaller não consegue criar ambientes virtuais
Duas falhas distintas ao empacotar o instalador: `Path(__file__)` aponta para a pasta temporária de extração, não para onde o executável está; e `venv.EnvBuilder` falha ao copiar `venvlauncher.exe`, porque o interpretador embutido não tem o layout de uma instalação Python normal. Resolvido usando `sys.executable` quando congelado e delegando a criação do ambiente a um Python real via subprocesso.

### 4.9 Acentuação quebra o interpretador de arquivos `.cmd`
Testado isoladamente: o `cmd.exe` lê o arquivo na codepage OEM, e os bytes UTF-8 de `ç`/`ã` re-tokenizam a linha de comentário, fazendo o script imprimir um erro espúrio antes de rodar. Os arquivos `.cmd` do projeto usam marcador sem acento por isso.

### 4.10 A política de execução do PowerShell bloqueia o instalador
Erro de segurança ao chamar `.ps1` diretamente. Resolvido com atalhos `.cmd` que invocam o PowerShell com `-ExecutionPolicy Bypass` — válido apenas para aquela execução, sem alterar configuração permanente da máquina.

### 4.11 O ambiente virtual versionado era inutilizável por terceiros
A intenção inicial era versionar tudo, inclusive o `.venv`, para reforçar o "hit and run". A inspeção mostrou o contrário: o `pyvenv.cfg` grava **caminhos absolutos da máquina de origem** (`home = C:\Python314`), e a pasta contém 16 executáveis e 14 bibliotecas compiladas só de Windows, sem o diretório `bin/` que o Linux usa. São 67 MB **inutilizáveis no Linux e quebrados em qualquer outra máquina Windows** — o oposto do objetivo. O instalador recria o ambiente correto para cada sistema em cerca de 30 segundos.
