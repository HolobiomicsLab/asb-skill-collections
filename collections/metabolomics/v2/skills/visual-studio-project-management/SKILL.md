---
name: visual-studio-project-management
description: Use when when you have cloned a multi-framework .NET project (e.g., MsdialWorkbench
  using .NET Framework 4.7.2, .NET Core 3.1, and .NET 6) and need to set up the build
  environment in Visual Studio, restore dependencies, select a specific build configuration
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3552
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3372
  tools:
  - Visual Studio
  - ReactiveExtensions
  - ReactiveProperty
  - .NET Standard
  - Visual Studio Community 2022
  - .NET Framework 4.7.2
  - WPF (Windows Presentation Foundation)
  - MsdialWorkbench
  techniques:
  - mass-spectrometry
  license_tier: restricted
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- If you intend to contribute to the GUI part of the code and would like to have access
  to a preview, we recommend using Visual Studio
- we recommend using Visual Studio
- utilizing packages such as ReactiveExtensions and ReactiveProperty
- The .NET class libraries adhere at least to the specifications of .NET Standard
  2.0
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01980
  all_source_dois:
  - 10.1021/acs.analchem.0c01980
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# visual-studio-project-management

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Configure and build a .NET multi-framework WPF application in Visual Studio by managing solution-level NuGet dependencies, selecting appropriate build configurations, and verifying successful compilation and runtime execution. This skill is essential for developers who need to reconstruct complex open-source metabolomics software from source.

## When to use

When you have cloned a multi-framework .NET project (e.g., MsdialWorkbench using .NET Framework 4.7.2, .NET Core 3.1, and .NET 6) and need to set up the build environment in Visual Studio, restore dependencies, select a specific build configuration (e.g., 'Debug vendor unsupported' vs. 'Release'), and ensure the WPF GUI application compiles and launches without errors on a Windows system.

## When NOT to use

- Input is a non-.NET project or uses a different UI framework (e.g., WinForms, ASP.NET, Qt) — use framework-specific build tools instead.
- Solution file references external NuGet repositories that are no longer available or require authentication not configured — resolve repository connectivity first.
- Target platform is not Windows or .NET Framework 4.7.2 runtime is not installed on the build machine — install required runtime or target a different framework.

## Inputs

- Visual Studio solution file (.sln)
- Project files (.csproj) with .NET Framework 4.7.2 target
- NuGet dependencies manifest (packages.config or .csproj package references)
- WPF XAML and C# source files
- Local Assemblies folder containing pre-built package binaries

## Outputs

- Compiled WPF executable (MsdialGuiApp.exe)
- Build artifacts in bin/Debug or bin/Release directory
- Successfully launched GUI application instance
- Build log with zero errors

## How to apply

Open the solution file (e.g., MsdialWorkbench.sln) in Visual Studio Community 2022 with .NET desktop development workload installed. Add the local Assemblies folder to NuGet Package sources via 'Manage NuGet Packages for Solution' to resolve framework dependencies (ReactiveExtensions, ReactiveProperty, and other packages adhering to .NET Standard 2.0). Select the appropriate Solution Configuration from the dropdown (e.g., 'Debug vendor unsupported' for open-source builds that support only mzML, abf, and cdf formats). Designate MsdialGuiApp as the Startup Project, then build using Visual Studio's integrated build system. Verify that the executable binary is generated in the output directory (bin/Release or bin/Debug) and confirm the application launches on a Windows system with the required .NET Framework 4.7.2 runtime installed.

## Related tools

