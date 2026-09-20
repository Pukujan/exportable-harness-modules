"""Red tests for the writing contract. Fail until goldens and the fragment hold."""

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from checkers.writing import run


def test_writing_contract() -> None:
    assert run() == 0
