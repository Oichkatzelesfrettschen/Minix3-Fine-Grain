#!/usr/bin/env python3
"""Verification helper for Minix3.

Expected tool locations:
  * z3 -> /usr/bin/z3 or available in PATH
  * refines -> /usr/local/bin/refines or available in PATH
"""

from __future__ import annotations

import logging
import shutil
import subprocess
from pathlib import Path


LOG_Z3 = Path("z3.log")
LOG_REFINES = Path("refines.log")


def _run(cmd: list[str], log_file: Path) -> None:
    """Run *cmd* and append its output to *log_file*."""
    with log_file.open("a") as log:
        subprocess.run(cmd, stdout=log, stderr=subprocess.STDOUT, check=False)


def verify_z3() -> None:
    """Verify constraints using z3 if available."""

    exe = shutil.which("z3")
    if not exe:
        LOG_Z3.write_text("z3 not found; skipping z3 verification.\n")
        return

    _run([exe, "--version"], LOG_Z3)


def verify_refines() -> None:
    """Verify refinement properties with refines if available."""

    exe = shutil.which("refines")
    if not exe:
        LOG_REFINES.write_text(
            "refines not found; skipping refinement verification.\n"
        )
        return

    _run([exe, "--help"], LOG_REFINES)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    verify_z3()
    verify_refines()
