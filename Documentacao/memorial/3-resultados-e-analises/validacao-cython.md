<!-- ! Alteração de IA - Revisar: arquivo criado ao separar o Memorial de Desenvolvimento
     por tópicos (Documentacao/memorial/).
     ! Motivo: o memorial único passou de 400 linhas misturando decisões, achados, pesquisa e
     referências; separado por tema, cada assunto é revisável sozinho e o índice mostra onde
     está cada coisa. Conteúdo MOVIDO sem reescrita; a numeração das seções é a do memorial
     original porque o próprio texto se refere a ela ("ver 4.12", "decisão 19"). -->
# Validação da hipótese de uso de Cython

Parte do [Memorial de Desenvolvimento](../../Memorial%20de%20Desenvolvimento.md) — sumário e demais tópicos lá.

## 7. Validação da hipótese de uso de Cython

**A premissa não se confirmou.** Verificação no repositório: nenhum arquivo `.pyx` ou `.pxd`, nenhuma chamada a `cythonize`, nenhum `import cython`, e o Cython sequer está instalado no ambiente. **Não há código Cython nosso no projeto.**

O que existe são **extensões compiladas de dependências de terceiros**, distribuídas já prontas: `httptools` (essa sim, gerada com Cython), `pydantic_core` e `watchfiles` (Rust), além de `greenlet`, `sqlalchemy`, `websockets` e `yaml` (C). São binários que já vêm compilados na instalação — não são código que escrevemos nem que compilamos.

### Medição

Para responder se compilar nosso código traria ganho, mediu-se a decomposição do tempo de uma inferência real de diagnóstico (`qwen2.5-coder:3b`, média de 3 execuções):

| Componente | Tempo | Fração |
|---|---|---|
| Inferência dentro do Ollama | 7,680 s | 79,07% |
| Transporte HTTP e espera de I/O | 2,033 s | 20,93% |
| **Nosso código Python** (serializar/desserializar JSON) | **0,000263 s** | **0,0027%** |
| **Total** | **9,713 s** | 100% |

**Teto de ganho se o nosso código Python fosse infinitamente rápido: 0,0027%.**

### Conclusão

O tempo do projeto é dominado por inferência do modelo (código C++ do llama.cpp, dentro do Ollama) e por espera de entrada e saída — nenhum dos dois acelerável por Cython. O código Python do projeto é orquestração: chama subprocessos, monta requisições e lê respostas.

Há ainda um conflito direto com a regra de projeto do "hit and run": **Cython exige um compilador C na máquina de destino** (MSVC no Windows, gcc no Linux). Foi exatamente por esse motivo que se escolheu `PyMySQL` em vez de `mysqlclient` — decisão já registrada no `requirements.txt`. Adotar Cython reintroduziria a dependência de toolchain que se decidiu evitar, e complicaria o empacotamento do `Cobaia.exe`.

**Recomendação: não adotar.** O ganho máximo teórico é de três milésimos de por cento, contra um custo real em portabilidade e em complexidade de instalação.

**Único ponto onde valeria reavaliar:** a poda da árvore de acessibilidade (Fase 4), que é o primeiro trecho do projeto a fazer trabalho de CPU não trivial em Python. O critério objetivo para reabrir a discussão: se a poda passar a consumir **mais de 5% do tempo total de um ciclo de diagnóstico**, medido com perfilador. Abaixo disso, não se justifica.


