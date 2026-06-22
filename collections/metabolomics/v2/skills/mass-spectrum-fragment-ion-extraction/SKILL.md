---
name: mass-spectrum-fragment-ion-extraction
description: Use when you have an experimental MS/MS spectrum (e.g., from MassBank or acquired data) for a single metabolite with known accurate precursor m/z and adduct type, and you need to generate a library entry with scored fragments for use in metabolite annotation pipelines.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_0091
  - http://edamontology.org/topic_3375
  tools:
  - MetaboAnnotatoR
  - R (version or higher)
  - R
  - xcms
  - RamClustR
  - MassBank
  techniques:
  - LC-MS
  - CE-MS
  - tandem-MS
derived_from:
- doi: 10.1021/acs.analchem.1c03032
  title: metaboannotator
evidence_spans:
- MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets
- start R (version "4.5.0" or higher)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_metaboannotator_cq
    doi: 10.1021/acs.analchem.1c03032
    title: metaboannotator
  dedup_kept_from: coll_metaboannotator_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c03032
  all_source_dois:
  - 10.1021/acs.analchem.1c03032
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-spectrum-fragment-ion-extraction

## Summary

Extract and score fragment ions from experimental MS/MS spectra to construct metabolite library entries. This skill converts raw fragmentation data into annotated peak lists with occurrence scores, enabling downstream metabolite identification in untargeted LC–MS workflows.

## When to use

You have an experimental MS/MS spectrum (e.g., from MassBank or acquired data) for a single metabolite with known accurate precursor m/z and adduct type, and you need to generate a library entry with scored fragments for use in metabolite annotation pipelines. Apply this skill when building custom fragment databases or validating spectral quality before annotation.

## When NOT to use

- You already have a validated library entry or are importing spectra from an established database (LipidPos, etc.) — use direct library loading instead of reconstructing.
- Your input spectrum is in profile (non-centroid) mode — centroid conversion is required upstream; genFragEntry assumes centroid input.
- You need to annotate multiple unknown features against many library entries — use the annotateRC function for batch annotation rather than extracting individual entries.

## Inputs

- MS/MS spectrum (centroid mode, from MassBank or raw LC–MS AIF data)
- Metabolite name (string, e.g., 'D-Pantothenic Acid')
- Adduct type (string, e.g., '[M+H]+')
- Accurate adduct m/z (numeric, e.g., 220.1206)

## Outputs

- Metabolite library entry (CSV file with m/z, fragment intensity, occurrence score, and metabolite annotation)
- Ranked fragment ion list with scoring metadata

## How to apply

Load the MS/MS spectrum into R and invoke the genFragEntry function, specifying the metabolite name, adduct type (e.g., [M+H]+), accurate adduct m/z, and output filename. The function applies peak detection using a noise threshold (default noise=0.005) and occurrence score assignment to peaks above the intensity threshold (default mpeaksThres=0.1), using a mass tolerance (default mzTol=0.01 m/z) to cluster and rank fragments. Peaks are scored using the mpeaksScore parameter (default 0.9) to reflect their relative importance. Export the resulting library entry as a CSV file containing metabolite identifier, fragment m/z, and occurrence scores for downstream matching against experimental features.

## Related tools

- **MetaboAnnotatoR** (R package that wraps genFragEntry function and provides the annotateRC function for matching extracted fragments against features) — https://github.com/gggraca/MetaboAnnotatoR
- **R** (Execution environment; requires version 4.5.0 or higher to run genFragEntry)
- **xcms** (Upstream LC–MS feature detection and processing; generates centroid-mode spectra suitable for fragment extraction)
- **RamClustR** (Upstream spectral clustering for AIF chromatograms; output can be processed with genFragEntry)
- **MassBank** (Data source for reference MS/MS spectra (e.g., MSBNK-RIKEN-PR100295) to extract and validate fragments) — https://massbank.eu/

## Examples

```
library(MetaboAnnotatoR); genFragEntry(metabolite_name='D-Pantothenic Acid', adduct_name='[M+H]+', accurate_mz=220.1206, spectrum_data=spectrum_df, noise=0.005, mpeaksThres=0.1, mzTol=0.01, output_file='pantothenic_acid_entry.csv')
```

## Evaluation signals

- Exported CSV file contains all expected columns (m/z, intensity, occurrence score, metabolite ID) with numeric and string values in expected ranges.
- Fragment m/z values align with known neutral losses or characteristic fragments for the metabolite class (e.g., pantothenic acid [M+H]+ at 220.1206 with expected low-mass losses).
- Peak count and m/z distribution match visual inspection of the raw MS/MS spectrum; no major peaks should be missing below the noise threshold (default 0.005).
- Occurrence scores range from 0 to 1 and reflect peak intensity ranking; highest-intensity peaks receive highest scores up to mpeaksScore=0.9.
- Mass tolerance (default 0.01 m/z) correctly clusters nearby peaks; no duplicate fragments within tolerance window in final library entry.

## Limitations

- Requires centroid-mode spectra; profile-mode data must be centroided upstream, which can loss resolution or introduce artifacts.
- Default parameters (noise=0.005, mpeaksThres=0.1, mzTol=0.01) are tuned for typical Orbitrap/time-of-flight instruments and may require re-optimization for other MS platforms or ionization modes.
- Fragment occurrence scores are relative within a single spectrum; cross-spectrum or cross-metabolite score comparisons are not standardized and should not be used for library-wide ranking.
- Spectra with very low signal-to-noise or extensive in-source fragmentation may yield incomplete or artifactual library entries; visual validation recommended.
- The function does not annotate fragment ion structures or neutral losses; m/z values alone are returned without chemical context.

## Evidence

- [other] genFragEntry function converts MS/MS spectra into library entries by attributing occurrence scores to peaks above mpeaksThres threshold and noise level: "The genFragEntry function converts MS/MS spectra into library entries by attributing occurrence scores to peaks above the mpeaksThres threshold and noise level, using default parameters: noise=0.005,"
- [intro] MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases: "MetaboAnnotatoR is designed to perform metabolite annotation of features from LC-MS All-ion fragmentation (AIF) datasets, using ion fragment databases"
- [other] Retrieve MS/MS spectrum from MassBank and invoke genFragEntry with default parameters, then export as CSV: "Retrieve the D-Pantothenic Acid [M+H]+ fragmentation spectrum from MassBank (accession MSBNK-RIKEN-PR100295). Load the spectrum data into R and invoke the genFragEntry function with default"
- [readme] It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode: "It requires raw LC-MS AIF chromatograms acquired/transformed in centroid mode."
- [readme] Vignette on generation of metabolite fragment database entry from MS/MS experimental spectra: "Generation of Metabolite fragment database entry from MS/MS experimental spectra."
