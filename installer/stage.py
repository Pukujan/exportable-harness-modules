"""Stage the text-half UX pack into a throwaway directory.

Never writes ~/.config/kilo, ~/.grok, ~/.config/opencode, or a Kilo extension
dist unless the caller passes allow_live=True. This module never sets that flag.
"""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

from installer.pack_prompt import append_rules, pack_prompt

PRODUCTS = ("kilo", "opencode", "pi", "grok", "deepseek")

_KNOWN_GOOD_AGENTS = Path("adapters") / "kilo" / "known-good" / "AGENTS.md"
_AGENT_PROMPT = Path("adapters") / "kilo" / "known-good" / "agent-prompt.txt"
_CSS = Path("modules") / "prose-type" / "adapters" / "kilo" / "kilo-claude-markdown.css"

def _grok_frontmatter(name: str, description: str) -> str:
    return (
        "---\n"
        f"name: {name}\n"
        f"description: {description}\n"
        "prompt_mode: full\n"
        "model: inherit\n"
        "permission_mode: plan\n"
        "agents_md: false\n"
        "---\n"
    )


_GROK_FRONTMATTER = _grok_frontmatter(
    "ehm-chat",
    "Throwaway profile. Replaces the Grok prompt for a controlled score. Do not install this into the live Grok config.",
)
_GROK_OFF_FRONTMATTER = _grok_frontmatter(
    "ehm-off",
    "Control profile. Answer only. Do not install this into the live Grok config.",
)

_OPENCODE_JSONC = """{
  "$schema": "https://opencode.ai/config.json",
  "permission": "ask",
  "instructions": ["AGENTS.md"]
}
"""

_OFF_BODY = "Answer the user."


class LiveConfigRefused(SystemExit):
    """Dest is a live gold config and allow_live is false. Nothing was written."""


def repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def live_roots() -> list[Path]:
    home = Path.home()
    return [
        home / ".config" / "kilo",
        home / ".grok",
        home / ".config" / "opencode",
    ]


def _expand(dest: Path) -> Path:
    return Path(os.path.expanduser(str(dest)))


def _same_or_inside(path: Path, root: Path) -> bool:
    path_s = os.path.normcase(os.path.abspath(str(path)))
    root_s = os.path.normcase(os.path.abspath(str(root)))
    if path_s == root_s:
        return True
    prefix = root_s.rstrip("\\/") + os.sep
    return path_s.startswith(prefix)


def _is_extension_dist(path: Path) -> bool:
    """True for a Kilo extension dist path (contains extension and dist)."""
    parts = [part.casefold() for part in Path(path).parts]
    has_extension = any("extension" in part for part in parts)
    has_dist = any(part == "dist" for part in parts)
    return has_extension and has_dist


def is_live(dest: Path) -> bool:
    """True if dest is inside a live root, or is a Kilo extension dist path."""
    dest = _expand(dest)
    probes = [dest]
    try:
        probes.append(dest.resolve())
    except OSError:
        pass
    roots: list[Path] = []
    for root in live_roots():
        roots.append(root)
        try:
            roots.append(root.resolve())
        except OSError:
            pass
    for probe in probes:
        for root in roots:
            if _same_or_inside(probe, root):
                return True
        if _is_extension_dist(probe):
            return True
    return False


def _touches_live(dest: Path) -> bool:
    """True if dest or any product directory we would write is live."""
    dest = _expand(dest)
    targets = [dest, dest.resolve()]
    for name in PRODUCTS:
        child = dest / name
        targets.append(child)
        try:
            targets.append(child.resolve())
        except OSError:
            pass
    return any(is_live(target) for target in targets)


def _refuse(dest: Path) -> None:
    raise LiveConfigRefused(
        "refusing to stage into a live config: "
        f"{dest}. Nothing was written. "
        "Live roots are ~/.config/kilo, ~/.grok, and ~/.config/opencode, "
        "plus a Kilo extension dist path."
    )


def _guard(path: Path, allow_live: bool) -> None:
    if not allow_live and (is_live(path) or _touches_live(path)):
        _refuse(path)


def source_hash() -> str:
    """Stable sha256 of the bytes that get copied. No timestamps, no dest path."""
    root = repo_root()
    hasher = hashlib.sha256()

    def add(label: str, data: bytes) -> None:
        hasher.update(label.encode("utf-8"))
        hasher.update(b"\0")
        hasher.update(data)
        hasher.update(b"\0")

    for rel in (_KNOWN_GOOD_AGENTS, _AGENT_PROMPT, _CSS):
        add(rel.as_posix(), (root / rel).read_bytes())
    add("pack_prompt", pack_prompt().encode("utf-8"))
    add("kilo_agents", kilo_agents_text().encode("utf-8"))
    add("opencode.jsonc", _OPENCODE_JSONC.encode("utf-8"))
    add("grok_frontmatter", _GROK_FRONTMATTER.encode("utf-8"))
    add("grok_off_frontmatter", _GROK_OFF_FRONTMATTER.encode("utf-8"))
    add("off_body", _OFF_BODY.encode("utf-8"))
    add("pi_models", (root / "adapters" / "pi" / "models.json").read_bytes())
    return hasher.hexdigest()


