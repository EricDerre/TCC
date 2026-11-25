#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, pacote I5 do instalador único, decisões 138 e 153): roda uma célula de
# teste do instalador num executor do GitHub Actions (grava o que a máquina já traz, roda o instalador como o README manda,
# roda a prova da instalação) e deixa a evidência numa pasta de rodada, com o `celula.json` e um resumo na página da execução.
# ! Motivo: o instalador nunca rodou em macOS nem em Windows recém-criado, e o Eric decidiu em 25/11/2026 que a prova em
# máquina nova, antes da entrega, é a das máquinas do GitHub. Sem um roteiro só para os três sistemas, cada tarefa do fluxo
# teria os passos escritos em YAML, sem teste, e a evidência de cada sistema sairia num formato diferente.
"""Uso, num executor do GitHub Actions, na raiz do repositório:
  python ferramentas/instalador_matriz/celula_actions.py --id M-15 --modo novo --ate N3 --saida "$RUNNER_TEMP/celulas" [--forcar-uv]
Grava <saida>/<id>/<data-hora>/ (celula.json, estado_inicial.txt, instalacao.log, conferir.log, registro.json, passos.json).
Sai com 0 se a prova não falhou e nenhuma versão impede; senão 1. Só biblioteca padrão; roda com o Python 3.9 ou mais novo."""
from __future__ import annotations

import argparse
import json
import os
import platform
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
# ! Alteração de IA - Revisar: os limites de tempo do instalador e da prova passam a 3600 s cada (antes 5400 e 7200) e entra `CELULAS_DO_ACTIONS`, a lista das quatro células do fluxo.
# ! Motivo: 5400 + 7200 s davam 210 min, mais que os 150 min (`timeout-minutes`) do `instalador.yml`; se o instalador demorasse, o GitHub cortava a tarefa antes de o `celula.json` ser gravado e a rodada ficava sem evidência. Somando 120 min, a prova sempre termina antes do corte. A lista de células existe aqui para o `importar_actions.py` recusar pacote de outra célula.
LIMITE_DO_INSTALADOR_S = 3600
LIMITE_DA_PROVA_S = 3600
CELULAS_DO_ACTIONS = ("CI-UBU", "CI-WIN", "M-15", "M-15I")
# O que a máquina já traz antes do instalador: os executores do GitHub não são máquinas limpas (vêm com Python, PHP, banco).
SONDAS_DO_ESTADO = {
    "python3": ["python3", "--version"], "python": ["python", "--version"], "py (Windows)": ["py", "-0p"],
    "php": ["php", "-v"], "php, extensões": ["php", "-m"], "mysql": ["mysql", "--version"], "mariadb": ["mariadb", "--version"],
    "brew": ["brew", "--version"], "winget": ["winget", "--version"], "ollama": ["ollama", "--version"],
    "curl": ["curl", "--version"], "sudo sem senha": ["sudo", "-n", "true"],
}


# ! Alteração de IA - Revisar: função nova `carimbo`: o nome da pasta da rodada (data e hora), no formato das outras células.
# ! Motivo: `importar_actions.py` e o leitor das rodadas esperam o nome AAAAMMDD-HHMMSS; montar o nome num lugar só evita pastas fora do padrão.
def carimbo(agora: datetime) -> str:
    """O nome da pasta da rodada, no formato das outras células: 20261126-120000."""
    return agora.strftime("%Y%m%d-%H%M%S")


# ! Alteração de IA - Revisar: função nova `_gravar`: grava texto em UTF-8 com fim de linha do Linux.
# ! Motivo: no executor do Windows o texto ganharia `\r\n` e o `Path.write_text(newline=...)` só existe do Python 3.10 em diante; o executor pode trazer o 3.9.
def _gravar(caminho: Path, texto: str) -> None:
    """Grava em UTF-8 com fim de linha do Linux. (O `newline` de `Path.write_text` só existe do Python 3.10 em diante, e o
    executor do Windows pode trazer o 3.9.)"""
    with open(caminho, "w", encoding="utf-8", newline="\n") as arquivo:
        arquivo.write(texto)


# ! Alteração de IA - Revisar: função nova `comando_do_instalador`: o comando que o README manda rodar em cada sistema.
# ! Motivo: a célula tem de instalar do mesmo jeito que uma pessoa instalaria, e não por um caminho só dela.
def comando_do_instalador(sistema: str) -> list[str]:
    """O que o README manda rodar: `install.cmd` no Windows, `./install.sh` no Linux e no macOS."""
    return ["cmd", "/c", "install.cmd"] if sistema == "Windows" else ["./install.sh"]


