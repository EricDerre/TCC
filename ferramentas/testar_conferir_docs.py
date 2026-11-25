# ! Alteração de IA - Revisar: arquivo novo (18/11/2026) com os testes da dispensa de tag para a saída capturada de uma célula de teste do
# instalador em `conferir_docs.py`, escritos antes do código: quais arquivos de uma pasta de rodada ficam cobertos pelo `celula.json` e quais
# continuam cobrados.
# ! Motivo: a primeira célula do WSL (L-U2404, rodada 20261118-193340) gravou 23 arquivos `.txt` de saída capturada em
# `Documentacao/memorial/5-metodo-e-ferramental/dados/instalador/celulas/`, e `conferir_docs.py` passou a terminar em `RESULTADO: 23 problema(s)`
# (`sem tag de IA`) para todas as sessões do projeto. Pôr a tag dentro desses arquivos mudaria a evidência; o Eric decidiu em 18/11/2026 que a
# saída capturada fica coberta pela tag do `celula.json` da pasta. Sem teste, a dispensa poderia engolir arquivo que deve continuar cobrado.
"""Testes de conferir_docs.py. Uso: python ferramentas/testar_conferir_docs.py"""
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import conferir_docs as cd

CELULA_COM_TAG = ('{"tag_ia": {"alteracao": "! Alteração de IA - Revisar: arquivo gerado pelo roteiro da célula", '
                  '"motivo": "! Motivo: a evidência de cada célula fica em arquivo"}, "id": "L-U2404"}')


class TesteEvidenciaDeCelula(unittest.TestCase):
    def setUp(self):
        self.raiz = Path(tempfile.mkdtemp(prefix="conferir_docs_"))
        self.rodada = (self.raiz / "Documentacao" / "memorial" / "5-metodo-e-ferramental" / "dados" / "instalador" / "celulas"
                       / "L-U2404" / "20261118-193340")
        (self.rodada / "suspeitas").mkdir(parents=True)

    def tearDown(self):
        shutil.rmtree(self.raiz, ignore_errors=True)

    def _grava(self, relativo: str, texto: str = "saida capturada\n") -> Path:
        caminho = self.rodada / relativo
        caminho.write_text(texto, encoding="utf-8")
        return caminho

    def teste_saida_capturada_fica_coberta_pelo_celula_json(self):
        self._grava("celula.json", CELULA_COM_TAG)
        capturados = [self._grava("os-release.txt"), self._grava("saida_preparo.txt", "0\n"), self._grava("suspeitas/HL1.txt")]
        for arquivo in capturados:
            self.assertTrue(cd.evidencia_de_celula(arquivo), arquivo.name)
        self.assertEqual(cd.conferir_tags(capturados), [])

    def teste_celula_json_e_registro_json_continuam_cobrados(self):
        manifesto = self._grava("celula.json", CELULA_COM_TAG)
        self.assertFalse(cd.evidencia_de_celula(manifesto))
        self.assertFalse(cd.evidencia_de_celula(self._grava("registro.json", "{}")))

    def teste_sem_celula_json_com_tag_nada_e_dispensado(self):
        arquivo = self._grava("os-release.txt")
        self.assertFalse(cd.evidencia_de_celula(arquivo), "sem celula.json na pasta da rodada")
        self._grava("celula.json", '{"id": "L-U2404"}')
        self.assertFalse(cd.evidencia_de_celula(arquivo), "celula.json sem a tag")

    def teste_fora_de_uma_pasta_de_rodada_nada_muda(self):
        outra = self.raiz / "Documentacao" / "memorial" / "celulas" / "x" / "y"
        outra.mkdir(parents=True)
        (outra / "celula.json").write_text(CELULA_COM_TAG, encoding="utf-8")
        solto = outra / "nota.txt"
        solto.write_text("x\n", encoding="utf-8")
        self.assertFalse(cd.evidencia_de_celula(solto), "pasta `celulas` que não é a do instalador")
        self._grava("celula.json", CELULA_COM_TAG)
        acima = self.rodada.parent / "leia.txt"
        acima.write_text("x\n", encoding="utf-8")
        self.assertFalse(cd.evidencia_de_celula(acima), "arquivo em celulas/<id>/, fora de uma rodada")


if __name__ == "__main__":
    unittest.main()
