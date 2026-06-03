#!/usr/bin/env python3

import argparse
from pathlib import Path

DEFAULT_FIGUREYA_ROOT = "/home/qiao/dockerai/FigureYa"


def iter_module_dirs(figureya_root: Path):
    for child in sorted(figureya_root.iterdir()):
        if not child.is_dir():
            continue
        if child.name.startswith("."):
            continue
        yield child


def module_has_rmd(module_dir: Path) -> bool:
    # Support both .Rmd and .rmd extensions
    return any(module_dir.glob("*.Rmd")) or any(module_dir.glob("*.rmd"))


def search_modules(figureya_root: Path, query: str, search_rmd: bool) -> list[str]:
    if not figureya_root.exists() or not figureya_root.is_dir():
        raise FileNotFoundError(f"FigureYa root not found or not a directory: {figureya_root}")

    q = query.lower()
    matches: list[str] = []

    for module_dir in iter_module_dirs(figureya_root):
        if not module_has_rmd(module_dir):
            continue

        name_hit = q in module_dir.name.lower()
        content_hit = False

        if (not name_hit) and search_rmd:
            # Search both .Rmd and .rmd files
            for rmd in list(module_dir.glob("*.Rmd")) + list(module_dir.glob("*.rmd")):
                try:
                    txt = rmd.read_text(encoding="utf-8", errors="ignore").lower()
                except OSError:
                    continue
                if q in txt:
                    content_hit = True
                    break

        if name_hit or content_hit:
            matches.append(module_dir.name)

    return matches


def main() -> None:
    p = argparse.ArgumentParser(description="Search FigureYa modules by name and optionally by .Rmd contents")
    p.add_argument("--figureya-root", default=DEFAULT_FIGUREYA_ROOT, help="Path to FigureYa repository root")
    p.add_argument("--query", required=True, help="Keyword to search")
    p.add_argument("--search-rmd", action="store_true", help="Also search inside .Rmd files")
    args = p.parse_args()

    root = Path(args.figureya_root).expanduser().resolve()
    for m in search_modules(root, args.query, args.search_rmd):
        print(m)


if __name__ == "__main__":
    main()