# ! Alteração de IA - Revisar: função nova `ambiente_do_instalador`: as variáveis que respondem às perguntas do instalador.
# ! Motivo: no executor ninguém digita; sem COBAIA_ROOT_SEM_SENHA (troca da entrada do root do MariaDB) e COBAIA_MARIADB_PORTATIL (baixar o zip do MariaDB) o instalador pararia esperando resposta até o limite de tempo.
# ! Alteração de IA - Revisar: nos três sistemas entram PYTHONIOENCODING=utf-8, PYTHONUTF8=1 e PYTHONUNBUFFERED=1 no ambiente do instalador.
# ! Motivo: no executor do Windows o Python escreve na codepage do sistema (acento do `instalacao.log` virava lixo, ou erro de codificação ao imprimir) e junta a saída em buffer, então um corte pelo tempo perdia o fim do log. Com UTF-8 e sem buffer o log sai legível e completo.
def ambiente_do_instalador(sistema: str, forcar_uv: bool, base: dict) -> dict:
    """As variáveis que respondem às perguntas do instalador, porque no executor não há ninguém para responder."""
    ambiente = dict(base)
    ambiente.update(PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONUNBUFFERED="1")
    if sistema == "Windows":
        ambiente["COBAIA_MARIADB_PORTATIL"] = "1"     # baixa o zip do MariaDB sem a pergunta "Baixar ...? [s/N]"
    else:
        ambiente["COBAIA_ROOT_SEM_SENHA"] = "1"       # aceita a troca da entrada do root do MariaDB sem a pergunta
        if forcar_uv:
            ambiente["COBAIA_FORCAR_UV"] = "1"        # o lançador ignora o Python do executor e traz o dele pelo uv
    return ambiente


# ! Alteração de IA - Revisar: função nova `ambiente_da_prova`: o ambiente de `python -m instalador.conferir`, com as três variáveis de UTF-8 e sem buffer.
# ! Motivo: a prova rodava com o ambiente do executor puro; no Windows o `conferir.log` saía na codepage do sistema e com a saída presa em buffer, como o `instalacao.log` antes do conserto.
def ambiente_da_prova(base: dict) -> dict:
    """O ambiente da prova: o do executor, mais as variáveis que põem a saída em UTF-8 e sem atraso."""
    ambiente = dict(base)
    ambiente.update(PYTHONIOENCODING="utf-8", PYTHONUTF8="1", PYTHONUNBUFFERED="1")
    return ambiente


# ! Alteração de IA - Revisar: função nova `python_da_prova`: escolhe o Python que roda `instalador.conferir`.
# ! Motivo: quando o lançador traz o Python pelo `uv` (pasta `.ferramentas/python`), a prova tem de usar o mesmo, e não o do executor, que pode ser de outra versão.
def python_da_prova(raiz: Path, sistema: str) -> str:
    """O Python com que a prova roda: o que o lançador trouxe pelo uv, se trouxe; senão o do sistema."""
    if sistema != "Windows":
        trazidos = sorted(raiz.glob(".ferramentas/python/*/bin/python3"))
        if trazidos:
            return str(trazidos[0])
        return "python3"
    return "python"


# ! Alteração de IA - Revisar: função nova `comando_da_prova`: monta o comando de `python -m instalador.conferir` da célula.
# ! Motivo: o comando precisa ser conferido por teste sem rodar a prova de verdade (que instala e sobe serviços).
def comando_da_prova(python: str, ident: str, saida: Path, ate: str, modelo: str) -> list[str]:
    return [python, "-m", "instalador.conferir", "--celula", ident, "--saida", str(saida), "--ate", ate, "--modelo-pequeno", modelo]


# ! Alteração de IA - Revisar: função nova `rodar_com_log`: roda um comando na raiz do repositório, com a entrada fechada e a saída num arquivo.
# ! Motivo: sem a entrada fechada uma pergunta inesperada do instalador travaria a execução até o limite do GitHub; sem o limite de tempo e o código 124 ou 127 a falha ficaria sem explicação no log.
def rodar_com_log(comando: list[str], log: Path, ambiente: dict, limite_s: int) -> int:
    """Roda na raiz do repositório, com a entrada fechada e a saída no arquivo. Devolve o código de saída; 124 se o tempo
    esgotou e 127 se o comando não pôde ser rodado, com o motivo no fim do log."""
    with open(log, "wb") as arquivo:
        try:
            return subprocess.run(comando, cwd=str(RAIZ), env=ambiente, stdin=subprocess.DEVNULL, stdout=arquivo,
                                  stderr=subprocess.STDOUT, timeout=limite_s, check=False).returncode
        except subprocess.TimeoutExpired:
            arquivo.write(f"\n[celula_actions] tempo esgotado depois de {limite_s} s\n".encode("utf-8"))
            return 124
        except OSError as e:
            arquivo.write(f"\n[celula_actions] não foi possível rodar {comando}: {e}\n".encode("utf-8"))
            return 127


