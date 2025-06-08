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
