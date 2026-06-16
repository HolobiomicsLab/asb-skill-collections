# Evaluation Strategy

## Direct Checks

- verify file environment.yml (or equivalent Conda specification) exists in the HiC-Pro repository root or documented installation path
- script_runs: execute 'conda env create -f environment.yml' (or specified environment file) without errors on a clean system
- verify conda environment activation succeeds with 'conda activate <env_name>'
- verify Python version in activated environment is >3.7 via 'python --version'
- verify bowtie2 binary is executable and resolvable in PATH of activated environment via 'which bowtie2' or 'bowtie2 --version'
- verify samtools binary version is >=1.9 in activated environment via 'samtools --version' output contains version number ≥1.9
- verify iced Python module is importable in activated environment via 'python -c "import iced; print(iced.__version__)"'
- verify bx-python (>=0.8.8) is importable in activated environment via 'python -c "import bx; print(bx.__version__)"' and version ≥0.8.8
- verify numpy (>=1.18.1) is importable in activated environment via 'python -c "import numpy; print(numpy.__version__)"' and version ≥1.18.1
- verify scipy (>=1.4.1) is importable in activated environment via 'python -c "import scipy; print(scipy.__version__)"' and version ≥1.4.1
- verify R is available and executable in activated environment via 'which R' or 'R --version'
- verify ggplot2 (>2.2.1) is installed in R environment via 'R --slave -e "packageVersion(\"ggplot2\")"' and version >2.2.1
- verify RColorBrewer is installed in R environment via 'R --slave -e "library(RColorBrewer); cat(packageVersion(\"RColorBrewer\"))"'

## Expert Review

- Review environment specification file for completeness: confirm all documented dependencies (Python >3.7, R packages, and external binaries) are listed with appropriate version constraints matching EnrichedIndex requirements
- Evaluate whether conda environment specification correctly pins or constrains versions to prevent dependency conflicts or breaking updates post-publication
- Assess whether bowtie2, samtools, and iced are specified as conda packages or external downloads; if external, verify installation instructions are clear and unambiguous
- Review whether environment specification handles platform-specific dependencies (e.g., different binary paths or compilation flags for Linux/macOS)
