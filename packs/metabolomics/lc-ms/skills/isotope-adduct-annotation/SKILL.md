---
name: isotope-adduct-annotation
description: Use when after completing peak picking, sample alignment, and before final MS2 spectrum extraction, when you have identified individual ion peaks across samples and need to link isotopic variants (e.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3637
  edam_topics:
  - http://edamontology.org/topic_3520
  - http://edamontology.org/topic_0121
  tools:
  - Centwave
  - SLAW
  - FeatureFinderMetabo
  - ADAP
  techniques:
  - LC-MS
  - tandem-MS
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
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c02687
  all_source_dois:
  - 10.1021/acs.analchem.1c02687
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# isotope-adduct-annotation

## Summary

Systematic grouping and annotation of isotopologue and adduct ions derived from the same precursor molecule, consolidating MS2 spectra and isotopic metadata after peak picking and sample alignment. This skill ensures that multiple ionic forms of a single compound are recognized as a single feature and annotated with their chemical relationships.

## When to use

Apply this skill after completing peak picking, sample alignment, and before final MS2 spectrum extraction, when you have identified individual ion peaks across samples and need to link isotopic variants (e.g., ¹³C-labeled forms) and different adduct forms ([M+H]⁺, [M+Na]⁺, [M+NH₄]⁺, etc.) of the same molecule into consolidated feature groups for annotation and quantification.

## When NOT to use

- Input data consists of already-grouped feature matrices or consensus spectra (grouping already performed upstream).
- MS data is in profile (non-centroided) mode; centroided data is required for reliable isotope and adduct pattern matching.
- DIA-MS experiments only; the SLAW workflow and this skill are designed for DDA experiments where MS2 scans are tied to specific precursors.

## Inputs

- Aligned feature peak table with m/z, retention time, and intensity across samples
- Raw LC-MS data file(s) in centroided mzML format containing MS1 and DDA-MS2 scans
- Processed spectral index or raw MS file references for MS2 spectrum retrieval

## Outputs

- Consolidated feature groups with isotopologue and adduct annotations
- Consolidated MS2 spectra (one representative or merged spectrum per feature group)
- Structured metadata file (JSON, mzTab, or proprietary format) with isotopic and adduct relationships encoded
- Annotated feature table linking original peaks to their feature group and chemical relationships

## How to apply

Load aligned feature data from the preceding peak picking and alignment workflow steps. Group ions by matching their m/z values and retention times while accounting for mass shifts corresponding to known isotope patterns (e.g., ¹³C: +1.003 Da, ¹⁸O: +2.004 Da) and common adduct mass differences. Assign isotopic relationships (monoisotopic vs. isotopologue) and adduct assignments based on observed m/z deltas and relative intensities. Consolidate multiple MS2 scans associated with the same feature group by selecting a representative spectrum or merging scans. Annotate each consolidated spectrum entry with both isotopic relationships and adduct information, then export to a structured format (e.g., JSON or mzTab) that preserves these groupings for downstream analysis.

## Related tools

- **Centwave** (Peak picking algorithm used upstream to detect individual ion peaks; output m/z and RT values feed into isotope-adduct grouping)
- **FeatureFinderMetabo** (Alternative peak picking algorithm whose output is used as input to isotope-adduct grouping workflow)
- **ADAP** (Alternative peak picking algorithm whose output is used as input to isotope-adduct grouping workflow)
- **SLAW** (Complete LC-MS processing pipeline that incorporates isotope-adduct grouping as a core step after alignment and before MS2 extraction) — https://github.com/zamboni-lab/SLAW

## Examples

```
docker run --rm -v /path/to/mzML:/input -v /path/to/output:/output zambonilab/slaw:latest
```

## Evaluation signals

- Each feature group contains exactly one monoisotopic peak (the lowest m/z form) plus zero or more isotopologues assigned with correct mass shifts (e.g., +1.003 Da for ¹³C).
- All ion peaks derived from the same compound are grouped together, and each group is assigned one or more adduct labels consistent with observed m/z differences (e.g., [M+H]⁺ vs. [M+Na]⁺ differ by ~21.98 Da).
- Consolidated MS2 spectra are successfully extracted and linked to their respective feature groups; no feature group lacks associated MS2 data if MS2 scans exist in the input.
- Output file structure preserves isotopic and adduct metadata (e.g., JSON keys indicating parent feature, isotope label, adduct assignment) and is schema-compliant with the declared output format.
- Isotope intensity ratios approximate theoretical values (e.g., M+1/M ~0.01–0.1 for organic molecules) within chemical noise variance.

## Limitations

- Isotope-adduct grouping relies on accurate preceding peak picking and alignment; errors in earlier steps propagate and cannot be corrected by grouping alone.
- DIA-MS2 spectra are not supported and will be skipped during MS2 consolidation; the skill applies only to DDA experiments where MS2 is tied to specific precursor m/z values.
- Requires input data to be centroided and of uniform polarity across all samples; mixed-polarity or profile-mode data will not be processed correctly.
- Grouping accuracy depends on retention time alignment precision; co-eluting isomers with different isotope patterns or adducts may be incorrectly merged if alignment error is large relative to LC peak width.

## Evidence

- [other] Reconstruct the Isotopologue and Adduct Grouping Component: "task_id=task_003 | title=Reconstruct the Isotopologue and Adduct Grouping Component"
- [other] SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and adducts, and gap-filling by data recursion.: "SLAW performs extraction of consolidated MS2 spectra and isotopic data as part of its complete processing pipeline, which follows peak picking, sample alignment, grouping of isotopologues and"
- [other] Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry.: "Consolidate multiple MS2 scans per feature group by merging or selecting representative spectrum(a). Annotate isotopic relationships and adduct information within each consolidated spectrum entry."
- [readme] Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic data: "Complete processing including peak picking, sample alignment, pick picking, grouping of isotopologues and adducts, gap-filling by data recursion, extraction of consolidated MS2 spectra and isotopic"
- [readme] All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard.: "All data must be centroided and of unique polarity. Centroided mzML can be obtained with ProteoWizard."
- [readme] DDA only. ... extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data: "extraction of consolidated MS2 spectra (only for DDA experiments! DIA-MS2 spectra will be skipped) and isotopic data"
