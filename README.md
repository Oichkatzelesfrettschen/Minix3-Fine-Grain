# Minix3 Fine-Grain Repository

This repository contains the Minix3 operating system source code used for research and development.

## Format Check Script

The `scripts/check_format.sh` script runs basic format and lint checks on the project.

### Usage

```bash
./scripts/check_format.sh
```

The script performs the following steps:

1. Runs **flake8** on selected Python directories.
2. Runs **black --check** on the same directories.
3. Runs **shellcheck** on every `*.sh` file in the repository.

The script exits with a non-zero status code if any of these tools report problems.

# Minix3 Fine-Grain

This repository contains a custom version of MINIX 3 used for research and
experimentation.

## Formal Verification and Style Checks

This section explains how to install dependencies, run style checks, and
generate verification artifacts. Before running the checks make sure all
dependencies are installed.

### Setup

Run `./setup.sh` from the repository root. This script configures networking and
installs development tools such as **flake8**, **shellcheck**, and **black** which
are needed for the style checks.

### Style Check

Execute `scripts/check_format.sh` to validate code formatting. The script prints
diagnostics to the console and writes a summary to `check_format.log` in the
current directory.

### Generating Proofs

Invoke `scripts/generate_proofs.py` to create formal verification artifacts.
The script requires the **TLA\+ Toolbox** and **FDR** to be installed and
accessible on your `PATH`.  Generated `.tla` and `.csp` files are placed in the
`proofs/` directory and a log is written to `proofs/proof.log`.

