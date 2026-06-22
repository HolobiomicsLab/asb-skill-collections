---
name: feature-group-spectral-mapping
description: Use when after sample alignment and isotopologue/adduct grouping are complete, when you need to associate MS2 spectral data (DDA-acquired) with the consolidated feature groups to enable MS/MS-based compound annotation or to bundle MS1 quantification with MS2 evidence.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - SLAW
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# Reconstruct the Isotopologue and Adduct Grouping Component

## Summary

Map consolidated MS2 spectra and isotopic metadata to feature groups (isotopologues and adducts) that have already been aligned and clustered across samples. This skill extracts representative tandem mass spectra for each feature group and annotates their isotopic relationships and adduct identities.

## When to use

After sample alignment and isotopologue/adduct grouping are complete, when you need to associate MS2 spectral data (DDA-acquired) with the consolidated feature groups to enable MS/MS-based compound annotation or to bundle MS1 quantification with MS2 evidence. Use this step before exporting final peaktables and spectral libraries.

## When NOT to use

- Input LC-MS data are DIA (data-independent acquisition): SLAW will skip DIA-MS2 spectra and only process MS1 features
- Feature grouping has not yet been performed: spectral mapping requires consolidated feature group assignments as input
- No MS2 data are present in the raw files (MS1-only experiments): no spectra can be consolidated or mapped

## Inputs

- Feature-grouped peaktable (with isotopologue and adduct assignments)
- Raw LC-MS mzML files (centroided, DDA-acquired)
- Sample metadata and polarity information

## Outputs

- Consolidated MS2 spectrum per feature group (e.g., MGF or mzTab with MS/MS spectra)
- Annotated isotopic and adduct metadata linked to each feature group
- Complete peaktable enriched with MS2 spectrum references

## How to apply

Load the feature-grouped data from the preceding alignment and grouping steps (isotopologues and adducts already consolidated by feature group ID). For each feature group, retrieve all MS2 scans associated with its member ions from the raw LC-MS files or a processed spectral index (matching by retention time and m/z tolerance). Consolidate multiple MS2 scans per feature group by selecting a representative spectrum (e.g., highest-intensity scan or merged consensus spectrum). Annotate each consolidated spectrum entry with isotopic relationships (e.g., M, M+1, M+2) and adduct type (e.g., [M+H]+, [M+Na]+) inferred from the grouping step. Export the consolidated spectra and their metadata to a structured output format (e.g., mzTab, JSON, or MGF) alongside the quantitative peaktable.

## Related tools

- **SLAW** (Complete untargeted LC-MS workflow orchestrator that performs feature grouping, gap-filling, and then spectral consolidation and export as integrated pipeline step) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm (one of three options) that detects LC-MS features before alignment and grouping)

## Examples

```
docker run --rm -v /path/to/input:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- All feature groups in the input peaktable have an associated consolidated MS2 spectrum entry in the output (completeness check)
- Isotopic annotations (M, M+1, M+2) and adduct identities match the grouping assignments from the prior step (consistency check)
- Retention time and m/z of each consolidated spectrum's precursor ion fall within the tolerance window of the feature group (validation against alignment)
- Output file format (MGF, mzTab, or JSON) is valid and can be parsed by downstream annotation tools (schema/format check)
- No duplicate spectra across feature groups; each MS2 scan is assigned to exactly one feature group (uniqueness check)

## Limitations

- DIA-MS2 spectra are skipped and not consolidated; only DDA-acquired MS2 data are processed
- Spectral consolidation assumes that multiple MS2 scans assigned to a single feature group are chemically identical; co-eluting isomers or isobaric species will be merged and may compromise annotation specificity
- Requires that raw mzML files remain accessible during the consolidation step; file paths must be correctly resolved
- Quality of consolidated spectra depends on prior alignment and grouping accuracy; errors in isotopologue/adduct assignment propagate to spectrum metadata

## Evidence

- [other] SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts, and gap-filling by data recursion.: "SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and"
- [other] 1. Load feature-grouped data from preceding alignment and grouping steps (isotopologues and adducts already consolidated by feature group). 2. Retrieve MS2 spectra associated with each feature group from raw LC-MS files or processed spectral index. 3. Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). 4. Annotate isotopic relationships and adduct information within each consolidated spectrum entry. 5. Export consolidated spectra and metadata to structured output file (e.g., JSON, mzTab, or proprietary format).: "1. Load feature-grouped data from preceding alignment and grouping steps (isotopologues and adducts already consolidated by feature group). 2. Retrieve MS2 spectra associated with each feature group"
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data: "extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data"
- [readme] Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported. All data must be centroided and of unique polarity.: "Raw MS data in mzML format. Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported."
