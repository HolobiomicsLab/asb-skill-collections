---
name: windows-desktop-application-deployment
description: Use when when you have cloned a .NET Framework or .NET Core WPF project from a GitHub repository and need to compile it into an executable binary for Windows deployment. Specifically, when the project uses ReactiveExtensions/ReactiveProperty packages, declares a .NET Framework 4.7.2 or .
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3222
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3172
  tools:
  - WPF (Windows Presentation Foundation)
  - ReactiveExtensions
  - ReactiveProperty
  - .NET Standard
  - Visual Studio Community 2022
  - .NET Framework 4.7.2
  - NuGet Package Manager
  - ReactiveExtensions & ReactiveProperty
  - GitHub Actions (dotnet_test.yml)
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.0c01980
  all_source_dois:
  - 10.1021/acs.analchem.0c01980
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# windows-desktop-application-deployment

## Summary

Build and deploy a Windows desktop WPF application from source code using Visual Studio, targeting .NET Framework 4.7.2, with NuGet dependency management and verification on a Windows runtime environment. This skill is essential when reconstructing metabolomics software (MS-DIAL) from source for reproducible open-science workflows.

## When to use

When you have cloned a .NET Framework or .NET Core WPF project from a GitHub repository and need to compile it into an executable binary for Windows deployment. Specifically, when the project uses ReactiveExtensions/ReactiveProperty packages, declares a .NET Framework 4.7.2 or .NET Standard 2.0 target, and you need to verify the build produces a working GUI application without vendor-locked dependencies.

## When NOT to use

- Input is a pre-compiled release binary from GitHub Releases — skip to testing/installation instead of rebuilding.
- Target platform is macOS or Linux — this skill is Windows-specific; use alternative .NET toolchains (dotnet CLI on non-Windows, or Mono) for cross-platform deployment.
- Project uses only .NET Core 3.1+ without WPF or Windows-specific UI framework — consider platform-agnostic .NET build workflows instead.

## Inputs

- Cloned source repository (GitHub URL or local path)
- Visual Studio project file (.sln, .csproj)
- NuGet package manifest (packages.config or .csproj PackageReference)
- Local Assemblies folder (if using proprietary or custom packages)
- Build configuration selector (e.g., 'Debug vendor unsupported' vs. 'Release')

## Outputs

- Executable binary (MsdialGuiApp.exe or equivalent)
- Compiled WPF application in bin/Debug or bin/Release directory
- Application running on Windows with verified GUI launch
- Confirmation of input format support (abf, cdf, mzML for open distributions)

## How to apply

Clone the repository (e.g., https://github.com/systemsomicslab/MsdialWorkbench) and open the .sln file in Visual Studio Community 2022 with .NET desktop development workload installed. Verify the project build target matches the declared framework (e.g., .NET Framework 4.7.2). Add the local Assemblies folder to the NuGet Package source, then restore dependencies including ReactiveExtensions and ReactiveProperty. Select the appropriate Solution Configuration (e.g., 'Debug vendor unsupported' for open-source distributions) and set the WPF GUI project (e.g., MsdialGuiApp) as the Startup Project. Build via the Visual Studio GUI or command-line using the project's build recipe. Verify the executable appears in the output directory (bin/Debug or bin/Release). Test the application launches on a Windows system with the required .NET Framework 4.7.2 runtime installed, confirming it loads without errors and supports only the permitted input formats (abf, cdf, mzML for 'vendor unsupported' configurations).

## Related tools

- **Visual Studio Community 2022** (IDE for building, restoring NuGet dependencies, and launching the WPF application; requires '.NET desktop development' workload) — https://visualstudio.microsoft.com/
- **.NET Framework 4.7.2** (Target runtime framework for the MsdialGuiApp WPF project compilation and execution)
- **NuGet Package Manager** (Resolves and restores ReactiveExtensions, ReactiveProperty, and other dependencies from local or remote sources)
- **WPF (Windows Presentation Foundation)** (UI framework used to build the desktop GUI components of the application)
- **ReactiveExtensions & ReactiveProperty** (NuGet packages providing reactive programming patterns for event-driven UI binding)
- **GitHub Actions (dotnet_test.yml)** (Automated CI/CD pipeline for testing builds; review 'test:' section to understand supported build configurations) — https://github.com/systemsomicslab/MsdialWorkbench/blob/master/.github/workflows/dotnet_test.yml

## Examples

```
# In Visual Studio GUI: Open MsdialWorkbench.sln → Tools > Manage NuGet Packages for Solution → Add local Assemblies folder as package source → Select 'Debug vendor unsupported' from Solution Configurations dropdown → Set MsdialGuiApp as Startup Project → Click ▶ MsdialGuiApp to build and run.
```

## Evaluation signals

- Executable file exists in the expected output directory (bin/Debug/MsdialGuiApp.exe or bin/Release/MsdialGuiApp.exe) with non-zero file size.
- Application launches on a Windows machine with .NET Framework 4.7.2 runtime installed without crashes or error dialogs.
- WPF GUI window appears with expected UI elements and is responsive to user interaction (button clicks, menu navigation).
- Build log reports zero errors and zero unresolved NuGet package warnings; all dependencies listed in .csproj or packages.config are successfully restored.
- For 'vendor unsupported' builds, verify that the application can open/process files in abf, cdf, or mzML formats but rejects proprietary manufacturer formats (e.g., Bruker .d, Thermo .raw).

## Limitations

- The 'Debug/Release vendor unsupported' configuration (used for open-source distribution) cannot read proprietary mass spectrometry data formats from instrument manufacturers; only abf (Reifycs), cdf (NetCDF), and mzML are supported. Official release binaries have additional format support but are closed-source.
- Unit testing infrastructure for partial functionalities is not currently set up for trial, limiting ability to validate individual components.
- Only MS-DIAL version 5 series has reproducible builds that can be guaranteed openly; earlier versions may have licensing or dependency restrictions.
- Build requires Visual Studio or equivalent .NET compilation toolchain; command-line dotnet CLI builds are not explicitly documented in the README and may require additional configuration.
- Application is Windows-only; WPF is not cross-platform. .NET Framework 4.7.2 runtime must be pre-installed on the target machine.

## Evidence

- [methods] .NET Framework 4.7.2 requirement: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [methods] WPF and reactive packages: "we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation"
- [methods] ReactiveExtensions and ReactiveProperty dependencies: "utilizing packages such as ReactiveExtensions and ReactiveProperty"
- [methods] Visual Studio build tool recommendation: "we recommend using Visual Studio"
- [readme] Build workflow steps: "Double click `MsdialWorkbench.sln` in the cloned repo. 4. Right-click on `MsdialWorkbench` in the Solution Explorer. 5. Click `Manage NuGet Packages for Solution...`."
- [readme] Supported input formats for vendor unsupported: "For the 'Debug/Release vendor unsupported' version, only the following formats are supported: **abf**(Reifycs), **cdf**(NetCDF), and **mzml**."
- [methods] Verification of successful build: "Verify the executable binary is generated in the output directory (e.g., bin/Release or bin/Debug)."
- [methods] Runtime verification on Windows: "Confirm the application launches without errors on a Windows system with the required .NET Framework 4.7.2 runtime."
