---
name: prima-gui-initialization-windows
description: Use when you are developing a standalone Perl application for Windows
  that requires a graphical interface and depends on external command-line tools (e.g.,
  Gnuplot for visualization).
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_0091
  tools:
  - Perl Prima
  - Gnuplot
  - Perl
  license_tier: open
derived_from:
- doi: 10.1002/cpz1.70009
  title: LipidOne 2.0
evidence_spans:
- Graphical User Interface, developed by using Perl Prima
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_lipidone_2_0_cq
    doi: 10.1002/cpz1.70009
    title: LipidOne 2.0
  dedup_kept_from: coll_lipidone_2_0_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1002/cpz1.70009
  all_source_dois:
  - 10.1002/cpz1.70009
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# prima-gui-initialization-windows

## Summary

Initialize a Perl Prima graphical user interface on Microsoft Windows with pre-launch verification of external dependencies (Gnuplot) before enabling application functionality. This skill ensures robust startup behavior and user feedback when critical runtime libraries are missing.

## When to use

You are developing a standalone Perl application for Windows that requires a graphical interface and depends on external command-line tools (e.g., Gnuplot for visualization). You need to detect the Windows environment, verify that required executables are available on the system PATH or in standard installation directories, and provide clear error messaging if dependencies are unmet before users attempt data operations.

## When NOT to use

- Target platform is not Microsoft Windows 64-bit (e.g., Linux, macOS, 32-bit Windows)
- Application does not require external command-line tools or all dependencies are bundled/embedded
- Users are expected to manage dependency installation outside the application launcher (e.g., via separate installer or package manager)

## Inputs

- Windows operating system environment context
- Perl runtime with Prima library installed
- System PATH environment variable
- Standard installation directories for external tools (e.g., C:\Program Files\gnuplot, C:\Program Files (x86)\gnuplot)

## Outputs

- Initialized Prima GUI window (on success)
- Error dialog with dependency status message (on failure)
- Startup log file with initialization status and timestamp
- Enabled or disabled application controls (dataset loading interface)

## How to apply

Create a Perl script entry point that first detects the Windows operating system environment. Initialize the Perl Prima graphical user interface framework to display the application window. Implement a pre-launch verification routine that searches the system PATH and standard installation directories for the required external tool (e.g., Gnuplot 5.4.2). If the dependency is not found, display an error dialog using Prima's native dialog widgets and halt execution to prevent user confusion or runtime crashes. If verification succeeds, enable the main application controls (e.g., dataset loading interface). Log the initialization outcome (success or failure) to a startup log file for troubleshooting.

## Related tools

- **Perl Prima** (Graphical user interface framework for rendering windows, dialogs, and interactive controls on Windows) — http://www.prima.eu.org/
- **Gnuplot** (External command-line graphing utility verified at startup; required for lipidomic data visualization) — http://www.gnuplot.info/
- **Perl** (Language runtime and interpreter for the application entry point and dependency verification logic)

## Evaluation signals

- Prima window appears on screen with expected title and controls (no crashes or black window)
- When Gnuplot 5.4.2 is present: startup log records 'initialization success' and dataset loading controls are enabled
- When Gnuplot is missing: Prima error dialog appears with descriptive message; execution halts before data operations; startup log records 'initialization failure' with reason
- System PATH and standard installation directories (e.g., Program Files\gnuplot) are checked in documented order with no exceptions raised
- Startup log file is created in predictable location and contains timestamp, OS version detection, and full dependency check results

## Limitations

- Skill is Windows-specific; porting to Linux/macOS requires separate platform detection and alternative GUI frameworks
- Only verifies presence of Gnuplot executable; does not validate version number or test Gnuplot functionality at runtime
- If Gnuplot is installed in a non-standard directory not on PATH, the verification will fail unless that directory is explicitly added to search paths
- Depends on Perl Prima availability; systems without Prima pre-installed will fail at module import time before this skill can execute

## Evidence

- [readme] LipidOne is a stand alone software entirely written in Perl and implemented for the Microsoft Windows operating system.: "LipidOne is a stand alone software entirely written in Perl and implemented for the Microsoft Windows operating system."
- [intro] Graphical User Interface, developed by using Perl Prima and Gnuplot libraries.: "Graphical User Interface, developed by using Perl Prima (http://www.prima.eu.org/) and Gnuplot (http://www.gnuplot.info/) libraries."
- [readme] GNUPLOT Graphic library. Download at http://www.gnuplot.info/ or https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/: "GNUPLOT Graphic library. Download at http://www.gnuplot.info/ or https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/"
- [other] Workflow step 3–5 describe verification routine that checks for Gnuplot availability and halts or enables controls accordingly.: "Implement a pre-launch verification routine that checks for Gnuplot 5.4.2 library availability on the system PATH or standard installation directories. If Gnuplot is not found, display an error"
- [other] Log initialization success or failure status to a startup log file.: "Log initialization success or failure status to a startup log file."
