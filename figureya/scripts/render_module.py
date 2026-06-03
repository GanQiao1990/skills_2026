#!/usr/bin/env python3

import argparse
import subprocess
from pathlib import Path

DEFAULT_FIGUREYA_ROOT = "/home/qiao/dockerai/FigureYa"
FILELIST_NAME = "filelist.txt"

_OUTPUT_FORMAT_MAP = {
    "html": "html_document",
    "pdf": "pdf_document",
}


def _pick_rmd_from_filelist(figureya_root: Path, module_dir: Path) -> Path | None:
    filelist_path = figureya_root / FILELIST_NAME
    if not filelist_path.exists():
        return None

    module_name = module_dir.name
    try:
        for raw_line in filelist_path.read_text(encoding="utf-8", errors="ignore").splitlines():
            line = raw_line.strip()
            if not line or "/" not in line:
                continue
            folder, rel_rmd = line.split("/", 1)
            if folder != module_name:
                continue
            candidate = figureya_root / folder / rel_rmd
            if candidate.exists():
                return candidate
    except OSError:
        return None

    return None


def _pick_rmd(figureya_root: Path, module_dir: Path, rmd_name: str | None) -> Path:
    if rmd_name:
        rmd = module_dir / rmd_name
        if not rmd.exists():
            raise FileNotFoundError(f"Rmd not found: {rmd}")
        return rmd

    routed_rmd = _pick_rmd_from_filelist(figureya_root, module_dir)
    if routed_rmd is not None:
        return routed_rmd

    # Support both .Rmd and .rmd extensions
    rmds = sorted(module_dir.glob("*.Rmd")) + sorted(module_dir.glob("*.rmd"))
    if not rmds:
        raise FileNotFoundError(f"No .Rmd or .rmd found in module directory: {module_dir}")
    return sorted(rmds, key=lambda p: (p.suffix.lower() != ".rmd", p.name))[0]


def _run(cmd: list[str], cwd: Path) -> None:
    proc = subprocess.run(cmd, cwd=str(cwd))
    if proc.returncode != 0:
        raise RuntimeError(f"Command failed with exit code {proc.returncode}: {' '.join(cmd)}")


def render_module(
    figureya_root: Path,
    module: str,
    fmt: str,
    output_dir: Path,
    rmd: str | None,
    run_install_deps: bool,
) -> None:
    module_dir = (figureya_root / module).resolve()
    if not module_dir.exists() or not module_dir.is_dir():
        raise FileNotFoundError(f"Module directory not found: {module_dir}")

    output_dir = output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    if run_install_deps:
        install_script = module_dir / "install_dependencies.R"
        if install_script.exists():
            _run(["Rscript", str(install_script)], cwd=module_dir)

    rmd_path = _pick_rmd(figureya_root, module_dir, rmd)

    if fmt not in _OUTPUT_FORMAT_MAP:
        raise ValueError(f"Unsupported --format '{fmt}'. Use one of: {', '.join(sorted(_OUTPUT_FORMAT_MAP))}")

    r_output_format = _OUTPUT_FORMAT_MAP[fmt]

    output_dir_str = str(output_dir).replace("\\", "/")

    r_expr_parts = [
        "rmarkdown::render(",
        f"input='{rmd_path.name}', ",
        f"output_format='{r_output_format}', ",
        f"output_dir='{output_dir_str}', ",
        "quiet=FALSE)",
    ]
    r_expr = "".join(r_expr_parts)

    _run(["Rscript", "-e", r_expr], cwd=module_dir)


def main() -> None:
    p = argparse.ArgumentParser(description="Render a FigureYa module .Rmd to HTML/PDF")
    p.add_argument("--figureya-root", default=DEFAULT_FIGUREYA_ROOT, help="Path to FigureYa repository root")
    p.add_argument("--module", required=True, help="Module folder name, e.g. FigureYa101PCA")
    p.add_argument("--format", default="html", choices=sorted(_OUTPUT_FORMAT_MAP.keys()))
    p.add_argument("--output-dir", required=True, help="Directory to write rendered outputs")
    p.add_argument("--rmd", default=None, help="Optional specific .Rmd filename inside module")
    p.add_argument("--no-install-deps", action="store_true", help="Skip running install_dependencies.R")
    args = p.parse_args()

    render_module(
        figureya_root=Path(args.figureya_root).expanduser().resolve(),
        module=args.module,
        fmt=args.format,
        output_dir=Path(args.output_dir),
        rmd=args.rmd,
        run_install_deps=(not args.no_install_deps),
    )


if __name__ == "__main__":
    main()
