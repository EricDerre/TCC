#!/usr/bin/env python3
# ! Alteração de IA - Revisar: as três estratégias de prompt comparadas no experimento.
# ! Motivo: o A/B de dois braços que estava planejado confundia duas coisas — o efeito da
# ESTRUTURA em estágios e o efeito dos NOMES dados a esses estágios. O trabalho PA-Tool
# (ACL 2026) mediu +17 pontos no Qwen2.5-3B só por alinhar nomes ao que o modelo viu no
# pré-treino; "análise léxica" carrega prior forte de tokenizar código-fonte, que é tarefa
# diferente de comparar payload HTTP. Com três braços, B contra C isola o efeito do nome.
#
# Decisões de formato, todas vindas da pesquisa:
#  - Uma única chamada por caso, nunca cadeia: em n estágios encadeados a confiabilidade é
#    p^n (com 6 estágios e p=0,85 dá ~38%), e em CPU cada chamada repaga o prefill.
#  - O raciocínio vem ANTES da resposta final. O estudo da Appier atribui parte da queda em
#    saída estruturada justamente a inverter essa ordem.
#  - Raciocínio livre, restrição só no rótulo final ("reason free, constrain late"): o
#    Constraint Tax mediu validade subindo de 61,5% para 100% enquanto a acurácia caía de
#    19,7% para 11,0% quando se restringe a saída inteira.
from taxonomia import CAUSAS_RAIZ

_LISTA_CAUSAS = "\n".join(f"  - {c}" for c in CAUSAS_RAIZ)

_FORMATO = f"""Depois do raciocínio, termine com estas três linhas, exatamente neste formato:
CAUSA_RAIZ: <um valor da lista abaixo, escrito igual>
CAMPO: <nome do campo afetado, ou "nenhum">
IMPACTO: <uma frase sobre o que o usuário vê>

Valores permitidos para CAUSA_RAIZ:
{_LISTA_CAUSAS}"""


def _dados_do_caso(caso: dict) -> str:
    e = caso["entrada"]
    linhas = [f"REQUISIÇÃO: {e.get('requisicao', '(não informada)')}"]
    if e.get("status") is not None:
        linhas.append(f"STATUS HTTP: {e['status']}")
    if e.get("contrato") and e["contrato"] != "n/a":
        linhas.append(f"CONTRATO ESPERADO PELA INTERFACE: {e['contrato']}")
    if e.get("corpo") is not None:
        linhas.append(f"CORPO DA RESPOSTA:\n{e['corpo']}")
    if e.get("arvore"):
        linhas.append(f"ÁRVORE DE ACESSIBILIDADE DA PÁGINA:\n{e['arvore']}")
    if e.get("seletor_quebrado"):
        linhas.append(f"SELETOR QUE FALHOU: {e['seletor_quebrado']}")
    linhas.append(f"SINTOMA OBSERVADO: {e.get('sintoma', '(não informado)')}")
    if e.get("observacao"):
        linhas.append(f"OBSERVAÇÃO ADICIONAL: {e['observacao']}")
    return "\n\n".join(linhas)


def linear(caso: dict) -> str:
    """Braço A — pergunta direta, sem estrutura de estágios imposta."""
    return f"""Você analisa falhas de integração entre uma interface web e sua API.

Leia os dados abaixo, explique em no máximo 3 frases o que deu errado, e então responda no formato pedido.

{_dados_do_caso(caso)}

{_FORMATO}"""


def estagiada_compilador(caso: dict) -> str:
    """Braço B — estágios nomeados pelas fases de um compilador (a hipótese a testar)."""
    return f"""Você analisa falhas de integração entre uma interface web e sua API, percorrendo
as mesmas fases de um compilador antes de concluir.

Percorra, brevemente, nesta ordem:
1. ANÁLISE LÉXICA: a resposta é legível? Está completa e no formato declarado?
2. ANÁLISE SINTÁTICA: a estrutura bate com a esperada? Há campo ausente, renomeado ou aninhado de forma diferente?
3. ANÁLISE SEMÂNTICA: os tipos e os valores fazem sentido? Há tipo trocado ou valor fora do domínio?
4. GERAÇÃO INTERMEDIÁRIA: o mapeamento entre as camadas está correto? Há escala, unidade ou chave de junção errada?
5. OTIMIZAÇÃO: há problema de tempo, de repetição ou de dado desatualizado?
6. GERAÇÃO DE CÓDIGO OBJETO: o que o usuário vê na tela corresponde ao dado recebido?

{_dados_do_caso(caso)}

{_FORMATO}"""


