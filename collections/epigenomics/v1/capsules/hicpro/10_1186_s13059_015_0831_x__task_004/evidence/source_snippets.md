# Evidence Snippets

## ev_001

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] Can a Conda environment be successfully created from an environment specification file with all required Python (>3.7) and R dependencies for HiC-Pro, and can tool binaries (bowtie2, samtools, iced) be correctly resolved within that environment?: '![Conda](https://img.shields.io/badge/Conda-build-brightgreen.svg)'

## ev_002

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[intro] HiC-Pro provides a flexible pipeline that supports automated installation of key dependencies; bowtie2 and samtools (>=1.9) can be automatically installed if not detected, and iced must be independently installed as it is no longer part of the HiC-Pro source code.: 'An optimized and flexible pipeline for Hi-C data processing'

## ev_003

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] HiC-Pro environment.yml specification file: 'we provide a `yml` file for conda with all required tools'

## ev_004

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Miniconda installation package or access to conda package manager: 'first install [miniconda](https://docs.conda.io/en/latest/miniconda.html)'

## ev_005

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Active Conda environment with all HiC-Pro dependencies installed and verified: 'conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV'

## ev_006

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Dependency verification report listing Python version, all Python package versions, R version, R package availability, tool binary paths, and iced module status: 'All dependencies will be checked during installation, and installed if possible'

## ev_007

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] conda: 'conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml'

## ev_008

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] Python (>3.7): 'Python (>3.7) libraries'

## ev_009

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] R: 'R (http://www.r-project.org/) with the following packages'

## ev_010

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] bowtie2: 'A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected'

## ev_011

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] samtools (>=1.9): 'samtools (>=1.9) can be automatically installed if not detected'

## ev_012

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] bx-python (>=0.8.8): 'bx-python (>=0.8.8) - https://pypi.python.org/pypi/bx-python'

## ev_013

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] numpy (>=1.18.1): 'numpy (>=1.18.1) - http://www.scipy.org/scipylib/download.html'

## ev_014

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] scipy (>=1.4.1): 'scipy (>=1.4.1) - http://www.scipy.org/scipylib/download.html'

## ev_015

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] pysam (>=0.15.4): 'pysam (>=0.15.4) - https://github.com/pysam-developers/pysam'

## ev_016

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] ggplot2 (>2.2.1): 'ggplot2 (>2.2.1)'

## ev_017

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] RColorBrewer: 'RColorBrewer'

## ev_018

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[methods] iced: 'Note that the iced module is also required (https://github.com/hiclib/iced)'

## ev_019

- Source: `agent2_synthesis`
- Reason: `agent2_traced`

[discussion] No changelog found: 'No changelog found.'
