<!-- ! Alteração de IA - Revisar: arquivo novo (30/09/2026) com a política de segurança do repositório: o que é inseguro de propósito no ambiente-alvo, o que conta como vulnerabilidade de verdade e como relatar em sigilo.
     ! Motivo: a lista de padrões de comunidade do GitHub marcava "Security policy" como pendente; sem este texto, alguém poderia abrir uma issue pública sobre a injeção de SQL do CobaiaFront, que é intencional, ou expor um defeito real dos instaladores antes de haver correção. -->
# Política de segurança

## O que é inseguro de propósito

Os dois sistemas em `Programacao/` são um **ambiente de teste** ("cobaia"), feito para ser alvo de um agente de QA. Os problemas abaixo são conhecidos, intencionais e **não devem ser relatados como vulnerabilidade**:

- **CobaiaFront** (site PHP legado, mantido intocado): consultas SQL sem preparação, senhas de usuário sem hash, credencial SMTP no código-fonte, sessão e validações frágeis.
- **CobaiaAPI** (FastAPI): CORS liberado para qualquer origem, token administrativo simples lido do `.env`, e um mecanismo de injeção de falhas que altera as respostas de propósito.
- **Contas de teste** com senhas triviais no `seed.sql`.

Por isso, rode os dois sistemas só em `localhost`, nunca os exponha à internet nem os use com dados reais, e não reutilize esses padrões em outro projeto.

## O que conta como vulnerabilidade

Relate, por favor, qualquer problema que possa afetar a máquina de quem usa o repositório ou a integridade do trabalho:

- instaladores (`install.*`, `Cobaia.exe`, `build_exe.ps1`) baixando ou executando algo que não deveriam, ou de fonte não confiável;
- scripts de `ferramentas/` ou de `experimentos/` que escrevam fora das pastas previstas ou apaguem dados;
- segredos reais commitados por engano (chaves, senhas de contas em uso, tokens);
- dependências com vulnerabilidade conhecida nos `requirements*.txt`.

## Como relatar

Use o canal privado do GitHub: na página do repositório, aba **Security**, opção **Report a vulnerability**. Não abra uma issue pública para isso. Descreva o que encontrou, como reproduzir e o impacto que enxerga.

O grupo responde em até sete dias e combina com quem relatou o momento de tornar o problema público, depois da correção.

## Versões cobertas

Só o ramo `main` recebe correções. Os registros de resultado em `resultados_alvo/` são históricos e não mudam.