# ! Alteração de IA - Revisar: função nova `estado_inicial`: grava o que a máquina já tinha instalado antes do instalador.
# ! Motivo: os executores do GitHub já trazem Python, PHP e banco; sem este registro o relatório diria "instalou" sem dizer se o instalador fez o trabalho ou se a ferramenta já estava lá.
def estado_inicial() -> str:
    """A saída de cada sonda de SONDAS_DO_ESTADO (as três primeiras linhas), ou 'ausente' quando o comando não existe."""
    linhas = [f"plataforma: {platform.platform()}", f"processador: {platform.machine()}", f"núcleos: {os.cpu_count()}", ""]
    for nome, comando in SONDAS_DO_ESTADO.items():
        if not shutil.which(comando[0]):
            linhas.append(f"== {nome}: ausente")
            continue
        try:
            r = subprocess.run(comando, stdin=subprocess.DEVNULL, capture_output=True, timeout=60, check=False)
            texto = (r.stdout + r.stderr).decode("utf-8", errors="replace").strip().splitlines()
            limite = 40 if "extens" in nome else 3
            linhas.append(f"== {nome}: código {r.returncode}, em {shutil.which(comando[0])}")
            linhas.extend("   " + linha for linha in texto[:limite])
        except (OSError, subprocess.TimeoutExpired) as e:
            linhas.append(f"== {nome}: não rodou ({e})")
    return "\n".join(linhas) + "\n"


# ! Alteração de IA - Revisar: função nova `montar_celula`: monta o dicionário do `celula.json` (id, até onde, máquina, commit do GitHub, códigos de saída).
# ! Motivo: a decisão 147 só dispensa da tag os arquivos de saída de uma pasta de rodada que tenha `celula.json` com a tag; e o relatório precisa saber de que commit e de que imagem de máquina veio cada rodada.
# ! Alteração de IA - Revisar: `montar_celula` ganha `modo` (vem do fluxo), `terminou` (False no `celula.json` gravado no começo, True no do fim), `resultado_do_instalador` (a chave `resultado` do `passos.json`) e grava também `fuso`.
# ! Motivo: o modo estava fixo em "novo" (a rodada de Windows e macOS, que ainda usa os passos antigos, ficaria mal rotulada); sem `terminou` uma tarefa cortada pelo GitHub não deixava como saber que a célula não chegou ao fim; o código de saída do `install.cmd` no Windows não é o do instalador (o `install.ps1` não o repassa), então vale o `resultado` do `passos.json`; as horas do `celula.json` são em UTC e o arquivo passa a dizer isso.
def montar_celula(ident: str, ate: str, modelo: str, forcar_uv: bool, inicio: datetime, fim: datetime, saidas: dict,
                  ambiente: dict, modo: str, terminou: bool, resultado_do_instalador: str = "") -> dict:
    """O `celula.json`: o que a célula rodou, em que máquina e a partir de que commit."""
    sistema, arquitetura = ambiente.get("RUNNER_OS", ""), ambiente.get("RUNNER_ARCH", "")
    if sistema:
        imagem = f"GitHub Actions: {sistema} {arquitetura}, imagem {ambiente.get('ImageOS', '?')} {ambiente.get('ImageVersion', '?')}"
    else:
        imagem = "GitHub Actions: sistema e imagem não informados"
    return {
        "tag_ia": {
            "alteracao": "! Alteração de IA - Revisar: arquivo gerado por ferramentas/instalador_matriz/celula_actions.py: o que a "
                         "célula rodou num executor do GitHub Actions e com que código de saída.",
            "motivo": "! Motivo: o plano do instalador único (decisão 143) pede a evidência de cada célula em arquivo, e a pasta "
                      "da rodada só fica dispensada da tag nos arquivos de saída capturada se tiver este arquivo (decisão 147).",
        },
        "id": ident, "modo": modo, "ate": ate, "modelo_pequeno": modelo, "forcar_uv": forcar_uv, "imagem": imagem,
        "terminou": terminou, "fuso": "UTC", "resultado_do_instalador": resultado_do_instalador,
        "actions": {"repositorio": ambiente.get("GITHUB_REPOSITORY", ""), "commit": ambiente.get("GITHUB_SHA", ""),
                    "execucao": ambiente.get("GITHUB_RUN_ID", ""), "tentativa": ambiente.get("GITHUB_RUN_ATTEMPT", ""),
                    "evento": ambiente.get("GITHUB_EVENT_NAME", "")},
        "inicio": inicio.strftime("%Y-%m-%dT%H:%M:%S"), "fim": fim.strftime("%Y-%m-%dT%H:%M:%S"),
        "saidas": {nome: str(codigo) for nome, codigo in saidas.items()},
    }


