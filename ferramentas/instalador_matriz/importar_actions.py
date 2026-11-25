#!/usr/bin/env python3
# ! Alteração de IA - Revisar: arquivo novo (25/11/2026, pacote I7 do instalador único, decisão 153): traz o pacote de evidência
# que o GitHub Actions entrega (`celula-<id>.zip`, baixado da página da execução) para
# `Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/celulas/<id>/<data-hora>/`, depois de conferir cada rodada.
# ! Motivo: o resultado do fluxo só existe no GitHub; o relatório e a dispensa da tag nos arquivos de saída dependem de a rodada
# estar em `celulas/` no mesmo formato das outras. Conferir antes de copiar evita guardar evidência incompleta, sem a tag da
# decisão 147, ou com o `id` trocado (o que misturaria rodadas de máquinas diferentes).
"""Uso: python ferramentas/instalador_matriz/importar_actions.py <celula-ID.zip> [<outro.zip> ...]
Abre cada zip numa pasta temporária (sem executar nada dele), confere cada rodada e copia para `celulas/`. Recusa tudo o que
não estiver certo e não regrava uma rodada que já existe. Imprime o resumo de cada rodada importada."""
import argparse
import json
import re
import shutil
import sys
import tempfile
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(RAIZ))
sys.path.insert(0, str(Path(__file__).resolve().parent))

import install  # noqa: E402
import ler_celula  # noqa: E402
from celula_actions import CELULAS_DO_ACTIONS  # noqa: E402

FORMATO_DA_PASTA = re.compile(r"^\d{8}-\d{6}$")
# ! Alteração de IA - Revisar: limite de 200 MB para a soma dos tamanhos descompactados de um pacote.
# ! Motivo: a evidência de uma célula são logs e JSON (alguns MB); um zip que se expande a gigabytes é arquivo errado ou malicioso e encheria o disco antes de qualquer conferência.
LIMITE_DESCOMPACTADO = 200 * 1024 * 1024


# ! Alteração de IA - Revisar: função nova `rodadas_do_pacote`: acha as pastas de rodada (as que têm `celula.json`) dentro do pacote já aberto.
# ! Motivo: o zip do GitHub tem `<id>/<data-hora>/celula.json` na raiz, mas um pacote mexido à mão pode ter outro nível; achar pelo `celula.json` evita depender da profundidade.
def rodadas_do_pacote(pasta: Path) -> list[Path]:
    """As pastas que têm `celula.json`, em ordem."""
    return sorted(p.parent for p in pasta.rglob("celula.json"))


# ! Alteração de IA - Revisar: função nova `conferir_rodada`: devolve os motivos para recusar uma rodada (vazio se está certa).
# ! Motivo: a rodada precisa ter a tag e o motivo no `celula.json` (decisão 147: é ela que cobre os logs capturados), o `id` igual ao nome da pasta de cima (senão a rodada entraria na célula errada) e o nome `AAAAMMDD-HHMMSS` (o leitor `ler_celula.pasta_mais_recente` ordena por esse nome).
def conferir_rodada(pasta: Path) -> list[str]:
    """Os motivos para recusar a rodada; lista vazia se está certa."""
    motivos = []
    arquivo = pasta / "celula.json"
    if not arquivo.exists():
        return [f"{pasta.name}: não há celula.json"]
    rotulo = f"{pasta.parent.name}/{pasta.name}"
    if not arquivo.is_file():
        return [f"{rotulo}: celula.json não é um arquivo"]
    try:
        texto = arquivo.read_text(encoding="utf-8-sig", errors="replace")
    except OSError as e:
        return [f"{rotulo}: não foi possível ler o celula.json ({e})"]
    if "de IA - Revisar" not in texto or "! Motivo" not in texto:
        motivos.append(f"{rotulo}: o celula.json não tem a tag e o motivo (de IA - Revisar e ! Motivo)")
    try:
        dados = json.loads(texto)
    except ValueError:
        motivos.append(f"{rotulo}: o celula.json não é JSON válido")
        dados = None
    if dados is not None and not isinstance(dados, dict):
        motivos.append(f"{rotulo}: o celula.json não é um objeto JSON")
        dados = None
    if dados is not None:
        ident = dados.get("id")
        if "actions" not in dados:
            motivos.append(f"{rotulo}: o celula.json não tem a chave actions (só rodada do GitHub Actions entra por aqui)")
        if ident not in CELULAS_DO_ACTIONS:
            motivos.append(f"{rotulo}: o id {ident} não é uma célula do fluxo ({', '.join(CELULAS_DO_ACTIONS)})")
        if ident is not None and ident != pasta.parent.name:
            motivos.append(f"{pasta.name}: o id do celula.json ({ident}) é diferente do nome da pasta de cima ({pasta.parent.name})")
    if not FORMATO_DA_PASTA.match(pasta.name):
        motivos.append(f"{pasta.parent.name}/{pasta.name}: o nome da pasta da rodada não tem o formato AAAAMMDD-HHMMSS")
    return motivos


