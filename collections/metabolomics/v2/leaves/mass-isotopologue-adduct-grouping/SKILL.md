---
name: mass-isotopologue-adduct-grouping
description: Use when after sample alignment has established consensus retention time
  and m/z coordinates across all samples, and you need to identify and merge peaks
  that represent isotopologues (e.g., ¹³C variants) or adducts (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3632
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - FeatureFinderMetabo
  - ADAP
  - SLAW
  techniques:
  - LC-MS
  license_tier: open
derived_from:
- doi: 10.1021/acs.analchem.1c02687
  title: slaw
evidence_spans:
- 'Wrapping of three main peak picking algorithms: Centwave, FeatureFinderMetabo,
  ADAP'
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_slaw_cq
    doi: 10.1021/acs.analchem.1c02687
    title: slaw
  dedup_kept_from: coll_slaw_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# mass-isotopologue-adduct-grouping

## Summary

Groups aligned LC-MS peaks by their isotopologue and adduct relationships using mass difference and intensity ratio criteria. This step consolidates redundant ion representations of the same molecular feature, reducing complexity in the final feature table.

## When to use

After sample alignment has established consensus retention time and m/z coordinates across all samples, and you need to identify and merge peaks that represent isotopologues (e.g., ¹³C variants) or adducts (e.g., [M+H]⁺, [M+Na]⁺) of the same underlying molecule rather than distinct features.

## When NOT to use

- Input data are profile (not centroided) spectra — grouping requires discrete peak m/z values.
- Mass accuracy is poor (>10 ppm) — isotope and adduct mass differences (0.99–1.01 Da) cannot be reliably distinguished from noise.
- Peak table already contains pre-grouped ions or has been processed by another tool that merged isotopologues — re-grouping may create artifacts.

## Inputs

- aligned peak table with retention time and m/z consensus coordinates
- sample-wise intensity matrices from peak picking
- mass calibration metadata (ppm tolerance)

## Outputs

- grouped feature table with isotopologue/adduct annotations
- consolidated peak intensity matrix (one row per feature group)
- isotopic composition assignments per feature

## How to apply

SLAW applies isotopologue and adduct grouping by comparing mass differences and intensity ratios between aligned peaks within each sample. Peaks are grouped if their mass difference matches known isotopic shifts (e.g., ~1.003 Da for ¹³C, ~0.994 Da for ¹⁸O) or common adduct mass offsets, and their intensity ratios conform to expected natural abundance patterns or co-ionization behavior. The grouping is performed as a distinct workflow step following sample alignment, consolidating redundant ion forms before gap-filling and final feature annotation. Success depends on accurate mass calibration (typically <5 ppm) and sufficient peak intensity dynamic range to resolve natural isotopic ratios.

## Related tools

- **Centwave** (Upstream peak picking algorithm; outputs peaks that are fed into isotopologue/adduct grouping)
- **FeatureFinderMetabo** (Upstream peak picking algorithm; outputs peaks that are fed into isotopologue/adduct grouping)
- **ADAP** (Upstream peak picking algorithm; outputs peaks that are fed into isotopologue/adduct grouping)
- **SLAW** (Container framework orchestrating the complete LC-MS workflow including isotopologue/adduct grouping as step 4) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/input:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Grouped features show expected natural abundance ratios for common isotopes (e.g., ¹³C ~1.1% relative intensity).
- Mass differences between grouped peaks match known isotope or adduct shifts (±0.005 Da tolerance).
- The count of features in the output table is less than the input aligned peak count, confirming redundant ions were merged.
- Retention times of grouped peaks are identical (consensus RT) and intensities are correlated across samples.
- No spurious grouping across unrelated molecules — peaks in the same group co-elute and share sample intensity patterns.

## Limitations

- Grouping accuracy depends on mass calibration; miscalibration (>5 ppm drift) may cause false negatives (failure to group true isotopologues) or false positives (erroneous grouping of unrelated peaks).
- Overlapping peaks with similar m/z in low-resolution or heavily congested regions may be incorrectly merged or split.
- Works only with DDA (data-dependent acquisition) MS2 data; DIA-MS2 spectra are not supported in SLAW and will be skipped during grouping.
- Natural abundance ratios can be distorted by sample complexity, ion suppression, or non-uniform ionization; ratios are used as heuristics, not absolute rules.

## Evidence

- [other] Group detected peaks by isotopologue and adduct relationships using mass difference and intensity ratio criteria.: "Group detected peaks by isotopologue and adduct relationships using mass difference and intensity ratio criteria."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic"
- [other] SLAW implements a complete processing pipeline comprising six sequential steps: peak picking, sample alignment, peak picking (repeated), grouping of isotopologues and adducts, gap-filling by data recursion, and extraction of consolidated MS2 spectra and isotopic data.: "SLAW implements a complete processing pipeline comprising six sequential steps: peak picking, sample alignment, peak picking (repeated), grouping of isotopologues and adducts, gap-filling by data"
- [readme] Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported.: "Files can include MS1 and DDA-MS2 scans. DIA-MS is not supported."
- [readme] All data must be centroided and of unique polarity.: "All data must be centroided and of unique polarity."
