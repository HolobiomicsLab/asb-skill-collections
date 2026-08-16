---
name: feature-annotation-via-isotope-adduct-grouping
description: Use when after peak detection and feature extraction have produced a
  composite feature table with m/z, retention time, and intensity values for individual
  samples.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3801
  edam_topics:
  - http://edamontology.org/topic_3370
  - http://edamontology.org/topic_0121
  tools:
  - Python
  - pymzml
  - khipu
  - JMS
  - HMDB 4
  - asari
  - mass2chem
  techniques:
  - LC-MS
  license_tier: restricted
derived_from:
- doi: 10.1038/s41467-023-39889-1
  title: asari
evidence_spans:
- Trackable and scalable Python program for high-resolution LC-MS metabolomics data
  preprocessing
- Trackable and scalable Python program for high-resolution metabolomics data processing.
- The default method uses `pymzml` to parse mzML files.
- The preannotaion is done via another package khipu (https://github.com/shuzhao-li-lab/khipu)
- The empirical compounds are searched against known compound database (default HMDB
  4) via another package JMS (https://github.com/shuzhao-li/JMS).
- known compound database (default HMDB 4)
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_asari
    doi: 10.1038/s41467-023-39889-1
    title: asari
  dedup_kept_from: coll_asari
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1038/s41467-023-39889-1
  all_source_dois:
  - 10.1038/s41467-023-39889-1
  zenodo_doi: 10.5281/zenodo.20794027
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# feature-annotation-via-isotope-adduct-grouping

> **License: restricted** — no clear open-source license detected for the underlying tool; verify licensing before commercial use or redistribution. <!-- asb-license-banner -->
## Summary

Group detected LC-MS peaks into empirical compounds by identifying isotopologue (13C/12C) and adduct (Na/H) relationships, then search the resulting neutral masses against metabolite databases to assign chemical identities. This skill bridges raw peak detection and metabolite annotation by collapsing degenerate ion signals into biological entities.

## When to use

After peak detection and feature extraction have produced a composite feature table with m/z, retention time, and intensity values for individual samples. Use this skill when you have detected features across multiple LC-MS samples and need to group related ions (isotopologues and adducts of the same neutral compound) and assign putative compound identities via database matching.

## When NOT to use

- Input is already a pre-annotated compound table or contains only singly-charged ions with no expected adducts or isotopologues.
- Data is from targeted metabolomics with known compound lists; use direct library matching instead.
- Raw mass spectra have not yet been processed into aligned mass tracks and detected features; perform mass track extraction and peak detection first.

## Inputs

- Detected feature table with m/z, retention time, intensity, and peak quality metrics (SNR, peak shape)
- Mass track alignment results (MassGrid with sample-wise or centroided alignments)
- Per-sample intensity and area values extracted from aligned mass tracks

## Outputs

- Annotated_empiricalCompounds.json with empirical compound groups, inferred neutral masses, isotope/adduct relationships, and matched database entries
- Feature_annotation.tsv mapping original features to empirical compounds and chemical identities
- Neutral mass assignments for each empirical compound group

## How to apply

First, apply pre-annotation using khipu to group features that differ by known mass shifts (13C/12C isotope spacing ~1.0033 Da, or Na/H adduct differences ~21.98 Da) into empirical compounds, inferring the neutral mass for each group. Validate anchor mass tracks by identifying m/z differences that match isotope or adduct patterns during mass track alignment (establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts). Then search each empirical compound's neutral mass against HMDB 4 or another reference database using JMS to retrieve matched formulas and candidate isomers. Record the matched annotations in the output JSON, preserving the trace back from empirical compound to individual features and their original m/z values.

## Related tools

- **khipu** (Pre-annotation tool to group isotopes and adducts into empirical compounds and infer neutral mass) — https://github.com/shuzhao-li-lab/khipu
- **JMS** (Search empirical compound neutral masses against metabolite databases (default HMDB 4) to retrieve matched formulas and isomers) — https://github.com/shuzhao-li/JMS
- **HMDB 4** (Reference metabolite database for compound identity matching by neutral mass)
- **asari** (Orchestrates pre-annotation workflow and exports annotated empirical compounds to JSON) — https://github.com/shuzhao-li/asari
- **mass2chem** (Low-level utility library for handling chemical formulas and adduct calculations) — https://github.com/shuzhao-li/mass2chem

## Examples

```
asari annotate -i /path/to/preferred_Feature_table.tsv -o /path/to/output/ -j annotation_job --workflow LC --mode pos
```

## Evaluation signals

- Empirical compounds group features that differ by exact isotope spacing (~1.0033 Da for 13C) or known adduct mass differences (~21.98 Da for Na/H), verified by inspection of grouped m/z values in Annotated_empiricalCompounds.json.
- Neutral mass values inferred for each empirical compound are consistent with the most abundant isotopologue (typically 12C dominant), and fall within the expected ppm tolerance (±5 ppm default) of matched database compounds.
- Output JSON preserves full traceability: each matched empirical compound record links back to original feature m/z, intensity, retention time, and the database entry (compound name, formula, InChI key) used for identification.
- No false positive isotope groupings: features that differ by <2× the mass tolerance (10 ppm default) in m/z but >2× tolerance are not grouped; features separated by >0.002 Da (~2 ppm at m/z 500) are evaluated separately.
- Database match confidence: matched compounds have acceptable adduct and isotope patterns for the ionization mode (positive or negative); unmatched or ambiguous groups are flagged or returned with lower confidence scores.

## Limitations

- Requires high mass resolution (typically >50,000 for LC-MS) to reliably separate isotopologues and minor adducts; low-resolution instruments may over-group features.
- Dependent on khipu and JMS software versions and the completeness/currency of the reference metabolite database; missing or incorrectly annotated compounds in HMDB will not be detected.
- Cannot distinguish between isobaric compounds (same neutral mass, different structure); multiple isomers may be returned and require additional MS/MS or orthogonal data to disambiguate.
- Assumes standard ionization chemistry (Na/H adducts, 13C isotopes); non-standard adducts or unusual in-source fragments may not be recognized.
- Performance and accuracy depend on upstream peak detection quality; poor peak shape, low SNR, or missed features in individual samples will propagate through grouping and reduce annotation completeness.

## Evidence

- [methods] Perform pre-annotation using khipu to group isotopes and adducts into empirical compounds, then search against HMDB 4 via JMS to obtain matched formulas and isomers.: "Perform pre-annotation using khipu to group isotopes and adducts into empirical compounds, then search against HMDB 4 via JMS to obtain matched formulas and isomers."
- [methods] Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts.: "Establish anchor mass tracks by finding m/z differences that match to either 13C/12C isotopes or Na/H adducts."
- [readme] khipu: generalized tree structure to annotate untargeted metabolomics and stable isotope tracing data. Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass.: "Pre-annotation tool to annotate degenerate ions in relationships to the original compound and infer neutral mass."
- [readme] efficient mass and empirical compound search functions. A few examples: // A LC-MS peak: "efficient mass and empirical compound search functions"
- [intro] Reproducible, track and backtrack between features and mass tracks (EICs). Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases: "Tracking peak quality, selectiviy metrics on m/z, chromatography and annotation databases"
