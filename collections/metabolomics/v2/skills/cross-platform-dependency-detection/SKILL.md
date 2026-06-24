---
name: cross-platform-dependency-detection
description: Use when when developing a standalone scientific application that relies
  on external binaries or libraries and must run on a specific operating system (e.g.,
  Microsoft Windows 64-bit). Use this skill to verify Gnuplot 5.4.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0336
  edam_topics:
  - http://edamontology.org/topic_3361
  tools:
  - Perl Prima
  - Gnuplot
  - Perl
  license_tier: restricted
derived_from:
- doi: 10.1002/cpz1.70009
  title: LipidOne 2.0
evidence_spans: []
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

# cross-platform-dependency-detection

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Detect and verify the availability of required external libraries and tools on the host operating system before launching a scientific application. This skill prevents runtime failures by validating prerequisites (e.g., Gnuplot 5.4.2) at startup and providing actionable feedback to the user.

## When to use

When developing a standalone scientific application that relies on external binaries or libraries and must run on a specific operating system (e.g., Microsoft Windows 64-bit). Use this skill to verify Gnuplot 5.4.2 or other critical dependencies exist on the system PATH or in standard installation directories before the GUI initializes or dataset loading is enabled.

## When NOT to use

- Input is a cross-platform application that bundles all dependencies (no external binaries to verify).
- The scientific workflow does not require external libraries or tools (pure Perl/Python/R application).
- Dependency verification has already been completed in an earlier pipeline stage.

## Inputs

- Windows operating system environment (detected at runtime)
- System PATH environment variable
- Standard application installation directories
- Perl script entry point

## Outputs

- Initialization success/failure status logged to startup log file
- Error dialog displayed in Perl Prima GUI (if dependency missing)
- Enabled or disabled dataset loading interface control
- Application halted or proceeded to main GUI

## How to apply

Implement a pre-launch verification routine in the application entry point that runs before the main graphical interface becomes operational. Detect the Windows operating system environment, then systematically search for the required external dependency (e.g., Gnuplot 5.4.2) in standard system locations and the PATH environment variable. If the dependency is found and is the correct version, log success and proceed to enable dataset loading controls. If the dependency is not found or is the wrong version, display an error dialog with the dependency name and version requirement, log the failure to a startup log file, and halt execution. This ensures users receive immediate, transparent feedback about missing prerequisites rather than encountering cryptic runtime errors during data analysis.

## Related tools

- **Perl Prima** (GUI framework for displaying dependency error dialogs and controlling user interaction if verification fails) — http://www.prima.eu.org/
- **Gnuplot** (External graphical library dependency being verified; version 5.4.2 is the required target) — http://www.gnuplot.info/
- **Perl** (Language for implementing the entry point script and verification routine logic) — github.com/matteogiulietti/LipidOne

## Evaluation signals

- Startup log file is created and contains initialization success or failure status with timestamp.
- If Gnuplot 5.4.2 is present on system PATH, dataset loading interface becomes enabled without error.
- If Gnuplot 5.4.2 is missing, an error dialog appears in Perl Prima GUI with the missing dependency name and version, and execution halts (application does not proceed to main workflow).
- Error dialog text and log message are consistent and mention Gnuplot 5.4.2 by name and version.
- Application does not proceed past the pre-launch verification routine if any required dependency is unavailable.

## Limitations

- Skill is specific to Microsoft Windows 64-bit; porting to macOS or Linux requires separate dependency paths and environment detection logic.
- Verification routine assumes Gnuplot is installed in standard locations or present on system PATH; non-standard installations may not be detected.
- Startup log file location and permissions must be writable; failure to write logs may mask dependency issues in production environments.
- Skill does not validate the integrity or correctness of the detected dependency binary; it only checks name and version string matching.

## Evidence

- [other] LipidOne initializes its graphical user interface using Perl Prima and verifies external dependencies on Microsoft Windows before allowing lipidomic dataset loading: "LipidOne is a standalone Perl application for Windows that develops its graphical user interface using Perl Prima and Gnuplot libraries, with Gnuplot 5.4.2 listed as a prerequisite download"
- [other] Verification workflow including detection, checking, and user feedback: "Implement a pre-launch verification routine that checks for Gnuplot 5.4.2 library availability on the system PATH or standard installation directories. If Gnuplot is not found, display an error"
- [readme] Windows platform and prerequisite specification in README: "LipidOne is a stand alone software entirely written in Perl and implemented for the Microsoft Windows operating system. Each operation is made very simple thanks to the Graphical User Interface,"
- [readme] Explicit Gnuplot version requirement and download link: "GNUPLOT Graphic library. Download at http://www.gnuplot.info/ or https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/"
