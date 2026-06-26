---
name: mass-spectrum-scan-parsing
description: Use when you have raw mass spectrometry data files from a Thermo instrument
  (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3357
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
  tools:
  - Aerith
  - Raxport
  - R
  - ThermoRawFileParser
  - mzR
  - MSnbase
  techniques:
  - LC-MS
  license_tier: open
  provenance_tier: literature
derived_from:
- doi: 10.1021/acs.analchem.5c03207
  title: Aerith
evidence_spans:
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans, calculate the theoretical isotopic peak envelope
- Aerith is an R package that provides interfaces to read and write mass spectrum
  scans
- Extract visualization information from `.FT2` files
- Aerith is an R package
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_aerith_cq
    doi: 10.1021/acs.analchem.5c03207
    title: Aerith
  dedup_kept_from: coll_aerith_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.5c03207
  all_source_dois:
  - 10.1021/acs.analchem.5c03207
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-scan-parsing

## Summary

Parse and extract mass spectrometry scan data from raw instrument files (Thermo .raw, .FT1/.FT2, mzML, MGF) into structured peak lists with m/z, intensity, and charge state information. This is the foundational step for annotating fragment ions and validating peptide-spectrum matches in stable isotope labeling experiments.

## When to use

You have raw mass spectrometry data files from a Thermo instrument (e.g., Orbitrap or IonTrap) or already-converted open formats (mzML, MGF) and need to extract individual MS1 or MS2 scans with their observed peak m/z values, intensities, and charge states before matching them against theoretical isotopic envelopes or fragment ion predictions. Particularly critical when working with heavily labeled samples (e.g., 52% 13C incorporation) where charge and isotope information must be preserved.

## When NOT to use

- Input data are already peak-picked and tabulated in a feature table (use directly for matching instead)
- You require raw ion current time-series data without peak centroiding; use native Thermo libraries instead of Raxport/ThermoRawFileParser
- Working with non-Thermo instruments (e.g., Bruker, Waters, ABSciex) without prior conversion to mzML or MGF; Raxport is Thermo-specific

## Inputs

- Thermo .raw file from mass spectrometer (Orbitrap or IonTrap)
- mzML or indexed mzML file (from ThermoRawFileParser or similar)
- MGF file (mascot generic format)
- Raxport-processed .FT1 or .FT2 file
- Scan number (integer identifier)
- Isolation window width (e.g., 5.0 Da for MS2)

## Outputs

- Structured peak list with m/z, intensity, and charge state per scan
- Precursor m/z and charge state (for MS2 scans)
- Scan metadata (retention time, MS level, scan number)
- Total ion current (TIC) chromatogram for quality control

## How to apply

Convert Thermo .raw files to intermediate .FT1 or .FT2 files using Raxport, extracting charge information (Orbitrap only) and MS1/MS2 scans. Alternatively, use ThermoRawFileParser to convert directly to mzML or MGF. Load the resulting file into Aerith using mzR (mzML/MGF) or Raxport-compatible parsers (FT2), specifying the scan number and isolation window width (e.g., 5.0 Da for MS2). Extract observed peak data (m/z, intensity) and precursor m/z with charge state. Verify data quality by inspecting TIC (total ion current) and scan frequency before proceeding to peak matching. Apply consistent parameter selection across replicate samples to ensure reproducibility.

## Related tools

- **Raxport** (Extract scans from Thermo .raw files with charge information (Orbitrap only) into .FT1/.FT2 intermediate format compatible with Aerith) — https://github.com/xyz1396/Raxport.net
- **ThermoRawFileParser** (Convert Thermo .raw files to open formats (mzML, indexed mzML, MGF, Parquet) on all platforms; alternative to Raxport for cross-platform compatibility) — https://github.com/CompOmics/ThermoRawFileParser
- **Aerith** (Read and parse mass spectrum scans from mzML, MGF, Raxport .FT2, pepXML, PIN, and Sipros TSV files; visualize TIC and prepare peaks for theoretical isotopic matching) — https://github.com/xyz1396/Aerith
- **mzR** (Bioconductor R package integrated into Aerith for direct parsing of mzML and MGF files within R environment)
- **MSnbase** (Bioconductor R package for parsing pepXML files and handling parsed mass spectrum objects in downstream R workflows)

## Examples

```
# Extract scans from Thermo .raw using Raxport
./Raxport.exe -i input.raw -o output.FT2

# Or convert to mzML using ThermoRawFileParser
ThermoRawFileParser -i=input.raw -f=1 -o=output_dir/

# Then load in R/Aerith
library(Aerith)
spectrum <- readMS2Spectrum('output.FT2', scanNumber=2596, isolationWindowWidth=5.0)
```

## Evaluation signals

- Verify TIC (total ion current) shows expected chromatographic profile and scan frequency is consistent with acquisition method
- Inspect a sample MS2 scan: precursor m/z matches expected peptide mass (within isolation window width, e.g., ±2.5 Da for 5.0 Da window); observed peaks have m/z, intensity, and charge state populated
- Charge state information is non-null for Orbitrap data (if using Raxport); will be null for IonTrap
- Peak m/z values are numeric and sorted in ascending order; intensities are positive and scale appropriately across replicates
- No missing or malformed scan entries; total number of parsed MS2 scans matches expected count from acquisition metadata

## Limitations

- Raxport extracts charge information only from Orbitrap scans; IonTrap scans will not include charge state and must be inferred downstream
- ThermoRawFileParser requires .NET Core 8 runtime on Linux/macOS; legacy versions require Mono (pre-1.5.0)
- mzML and MGF formats discard some native Thermo metadata (e.g., instrument resolution tuning); use .FT2 if full fidelity required
- Peak picking algorithms (native Thermo vs. disable with -p flag in ThermoRawFileParser) can affect observed peak positions and intensities; consistent parameter selection is critical for cross-sample comparison
- Aerith's mzR integration is limited to Bioconductor ecosystems; non-R workflows require alternative parsers (e.g., pymzML, mzLib)

## Evidence

- [readme] Aerith is an R package that provides interfaces to read and write mass spectrum scans: "Aerith is an R package that provides interfaces to read and write mass spectrum scans"
- [readme] Raxport extracts scans from Thermo raw files; charge information only in Orbitrap: "Raxport is a simple program which extracts scans from raw files generated by mass spectrometers from ThermoFisher. It supports both Orbitrap and IonTrap scans. However, the generated `.FT1` or `.FT2`"
- [readme] ThermoRawFileParser converts to multiple output formats on cross-platform: "A tool allowing reading Thermo RAW mass spectrometer files and converting to common open formats on all platforms supporting .NET Core. Supported formats: * MGF * mzML and indexed mzML * Apache"
- [intro] Aerith accepts multiple spectral data file formats: "Aerith accepts spectral data files in multiple formats, including Raxport-processed FT2, mzML, and MGF files, as well as pepXML and PIN files (Percolator outputs), and TSV files from the Sipros"
- [intro] mzR integration for parsing mzML and MGF in Aerith: "Integration with the mzR package from Bioconductor allows direct parsing of mzML and MGF files"
- [abstract] Verify data quality using TIC and scan frequency analysis: "Always verify data quality using TIC and scan frequency analysis"
- [other] Concrete task workflow specifies isolation window and parameters: "annotatePSM accepts observed peak data (m/z, intensity, charge), peptide sequence (HYAHVDCPGHADYVK), charge states (1:2), isotope atom (C13), incorporation probability (0.52), precursor m/z, and"