# ! Alteração de IA - Revisar: função nova `veredito`: 0 se a prova gravou o registro e nada falhou nem foi impedido por versão; senão 1.
# ! Motivo: o código de saída do instalador sozinho não diz se a instalação ficou de pé; quem diz é o `registro.json` da prova. Nível `nao_coube` (3,1 GB livres para o modelo, por exemplo) não é falha da instalação.
def veredito(registro: dict | None) -> int:
    """0 se a prova gravou o registro, nenhum nível falhou e nenhuma versão impede; senão 1."""
    if not registro:
        return 1
    return 1 if registro.get("falhou") or registro.get("impedida_por_versao") else 0


# ! Alteração de IA - Revisar: função nova `_fim_do_log`: devolve as últimas 60 linhas de um log (ou "(arquivo não gravado)").
# ! Motivo: o resumo da página da execução mostra só o fim de `instalacao.log` e `conferir.log`; ler o arquivo inteiro encheria a página, e um log que não foi gravado não pode derrubar o resumo.
def _fim_do_log(caminho: Path, linhas: int = 60) -> str:
    if not caminho.exists():
        return "(arquivo não gravado)"
    return "\n".join(caminho.read_text(encoding="utf-8", errors="replace").splitlines()[-linhas:])


# ! Alteração de IA - Revisar: função nova `resumo_em_markdown`: o texto que aparece na página da execução do GitHub (níveis, versões e o fim dos dois logs).
# ! Motivo: sem o resumo, ver o resultado de uma célula exigiria baixar o pacote e abrir os logs; a página da execução mostra de cara até onde a instalação chegou.
def resumo_em_markdown(celula: dict, registro: dict | None, fim_instalacao: str, fim_prova: str) -> str:
    """O resumo que aparece na página da execução: níveis, versões e o fim dos dois logs."""
    partes = [f"## Célula {celula['id']}", "", f"- Máquina: {celula['imagem']}",
              f"- Prova pedida até o nível {celula['ate']}", f"- Códigos de saída: {json.dumps(celula['saidas'], ensure_ascii=False)}"]
    if celula.get("resultado_do_instalador"):
        partes.append(f"- Resultado gravado pelo instalador: {celula['resultado_do_instalador']}")
    partes.append("")
    if registro:
        partes += [f"Nível alcançado: **{registro.get('alcancado', '?')}**. Falhou: {registro.get('falhou')}. "
                   f"Versões que impedem: {registro.get('impedida_por_versao') or 'nenhuma'}.", "",
                   "| Nível | Estado | Segundos | Detalhe |", "|---|---|---|---|"]
        for nivel, dados in registro.get("niveis", {}).items():
            detalhe = " ".join(str(dados.get("detalhe", "")).split())[:300].replace("|", "/")
            partes.append(f"| {nivel} | {dados.get('estado')} | {dados.get('segundos')} | {detalhe} |")
        partes += ["", "| Ferramenta | Encontrada | Testada | Estado |", "|---|---|---|---|"]
        for nome, dados in registro.get("versoes", {}).items():
            partes.append(f"| {nome} | {dados.get('encontrada')} | {dados.get('testada')} | {dados.get('estado')} |")
    else:
        partes.append("**a prova não gravou o registro** (`registro.json`): veja o fim do log da prova, abaixo.")
    partes += ["", "<details><summary>Fim do log do instalador</summary>", "", "```", fim_instalacao, "```", "</details>", "",
               "<details><summary>Fim do log da prova</summary>", "", "```", fim_prova, "```", "</details>", ""]
    return "\n".join(partes)


