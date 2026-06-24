---
name: dotnet-framework-development
description: Use when you need to compile and test a .NET-based metabolomics or bioinformatics
  desktop application (e.g., MS-DIAL version 5 series) from source code, or you are
  implementing new parsing or data-processing modules that must integrate with WPF
  UI frameworks and ReactiveExtensions patterns.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_0004
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_3520
  tools:
  - .NET Framework
  - .NET 6
  - .NET Standard
  - GitHub Actions
  - Visual Studio Community 2022
  - Visual Studio Code
  - .NET Framework 4.7.2
  - .NET Standard 2.0
  - WPF (Windows Presentation Foundation)
  - ReactiveExtensions / ReactiveProperty
  techniques:
  - mass-spectrometry
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.0c01980
  title: CorrDec
evidence_spans:
- the main MsdialGuiApp project can be built using .NET Framework 4.7.2
- we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and
  .NET 6
- The .NET class libraries adhere at least to the specifications of .NET Standard
  2.0
- To conduct tests, please refer to section `test:` of GitHub Actions
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

# dotnet-framework-development

## Summary

Set up and build .NET Framework / .NET Core / .NET 6 desktop applications using Visual Studio, manage NuGet dependencies, and configure solution build profiles for reproducible compiled binaries. Essential for contributing to or extending open-source .NET projects like MS-DIAL that support multiple .NET runtime targets.

## When to use

You need to compile and test a .NET-based metabolomics or bioinformatics desktop application (e.g., MS-DIAL version 5 series) from source code, or you are implementing new parsing or data-processing modules that must integrate with WPF UI frameworks and ReactiveExtensions patterns. This skill applies when the project uses .NET Standard 2.0 class libraries to maintain compatibility across .NET Framework 4.7.2, .NET Core 3.1, and .NET 6 runtime targets.

## When NOT to use

- You are using a pre-built binary release of MS-DIAL and only need to run the application (not compile source).
- Your project targets non-Windows platforms exclusively; MS-DIAL is Windows-only and requires WPF.
- You need to analyze vendor-specific proprietary mass spectrometry formats (RAW, d, etc.); the 'vendor unsupported' build configuration only supports mzML, CDF, and ABF formats.

## Inputs

- MS-DIAL source repository (GitHub clone)
- .NET solution file (.sln)
- Project files (.csproj, .vbproj)
- NuGet package manifest (packages.config or .csproj PackageReference)
- Local Assemblies folder (vendor libraries)

## Outputs

- Compiled executable (.exe)
- Build artifacts (DLL assemblies, WPF XAML binaries)
- Test results from GitHub Actions CI/CD pipeline
- Debug or Release build configuration output

## How to apply

Install Visual Studio Community 2022 with the '.NET desktop development' workload selected. Clone the repository (e.g., `git clone https://github.com/systemsomicslab/MsdialWorkbench`) and open the `.sln` solution file. Right-click on the solution and add the local `Assemblies` folder as a NuGet package source to resolve private dependencies. Select the appropriate solution configuration (e.g., 'Debug vendor unsupported' for vendor-independent builds or 'Debug/Release vendor supported' for official releases) from the pull-down menu. Set the startup project to the desired UI application (e.g., `MsdialGuiApp`). Execute the build via the ▶ button or Visual Studio build menu. For CI/CD validation, inspect the `.github/workflows/dotnet_test.yml` file to understand automated test entry points and replicate those tests locally or trigger them via GitHub Actions. Verify that the compiled executable runs without errors and loads sample data files (mzML, CDF, ABF) to confirm parser integration.

## Related tools

- **Visual Studio Community 2022** (IDE for .NET project compilation, dependency management via NuGet, and debugging) — https://visualstudio.microsoft.com/
- **Visual Studio Code** (Lightweight alternative text editor for .NET source code editing)
- **.NET Framework 4.7.2** (Primary runtime target for desktop applications in MS-DIAL version 5)
- **.NET 6** (Modern cross-platform runtime target supported alongside .NET Framework)
- **.NET Standard 2.0** (Shared library compatibility layer used by MS-DIAL class libraries)
- **GitHub Actions** (CI/CD pipeline for automated testing and reproducible builds) — https://github.com/systemsomicslab/MsdialWorkbench/blob/master/.github/workflows/dotnet_test.yml
- **WPF (Windows Presentation Foundation)** (UI framework for MS-DIAL desktop GUI implementation)
- **ReactiveExtensions / ReactiveProperty** (NuGet packages for reactive event-driven programming patterns in UI layer)

## Examples

```
git clone https://github.com/systemsomicslab/MsdialWorkbench && cd MsdialWorkbench && start MsdialWorkbench.sln
```

## Evaluation signals

- Executable (.exe) compiles without errors or unresolved NuGet package references.
- Solution configuration selection matches intended build variant ('Debug vendor unsupported' vs. 'Release vendor supported').
- GitHub Actions test workflow passes on commit, confirming reproducibility across CI environment.
- Compiled application successfully loads and parses a sample mzML file without crashes or data structure mismatches.
- NuGet package source correctly resolves private Assemblies folder dependencies; no missing DLL or version conflict warnings.

## Limitations

- Unit testing infrastructure for partial functionalities is not currently set up for trial; comprehensive test coverage may be incomplete.
- The 'vendor unsupported' build configuration cannot read proprietary mass spectrometry manufacturer data formats (only mzML, CDF, ABF supported); users must pre-convert data if working with vendor-specific formats.
- Only MS-DIAL version 5 series has reproducible builds guaranteed to be buildable from open source; earlier versions may rely on vendor SDKs or proprietary components.
- WPF dependency means the application is Windows-only and cannot be compiled or run on Linux or macOS without additional runtime abstraction or porting effort.

## Evidence

- [readme] In the `Workloads` selection, choose `.NET desktop development`: "In the `Workloads` selection, choose `.NET desktop development`"
- [methods] we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6: "we primarily utilize the frameworks of .NET Framework 4.7.2, .NET Core 3.1, and .NET 6"
- [methods] The .NET class libraries adhere at least to the specifications of .NET Standard 2.0: "The .NET class libraries adhere at least to the specifications of .NET Standard 2.0"
- [methods] we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation: "we are using the WPF (Windows Presentation Foundation) UI framework for GUI implementation"
- [methods] only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly: "only the version 5 series of MS-DIAL has reproducible builds that can be guaranteed openly"
- [readme] Add the `Assemblies` folder in this repo to the **Package source:**: "Add the `Assemblies` folder in this repo to the **Package source:**"
- [readme] Due to licensing restrictions, this version cannot read proprietary data formats from mass spectrometry manufacturers. However, the [release versions] distributed with official releases can read these proprietary formats. For the 'Debug/Release vendor unsupported' version, only the following formats are supported: **abf**(Reifycs), **cdf**(NetCDF), and **mzml**: "only the following formats are supported: **abf**(Reifycs), **cdf**(NetCDF), and **mzml**"
- [methods] To conduct tests, please refer to section `test:` of GitHub Actions: "To conduct tests, please refer to section `test:` of GitHub Actions"
