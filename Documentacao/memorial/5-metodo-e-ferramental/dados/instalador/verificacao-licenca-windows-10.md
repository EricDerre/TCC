<!-- ! Alteração de IA - Revisar: arquivo novo (18/11/2026) com a verificação, em fonte da Microsoft, de como se consegue um Windows 10 para teste em máquina virtual e do que a licença permite sem ativação.
     ! Motivo: na ficha 82 de `pendencias.md` o Eric respondeu que a ISO oficial do Windows 10 continua disponível e pediu para verificar se dá para testar "sem a licença, em modo de teste ou de avaliação"; a decisão 142 depende dessas respostas, e a regra do projeto é não escrever fato sem origem. Cada linha abaixo traz a URL e a data de acesso; as citações são curtas e literais. -->
# Windows 10 para teste em máquina virtual: o que existe e o que a licença permite

Verificação feita em 18/11/2026, só de leitura, pelo Claude, na sessão do teste dos instaladores. Complementa a seção 2 de [`pesquisa-windows.md`](pesquisa-windows.md).

## 1. A ISO oficial existe

A página "Baixar o Windows 10" da Microsoft continua no ar e oferece a ferramenta de criação de mídia, com o botão "Baixar agora"; a ferramenta gera o arquivo ISO. A mesma página diz, em português: "Para começar, primeiro você precisará ter uma licença para instalar o Windows 10."

Fonte: https://www.microsoft.com/pt-br/software-download/windows10 (acesso em 18/11/2026).

## 2. A versão de avaliação do Windows 10 não existe mais

O endereço da avaliação do Windows 10 Enterprise no Centro de Avaliação responde com um redirecionamento permanente (301) para um texto do blog do Windows sobre o fim do suporte. A página inicial do Centro de Avaliação lista, de sistemas para computador de mesa, só o Windows 11 Enterprise, o Windows 11 IoT Enterprise LTSC e o kit de laboratório do Windows 11; nenhuma edição do Windows 10.

Fontes: https://www.microsoft.com/en-us/evalcenter/evaluate-windows-10-enterprise (redireciona para https://blogs.windows.com/windowsexperience/2024/10/31/how-to-prepare-for-windows-10-end-of-support-by-moving-to-windows-11-today/) e https://www.microsoft.com/en-us/evalcenter/ (acesso em 18/11/2026).

## 3. O que os termos de licença do Windows 10 dizem

Documento: "Microsoft Software License Terms, Windows Operating System", versão de varejo do Windows 10, com a indicação "Last updated June 2018". O texto foi extraído do PDF oficial com o PyMuPDF.

- Seção 2 (direitos de instalação e uso): a licença dá o direito de instalar e rodar uma instância do sistema em um dispositivo; "dispositivo" é um sistema físico ou virtual; para usar o sistema em mais de um dispositivo virtual é preciso uma licença separada para cada instância.
- Seção 5 (software autorizado e ativação): o uso só é autorizado se a pessoa estiver "properly licensed and the software has been properly activated"; a mesma seção proíbe contornar a ativação.
- Seção 14, item d (ii) (avaliação): trata do software fornecido como versão de avaliação, de teste ou de demonstração, que não pode ser usado em ambiente de produção nem depois do período de avaliação. Não cobre uma instalação comum feita sem chave.

Fonte: https://www.microsoft.com/content/dam/microsoft/usetm/documents/windows/10/retail-packaged/UseTerms_Retail_Windows_10_English.pdf (acesso em 18/11/2026).

## 4. O que acontece num Windows sem ativação

A instalação aceita seguir sem chave, e o sistema roda com a marca "Ativar o Windows" na tela e com a personalização bloqueada. Isso vem de respostas no fórum de perguntas da Microsoft e de guias de terceiros; não foi encontrada página oficial que descreva esse uso como um modo permitido. A página de suporte "Ativar o Windows" diz que a ativação liga a chave ou a licença digital ao equipamento e que, sem uma das duas, não dá para ativar.

Fontes: https://support.microsoft.com/en-us/windows/activate-windows-c39005d4-95ee-b91e-b399-2820fda32227 e https://learn.microsoft.com/en-gb/answers/questions/5674262/how-to-get-rid-of-activate-windows-watermark-on-sc (acesso em 18/11/2026; a segunda é fórum, não documentação).

## 5. O que a Microsoft ainda deixa avaliar sem licença

- Windows 11 Enterprise, 90 dias (seção 2 de `pesquisa-windows.md`).
- Windows Server 2016, 2019, 2022 e 2025. Para o Windows Server 2022, a página diz que a edição de avaliação expira em 180 dias, que há ISO e VHD de 64 bits nas edições Standard e Datacenter, que pede um registro antes do download e que a avaliação precisa ser ativada pela internet nos primeiros 10 dias para não desligar sozinha. Os requisitos de memória e de disco não estão na página.

Fontes: https://www.microsoft.com/en-us/evalcenter/ e https://www.microsoft.com/en-us/evalcenter/evaluate-windows-server-2022 (acesso em 18/11/2026).

## Conclusão

Um Windows 10 sem ativação numa máquina virtual funciona, mas não é um uso que os termos de licença autorizam, e a versão de avaliação que cobriria o teste deixou de ser oferecida. Os caminhos legítimos para o Windows 10 são uma licença própria ou uma máquina que já tenha o Windows 10 licenciado. O sistema limpo mais próximo que a Microsoft ainda deixa avaliar é o Windows Server 2022, que é da mesma geração do Windows 10 e está na lista de sistemas suportados pelo Playwright (Windows Server 2019 em diante, seção 5 de `pesquisa-windows.md`); ele não é o Windows 10 de mesa, e o relatório do teste tem de dizer isso.

## O que não foi confirmado

- O tamanho da ISO do Windows 10 e o da ISO do Windows Server 2022.
- Se o Microsoft Defender vem ligado no Windows Server 2022 de avaliação; o teste registra o que encontrar.
- Texto oficial da Microsoft sobre as limitações de um Windows não ativado (só fórum e terceiros).
