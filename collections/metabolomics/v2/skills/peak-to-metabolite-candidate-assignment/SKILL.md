---
name: peak-to-metabolite-candidate-assignment
description: Use when you have a raw peak-intensity matrix from untargeted LC-MS data (organized as rows=peaks, columns=samples) and need to generate initial candidate metabolite assignments.
license: CC-BY-4.0
metadata:
  edam_operation: http://edamontology.org/operation_3627
  edam_topics:
  - http://edamontology.org/topic_3172
  - http://edamontology.org/topic_0621
  tools:
  - mWISE
  - R
  - CAMERA
  - cliqueMS
  - KEGG database
  techniques:
  - LC-MS
derived_from:
- doi: 10.1021/acs.analchem.1c00238
  title: mWISE
evidence_spans:
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package that provides tools for context-based annotation of untargeted LC-MS data.
- mWISE (metabolomics Wise Inference of Speck Entities) is an R package
- The default table of adducts and fragments is built using information from CAMERA R package
- The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.
- information from CAMERA R package, H. Tong et al., and cliqueMS.
claims: []
provenance:
  collection: https://w3id.org/holobiomicslab/asb-skill/collection/metabolomics/v2
  assembled_by: scripts/collect_metabolomics_collection.py
  sources:
  - build: coll_mwise_cq
    doi: 10.1021/acs.analchem.1c00238
    title: mWISE
  dedup_kept_from: coll_mwise_cq
schema_version: 0.2.0
attribution:
  generator: AgenticScienceBuilder
  original_doi: 10.1021/acs.analchem.1c00238
  all_source_dois:
  - 10.1021/acs.analchem.1c00238
  zenodo_doi: TODO-zenodo
  curators: []
  promoter: Louis-Félix Nothias
  sponsor: CNRS & Université Côte d'Azur
---

# peak-to-metabolite-candidate-assignment

## Summary

Annotate observed LC-MS peaks (m/z values) to KEGG database metabolites by matching peak mass-to-charge ratios against a precomputed table of KEGG compounds with their known adducts and in-source fragments. This is the first step in mWISE's three-stage untargeted metabolomics annotation pipeline, designed to overcome the bottleneck of assigning chemical identities to detected peaks.

## When to use

You have a raw peak-intensity matrix from untargeted LC-MS data (organized as rows=peaks, columns=samples) and need to generate initial candidate metabolite assignments. Apply this skill when you have not yet annotated peaks to chemical entities and possess (or can construct) a reference table of KEGG compounds with their expected adduct and fragment masses for your ion polarity mode (positive or negative).

## When NOT to use

- Your input is already an annotated feature table or has been through downstream clustering/filtering steps; the matching stage is the first step and should not be applied post-filtering.
- You lack a reference compound table (Cpd.Add) and do not have access to KEGG database identifiers and their exact masses.
- Your LC-MS data is from targeted metabolomics with a predefined compound list; this skill is designed for untargeted discovery where candidates must be generated de novo.

## Inputs

- Peak.List: peak-intensity matrix (rows=detected peaks, columns=samples/replicates) with m/z and intensity values
- Cpd.Add table: reference table of KEGG compounds with precomputed adduct and fragment m/z values
- Ion polarity setting: string ('negative' or 'positive') specifying the LC-MS acquisition mode

## Outputs

- Peak.Cpd candidate table: annotated matrix where each row is a detected peak and columns contain matched KEGG identifiers and their scoring metrics
- Original Peak.List: returned unchanged for downstream processing

## How to apply

Load the peak-intensity matrix (Peak.List) and a precomputed Cpd.Add table containing KEGG identifiers with their adduct- and fragment-derived m/z values into R. Execute the matchingStage function from mWISE, specifying the ion polarity (negative or positive mode). For each observed peak m/z, the function tests all possible neutral mass candidates derived by subtracting or adding the adduct/fragment masses from the Cpd.Add table. Peaks are matched to KEGG compounds when the observed m/z falls within a mass tolerance window (typically determined by instrument accuracy). The function returns an annotated Peak.Cpd table where each row is a detected peak and columns contain matched KEGG identifiers with their associated scoring metrics. The Cpd.Add table itself can be built from CAMERA, cliqueMS, and literature sources, or a user can subset the default adducts and fragments based on their experimental settings to improve accuracy.

## Related tools

- **mWISE** (Core R package providing the matchingStage function and Peak.List/Peak.Cpd data structures for peak-to-metabolite matching) — https://dev.b2s.club/b2slab/mWISE
- **R** (Execution environment for mWISE and the matchingStage function)
- **KEGG database** (Source of metabolite identifiers, chemical structures, and exact masses used to construct the Cpd.Add reference table)
- **CAMERA** (R package that generates adduct and fragment mass information used to build the default Cpd.Add table)
- **cliqueMS** (Tool contributing adduct and fragment reference data to the default Cpd.Add table)

## Examples

```
data('sample.dataset'); data('sample.keggDB'); Cpd.Add <- buildCpd.Add(sample.keggDB); results <- matchingStage(sample.dataset$Peak.List, Cpd.Add, polarity='negative')
```

## Evaluation signals

- Peak.Cpd output table has the same number of rows as the input Peak.List, confirming all peaks were processed.
- Each matched peak has at least one KEGG candidate identifier in the output; unmatched peaks appear with missing/NA entries.
- Scoring metrics for matched candidates are numeric and within expected ranges (e.g., mass error in ppm relative to observed m/z).
- The observed distribution of adduct types assigned to peaks matches the expected ion chemistry for the polarity mode (e.g., [M-H]⁻ dominant in negative mode).
- Downstream clustering and filtering steps (applied to Peak.Cpd candidates) produce a reduced, coherent feature set, indicating initial matches are reasonable.

## Limitations

- The quality of matching depends critically on the completeness and accuracy of the Cpd.Add reference table; missing or incorrectly annotated adducts/fragments will result in false negatives or misassignments.
- Mass tolerance and scoring thresholds are not explicitly parameterized in the provided article; users must rely on mWISE defaults or tune based on instrument specifications, which may affect sensitivity and specificity.
- In-source fragments and adducts that are not included in the Cpd.Add table (or are below the frequency threshold if filtering is applied) will not be matched, potentially eliminating valid candidates.
- The matching stage alone does not resolve peaks that originate from the same metabolite or filter out spurious candidates; these are addressed in subsequent clustering and filtering stages, so raw Peak.Cpd output may contain noise.

## Evidence

- [other] The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original Peak.List and an annotated Peak.Cpd table mapping peaks to KEGG candidate compounds.: "The matchingStage function accepts a Peak.List (peak-intensity matrix), a Cpd.Add table of KEGG compounds with adducts/fragments, and a polarity setting, and returns a list containing the original"
- [other] For each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments.: "match each observed m/z value against the KEGG database by testing all possible neutral mass candidates derived from the Cpd.Add adducts and fragments"
- [intro] mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database: "mWISE integrates several strategies to provide a fast annotation of peak-intensity tables. It consists of three main steps aimed at i) matching mass-to-charge ratio values to KEGG database"
- [intro] The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS.: "The default table of adducts and fragments is built using information from CAMERA R package, H. Tong et al., and cliqueMS."
- [intro] A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their: "A subset of the adducts or fragments available in mWISE can be selected for the matching stage. This is strongly recommended, since the expertise of the users with the experimental settings of their"
- [intro] untargeted LC-MS data annotation is a major bottleneck in computational metabolomics: "untargeted LC-MS data annotation is a major bottleneck in computational metabolomics"