def estagiada_dominio(caso: dict) -> str:
    """Braço C — mesma estrutura do braço B, com nomes do domínio HTTP/API."""
    return f"""Você analisa falhas de integração entre uma interface web e sua API, verificando
uma coisa de cada vez antes de concluir.

Verifique, brevemente, nesta ordem:
1. LEITURA DA RESPOSTA: o corpo é legível, completo e no formato declarado?
2. CAMPOS PRESENTES: falta algum campo do contrato? Algum veio com outro nome ou outra forma?
3. TIPOS E VALORES: algum campo veio com tipo diferente ou com valor fora do domínio permitido?
4. TRADUÇÃO ENTRE CAMADAS: escala, unidade, data ou chave de ligação entre entidades estão corretas?
5. TEMPO E REPETIÇÃO: houve demora, limite de requisições, dado desatualizado ou registro duplicado?
6. RESULTADO NA TELA: o que o usuário vê corresponde ao dado que chegou?

{_dados_do_caso(caso)}

{_FORMATO}"""


_FORMATO_COM_FONTE = _FORMATO.replace(
    "termine com estas três linhas", "termine com estas quatro linhas"
).replace(
    "IMPACTO: <uma frase sobre o que o usuário vê>",
    "IMPACTO: <uma frase sobre o que o usuário vê>\n"
    'FONTE: <identificadores da documentação que usou, entre colchetes, ou "nenhum">',
)


def linear_com_biblioteca(caso: dict, contexto: str) -> str:
    """! Alteração de IA - Revisar: o prompt linear da Fase 2-A precedido pela documentação
    do sistema, com uma quarta linha de saída (FONTE) para o modelo citar o verbete usado.
    ! Motivo: a Fase 2-A mostrou que linear vence as estratégias em estágios (37,4% contra
    29,7% e 31,1%), então a Fase 2-B fixa esse prompt e varia só a biblioteca. A
    documentação vem ANTES do caso por duas razões medidas na literatura (Memorial §6.3):
    o começo do contexto é uma das duas posições em que modelos pequenos ainda acham a
    informação (Lost in the Middle), e prefixo idêntico entre chamadas é o único arranjo
    em que o cache de KV do Ollama pode reaproveitar o prefill. A linha FONTE é o que
    permite medir ancoragem — se a resposta se apoiou de fato no verbete recebido."""
    return f"""{contexto}

=====

Você analisa falhas de integração entre uma interface web e sua API.

Leia os dados abaixo, consulte a documentação acima quando ajudar, explique em no máximo 3 frases o que deu errado, e então responda no formato pedido.

{_dados_do_caso(caso)}

{_FORMATO_COM_FONTE}"""


