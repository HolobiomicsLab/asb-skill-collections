---
name: r-package-installation-verification
description: Use when after installing R or modifying an R environment via conda, package managers, or container images; before running any pipeline step that depends on R packages for statistical analysis, visualization, or data normalization.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3096
  edam_topics:
  - http://edamontology.org/topic_0769
  - http://edamontology.org/topic_0091
  tools:
  - MultiQC 1.8
  - R
  - bowtie2
  - samtools (>=1.9)
  - numpy (>=1.18.1)
  - scipy (>=1.4.1)
  - pysam (>=0.15.4)
  - ggplot2 (>2.2.1)
  - RColorBrewer
  - iced
  - ggplot2
  - grid
  - conda
derived_from:
- doi: 10.1186/s13059-015-0831-x
  title: hicpro
evidence_spans:
- R (http://www.r-project.org/) with the following packages
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected.
- A couple of tools such as `bowtie2` and `samtools` (>=1.9) can be automatically installed if not detected
- samtools (>=1.9) can be automatically installed if not detected
- numpy (>=1.18.1) - http://www.scipy.org/scipylib/download.html
- scipy (>=1.4.1) - http://www.scipy.org/scipylib/download.html
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/epigenomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_hicpro
    doi: 10.1186/s13059-015-0831-x
    title: hicpro
  dedup_kept_from: coll_hicpro
schema_version: 0.2.0
---

# R package installation verification

## Summary

Verify that required R packages (ggplot2, RColorBrewer, grid) are correctly installed and importable in the active R environment. This skill ensures that downstream R-based analysis steps in bioinformatics pipelines (such as HiC-Pro's visualization and normalization workflows) will succeed.

## When to use

After installing R or modifying an R environment via conda, package managers, or container images; before running any pipeline step that depends on R packages for statistical analysis, visualization, or data normalization. Particularly critical when setting up HiC-Pro or similar pipelines that require specific R package versions (e.g., ggplot2 >2.2.1) for Hi-C contact map plotting and quality-control reporting.

## When NOT to use

- R packages are already confirmed to be installed and functional in the current session (re-verification is redundant).
- The pipeline does not use R (e.g., pure Python workflows without R dependencies).
- Installing new R packages — this skill verifies existing installations, not installs them; use install.packages() or conda install for installation.

## Inputs

- R environment (active shell or conda environment)
- R installation path or conda environment specification
- List of required package names and minimum version constraints (e.g., ggplot2 >2.2.1)

## Outputs

- Verification report listing each package name, load status (success/failure), and installed version
- Error messages or warnings if any package failed to load
- Summary of R version and library paths used

## How to apply

Launch an R session (interactive or via Rscript) and attempt to load each required package using the library() function. For HiC-Pro, verify ggplot2 (>2.2.1), RColorBrewer, and grid packages are available and callable. If a package fails to load, check the R version (must match pipeline requirements), verify the package was installed to the correct library path, and re-install if necessary via install.packages() or conda. Document the successful load of each package and its version number. The rationale is that R packages installed but not in the R_LIBPATHS or with incompatible versions will cause silent or cryptic runtime failures downstream; early verification prevents wasted compute.

## Related tools

- **R** (Runtime environment for executing library() verification and running downstream statistical/visualization tasks) — http://www.r-project.org/
- **ggplot2** (Required R package for plotting and visualizing Hi-C contact maps and QC metrics; version constraint ggplot2 >2.2.1)
- **RColorBrewer** (Required R package for color palette generation in HiC-Pro visualization outputs)
- **grid** (Base R graphics package required as a dependency for ggplot2 and multi-panel plot layouts)
- **conda** (Package manager used to install R and R packages into isolated environments; enables reproducible R environment setup) — https://docs.conda.io/en/latest/miniconda.html

## Examples

```
Rscript -e 'library(ggplot2); library(RColorBrewer); library(grid); cat("R packages loaded successfully\n"); sessionInfo()'
```

## Evaluation signals

- Each required package (ggplot2, RColorBrewer, grid) returns TRUE when passed to require() or library(), indicating successful import.
- Package version strings printed by packageVersion() or sessionInfo() meet or exceed the documented minimum (e.g., ggplot2 version >2.2.1).
- R_LIBPATHS environment variable points to the correct conda or system library directory containing the installed packages.
- No warnings or errors appear in the R console output when loading packages (except non-critical deprecation notices).
- Downstream R scripts that depend on these packages execute without 'package not found' errors or missing function errors.

## Limitations

- Verification confirms presence but does not detect functional bugs or missing sub-dependencies within a package; a successful library() load does not guarantee correct behavior at runtime.
- Version constraints (e.g., ggplot2 >2.2.1) are specified in the HiC-Pro documentation but may not be automatically enforced; the user must manually check packageVersion() output.
- R package installation from source (rather than pre-compiled binaries via conda) may fail silently if system compilers or headers are missing; library() success does not verify the build succeeded correctly.
- Platform-specific issues (e.g., macOS missing GNU core utilities, Windows library path separators) may cause packages to install but fail to load correctly; verification should be repeated on the target platform.
- No changelog or version history is provided in HiC-Pro's source for detecting which package versions were last validated; users must cross-reference with the original article or conda environment.yml lock files.

## Evidence

- [other] Verify that R is available and that required packages (ggplot2 >2.2.1, RColorBrewer, grid) are installed by testing library() calls in R.: "Verify that R is available and that required packages (ggplot2 >2.2.1, RColorBrewer, grid) are installed by testing library() calls in R."
- [methods] R with the following packages: RColorBrewer and ggplot2 (>2.2.1): "R with the *RColorBrewer* and *ggplot2 (>2.2.1)* packages"
- [methods] All required Python libraries and R packages must be installed and importable before pipeline execution.: "verify that all required Python libraries (bx-python >=0.8.8, numpy >=1.18.1, scipy >=1.4.1, pysam >=0.15.4, argparse) are installed and importable"
- [readme] conda env create enables environment creation with all dependencies; activation and verification are essential steps.: "conda env create -f MY_INSTALL_PATH/HiC-Pro/environment.yml -p WHERE_TO_INSTALL_MY_ENV
conda activate WHERE_TO_INSTALL_MY_ENV"
- [methods] R package dependencies and version constraints are documented for HiC-Pro visualization pipelines.: "Python (>3.7) with *pysam (>=0.15.4)*, *bx-python(>=0.8.8)*, *numpy(>=1.18.1)*, and *scipy(>=1.4.1)* libraries. Note that the current version no longer supports python 2
- R with the *RColorBrewer*"