- **Visual Studio Community 2022** (Primary IDE for opening solution, managing NuGet packages, selecting build configurations, and compiling the WPF application) — https://visualstudio.microsoft.com/
- **.NET Framework 4.7.2** (Target framework for MsdialGuiApp WPF project compilation and runtime execution)
- **ReactiveExtensions** (NuGet package dependency for reactive programming patterns in WPF UI)
- **ReactiveProperty** (NuGet package dependency for reactive property bindings in WPF data models)
- **WPF (Windows Presentation Foundation)** (UI framework used for GUI implementation; managed by Visual Studio's design and build toolchain)
- **MsdialWorkbench** (Source repository containing solution and project files to be built) — https://github.com/systemsomicslab/MsdialWorkbench

## Evaluation signals

- Build output shows zero errors and zero warnings (or only expected warnings from third-party packages).
- Executable file (MsdialGuiApp.exe) is present in bin/Release or bin/Debug directory with a recent timestamp matching the build time.
- Application launches without throwing unhandled exceptions; GUI window renders and responds to user input.
- NuGet restore completes successfully with all ReactiveExtensions, ReactiveProperty, and .NET Standard 2.0 packages resolved from local or remote sources.
- Solution Configuration dropdown reflects the selected build variant (e.g., 'Debug vendor unsupported' shows mzML/abf/cdf format support; 'Release' variant may include vendor SDKs if licensed).

## Limitations

- The 'Debug/Release vendor unsupported' configuration is restricted to open-source distribution and supports only mzML, abf (Reifycs), and cdf (NetCDF) raw data formats; proprietary mass spectrometry vendor formats require the official release build with vendor SDKs, which is not available in the open-source repository.
- Unit testing infrastructure for partial functionalities is not currently set up, so developers cannot rely on automated test suites to validate changes during development.
- Only MS-DIAL version 5 series provides reproducible builds guaranteed to be openly reproducible; earlier versions may have build reproducibility issues.
- Visual Studio 2022 with .NET desktop development workload is required; Visual Studio Code, while mentioned as a coding environment, does not provide the integrated build and NuGet management UI used in this workflow.
- Build success depends on Windows operating system and .NET Framework 4.7.2 runtime; cross-platform builds to Linux or macOS are not supported by this WPF project.

## Evidence

- [methods] we recommend using Visual Studio: "we recommend using Visual Studio"
- [methods] we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [methods] utilizing packages such as ReactiveExtensions and ReactiveProperty: "utilizing packages such as ReactiveExtensions and ReactiveProperty"
- [methods] we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation: "we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation"
- [readme] Double click `MsdialWorkbench.sln` in the cloned repo. Right-click on `MsdialWorkbench` in the Solution Explorer. Click `Manage NuGet Packages for Solution...`. Add the `Assemblies` folder in this repo to the **Package source:**.: "Double click `MsdialWorkbench.sln` in the cloned repo. Right-click on `MsdialWorkbench` in the Solution Explorer. Click `Manage NuGet Packages for Solution...`. Add the `Assemblies` folder in this"
- [readme] Select `Debug vendor unsupported` from the `Solution Configurations` pull-down menu. Select `MsdialGuiApp` from the `Startup Projects` pull-down menu. Click `▶ MsdialGuiApp` button on the right side of 8.: "Select `Debug vendor unsupported` from the `Solution Configurations` pull-down menu. Select `MsdialGuiApp` from the `Startup Projects` pull-down menu. Click `▶ MsdialGuiApp` button on the right side"
- [readme] The 'Debug/Release vendor unsupported' version is a special configuration designed for the purpose of source code distribution. Due to licensing restrictions, this version cannot read proprietary data formats from mass spectrometry manufacturers. However, the [release versions](https://github.com/systemsomicslab/MsdialWorkbench/releases) distributed with official releases can read these proprietary formats. For the 'Debug/Release vendor unsupported' version, only the following formats are supported: **abf**(Reifycs), **cdf**(NetCDF), and **mzml**.: "The 'Debug/Release vendor unsupported' version is a special configuration designed for the purpose of source code distribution. Due to licensing restrictions, this version cannot read proprietary"
- [readme] Download and install [Visual Studio Community 2022](https://visualstudio.microsoft.com/). (In the `Workloads` selection, choose `.NET desktop development`. ): "Download and install [Visual Studio Community 2022](https://visualstudio.microsoft.com/). (In the `Workloads` selection, choose `.NET desktop development`. )"
- [methods] only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
- [methods] we apologize that the unit testing aspect for partial functionalities is not currently set up for trial: "we apologize that the unit testing aspect for partial functionalities is not currently set up for trial"
