---
name: mass-spectrometry-data-extraction
description: Use when after peak picking, sample alignment, and isotopologue/adduct grouping steps have been completed in an untargeted LC-MS workflow.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3823
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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

# Mass Spectrometry Data Extraction

## Summary

Extraction and consolidation of MS2 spectra and isotopic data from grouped feature ions across LC-MS samples following peak picking, alignment, and grouping workflows. This skill ensures that tandem MS spectra are retrieved from raw files, deduplicated or merged across multiple scans per feature group, and annotated with isotopologue and adduct relationships.

## When to use

After peak picking, sample alignment, and isotopologue/adduct grouping steps have been completed in an untargeted LC-MS workflow. Apply this skill when you need consolidated MS2 spectra for each feature group (rather than raw per-scan spectra) and must integrate isotopic relationship metadata into the final spectral output.

## When NOT to use

- Input data are profile (non-centroided) or DIA-mode MS2 spectra; SLAW skips DIA-MS2 spectra
- Feature groups have not yet been consolidated for isotopologues and adducts; grouping must precede extraction
- Raw MS data are in vendor-proprietary binary format (not mzML); conversion is required first

## Inputs

- Feature-grouped peak table (rows=feature groups, columns=samples; isotopologues and adducts already consolidated)
- Raw LC-MS data files in mzML format (centroided, DDA mode, single polarity)
- Feature group metadata including isotopologue and adduct relationships
- MS2 scan index or raw spectral data linked to feature group retention times and m/z values

## Outputs

- Consolidated MS2 spectra file (mzTab, MGF, or JSON format) with one spectrum per feature group
- Annotated spectrum metadata including isotopologue relationships and adduct type assignments
- Feature group–to–MS2 spectrum mapping table

## How to apply

Load feature-grouped data that has already been consolidated by prior alignment and grouping steps (isotopologues and adducts pre-grouped by feature group ID). Retrieve MS2 scans associated with each feature group from raw mzML files or indexed spectral data structures. For each feature group with multiple MS2 scans, consolidate by merging or selecting a representative spectrum (e.g., highest signal-to-noise or consensus merge). Annotate the consolidated entry with isotopic relationships (e.g., [M+1], [M+2]) and adduct designations (e.g., [M+H]+, [M+Na]+) extracted from the grouping metadata. Export the consolidated spectra and their isotopic/adduct annotations to a structured output format (mzTab, JSON, or MGF) for downstream annotation or library matching.

## Related tools

- **Centwave** (Peak picking algorithm whose output (feature table) feeds into this extraction workflow)
- **FeatureFinderMetabo** (Alternative peak picking algorithm whose output feeds into this extraction workflow)
- **ADAP** (Alternative peak picking algorithm whose output feeds into this extraction workflow)
- **SLAW** (Complete untargeted LC-MS workflow that wraps peak picking, alignment, grouping, gap-filling, and consolidation of MS2 spectra and isotopic data) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/input/mzML:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- All feature groups in the consolidated output have a non-null MS2 spectrum entry (or documented reason for absence, e.g., MS2-only sample type)
- Each consolidated spectrum is tagged with isotopologue designation (e.g., [M], [M+1], [M+2]) and adduct type (e.g., [M+H]+, [M+Na]+) consistent with grouping metadata
- The consolidated output file is valid and parseable (mzTab/MGF/JSON schema compliance)
- Number of consolidated spectra equals the number of feature groups in the input feature table
- Cross-check: spot-verify 3–5 feature groups by confirming their MS2 scans exist in the raw mzML file at the correct retention time and m/z tolerance

## Limitations

- DIA-mode MS2 spectra are skipped; SLAW supports DDA mode only
- Requires pre-grouped (isotopologue and adduct) feature table as input; not applicable to ungrouped peak tables
- MS2 scans must be from centroided data; profile-mode or vendor-specific formats will cause errors or be rejected
- If multiple MS2 spectra map to the same feature group, the consolidation method (merge vs. select) must be pre-configured; no in-situ decision logic
- DDA-MS2 scans are mapped to MS1 features post-hoc; very low-abundance or noisy spectra may not be reliably retrieved if retention time or m/z alignment is poor

## Evidence

- [other] SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts, and gap-filling by data recursion.: "SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and"
- [other] Load feature-grouped data from preceding alignment and grouping steps (isotopologues and adducts already consolidated by feature group). Retrieve MS2 spectra associated with each feature group from raw LC-MS files or processed spectral index.: "Load feature-grouped data from preceding alignment and grouping steps (isotopologues and adducts already consolidated by feature group). Retrieve MS2 spectra associated with each feature group from"
- [other] Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry.: "Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data: "extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