# ! Alteração de IA - Revisar: nova constante de módulo com o texto fixo do segundo prompt
# da Fase 3 (bloco de correção do caso + instruções de proposta de edição), usada por
# proposta_de_edicao logo abaixo.
# ! Motivo: evolucao_biblioteca.parsear_propostas espera exatamente este formato de bloco
# (CAMPOS_PROPOSTA lista os mesmos nomes de campo -- OPERACAO, VERBETE, TRECHO, TITULO,
# SISTEMA, ENTIDADE, CAUSAS, ARQUIVOS, PALAVRAS_CHAVE, SINTOMAS, TEXTO, MOTIVO); manter o
# texto como constante, fora da função, é o que deixa claro que só os sete valores
# passados a .format() variam por caso -- o restante do texto é fixo, palavra por palavra.
_FORMATO_PROPOSTA = """=====

CORREÇÃO DESTE CASO
CAUSA_RAIZ CORRETA: {causa_correta}
CAMPO AFETADO: {campo_afetado}
SEU DIAGNÓSTICO: {causa_respondida} — {veredito}

VERBETE DEDICADO A ESSA CAUSA (pode não ter aparecido antes):
{verbete_ouro_renderizado}

Agora você pode melhorar a documentação para que um PRÓXIMO caso parecido — não este — seja diagnosticado certo. Regras:
- A documentação nunca é apagada nem reescrita: você só ACRESCENTA. "nota" acrescenta uma observação a um verbete; "retificacao" acrescenta uma correção apontando o trecho errado; "novo_verbete" cria um verbete novo.
- Escreva sobre o sistema e o tipo de falha, em termos gerais. Não copie o sintoma, a observação nem o corpo deste caso; não cite o identificador do caso.
- No MOTIVO, diga com suas palavras qual evidência do caso mostrou a lacuna.
- Só cite arquivos, endpoints e tabelas que apareçam na documentação acima.
- Só use como VERBETE os identificadores que apareceram acima entre colchetes: {ids_visiveis}.
- TEXTO com 60 a 280 caracteres, uma ou duas frases, sem lista. MOTIVO com 20 a 240 caracteres.
- No máximo 2 propostas. Se a documentação já bastava, responda só a palavra: NENHUMA

Formato, exatamente assim, um bloco por proposta:

PROPOSTA 1
OPERACAO: nota | retificacao | novo_verbete
VERBETE: <id entre colchetes; em novo_verbete, um id novo em minusculas-com-hifens>
TRECHO: <so em retificacao: trecho curto do verbete que esta errado, copiado igual>
TITULO: <so em novo_verbete>
SISTEMA: <so em novo_verbete: CobaiaFront | CobaiaAPI | Infraestrutura | Ambos>
ENTIDADE: <so em novo_verbete: Produto | Tipo | Usuario | Pedido | Interface | Infraestrutura>
CAUSAS: <so em novo_verbete: 1 a 3 valores de CAUSA_RAIZ separados por virgula>
ARQUIVOS: <opcional: caminhos citados na documentacao acima, ou "nenhum">
PALAVRAS_CHAVE: <ate 5 termos novos separados por virgula, ou "nenhuma">
SINTOMAS: <ate 3 sintomas novos separados por virgula, ou "nenhum">
TEXTO: <o que acrescentar>
MOTIVO: <por que isso faria o proximo diagnostico acertar, e qual evidencia deste caso mostrou a lacuna>
FIM

Valores permitidos para CAUSAS:
{lista_causas}"""


def proposta_de_edicao(prompt_diagnostico: str, resposta_diagnostico: str, caso: dict,
                       acertou: bool, causa_respondida: str | None,
                       verbete_ouro_renderizado: str, ids_visiveis: list[str]) -> str:
    """! Alteração de IA - Revisar: segundo prompt da Fase 3 (aprendizado) -- devolve a
    CONTINUAÇÃO LITERAL do prompt de diagnóstico (prompt_diagnostico) mais a resposta que
    o modelo deu (resposta_diagnostico), seguida do bloco de correção do caso e das
    instruções de proposta de edição (_FORMATO_PROPOSTA).
    ! Motivo: nos 54 casos de aprendizado, mandar os dois prompts como mensagens separadas
    ou reescrever qualquer trecho do primeiro invalidaria o cache de prefixo do Ollama --
    só um prefixo byte a byte idêntico entre as duas chamadas reaproveita o prefill
    (achado 4.21 do Memorial: a bateria em CPU nesta máquina fica em ~60h com o cache,
    contra ~75h sem ele)."""
    gabarito = caso["gabarito"]
    campo_afetado = gabarito["campo_afetado"] or "nenhum"
    causa_respondida_txt = causa_respondida or "(sem CAUSA_RAIZ)"
    veredito = "correto" if acertou else "incorreto"
    ids_visiveis_txt = ", ".join(f"[{i}]" for i in ids_visiveis)
    correcao_e_instrucoes = _FORMATO_PROPOSTA.format(
        causa_correta=gabarito["causa_raiz"], campo_afetado=campo_afetado,
        causa_respondida=causa_respondida_txt, veredito=veredito,
        verbete_ouro_renderizado=verbete_ouro_renderizado,
        ids_visiveis=ids_visiveis_txt, lista_causas=_LISTA_CAUSAS)
    return f"{prompt_diagnostico}\n\n{resposta_diagnostico}\n\n{correcao_e_instrucoes}"


ESTRATEGIAS = {
    "linear": linear,
    "compilador": estagiada_compilador,
    "dominio": estagiada_dominio,
}
