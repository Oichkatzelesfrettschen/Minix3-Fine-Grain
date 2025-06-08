# Minix3 Fine-Grain

This repository contains a custom version of MINIX 3 used for research and
experimentation.

## Formal Verification and Style Checks

Before running the checks make sure all dependencies are installed.

### Setup

Run `./setup.sh` from the repository root. This script configures networking and
installs development tools such as **flake8**, **shellcheck**, and **black** which
are needed for the style checks.

### Style Check

Execute `scripts/check_format.sh` to validate code formatting.  The script
prints diagnostics to the console and writes a summary to `check_format.log` in
the current directory.

### Generating Proofs

Invoke `scripts/generate_proofs.py` to create formal verification artifacts.
The script requires the **TLA\+ Toolbox** and **FDR** to be installed and
accessible on your `PATH`.  Generated `.tla` and `.csp` files are placed in the
`proofs/` directory.

