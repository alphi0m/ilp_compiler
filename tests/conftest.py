import subprocess
import sys
from pathlib import Path

import pytest

RADICE = Path(__file__).parent.parent
sys.path.insert(0, str(RADICE / "src"))
MAIN = RADICE / "src" / "main.py"


@pytest.fixture
def esegui_file(tmp_path):
    def _esegui(percorso, input_testo=""):
        return subprocess.run(
            [sys.executable, str(MAIN), str(percorso),
             "-o", str(tmp_path / "uscita.ll"), "--run"],
            input=input_testo,
            capture_output=True,
            text=True,
        )

    return _esegui


@pytest.fixture
def esegui(tmp_path, esegui_file):
    def _esegui(sorgente, input_testo=""):
        file = tmp_path / "programma.al"
        file.write_text(sorgente, encoding="utf-8")
        return esegui_file(file, input_testo)

    return _esegui
