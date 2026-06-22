---
name: dotnet-project-build-configuration
description: Use when you are attempting to compile a WPF-based .NET desktop application from source code that targets multiple .NET Framework versions, have cloned a repository with an .sln solution file, and need to resolve framework-specific NuGet dependencies (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3695
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - ReactiveExtensions
  - ReactiveProperty
  - .NET Standard
  - Visual Studio 2022
  - Visual Studio Code
  - .NET Framework 4.7.2
  - NuGet Package Manager
  - WPF (Windows Presentation Foundation)
  - MsdialWorkbench GitHub Repository
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- utilizing packages such as ReactiveExtensions and ReactiveProperty
- The .NET class libraries adhere at least to the specifications of .NET Standard 2.0
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_corrdec_cq
    doi: 10.1021/acs.analchem.0c01980
    title: CorrDec
  dedup_kept_from: coll_corrdec_cq
schema_version: 0.2.0
---

# dotnet-project-build-configuration

## Summary

Configure and build a .NET project targeting multiple framework versions (4.7.2, Core 3.1, .NET 6) with proper NuGet dependency resolution and WPF GUI compilation. This skill ensures reproducible desktop application builds from source across Windows development environments.

## When to use

You are attempting to compile a WPF-based .NET desktop application from source code that targets multiple .NET Framework versions, have cloned a repository with an .sln solution file, and need to resolve framework-specific NuGet dependencies (e.g., ReactiveExtensions, ReactiveProperty) before generating an executable binary.

## When NOT to use

- Input is a pre-compiled release binary from GitHub Releases (does not require build configuration)
- Target application uses proprietary vendor SDK formats and you need to read MS vendor-specific raw data formats — use official release versions instead of vendor-unsupported source builds
- Development environment lacks .NET Framework 4.7.2 runtime or Visual Studio 2022 with .NET desktop development workload installed

## Inputs

- MsdialWorkbench.sln solution file
- MsdialGuiApp project file (targeting .NET Framework 4.7.2)
- .NET class libraries adhering to .NET Standard 2.0 specifications
- Local Assemblies folder containing NuGet packages
- Project source code with ReactiveExtensions and ReactiveProperty dependencies

## Outputs

- Compiled MsdialGuiApp executable binary (MSDIAL.exe or equivalent)
- Built WPF GUI application with ReactiveExtensions/ReactiveProperty UI framework
- Debug or Release build artifacts in bin/Debug or bin/Release directories

## How to apply

Clone the MsdialWorkbench repository and open the .sln file in Visual Studio 2022 with .NET desktop development workload installed. Add the local 'Assemblies' folder as a NuGet package source to resolve framework-specific packages. Select the appropriate build configuration (Debug or Release with vendor unsupported mode for source distributions, which limits input to mzML, cdf, and abf formats). Restore NuGet dependencies via the package manager, then set MsdialGuiApp as the startup project and target .NET Framework 4.7.2 as the build target. Compile using Visual Studio's build system and verify the executable binary appears in the output directory (bin/Release or bin/Debug). Confirm the application launches without errors on a Windows system with .NET Framework 4.7.2 runtime installed.

## Related tools

- **Visual Studio 2022** (Primary IDE for opening .sln file, managing NuGet packages, and compiling WPF project) — https://visualstudio.microsoft.com/
- **Visual Studio Code** (Alternative IDE supported for coding the project)
- **.NET Framework 4.7.2** (Target framework version for MsdialGuiApp WPF compilation)
- **NuGet Package Manager** (Resolves ReactiveExtensions and ReactiveProperty dependencies from local Assemblies folder)
- **WPF (Windows Presentation Foundation)** (UI framework for GUI implementation)
- **ReactiveExtensions** (Dependency for reactive programming patterns in WPF application)
- **ReactiveProperty** (Dependency for reactive property bindings in WPF application)
- **MsdialWorkbench GitHub Repository** (Source code repository to clone) — https://github.com/systemsomicslab/MsdialWorkbench

## Evaluation signals

- Executable binary (MSDIAL.exe) is successfully generated in the bin/Release or bin/Debug output directory
- Application launches without runtime errors on Windows with .NET Framework 4.7.2 installed
- NuGet package restore completes without missing dependency errors for ReactiveExtensions and ReactiveProperty
- Build configuration shows no unresolved assembly references or version mismatch warnings for .NET Standard 2.0 class libraries
- WPF GUI renders and responds to user interactions without initialization exceptions

## Limitations

- The vendor-unsupported build configuration (Debug/Release vendor unsupported) can only read mzML, cdf, and abf data formats; proprietary MS vendor formats require official release binaries
- Unit testing infrastructure for partial functionalities is not currently set up for trial in the repository
- Build reproducibility is officially guaranteed only for version 5 series; other versions may have non-deterministic output
- Requires Windows development environment; cross-platform builds require alternative .NET 6 project configuration

## Evidence

- [methods] The MsdialWorkbench project uses .NET Framework 4.7.2, .NET Core 3.1, and .NET 6: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [methods] WPF GUI uses ReactiveExtensions and ReactiveProperty packages: "utilizing packages such as ReactiveExtensions and ReactiveProperty"
- [readme] Vendor-unsupported build mode restricts input to specific formats: "For the 'Debug/Release vendor unsupported' version, only the following formats are supported: **abf**(Reifycs), **cdf**(NetCDF), and **mzml**."
- [readme] Build configuration selection and startup project configuration steps: "Select `Debug vendor unsupported` from the `Solution Configurations` pull-down menu. Select `MsdialGuiApp` from the `Startup Projects` pull-down menu."
- [methods] .NET Standard 2.0 class library compliance: "The .NET class libraries adhere at least to the specifications of .NET Standard 2.0"
