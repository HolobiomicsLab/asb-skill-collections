---
name: ms2-spectrum-consolidation
description: Use when after peak picking, sample alignment, and isotopologue/adduct grouping are complete, and you have DDA-MS2 scans associated with grouped feature ions.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3932
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - SLAW
  - FeatureFinderMetabo
  - ADAP
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# MS2 Spectrum Consolidation

## Summary

Consolidate multiple MS2 scans per feature group into representative spectra with annotated isotopic relationships and adduct information. This skill extracts and merges MS2 data from DDA LC-MS experiments after isotopologue and adduct grouping is complete, producing structured spectral entries suitable for annotation and export.

## When to use

Apply this skill after peak picking, sample alignment, and isotopologue/adduct grouping are complete, and you have DDA-MS2 scans associated with grouped feature ions. Use it when you need to consolidate multiple MS2 spectra per feature group into single representative entries for downstream compound annotation or spectral library building. Not applicable to DIA-MS data or when MS2 spectra are absent.

## When NOT to use

- Input data includes DIA-MS experiments (SLAW explicitly skips DIA-MS2 spectra; only DDA is supported)
- MS2 spectra are not present in the dataset or the raw mzML files contain MS1 data only
- Feature grouping (isotopologues and adducts) has not yet been completed; consolidation requires pre-grouped data

## Inputs

- Feature-grouped LC-MS data with isotopologues and adducts consolidated
- Raw LC-MS mzML files containing DDA-MS2 scans
- Processed spectral index mapping feature groups to MS2 scan identifiers
- Feature group metadata including isotopic relationships and adduct assignments

## Outputs

- Consolidated MS2 spectra (merged or representative per feature group)
- Structured spectral export file (JSON, mzTab, or proprietary format)
- Annotated MS2 metadata including isotopic and adduct information
- Feature group–to–MS2 mapping table

## How to apply

Beginning with feature-grouped LC-MS data where isotopologues and adducts have already been consolidated, retrieve all MS2 spectra linked to each feature group from raw mzML files or a processed spectral index. Merge or select a representative MS2 spectrum per feature group (e.g., by highest intensity or median RT). Annotate each consolidated spectrum entry with isotopic relationships (e.g., ¹³C labeling patterns) and adduct information (e.g., [M+H]⁺, [M+Na]⁺) derived from the grouping step. Export the consolidated spectra and metadata to a structured format (JSON, mzTab, or proprietary format) with explicit links back to the feature group identifiers. Verify output by confirming that each feature group has exactly one consolidated MS2 entry and that isotopic/adduct annotations are present and consistent with the grouping rationale.

## Related tools

- **SLAW** (Complete LC-MS processing pipeline that performs MS2 spectrum consolidation as part of its workflow after peak picking, alignment, and isotopologue/adduct grouping) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm wrapped by SLAW; produces feature detections that precede spectrum consolidation)
- **FeatureFinderMetabo** (Alternative peak picking algorithm wrapped by SLAW; produces feature detections that precede spectrum consolidation)
- **ADAP** (Alternative peak picking algorithm wrapped by SLAW; produces feature detections that precede spectrum consolidation)

## Evaluation signals

- Each feature group has exactly one consolidated MS2 spectrum entry (no duplicates, no missing entries)
- Isotopic and adduct annotations are present in all consolidated spectrum records and match the isotopologue/adduct grouping assignments
- MS2 scan RT and m/z values fall within the expected ranges for their assigned feature groups
- Export file is valid and parseable in the target format (JSON schema validation, mzTab compliance, etc.)
- Feature group identifiers in the consolidated spectra match identifiers from the preceding grouping step with no misalignments

## Limitations

- Only DDA-MS2 spectra are supported; DIA-MS data and targeted MS2 experiments may not consolidate correctly or are explicitly skipped
- Consolidation quality depends on prior isotopologue/adduct grouping accuracy; errors in grouping propagate to consolidated spectra
- Multiple MS2 scans per feature group are merged or reduced to a single representative spectrum, potentially losing spectral heterogeneity or scan-to-scan variability information
- Requires input data in centroided mzML format with unique polarity per batch; profile mode or mixed-polarity data will cause preprocessing to fail

## Evidence

- [other] SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts, and gap-filling by data recursion.: "SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts"
- [other] 1. Load feature-grouped data from preceding alignment and grouping steps (isotopologues and adducts already consolidated by feature group). 2. Retrieve MS2 spectra associated with each feature group from raw LC-MS files or processed spectral index. 3. Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). 4. Annotate isotopic relationships and adduct information within each consolidated spectrum entry. 5. Export consolidated spectra and metadata to structured output file (e.g., JSON, mzTab, or proprietary format).: "Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data: "extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
