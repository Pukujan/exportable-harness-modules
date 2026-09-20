import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from checkers.tokens import run


def test_tokens() -> None:
    assert run() == 0
