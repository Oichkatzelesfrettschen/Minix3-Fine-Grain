#!/usr/bin/env python3
"""Utilities for verifying Minix3 locking algorithms using TLA+ and CSP."""

from __future__ import annotations


import shutil
import subprocess
from pathlib import Path
from typing import Tuple


class FormalVerificationPipeline:
    """Automate generation and checking of lock specifications."""

    def __init__(self, project_dir: str) -> None:
        self.project_dir = Path(project_dir)
        self.tla_dir = self.project_dir / "formal_specs" / "tla"
        self.csp_dir = self.project_dir / "formal_specs" / "csp"
        self.results_dir = self.project_dir / "verification_results"

        # Create directories if they do not exist.
        for directory in (self.tla_dir, self.csp_dir, self.results_dir):
            directory.mkdir(parents=True, exist_ok=True)

    def generate_tla_spec(self, lock_type: str) -> Path:
        """Write a TLA+ specification for *lock_type* and return the path."""
        template = r"""
---- MODULE {lock_type}Lock ----
EXTENDS Integers, TLC

CONSTANTS NumProcs
ASSUME NumProcs \in Nat /\ NumProcs > 0

VARIABLES owner
vars == <<owner>>

Init == owner = 0

Lock(p) == /\ owner = 0
           /\ owner' = p

Unlock(p) == /\ owner = p
             /\ owner' = 0

Next == \E p \in 1..NumProcs: Lock(p) \/ Unlock(p)

Spec == Init /\ [][Next]_vars

MutualExclusion == owner = 0 \/ owner \in 1..NumProcs
"""
        spec = template.format(lock_type=lock_type.capitalize())
        spec_file = self.tla_dir / f"{lock_type}_lock.tla"
        spec_file.write_text(spec)
        return spec_file

    def run_tlc(self, spec_file: Path) -> Tuple[bool, Path]:
        """Run the TLC model checker and return success flag and log path."""
        cfg = (
            "SPECIFICATION Spec\n"
            "INVARIANT MutualExclusion\n"
            "CONSTANTS NumProcs = 2\n"
        )
        cfg_file = spec_file.with_suffix(".cfg")
        cfg_file.write_text(cfg)

        tla_jar = Path("/opt/tla-toolbox/tla2tools.jar")
        if not tla_jar.exists():
            out_file = self.results_dir / f"{spec_file.stem}_tlc.txt"
            out_file.write_text("tla2tools.jar not found\n")
            return False, out_file

        cmd = [
            "java",
            "-jar",
            str(tla_jar),
            "-config",
            str(cfg_file),
            str(spec_file),
        ]
        result = subprocess.run(cmd, capture_output=True, text=True)
        out_file = self.results_dir / f"{spec_file.stem}_tlc.txt"
        out_file.write_text(result.stdout + result.stderr)
        return result.returncode == 0, out_file

    def generate_csp_spec(self, lock_type: str) -> Path:
        """Write a CSP specification for *lock_type* and return the path."""
        template = """
-- {lock_type} lock specification
channel lock, unlock : ProcID
ProcID = {{0..1}}

LOCK = lock?p -> unlock!p -> LOCK
PROC(id) = lock!id -> unlock!id -> PROC(id)
SYSTEM = LOCK ||| id:ProcID @ PROC(id)
"""
        spec = template.format(lock_type=lock_type)
        spec_file = self.csp_dir / f"{lock_type}_lock.csp"
        spec_file.write_text(spec)
        return spec_file

    def run_fdr(self, spec_file: Path) -> Tuple[bool, Path]:
        """Run the FDR refinement checker on *spec_file* if available."""

        if shutil.which("refines") is None:
            out_file = self.results_dir / f"{spec_file.stem}_fdr.txt"
            out_file.write_text("refines command not found\n")
            return False, out_file

        cmd = ["refines", str(spec_file)]
        result = subprocess.run(cmd, capture_output=True, text=True)
        out_file = self.results_dir / f"{spec_file.stem}_fdr.txt"
        out_file.write_text(result.stdout + result.stderr)
        return result.returncode == 0, out_file


def main() -> None:
    pipeline = FormalVerificationPipeline(Path(__file__).resolve().parents[1])
    for lock in ("spinlock", "ticket", "mcs"):
        tla_spec = pipeline.generate_tla_spec(lock)
        success, log = pipeline.run_tlc(tla_spec)
        print(f"TLA+ for {lock}: {'OK' if success else 'FAIL'} (log: {log})")

        csp_spec = pipeline.generate_csp_spec(lock)
        success, log = pipeline.run_fdr(csp_spec)
        print(f"CSP for {lock}: {'OK' if success else 'FAIL'} (log: {log})")


if __name__ == "__main__":
    main()
