import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from checkers.hot_reload import run


def test_hot_reload_gate() -> None:
    assert run() == 0
