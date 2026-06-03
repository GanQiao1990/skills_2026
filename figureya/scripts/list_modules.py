#!/usr/bin/env python3

import argparse
from pathlib import Path

DEFAULT_FIGUREYA_ROOT = "/home/qiao/dockerai/FigureYa"


def _has_rmd(module_dir: Path) -> bool:
    return any(module_dir.glob("*.Rmd")) or any(module_dir.glob("*.rmd"))


def list_modules(figureya_root: Path) -> list[str]:
    if not figureya_root.exists() or not figureya_root.is_dir():
        raise FileNotFoundError(f"FigureYa root not found or not a directory: {figureya_root}")

    modules: list[str] = []
    for child in sorted(figureya_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        if _has_rmd(child):
            modules.append(child.name)
    return modules


def main() -> None:
    p = argparse.ArgumentParser(description="List FigureYa module directories containing at least one .Rmd")
    p.add_argument("--figureya-root", default=DEFAULT_FIGUREYA_ROOT, help="Path to FigureYa repository root")
    args = p.parse_args()

    root = Path(args.figureya_root).expanduser().resolve()
    for m in list_modules(root):
        print(m)


if __name__ == "__main__":
    main()
