"""Stage the text-half UX pack. Default path refuses live gold configs.

Run from the repo root:

    python install.py install
    python install.py update
    python install.py check

Do not pass --i-understand-this-overwrites-a-live-config. That flag exists so a
deliberate overwrite is possible elsewhere. This entry point never sets it
unless the operator passes it on the command line.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from installer.stage import (  # noqa: E402
    LiveConfigRefused,
    is_live,
    repo_root,
    source_hash,
    stage,
)


def _default_dest() -> Path:
    return repo_root() / "dist" / "install"


def _add_dest_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--dest",
        type=Path,
        default=None,
        help="Stage directory. Default is <repo>/dist/install.",
    )
    parser.add_argument(
        "--into",
        type=Path,
        default=None,
        help="Destination override. Still refuses live roots unless the overwrite flag is also passed.",
    )
    parser.add_argument(
        "--i-understand-this-overwrites-a-live-config",
        action="store_true",
        help=(
            "Allow writing into a live gold config. Default refuses. "
            "Do not pass this on the machine that holds the working Kilo install."
        ),
    )


def _dest_from(args: argparse.Namespace) -> Path:
    if args.into is not None:
        return args.into
    if args.dest is not None:
        return args.dest
    return _default_dest()


def _allow_from(args: argparse.Namespace) -> bool:
    return bool(args.i_understand_this_overwrites_a_live_config)


def _print_result(result: dict) -> None:
    print(f"dest: {result['dest']}")
    print(f"hash: {result['hash']}")
    written = "true" if result["live_configs_written"] else "false"
    print(f"live_configs_written: {written}")


def _installed_hash(dest: Path) -> str | None:
    receipt = dest / "receipt.json"
    if not receipt.is_file():
        return None
    try:
        data = json.loads(receipt.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    value = data.get("hash", data.get("pack_hash"))
    return value if isinstance(value, str) else None


def cmd_install(args: argparse.Namespace) -> int:
    result = stage(_dest_from(args), allow_live=_allow_from(args))
    _print_result(result)
    return 0


def cmd_update(args: argparse.Namespace) -> int:
    dest = _dest_from(args)
    previous = _installed_hash(dest)
    current = source_hash()
    result = stage(dest, allow_live=_allow_from(args))
    _print_result(result)
    if previous is None:
        print("hash changed: no previous receipt")
    elif previous != current:
        print("hash changed")
    else:
        print("hash unchanged")
    return 0


def _fail(message: str) -> None:
    print(f"check failed: {message}", file=sys.stderr)
    raise SystemExit(1)


_LIVE_FILES = (
    "AGENTS.md",
    "kilo.json",
    "kilo.jsonc",
    "config.toml",
    "opencode.json",
    "opencode.jsonc",
)


def _snapshot(root: Path) -> dict[str, tuple[int, int] | None]:
    """Size and mtime of instruction files only. Does not read file bytes or log trees."""
    found: dict[str, tuple[int, int] | None] = {}
    if not root.is_dir():
        return found
    for name in _LIVE_FILES:
        path = root / name
        if path.is_file():
            stat = path.stat()
            found[name] = (stat.st_size, stat.st_mtime_ns)
        else:
            found[name] = None
    return found


def _live_unchanged(before: dict[Path, dict[str, tuple[int, int]]]) -> None:
    for root, snap in before.items():
        after = _snapshot(root)
        if after != snap:
            _fail(f"live config changed during check: {root}")


def _try_fixtures() -> None:
    """Score in-memory samples. Does not start the model loop."""
    try:
        from installer.corpus import asks
        from installer.score import score_reply
    except ImportError:
        print("note: installer.score and installer.corpus are not written yet; the loop worker owns them.")
        return
    items = asks()
    if len(items) != 50:
        _fail(f"local fixture: asks() returned {len(items)}, expected 50")
    kinds = {item.get("kind") for item in items}
    if kinds != {"chat", "code"}:
        _fail(f"local fixture: unexpected ask kinds {sorted(kinds)}")
    chat_pass = score_reply(
        "chat",
        "A short question does not need a summary block. **Answer first.**\n"
        "\n"
        "The second paragraph keeps the reply chunked, not mini.",
    )
    if chat_pass.get("pass") is not True:
        _fail(f"local fixture: chat sample should pass, got {chat_pass}")
    chat_miss = score_reply(
        "chat",
        "Printing TL;DR is the miss. **This is bold.**\n"
        "\n"
        "The second paragraph keeps the reply from being a single chunk.",
    )
    if chat_miss.get("pass") is not False:
        _fail("local fixture: a reply that prints the summary label should fail")
    code_pass = score_reply("code", "I would use a single line break.\n")
    if code_pass.get("pass") is not True:
        _fail(f"local fixture: code sample should pass, got {code_pass}")
    print("local fixture: score and corpus ok")


def _verify_stage(dest: Path) -> None:
    if is_live(dest):
        _fail(f"check dest is live and would be refused: {dest}")
    result = stage(dest, allow_live=False)
    if result["live_configs_written"] is not False:
        _fail("stage reported live_configs_written true")
    if result["hash"] != source_hash():
        _fail("stage hash does not match source_hash()")
    expected = {
        dest / "kilo" / "AGENTS.md",
        dest / "kilo" / "agent-prompt.txt",
        dest / "kilo" / "kilo-claude-markdown.css",
        dest / "kilo" / "receipt.json",
        dest / "opencode" / "AGENTS.md",
        dest / "opencode" / "opencode.jsonc",
        dest / "opencode" / "receipt.json",
        dest / "pi" / "SYSTEM.md",
        dest / "pi" / "receipt.json",
        dest / "grok" / "chat-profile.md",
        dest / "grok" / "off-profile.md",
        dest / "grok" / "receipt.json",
        dest / "deepseek" / "SYSTEM.md",
        dest / "deepseek" / "receipt.json",
        dest / "receipt.json",
    }
    missing = [str(path) for path in sorted(expected) if not path.is_file()]
    if missing:
        _fail("missing staged files: " + ", ".join(missing))
    if (dest / "kilo" / "kilo.jsonc").exists() or (dest / "kilo" / "kilo.json").exists():
        _fail("staged a fake kilo.jsonc")

    from installer.pack_prompt import PROVED_RULES

    agents = (dest / "kilo" / "AGENTS.md").read_text(encoding="utf-8")
    profile = (dest / "grok" / "chat-profile.md").read_text(encoding="utf-8")
    for rule in PROVED_RULES:
        if rule not in agents:
            _fail("kilo AGENTS.md is missing a proved rule")
        if rule not in profile:
            _fail("grok chat-profile.md is missing a proved rule")
    if "prompt_mode: full" not in profile or "agents_md: false" not in profile:
        _fail("grok chat-profile.md frontmatter is wrong")
    off = (dest / "grok" / "off-profile.md").read_text(encoding="utf-8")
    body = off.split("---", 2)[-1].strip()
    if body != "Answer the user.":
        _fail("off-profile.md body is not the control arm")
    opencode = (dest / "opencode" / "opencode.jsonc").read_text(encoding="utf-8")
    if '"instructions": ["AGENTS.md"]' not in opencode:
        _fail("opencode.jsonc is missing instructions")
    deepseek = json.loads((dest / "deepseek" / "receipt.json").read_text(encoding="utf-8"))
    blob = json.dumps(deepseek)
    if "not hooked" not in blob.lower() and "not hooked" not in deepseek.get("how_to_point", "").lower():
        _fail("deepseek receipt does not say the binary was not hooked")
    if deepseek.get("live_configs_written") is not False:
        _fail("deepseek receipt says live configs were written")
    top = json.loads((dest / "receipt.json").read_text(encoding="utf-8"))
    if top.get("hash") != result["hash"] or top.get("live_configs_written") is not False:
        _fail("top-level receipt.json does not match the stage result")


def _verify_refuse() -> None:
    probe = repo_root() / "dist" / "live-guard-probe" / "extensions" / "kilocode.kilo-code" / "dist"
    if not is_live(probe):
        _fail("is_live() did not treat an extension dist path as live")
    refused = False
    try:
        stage(probe, allow_live=False)
    except LiveConfigRefused:
        refused = True
    except SystemExit as exc:
        if exc.code in (0, None):
            _fail("stage() exited cleanly for a live extension dist path")
        refused = True
    if not refused:
        _fail("stage() did not refuse a live extension dist path")
    if probe.exists():
        _fail("stage() created a refused live extension dist path")

    home_kilo = Path.home() / ".config" / "kilo"
    if not is_live(home_kilo):
        _fail("is_live() is not true for Path.home()/'.config'/'kilo'")
    for root in (
        Path.home() / ".grok",
        Path.home() / ".config" / "opencode",
    ):
        if not is_live(root):
            _fail(f"is_live() is not true for {root}")
    if is_live(repo_root() / "dist" / "install"):
        _fail("default dest dist/install was treated as live")


def cmd_check(_args: argparse.Namespace) -> int:
    before = {
        root: _snapshot(root)
        for root in (
            Path.home() / ".config" / "kilo",
            Path.home() / ".grok",
            Path.home() / ".config" / "opencode",
        )
    }
    _verify_refuse()
    check_dest = repo_root() / "dist" / "install-check"
    _verify_stage(check_dest)
    _try_fixtures()
    _live_unchanged(before)
    print(f"check dest: {check_dest}")
    print(f"hash: {source_hash()}")
    print("is_live home/.config/kilo: true")
    print("live_configs_written: false")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="install.py")
    sub = parser.add_subparsers(dest="cmd", required=True)

    install = sub.add_parser("install", help="Stage the pack. Refuses live roots.")
    _add_dest_args(install)
    install.set_defaults(func=cmd_install)

    update = sub.add_parser("update", help="Restage and say whether the pack hash changed.")
    _add_dest_args(update)
    update.set_defaults(func=cmd_update)

    check = sub.add_parser("check", help="Verify staging and the live-config refusal.")
    check.set_defaults(func=cmd_check)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return int(args.func(args))
    except LiveConfigRefused as exc:
        print(exc, file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