# ! Alteração de IA - Revisar: função nova `main`: a ordem da célula (estado inicial, instalador, prova, passos.json, celula.json, resumo, código de saída).
# ! Motivo: a prova roda mesmo quando o instalador sai com erro, porque é ela que diz até onde a instalação chegou; o `celula.json` é gravado por último para registrar os dois códigos de saída.
# ! Alteração de IA - Revisar: o `main` passa a (1) trocar a saída padrão por UTF-8, (2) gravar o `celula.json` logo depois de criar a pasta, com `terminou` falso, e regravá-lo no fim com `terminou` verdadeiro, (3) exigir `--modo` (`como-esta` ou `novo`) e (4) ler o `resultado` do `passos.json`.
# ! Motivo: se o GitHub cortasse a tarefa no meio, a pasta subia sem `celula.json` e o importador a recusava, sem prova de que a célula não terminou; o modo da rodada vem do fluxo porque o Windows e o macOS ainda rodam o instalador antigo; e no Windows o código de saída do `install.cmd` não é o do instalador, então o resultado que vale é o gravado no `passos.json`.
def main(argv: list[str] | None = None) -> int:
    for fluxo in (sys.stdout, sys.stderr):
        try:
            fluxo.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--id", required=True)
    ap.add_argument("--modo", required=True, choices=("como-esta", "novo"))
    ap.add_argument("--ate", choices=("N1", "N2", "N3", "N4"), default="N3")
    ap.add_argument("--saida", required=True, type=Path)
    ap.add_argument("--modelo-pequeno", default="qwen2.5:0.5b-instruct")
    ap.add_argument("--forcar-uv", action="store_true")
    args = ap.parse_args(argv)
    sistema = platform.system()
    inicio = datetime.now(timezone.utc).replace(tzinfo=None)
    pasta = args.saida / args.id / carimbo(inicio)
    pasta.mkdir(parents=True, exist_ok=True)
    _gravar(pasta / "celula.json", json.dumps(
        montar_celula(args.id, args.ate, args.modelo_pequeno, args.forcar_uv, inicio, inicio, {}, dict(os.environ),
                      modo=args.modo, terminou=False), ensure_ascii=False, indent=1) + "\n")
    _gravar(pasta / "estado_inicial.txt", estado_inicial())
    saidas = {}
    saidas["instalador"] = rodar_com_log(comando_do_instalador(sistema), pasta / "instalacao.log",
                                         ambiente_do_instalador(sistema, args.forcar_uv, dict(os.environ)), LIMITE_DO_INSTALADOR_S)
    print(f"[celula {args.id}] instalador saiu com {saidas['instalador']}", flush=True)
    prova = comando_da_prova(python_da_prova(RAIZ, sistema), args.id, pasta, args.ate, args.modelo_pequeno)
    saidas["conferir"] = rodar_com_log(prova, pasta / "conferir.log", ambiente_da_prova(dict(os.environ)), LIMITE_DA_PROVA_S)
    print(f"[celula {args.id}] prova saiu com {saidas['conferir']}", flush=True)
    passos = RAIZ / ".ferramentas" / "instalacao" / "passos.json"
    resultado_do_instalador = ""
    if passos.exists():
        shutil.copyfile(passos, pasta / "passos.json")
        try:
            dados_dos_passos = json.loads(passos.read_text(encoding="utf-8-sig"))
            if isinstance(dados_dos_passos, dict):
                resultado_do_instalador = str(dados_dos_passos.get("resultado", ""))
        except ValueError:
            resultado_do_instalador = ""
    registro = None
    if (pasta / "registro.json").exists():
        try:
            registro = json.loads((pasta / "registro.json").read_text(encoding="utf-8"))
        except ValueError:
            registro = None
    celula = montar_celula(args.id, args.ate, args.modelo_pequeno, args.forcar_uv, inicio,
                           datetime.now(timezone.utc).replace(tzinfo=None), saidas, dict(os.environ), modo=args.modo,
                           terminou=True, resultado_do_instalador=resultado_do_instalador)
    _gravar(pasta / "celula.json", json.dumps(celula, ensure_ascii=False, indent=1) + "\n")
    resumo = resumo_em_markdown(celula, registro, _fim_do_log(pasta / "instalacao.log"), _fim_do_log(pasta / "conferir.log"))
    destino = os.environ.get("GITHUB_STEP_SUMMARY")
    if destino:
        with open(destino, "a", encoding="utf-8") as arquivo:
            arquivo.write(resumo + "\n")
    print(resumo, flush=True)
    return veredito(registro)


if __name__ == "__main__":
    sys.exit(main())
