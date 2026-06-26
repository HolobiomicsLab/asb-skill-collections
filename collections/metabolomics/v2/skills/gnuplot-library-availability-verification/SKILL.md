---
name: gnuplot-library-availability-verification
description: Use when when deploying a Perl-based GUI application (such as LipidOne)
  on Microsoft Windows that depends on Gnuplot for visualization, and you need to
  ensure the application will not crash during dataset loading or plotting operations
  due to missing or inaccessible Gnuplot binaries.
license: CC-BY-4.0
metadata:
  edam_topics:
  - http://edamontology.org/topic_3172
  tools:
  - Gnuplot
  - Perl Prima
  - Perl
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1002/cpz1.70009
  title: LipidOne 2.0
evidence_spans:
- https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/
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

# gnuplot-library-availability-verification

## Summary

Verify that Gnuplot 5.4.2 is installed and accessible on the system PATH before initializing a Perl Prima GUI application for lipidomic analysis. This skill prevents runtime failures by detecting missing graphing library dependencies at application startup.

## When to use

When deploying a Perl-based GUI application (such as LipidOne) on Microsoft Windows that depends on Gnuplot for visualization, and you need to ensure the application will not crash during dataset loading or plotting operations due to missing or inaccessible Gnuplot binaries.

## When NOT to use

- The application does not use Gnuplot for visualization or does not require external graphing libraries.
- Gnuplot verification is already performed by a wrapper script or dependency manager (e.g., Docker, conda, or installer) before Perl application launch.
- The target platform is not Microsoft Windows 64-bit (e.g., Linux or macOS with different PATH conventions and installation directories).

## Inputs

- Windows operating system environment (64-bit)
- Perl application entry point (script or compiled binary)
- System PATH environment variable
- Standard Gnuplot installation directories on Windows

## Outputs

- Boolean verification result (Gnuplot 5.4.2 found and accessible: true/false)
- Startup log file (text) recording verification success or failure
- Prima GUI dialog box (error message if verification fails)
- Enabled or disabled dataset loading interface control (downstream GUI state)

## How to apply

Implement a pre-launch verification routine in the Perl entry point that systematically checks for Gnuplot 5.4.2 availability before initializing the Perl Prima interface. Query the system PATH and common installation directories (e.g., Program Files, AppData) for the Gnuplot executable. If the executable is found, confirm its version matches or is compatible with 5.4.2 by parsing version output. If Gnuplot is not found or version verification fails, display an error dialog in Prima naming the missing component and the required version, then halt execution. Log the verification result (success or failure) to a startup log file for debugging and user support. Enable dataset loading interface controls only after successful verification.

## Related tools

- **Perl Prima** (Graphical user interface framework used to display error dialogs and initialize the application window during verification) — http://www.prima.eu.org/
- **Gnuplot** (External graphing library whose availability is verified; version 5.4.2 is the required prerequisite) — https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/
- **Perl** (Scripting language in which the verification routine and entry point are implemented)

## Evaluation signals

- Startup log file contains a success entry when Gnuplot 5.4.2 is correctly installed and accessible.
- Prima error dialog is displayed with a message naming Gnuplot 5.4.2 when the executable is not found or version mismatch occurs.
- Application execution halts (non-zero exit code) immediately after verification failure before GUI initialization completes.
- Dataset loading interface controls are enabled only after verification success is logged.
- Version query of discovered Gnuplot returns output matching version 5.4.2 (or confirmed compatible version).

## Limitations

- Verification assumes Gnuplot is installed in standard Windows directories or on the system PATH; non-standard or portable installations may not be detected.
- Version matching logic requires exact or well-defined compatibility rules; minor version drift (e.g., 5.4.1 vs. 5.4.2) may cause false failures if not handled permissively.
- Verification does not test Gnuplot functionality (e.g., whether it can actually generate plots); it only confirms executable presence and version.
- Microsoft Windows-specific PATH and registry conventions are assumed; cross-platform applications will require OS-specific verification branches.

## Evidence

- [readme] LipidOne is a stand alone software entirely written in Perl and implemented for the Microsoft Windows operating system.: "stand alone software entirely written in Perl and implemented for the Microsoft Windows operating system"
- [readme] Each operation is made very simple thanks to the Graphical User Interface, developed by using Perl Prima and Gnuplot libraries.: "Graphical User Interface, developed by using Perl Prima (http://www.prima.eu.org/) and Gnuplot (http://www.gnuplot.info/) libraries"
- [readme] GNUPLOT Graphic library. Download at http://www.gnuplot.info/ or https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/: "GNUPLOT Graphic library. Download at http://www.gnuplot.info/ or https://sourceforge.net/projects/gnuplot/files/gnuplot/5.4.2/"
- [other] Implement a pre-launch verification routine that checks for Gnuplot 5.4.2 library availability on the system PATH or standard installation directories.: "pre-launch verification routine that checks for Gnuplot 5.4.2 library availability on the system PATH or standard installation directories"
- [other] If Gnuplot is not found, display an error dialog in Prima and halt execution; otherwise, enable the dataset loading interface control.: "If Gnuplot is not found, display an error dialog in Prima and halt execution; otherwise, enable the dataset loading interface control"