# ! Alteração de IA - Revisar: função nova `importar`: abre o zip (ou lê a pasta), confere todas as rodadas e só então copia.
# ! Motivo: se uma rodada de um pacote com várias estiver errada, nenhuma é gravada pela metade; a extração usa `install.extrair_zip_seguro`, que recusa nome de arquivo que saia da pasta temporária (o zip é arquivo baixado, nada dele é executado).
# ! Alteração de IA - Revisar: `importar` passa a (1) transformar qualquer falha de abrir ou extrair o zip em recusa com o motivo, (2) recusar zip cujo tamanho descompactado passe de `limite_descompactado` antes de extrair e (3) apagar as rodadas já copiadas se a cópia de uma delas falhar.
# ! Motivo: zip corrompido, com método de compressão que o Python não lê ou sem permissão no disco estourava com traceback em vez de dizer qual pacote está ruim; um zip enorme encheria o disco antes da conferência; e uma cópia que parasse no meio de um pacote com várias rodadas deixava rodadas soltas em `celulas/`, e a regravação seria depois recusada como "já existe".
def importar(zip_ou_pasta: Path, celulas: Path, limite_descompactado: int = LIMITE_DESCOMPACTADO) -> list[Path]:
    """Copia as rodadas do pacote para `celulas/<id>/<data-hora>/` e devolve as pastas gravadas. Levanta `ValueError` com o
    motivo se alguma rodada não está certa ou já existe no destino (nesse caso nada é gravado)."""
    zip_ou_pasta = Path(zip_ou_pasta)
    temporaria = Path(tempfile.mkdtemp(prefix="cobaia_actions_"))
    try:
        if zip_ou_pasta.is_dir():
            origem = zip_ou_pasta
        else:
            try:
                with zipfile.ZipFile(zip_ou_pasta) as z:
                    total = sum(item.file_size for item in z.infolist())
                if total > limite_descompactado:
                    raise ValueError(f"{zip_ou_pasta.name}: o pacote descompactado é grande demais ({total} bytes; o limite é "
                                     f"{limite_descompactado}); a evidência são logs e JSON")
                install.extrair_zip_seguro(zip_ou_pasta, temporaria)
            except (zipfile.BadZipFile, NotImplementedError, RuntimeError, OSError) as e:
                raise ValueError(f"{zip_ou_pasta.name} não é um zip que se possa abrir e extrair ({type(e).__name__}): {e}")
            origem = temporaria
        rodadas = rodadas_do_pacote(origem)
        if not rodadas:
            raise ValueError(f"{zip_ou_pasta.name}: não há celula.json em nenhuma pasta do pacote")
        motivos = []
        for rodada in rodadas:
            motivos.extend(conferir_rodada(rodada))
            destino = celulas / rodada.parent.name / rodada.name
            if destino.exists():
                motivos.append(f"{rodada.parent.name}/{rodada.name}: a rodada já existe em {destino} (evidência não se regrava)")
        if motivos:
            raise ValueError("; ".join(motivos))
        gravadas = []
        try:
            for rodada in rodadas:
                destino = celulas / rodada.parent.name / rodada.name
                destino.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(rodada, destino)
                gravadas.append(destino)
        except (OSError, shutil.Error) as e:
            for pasta in gravadas:
                shutil.rmtree(pasta, ignore_errors=True)
            raise ValueError(f"{zip_ou_pasta.name}: a cópia de uma rodada falhou ({e}); as {len(gravadas)} rodada(s) já copiadas "
                             "nesta chamada foram removidas")
        return gravadas
    finally:
        shutil.rmtree(temporaria, ignore_errors=True)


# ! Alteração de IA - Revisar: função nova `main`: importa cada zip da linha de comando e imprime o resumo de cada rodada gravada.
# ! Motivo: depois de baixar os quatro pacotes do GitHub, um comando só os traz e já mostra o que cada célula alcançou, sem abrir os logs.
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pacotes", nargs="+", type=Path, help="zip baixado da página da execução, ou pasta já extraída")
    args = ap.parse_args(argv)
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    codigo = 0
    for pacote in args.pacotes:
        try:
            gravadas = importar(pacote, ler_celula.CELULAS)
        except ValueError as e:
            print(f"RECUSADO {pacote}: {e}", file=sys.stderr)
            codigo = 1
            continue
        for pasta in gravadas:
            print(ler_celula.em_texto(ler_celula.resumir(pasta)))
    return codigo


if __name__ == "__main__":
    sys.exit(main())
