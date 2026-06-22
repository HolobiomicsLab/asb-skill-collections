---
name: nuget-dependency-resolution
description: Use when you are preparing to build a .NET project (WPF, class library, or console application) and need to ensure all declared NuGet package dependencies are available in the build environment. This is particularly necessary when the project uses custom or private package sources (e.
license: CC-BY-4.0
metadata:
  edam_topics: []
  tools:
  - ReactiveExtensions
  - ReactiveProperty
  - .NET Standard
  - NuGet Package Manager
  - Visual Studio
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

# NuGet Dependency Resolution

## Summary

Resolve and restore .NET NuGet package dependencies required to build a .NET project, including managing package sources and version specifications. This skill is essential when building .NET Framework or .NET Core projects to ensure all required libraries (e.g., ReactiveExtensions, ReactiveProperty) are available before compilation.

## When to use

You are preparing to build a .NET project (WPF, class library, or console application) and need to ensure all declared NuGet package dependencies are available in the build environment. This is particularly necessary when the project uses custom or private package sources (e.g., an on-disk 'Assemblies' folder) in addition to standard NuGet.org feeds, or when building from a freshly cloned repository where packages have not yet been restored.

## When NOT to use

- The project is already fully compiled or you are only running a pre-built executable — dependency resolution is unnecessary.
- Your project uses only system-installed or GAC (Global Assembly Cache) assemblies with no external NuGet dependencies.
- You are modifying only non-compiled artifacts (e.g., documentation or configuration files) that do not require recompilation.

## Inputs

- .NET solution file (.sln)
- Project files (.csproj or .vbproj)
- packages.config or PackageReference declarations
- Package source configuration (NuGet.config or Visual Studio settings)
- Optional: local package folder (e.g., Assemblies/)

## Outputs

- Restored NuGet packages in local cache (typically ~/.nuget/packages or project packages folder)
- Resolution report (success/failure per package)
- Project ready for compilation with all dependencies available

## How to apply

Open the .NET project solution (e.g., MsdialWorkbench.sln) in Visual Studio. Right-click on the solution in Solution Explorer and select 'Manage NuGet Packages for Solution...'. If the project depends on packages in a custom location, add that path to the package sources configuration (e.g., adding a local 'Assemblies' folder). Initiate package restore, which will download or locate all declared dependencies and their transitive dependencies, matching version constraints specified in project files or packages.config. Verify that restore completes without errors and that all package binaries are available in the local cache before proceeding to compilation. The restore process respects the target framework version (e.g., .NET Framework 4.7.2, .NET Standard 2.0) when resolving compatible package versions.

## Related tools

- **NuGet Package Manager** (Resolves and restores NuGet packages and their transitive dependencies from configured sources)
- **Visual Studio** (Hosts the NuGet Package Manager UI and executes package restore via Solution Explorer) — https://visualstudio.microsoft.com/
- **ReactiveExtensions** (Example reactive programming library package required for WPF event handling in MsdialGuiApp)
- **ReactiveProperty** (Example reactive property binding package required for MsdialGuiApp WPF UI implementation)

## Evaluation signals

- NuGet restore operation completes with zero error messages and all packages report 'installed' status
- The local NuGet cache contains all declared packages and their transitive dependencies with correct versions matching target framework constraints
- Subsequent project compilation in Visual Studio successfully resolves all package assembly references with no unresolved reference errors
- The Visual Studio Solution Explorer shows no warning or error indicators on the solution or project nodes after restore completes
- Custom package sources (e.g., local Assemblies folder) are correctly registered and do not produce 'source not found' warnings during restore

## Limitations

- NuGet dependency resolution requires network access to configured package sources (unless all packages are available locally) and may fail if sources are unavailable or credentials are incorrect.
- The public 'vendor unsupported' build configuration of MsdialWorkbench may have different package requirements or constraints than the licensed vendor-supported release builds.
- Package versions must be compatible with the target framework (e.g., .NET Framework 4.7.2 or .NET Standard 2.0); some packages may not publish builds for older or newer framework versions, causing restore to fail.
- Custom package sources (e.g., private Assemblies folders) must be explicitly added to the package source list; omitting them will cause restore to fail for packages only available in those sources.

## Evidence

- [readme] package source configuration for MsdialWorkbench: "Add the `Assemblies` folder in this repo to the **Package source:**."
- [readme] NuGet package manager interaction workflow: "Right-click on `MsdialWorkbench` in the Solution Explorer. Click `Manage NuGet Packages for Solution...`."
- [methods] required NuGet package dependencies for MsdialGuiApp: "Restore NuGet dependencies including ReactiveExtensions and ReactiveProperty packages."
- [methods] framework-specific package resolution: "The .NET class libraries adhere at least to the specifications of .NET Standard 2.0"
