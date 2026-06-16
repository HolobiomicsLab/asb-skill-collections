---
name: spectral-metadata-integration
description: Use when after isotopologue and adduct grouping has been completed and you need to associate MS2 spectra with consolidated feature groups in DDA LC-MS experiments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3633
  edam_topics:
  - http://edamontology.org/topic_0121
  - http://edamontology.org/topic_3520
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
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v1
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw
schema_version: 0.2.0
---

# Spectral Metadata Integration

## Summary

Extract, consolidate, and annotate MS2 spectra with isotopic relationships and adduct information across grouped feature ions in untargeted LC-MS workflows. This skill bridges peak-picked, aligned, and grouped features to their corresponding tandem mass spectra and isotopic metadata, producing a unified spectral-feature data structure.

## When to use

Apply this skill after isotopologue and adduct grouping has been completed and you need to associate MS2 spectra with consolidated feature groups in DDA LC-MS experiments. This is the final consolidation step before annotation or export, particularly when downstream analysis requires both quantitative feature tables and fragmentation spectra linked by isotopic/adduct relationships.

## When NOT to use

- Input data is DIA (data-independent acquisition) rather than DDA; SLAW explicitly skips DIA-MS2 spectra and consolidation is not applicable.
- MS2 spectra have not yet been aligned to MS1 features; run alignment and grouping steps first.
- Raw data is not centroided or contains mixed polarity; spectral consolidation requires well-preprocessed, single-polarity centroided mzML.

## Inputs

- feature-grouped data (isotopologues and adducts already consolidated by feature group)
- raw LC-MS data files in mzML format (centroided, single polarity, DDA scans)
- processed spectral index or raw file access for MS2 retrieval

## Outputs

- consolidated MS2 spectra per feature group
- annotated spectral metadata (isotopic relationships, adduct assignments)
- structured output file (JSON, mzTab, or proprietary format)

## How to apply

Retrieve MS2 scans associated with each feature group from raw mzML files or a processed spectral index. For each feature group (which already contains consolidated isotopic and adduct assignments from prior grouping steps), merge or select representative MS2 spectrum(a) that correspond to that group's retention time and m/z window. Annotate each consolidated spectrum entry with metadata including isotopic assignments (e.g., [M], [M+2], [M+4] for chlorine isotopologues) and detected adducts (e.g., [M+H]+, [M+Na]+). Export the consolidated spectra alongside feature table metadata in a structured format such as JSON, mzTab, or vendor-specific format. The consolidation preserves the grouping logic established in prior steps, ensuring that all spectra attributed to a single feature group are labeled consistently.

## Related tools

- **SLAW** (Complete LC-MS processing workflow that performs spectral consolidation as the final step after peak picking, alignment, isotopologue/adduct grouping, and gap-filling) — https://github.com/zamboni-lab/SLAW
- **Centwave** (Peak picking algorithm wrapped by SLAW; produces initial peaks from which MS2 associations are later made)

## Examples

```
docker run --rm -v /path/to/input:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Each feature group in the output has exactly one consolidated MS2 spectrum or explicitly documented multiple representative spectra with clear selection criteria.
- All isotopic relationships (e.g., [M], [M+2]) and adduct forms ([M+H]+, [M+Na]+) present in the grouped feature data are carried forward and annotated in the consolidated spectrum metadata.
- RT and m/z ranges of consolidated spectra align with the feature group boundaries established in prior grouping steps (no orphaned or misaligned spectra).
- Structured output follows expected schema (JSON schema validation, mzTab compliance, or vendor format specification) and all required fields are populated.
- Cross-sample consistency: the same feature group (same m/z, RT, isotopic/adduct assignment) maps to coherent MS2 spectra across replicate samples.

## Limitations

- Only applicable to DDA LC-MS; DIA-MS2 spectra are excluded and will be skipped.
- Requires prior successful peak picking, sample alignment, and isotopologue/adduct grouping; if grouping is incomplete or erroneous, spectral consolidation will propagate those errors.
- Multiple MS2 scans per feature group may require a representative selection strategy; averaging or merging spectra can dilute low-abundance fragment ions.
- Consolidation relies on accurate RT alignment; misaligned features will produce spectra erroneously assigned to wrong feature groups.
- Input mzML files must be centroided and of uniform polarity; profile-mode or mixed-polarity data will cause retrieval and consolidation failures.

## Evidence

- [intro] SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts, and gap-filling by data recursion.: "extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts, and"
- [other] Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry.: "Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data: "extraction of consolidated MS2 spectra and isotopic data"
- [readme] Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported.: "Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported."
- [readme] All data must be centroided and of unique polarity.: "All data must be centroided and of unique polarity."