def kilo_agents_text() -> str:
    raw = (repo_root() / _KNOWN_GOOD_AGENTS).read_text(encoding="utf-8")
    return append_rules(raw)


def _how_to(product: str, product_dir: Path) -> str:
    shown = str(product_dir)
    if product == "kilo":
        return (
            f"Copy AGENTS.md and agent-prompt.txt from {shown} into a new Kilo config, "
            "and kilo-claude-markdown.css only if that Kilo has a webview. "
            "Do not write ~/.config/kilo or the extension dist."
        )
    if product == "opencode":
        return (
            f'opencode run --dir "{shown}" --model yolo-auto/qwen3.8-flash --format json "<ask>". '
            "Do not edit ~/.config/opencode."
        )
    if product == "pi":
        return f'Set PI_CODING_AGENT_DIR to "{shown}". Do not write ~/.pi/agent/.'
    if product == "grok":
        profile = product_dir / "chat-profile.md"
        return (
            f'grok -p "<ask>" --agent "{profile}" --permission-mode plan. '
            "Do not write ~/.grok. off-profile.md is the control arm and must not be installed."
        )
    return (
        "DeepSeek binary was not hooked. "
        f"SYSTEM.md is staged at {shown} only. No live config was written."
    )


def _write_text(path: Path, text: str, allow_live: bool) -> None:
    _guard(path, allow_live)
    path.parent.mkdir(parents=True, exist_ok=True)
    _guard(path, allow_live)
    if not text.endswith("\n"):
        text += "\n"
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def _write_bytes(path: Path, data: bytes, allow_live: bool) -> None:
    _guard(path, allow_live)
    path.parent.mkdir(parents=True, exist_ok=True)
    _guard(path, allow_live)
    path.write_bytes(data)


def _write_json(path: Path, payload: dict, allow_live: bool) -> None:
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    _write_text(path, text, allow_live)


def _render_profile(body: str, frontmatter: str = _GROK_FRONTMATTER) -> str:
    return frontmatter + "\n" + body.strip("\n") + "\n"


def _receipt(product: str, digest: str, product_dir: Path, wrote_live: bool) -> dict:
    payload = {
        "hash": digest,
        "pack_hash": digest,
        "product": product,
        "live_configs_written": wrote_live,
        "how_to_point": _how_to(product, product_dir),
    }
    if product == "deepseek":
        payload["binary_hooked"] = False
        payload["receipt_line"] = "DeepSeek binary was not hooked."
    return payload


def stage(dest: Path, allow_live: bool = False) -> dict:
    """Write product dirs under dest. Refuses live roots unless allow_live is true.

    Never sets allow_live itself. Returns hash, dest, products, live_configs_written.
    """
    if allow_live is not False and allow_live is not True:
        raise TypeError("allow_live must be a bool")
    dest = _expand(Path(dest))
    if not dest.is_absolute():
        dest = (Path.cwd() / dest).resolve()
    else:
        dest = dest.resolve()

    if _touches_live(dest) and not allow_live:
        _refuse(dest)

    wrote_live = bool(allow_live and _touches_live(dest))
    digest = source_hash()
    root = repo_root()
    prompt = pack_prompt()
    agents = kilo_agents_text()

    kilo_dir = dest / "kilo"
    opencode_dir = dest / "opencode"
    pi_dir = dest / "pi"
    grok_dir = dest / "grok"
    deepseek_dir = dest / "deepseek"

    _write_text(kilo_dir / "AGENTS.md", agents, allow_live)
    _write_bytes(kilo_dir / "agent-prompt.txt", (root / _AGENT_PROMPT).read_bytes(), allow_live)
    _write_bytes(kilo_dir / "kilo-claude-markdown.css", (root / _CSS).read_bytes(), allow_live)

    _write_text(opencode_dir / "AGENTS.md", prompt, allow_live)
    _write_text(opencode_dir / "opencode.jsonc", _OPENCODE_JSONC, allow_live)

    _write_text(pi_dir / "SYSTEM.md", prompt, allow_live)
    _write_bytes(pi_dir / "models.json", (root / "adapters" / "pi" / "models.json").read_bytes(), allow_live)

    _write_text(grok_dir / "chat-profile.md", _render_profile(prompt), allow_live)
    _write_text(grok_dir / "off-profile.md", _render_profile(_OFF_BODY, _GROK_OFF_FRONTMATTER), allow_live)

    _write_text(deepseek_dir / "SYSTEM.md", prompt, allow_live)

    for name, product_dir in (
        ("kilo", kilo_dir),
        ("opencode", opencode_dir),
        ("pi", pi_dir),
        ("grok", grok_dir),
        ("deepseek", deepseek_dir),
    ):
        _write_json(
            product_dir / "receipt.json",
            _receipt(name, digest, product_dir, wrote_live),
            allow_live,
        )

    _write_json(
        dest / "receipt.json",
        {
            "hash": digest,
            "pack_hash": digest,
            "dest": str(dest),
            "products": list(PRODUCTS),
            "live_configs_written": wrote_live,
        },
        allow_live,
    )

    return {
        "hash": digest,
        "dest": str(dest),
        "products": list(PRODUCTS),
        "live_configs_written": wrote_live,
    }
