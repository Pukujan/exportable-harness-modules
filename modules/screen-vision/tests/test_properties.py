import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
from checkers.vision import run


def test_vision_properties() -> None:
    assert run() == 0
